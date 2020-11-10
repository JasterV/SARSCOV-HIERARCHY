
//! The goal of this module is to optimize the global sequence alignment
//! process of many sequences implementing the Needleman-Wunsch algorithm
//! And getting help of the Rayon Crate to parallelize the execution.

use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

mod matrix;

pub use matrix::Matrix;
use rayon::prelude::*;
use std::cmp::{max, min};
use std::collections::HashMap;

const GAP: u16 = 2;
const MATCH: u16 = 0;
const MISMATCH: u16 = 1;

#[allow(unused_variables)]
#[pymodule]
fn seqalign(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(par_compare))?;
    m.add_wrapped(wrap_pyfunction!(compare_samples))?;
    Ok(())
}

/// Just a wrapper for the needleman_wunsch function
/// to be used in python.
#[pyfunction]
pub fn compare_samples(s1: &str, s2: &str) -> PyResult<u16> {
    let result = needleman_wunsch(s1, s2);
    Ok(result)
}

/// Gets a Vector of tuples that contains 2 keys of the HashMap parameter, 
/// then compare the samples contained on the HashMap 2 by 2 through multi-processing. 
/// To do that, the parallel iterator and map functions of the Rayon Crate are used.
#[pyfunction]
pub fn par_compare(v: Vec<(&str, &str)>, map: HashMap<&str, &str>, num_threads: &str) -> PyResult<Vec<(String, String, u16)>> {
    std::env::set_var("RAYON_NUM_THREADS", num_threads);
    let results = 
            v.par_iter()
            .map(|x| {
                (
                    (x.0).to_string(),
                    (x.1).to_string(),
                    needleman_wunsch(map[x.0], map[x.1]),
                )
            })
            .collect();
    Ok(results)
}

/// Performs global sequence alignment of two `&str` using the Needleman-Wunsch classic algorithm.
/// Returns the distances between the 2 samples, computed considering a MATCH a value
/// of distance 0, a GAP distance of 2 and a MISMATCH distance of 1.
/// 
/// # Examples
/// ```
///     let s = String::from("HELLO");
///     let s1 = String::from("HHELLO");
/// 
///     let result = needleman_wunsch(&s, &s1); // The alignment would produce
///                                             // the sequences 'HHELLO' and '-HELLO'.
///                                             // so result is equal to 0*5 + 2
/// ```
pub fn needleman_wunsch(x: &str, y: &str) -> u16 {
    let (x_len, y_len) = (x.len(), y.len());
    let mut matrix: Matrix<u16> = Matrix::new(x_len + 1, y_len + 1);

    for i in 0..max(x_len + 1, y_len + 1) {
        let value = GAP * i as u16;
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
            let min_val = min(min(fit, delete), min(fit, insert));
            matrix[(i + 1, j + 1)] = min_val;
        }
    }

    matrix[(x_len, y_len)]
}

fn check_match(b1: u8, b2: u8) -> u16 {
    if b1 == b2 || b1 == b'N' || b2 == b'N' {
        MATCH
    } else {
        MISMATCH
    }
}
