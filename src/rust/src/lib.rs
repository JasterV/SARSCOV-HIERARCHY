use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

mod matrix;

pub use matrix::Matrix;
use std::cmp::max;

const GAP: isize = -2;
const MATCH: isize = 1;
const MISMATCH: isize = -1;

#[pymodule]
fn seqalign(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(needleman_wunsch))?;
    Ok(())
}

#[pyfunction]
pub fn needleman_wunsch(s1: &str, s2: &str) -> PyResult<f64> {
    let matrix: Matrix = align(s1, s2);
    let result: f64 = optimal_alignment(&matrix, s1, s2);
    Ok(result)
}

fn optimal_alignment(matrix: &Matrix, s1: &str, s2: &str) -> f64 {
    let (bs1, bs2) = (s1.as_bytes(), s2.as_bytes());
    let (mut i, mut j) = (s1.len(), s2.len());
    let (mut matches, mut length) = (0.0, 0.0);

    while i > 0 || j > 0 {
        if i > 0
            && j > 0
            && matrix.get(i, j) == matrix.get(i - 1, j - 1) + check_match(bs1[i - 1], bs2[j - 1])
        {
            if bs1[i - 1] == bs2[j - 1] {
                matches += 1.0
            }
            i -= 1;
            j -= 1;
        } else if i > 0 && matrix.get(i, j) == matrix.get(i - 1, j) + GAP {
            i -= 1;
        } else {
            j -= 1;
        }
        length += 1.0;
    }
    matches / length
}

fn align(x: &str, y: &str) -> Matrix {
    let mut matrix: Matrix = Matrix::new(x.len() + 1, y.len() + 1);

    for i in 0..(x.len() + 1) {
        let value = GAP * i as isize;
        matrix.set(value, i, 0);
    }
    for j in 0..(y.len() + 1) {
        let value = GAP * j as isize;
        matrix.set(value, 0, j);
    }

    for (i, c1) in x.bytes().enumerate() {
        for (j, c2) in y.bytes().enumerate() {
            let fit = matrix.get(i, j) + check_match(c1, c2);
            let delete = matrix.get(i, j + 1) + GAP;
            let insert = matrix.get(i + 1, j) + GAP;
            let max_val = max(max(fit, delete), max(fit, insert));
            matrix.set(max_val, i + 1, j + 1);
        }
    }
    matrix
}

fn check_match(b1: u8, b2: u8) -> isize {
    if b1 == b2 {
        MATCH
    } else {
        MISMATCH
    }
}
