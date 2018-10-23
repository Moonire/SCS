import numpy as np
import numpy.linalg as LA


def filtering(alpha, beta, vand, y, e=.3):
    """
    filtering outlier points
    """
    alpha = np.array([np.dot(p, y) for p in alpha])
    E_Sxy = 1/np.matmul(alpha, LA.pinv(vand))[0]

    def condition(Sxy): return (np.abs(Sxy-E_Sxy) < e*E_Sxy)

    # added in all test denominatos
    eps = 10e-8

    # one term tests
    # a_j
    def test_1b(j): return (beta[j-1]-beta[j])/(alpha[j-1]-alpha[j+1]+eps)

    def test_1f(j): return (beta[j]-beta[j+1])/(alpha[j+1]-alpha[j+2]+eps)

    # b_j
    def test_2b(j): return (beta[j-1]-beta[j+1])/(alpha[j-1]-alpha[j]+eps)

    def test_2f(j): return (beta[j+1]-beta[j+2])/(alpha[j]-alpha[j+1]+eps)

    # a_(j-1)
    def test_3b(j): return (beta[j-2]-beta[j-1])/(alpha[j-2]-alpha[j]+eps)

    def test_3f(j): return (beta[j-1]-beta[j])/(alpha[j]-alpha[j+1]+eps)

    # b_(j-1)
    def test_4b(j): return (beta[j-2]-beta[j])/(alpha[j-2]-alpha[j-1]+eps)

    def test_4f(j): return (beta[j]-beta[j+1])/(alpha[j-1]-alpha[j]+eps)

    # to delete a_(j-1) and b_(j-1), this value should pass the ESxy test
    def test__c(j): return (beta[j-2]-beta[j+1])/(alpha[j-2]-alpha[j-1]+eps)

    # two terms tests
    # a_j and b_j
    def test_5(j): return (beta[j-1]-beta[j+1])/(alpha[j-1]-alpha[j+1]+eps)

    # a_(j-1) and b_(j-1)
    def test_6(j): return (beta[j-2]-beta[j])/(alpha[j-2]-alpha[j]+eps)

    # a_j and a_j+1
    def test_7(j): return (beta[j-1]-beta[j])/(alpha[j-1]-alpha[j+2]+eps)

    # b_j and b_j+1
    def test_8(j): return (beta[j-1]-beta[j+2])/(alpha[j-1]-alpha[j]+eps)

    # b_j and a_(j-1)
    def test_9(j): return (beta[j-1]-beta[j+1])/(alpha[j]-alpha[j+1]+eps)

    # b_(j-1) and a_j
    def test_10(j): return (beta[j]-beta[j+1])/(alpha[j-1]-alpha[j+1]+eps)

    # three terms tests
    # a_(j-1), a_j, a_(j+1)
    def test_11_b(j): return (beta[j-1]-beta[j])/(alpha[j+2]-alpha[j+3]+eps)

    def test_11_f(j): return (beta[j]-beta[j+1])/(alpha[j+3]-alpha[j+4]+eps)

    # b_(j-1), b_j, b_(j+1)
    def test_12_b(j): return (beta[j+2]-beta[j+3])/(alpha[j-1]-alpha[j]+eps)

    def test_12_f(j): return (beta[j+3]-beta[j+4])/(alpha[j]-alpha[j+1]+eps)

    # a_(j-1), b_(j-1), b_j
    def test_13_b(j): return (beta[j-2]-beta[j+1])/(alpha[j-2]-alpha[j]+eps)

    def test_13_f(j): return (beta[j+1]-beta[j+2])/(alpha[j]-alpha[j+1]+eps)

    # a_(j-1), a_j, b_(j-1)
    def test_14_b(j): return (beta[j-2]-beta[j])/(alpha[j-2]-alpha[j+1]+eps)

    def test_14_f(j): return (beta[j]-beta[j+1])/(alpha[j+1]-alpha[j+2]+eps)

    # b_(j-1), a_j, bj
    def test_15_b(j): return (beta[j-2]-beta[j+1])/(alpha[j-2]-alpha[j-1]+eps)

    def test_15_f(j): return (beta[j+1]-beta[j+2])/(alpha[j-1]-alpha[j+1]+eps)

    # a_(j-1), a_j, bj
    def test_16_b(j): return (beta[j-2]-beta[j-1])/(alpha[j-2]-alpha[j+1]+eps)

    def test_16_f(j): return (beta[j-1]-beta[j+1])/(alpha[j+1]-alpha[j+2]+eps)

    # a_j, b_(j-1), b_(j+1)
    def test_17_b(j): return (beta[j-2]-beta[j])/(alpha[j-2]-alpha[j-1]+eps)

    def test_17_f(j): return (beta[j]-beta[j+2])/(alpha[j-1]-alpha[j+1]+eps)

    # a_(j-1), a_(j+1), b_j
    def test_18_b(j): return (beta[j-2]-beta[j-1])/(alpha[j-2]-alpha[j]+eps)

    def test_18_f(j): return (beta[j-1]-beta[j+1])/(alpha[j]-alpha[j+2]+eps)

    return alpha, beta