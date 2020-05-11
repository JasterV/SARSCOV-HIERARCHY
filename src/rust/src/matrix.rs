#![allow(non_snake_case)]
#![allow(dead_code)]

//! A 2D Matrix of integers.
//! This Module contains the [`Matrix`] type
//! and its implementation.
//! 
//! # Examples
//!
//! There are one way to create a new [`Matrix`] by giving the number
//! Of wows and columns:
//!
//! ```
//! let mut m = Matrix::new(5, 6);
//! ```
//!
//! You can set and get elements into the Matrix using the [`get`] and [`set`] methods:
//!
//!  ```
//!     let (value, i, j) = (5, 2, 3);
//!     m.set(value, i j);
//!     let new_value = m.get(i, j);
//!  ```
//! 
//! This module let you create a 2D growable vector of integers:
//! 
//! ```
//!     let mut vec : Vector<Vector<isize>> = Matrix::vec_2d(3, 4);
//! ```

pub struct Matrix {
    vec: Vec<Vec<isize>>,
}

impl Matrix {
    pub fn new(n: usize, m: usize) -> Matrix {
        Matrix {
            vec: Matrix::vec_2d(n, m),
        }
    }
    
    pub fn get(&self, i: usize, j: usize) -> isize {
        self.vec[i][j]
    }

    pub fn set(&mut self, value: isize, i: usize, j: usize) {
        self.vec[i][j] = value;
    }

    pub fn vec_2d(n: usize, m: usize) -> Vec<Vec<isize>> {
        let mut matrix: Vec<Vec<isize>> = Vec::with_capacity(n);
        for _ in 0..n {
            let mut row: Vec<isize> = Vec::with_capacity(m);
            for _ in 0..m {
                row.push(0);
            }
            matrix.push(row);
        }
        matrix
    }
}
