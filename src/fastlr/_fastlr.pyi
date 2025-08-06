from __future__ import annotations
import numpy
import numpy.typing
import typing

__all__ = ["check_arma", "irls"]

def check_arma() -> None:
    """
    Check armadillo info
    """

def irls(
    arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64],
    arg1: typing.Annotated[numpy.typing.ArrayLike, numpy.float64],
    arg2: typing.SupportsFloat,
    arg3: typing.SupportsInt,
) -> dict:
    """
    Run Iteratively Reweighted Least Squares (IRLS)
    """
