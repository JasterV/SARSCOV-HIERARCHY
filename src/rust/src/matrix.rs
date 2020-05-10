#![allow(non_snake_case)]
#![allow(dead_code)]

pub struct Matrix {
    vec: Vec<Vec<isize>>,
}

impl Matrix {
    pub fn new(n: usize, m: usize) -> Matrix {
        Matrix {
            vec: Matrix::build_2D_Vector(n, m),
        }
    }

    pub fn get(&self, i: usize, j: usize) -> isize {
        self.vec[i][j]
    }

    pub fn set(&mut self, value: isize, i: usize, j: usize) {
        self.vec[i][j] = value;
    }

    pub fn build_2D_Vector(n: usize, m: usize) -> Vec<Vec<isize>> {
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
