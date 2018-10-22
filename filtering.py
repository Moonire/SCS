import numpy as np
import numpy.linalg as LA


def filter(self, beta, vand, e=.3):
    """
    filtering outlier points
    """
    alpha = np.array([np.dot(p, self.y) for p in self.src_sorted_by_alpha])
    E_Sxy = 1/np.matmul(alpha, LA.pinv(vand))[0]

    def S_xy(j): return (beta[j-1]-beta[j])/(alpha[j-1]-alpha[j]+10e-8)

    def condition(Sxy): return (np.abs(Sxy-E_Sxy) < e*E_Sxy)

    # one element filtering

    def test_ab(j): return (beta[j-1]-beta[j])/(alpha[j-1]-alpha[j+1])

    def test_af(j): return (beta[j]-beta[j+1])/(alpha[j+1]-alpha[j+2])

    def test_bb(j): return (beta[j-1]-beta[j+1])/(alpha[j-1]-alpha[j])

    def test_bf(j): return (beta[j+1]-beta[j+2])/(alpha[j]-alpha[j+1])

    # two elements filtering

    # three elements filtering
