import fastlr

import polars as pl
import numpy as np

X = pl.read_csv("data/X.csv").to_numpy(order="fortran")
y = pl.read_csv("data/y.csv")["y"].to_numpy()  # vectors are fortran always

output = fastlr.fastlr(X, y)
r_coefficientss = pl.read_csv("data/coefs.csv")["coefs"].to_numpy().ravel()
r_coefficientss_fastlr = (
    pl.read_csv("data/coefs_fastlrR.csv")["coefs"].to_numpy().ravel()
)
assert np.allclose(output.coefficients.ravel(), r_coefficientss)
assert np.allclose(r_coefficientss, r_coefficientss_fastlr)
print(" cpp estimates (in python & R) matches fastglm estimates ".center(80, "*"))
