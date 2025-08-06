"""
Simple test to check that the cpp and python modules work.
An equivalent R version can be found inside r-tests/test_fastlr.R
"""

import numpy as np
import fastlr

X = np.array(
    [
        [-1.00, 0.36],
        [-0.00, 1.12],
        [-1.88, -0.62],
        [0.18, 1.41],
        [0.24, 1.33],
        [-0.36, 0.52],
        [1.51, 2.58],
        [0.74, 1.93],
        [0.75, 1.71],
        [-1.70, -0.58],
        [-0.22, 0.73],
        [0.28, 1.45],
        [0.87, 2.08],
        [0.37, 1.48],
        [0.22, 1.63],
        [-0.16, 0.84],
        [-0.99, -0.01],
        [-0.32, 0.55],
        [1.06, 2.24],
        [-1.00, 0.18],
        [-0.11, 1.00],
        [1.27, 2.33],
        [0.13, 1.44],
        [-0.47, 0.43],
        [-0.55, 0.55],
        [0.38, 1.62],
        [-1.35, -0.06],
        [0.61, 1.72],
        [-0.65, 0.64],
        [0.24, 1.37],
        [0.94, 1.92],
        [-1.16, 0.19],
        [-0.25, 1.04],
        [-0.57, 0.50],
        [-0.72, 0.65],
        [-0.33, 1.05],
        [2.30, 3.57],
        [-0.32, 0.79],
        [-0.20, 0.67],
        [-0.06, 1.15],
        [-1.69, -0.61],
        [0.59, 1.67],
        [-1.19, 0.01],
        [0.24, 1.47],
        [-0.42, 0.87],
        [0.47, 1.58],
        [0.24, 1.19],
        [-0.56, 0.62],
        [-0.24, 0.88],
        [1.19, 2.28],
    ]
)
y = np.array(
    [
        1,
        0,
        0,
        0,
        0,
        1,
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        1,
        0,
        0,
        0,
        1,
        0,
        1,
        0,
        0,
        1,
        1,
        0,
        1,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        1,
        0,
        1,
        0,
        0,
        1,
        0,
        0,
        0,
        1,
        1,
        0,
        0,
        0,
        0,
        1,
        0,
    ]
)


def test_works():
    """Test that the fastlr module works with the provided data."""

    expected = np.array([0.01578324, -0.40486642])
    output = fastlr.fastlr(X, y, method="cpp")
    assert np.allclose(output.coefficients, expected)
    output = fastlr.fastlr(X, y, method="python")
    assert np.allclose(output.coefficients, expected)
