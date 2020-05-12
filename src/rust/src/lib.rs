use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

mod matrix;

pub use matrix::Matrix;
use std::cmp::max;

const GAP: i16 = -2;
const MATCH: i16 = 1;
const MISMATCH: i16 = -1;

#[allow(unused_variables)]
#[pymodule]
fn seqalign(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(needleman_wunsch))?;
    Ok(())
}

/// Performs global sequence alignment of two `&str`
/// using the Needleman-Wunsch classic algorithm.
/// The returning value is a ratio whose value is the result of
/// dividing the matches between the two aligned sequences by
/// the length of the aligned sequences.
#[pyfunction]
pub fn needleman_wunsch(s1: &str, s2: &str) -> PyResult<f64> {
    let matrix: Matrix<i16> = align(s1, s2);
    let result: f64 = optimal_alignment(&matrix, s1, s2);
    Ok(result)
}

fn optimal_alignment(matrix: &Matrix<i16>, s1: &str, s2: &str) -> f64 {
    let (bs1, bs2) = (s1.as_bytes(), s2.as_bytes());
    let (mut i, mut j) = (s1.len(), s2.len());
    let (mut matches, mut length) = (0.0, 0.0);
    while i > 0 || j > 0 {
        if i > 0
            && j > 0
            && matrix[(i, j)] == matrix[(i - 1, j - 1)] + check_match(bs1[i - 1], bs2[j - 1])
        {
            if bs1[i - 1] == bs2[j - 1] {
                matches += 1.0
            }
            i -= 1;
            j -= 1;
        } else if i > 0 && matrix[(i, j)] == matrix[(i - 1, j)] + GAP {
            i -= 1;
        } else {
            j -= 1;
        }
        length += 1.0;
    }
    matches / length
}

fn align(x: &str, y: &str) -> Matrix<i16> {
    let (x_len, y_len) = (x.len(), y.len());
    let mut matrix: Matrix<i16> = Matrix::new(x_len + 1, y_len + 1);

    for i in 0..max(x_len + 1, y_len + 1) {
        let value = GAP * (i as i16);
        if i < x_len + 1 {
            matrix[(i, 0)] = value;
        }
        if i < y_len + 1 {
            matrix[(0, i)] = value;
        }
    }

    for (i, c1) in x.bytes().enumerate() {
        for (j, c2) in y.bytes().enumerate() {
            let fit = matrix[(i, j)] + check_match(c1, c2);
            let delete = matrix[(i, j + 1)] + GAP;
            let insert = matrix[(i + 1, j)] + GAP;
            let max_val = max(max(fit, delete), max(fit, insert));
            matrix[(i + 1, j + 1)] = max_val;
        }
    }
    matrix
}

fn check_match(b1: u8, b2: u8) -> i16 {
    if b1 == b2 || b1 == b'N' || b2 == b'N' {
        MATCH
    } else {
        MISMATCH
    }
}
