#![allow(non_snake_case)]
#![allow(dead_code)]

use std::default::Default;
use std::ops::{Index, IndexMut};

pub struct Matrix<T> {
    vec: Vec<T>,
    cols: usize,
}

impl<T> Matrix<T>
where
    T: Default,
{
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
