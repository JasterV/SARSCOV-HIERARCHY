#![allow(non_snake_case)]
#![allow(dead_code)]

//! A wrapper for a 2D vector.
//! 
//! This Module contains the Matrix type that allows
//! you to create a matrix of any type that implements the
//! Default trait.

use std::default::Default;
use std::ops::{Index, IndexMut};


/// A wrapper for a 2D vector.
/// 
/// The Matrix struct accepts any type that implements the Default trait.
///    
/// # Examples
/// 
/// ```
///     let rows = 10;
///     let cols = 10;
///     let mut m : Matrix<isize> = Matrix::new(rows, cols);
///     m[(0, 0)] = 3;
///     m[(0, 1)] = 5;
/// 
///     let num = m[(0, 0)];
/// 
///     let score = m.get(0, 1).expect("Error getting an immutable reference");
/// 
///     // *score = 34; Uncommenting this line will result as an error    
/// 
///     let score = m.get_mut(0, 1).expect("Error getting a mutable reference");
/// 
///     *score = 10; // now m[(0, 1)] is equal to 10
/// ```
pub struct Matrix<T> {
    vec: Vec<T>,
    cols: usize,
}

impl<T> Matrix<T>
where
    T: Default,
{
    /// Creates a new instance of Matrix 
    /// filling it with the default value of the type T
    /// 
    /// # Example
    /// ```
    ///     let mut m : Matrix<isize> = Matrix::new(10, 20);
    ///     // Now the matrix is filled entirely with the default value
    ///     // of the isize primitive type which is 0.
    /// ```
    /// 
    pub fn new(n: usize, m: usize) -> Matrix<T> {
        Matrix {
            vec: Matrix::vec_2d(n, m),
            cols: m,
        }
    }

    pub fn get(&self, i: usize, j: usize) -> Option<&T> {
        self.vec.get(i * self.cols + j)
    }

    pub fn get_mut(&mut self, i: usize, j: usize) -> Option<&mut T> {
        self.vec.get_mut(i * self.cols + j)
    }

    fn vec_2d(n: usize, m: usize) -> Vec<T> {
        let mut matrix: Vec<T> = Vec::with_capacity(n * m);
        matrix.resize_with(n * m, Default::default);
        matrix
    }
}

impl<T> Index<(usize, usize)> for Matrix<T>
where
    T: Default,
{
    type Output = T;
    fn index(&self, idx: (usize, usize)) -> &Self::Output {
        self.get(idx.0, idx.1).expect("Index out of bounds")
    }
}

impl<T> IndexMut<(usize, usize)> for Matrix<T>
where
    T: Default,
{
    fn index_mut(&mut self, idx: (usize, usize)) -> &mut Self::Output {
        self.get_mut(idx.0, idx.1).expect("Index out of bounds")
    }
}
