# coverage:ignore
"""Test cases for compute_lambda_df.py
"""
from os import path

import numpy as np
import pytest

from openfermion.resource_estimates import HAVE_DEPS_FOR_RESOURCE_ESTIMATES, df

if HAVE_DEPS_FOR_RESOURCE_ESTIMATES:
    from openfermion.resource_estimates.molecule import load_casfile_to_pyscf


@pytest.mark.skipif(not HAVE_DEPS_FOR_RESOURCE_ESTIMATES, reason="pyscf and/or jax not installed.")
def test_reiher_df_bliss_lambda():
    """Reproduce Reiher et al orbital DF lambda for DF+LRPS method of J. Chem. Theory Comput. 2025, 21, 2, 703–713"""

    THRESH = 1e-8
    NAME = path.join(path.dirname(__file__), '../integrals/eri_reiher.h5')
    _, mf = load_casfile_to_pyscf(NAME, num_alpha=27, num_beta=27)
    eri_rr, LR, L, Lxi = df.factorize(mf._eri, thresh=THRESH)
    total_lambda = df.compute_lambda_df_with_bliss_post_processing(mf, LR)
    assert eri_rr.shape[0] * 2 == 108
    assert np.isclose(np.round(total_lambda, decimals=1), 169.4)