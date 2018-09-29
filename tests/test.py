import pytest
import numpy as np
from scs import SCS


M = {'N': 20, 'Tx': 0, 'Ty': 0, 'Sx': 2, 'Sy': 3, 'theta': np.pi/6}


def test_scs_fit():
    # computing the transfomation matrix
    T = np.array([[M['Sx'] * np.cos(M['theta']), M['Sx'] * -np.sin(M['theta']), M['Tx']],
                  [M['Sy'] * np.sin(M['theta']), M['Sy'] * np.cos(M['theta']), M['Ty']],
                  [0, 0, 1]])

    # generation of the point sets
    src = np.random.random((M['N'], 2)) - 1/2

    src_ = np.hstack((src, np.ones(src.shape[0])[:, np.newaxis]))
    dst = np.matmul(T, src_.T)[0:2].T

    # computation the transformation matrix using SCS
    m = SCS(src, dst)
    m.fit()

    assert np.allclose(m.T, T)
