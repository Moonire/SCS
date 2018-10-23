import numpy as np
import numpy.linalg as LA


def filtering(src, dst, alpha, beta, vand, y, e=.3):
    """
    filtering outlier points

    the tests are implemened very naively, not to say in a horrible
    manner in the purpose of making the testing of the filtering
    as easy and CLEAR as possible.
    Once the logic of the filtering is correctly implemented,
    we will condence the tests to the stict minimum

    Also please don't laught or cry.
    """
    alpha = np.array([np.dot(p, y) for p in alpha])
    E_Sxy = 1/np.matmul(alpha, LA.pinv(vand))[0]

    def condition(Sxy): return (np.abs(Sxy-E_Sxy) < e*E_Sxy)

    def test(a, b, c, d): return (beta[a]-beta[b])/(alpha[c]-alpha[d]+10e-8)

    # one term tests
    # a_j and a_j-1
    def test_1b(j): test(j-1, j, j-1, j+1)

    def test_1f(j): test(j, j+1, j+1, j+2)

    # b_j and b_j-1
    def test_2b(j): test(j-1, j+1, j-1, j)

    def test_2f(j): test(j+1, j+2, j, j+1)

    # to delete a_(j-1) and b_(j-1), this value should pass the ESxy test
    def test_c(j): (j-2, j+1, j-2, j-1)

    # two terms tests
    # (a_j and b_j) or (a_(j-1) and b_(j-1))
    def test_5(j): test(j-1, j+1, j-1, j+1)

    # a_j and a_j+1
    def test_7(j): test(j-1, j, j-1, j+2)

    # b_j and b_j+1
    def test_8(j): test(j-1, j+2, j-1, j)

    # b_j and a_(j-1)
    def test_9(j): test(j-1, j+1, j, j+1)

    # b_(j-1) and a_j
    def test_10(j): test(j, j+1, j-1, j+1)

    # three terms tests
    # a_(j-1), a_j, a_(j+1)
    def test_11_b(j): test(j-1, j, j+2, j+3)

    def test_11_f(j): test_11_b(j+1)

    # b_(j-1), b_j, b_(j+1)
    def test_12_b(j): test(j+2, j+3, j-1, j)

    def test_12_f(j): test_12_b(j+1)

    # a_(j-1), b_(j-1), b_j
    def test_13_b(j): test(j-2, j+1, j-2, j)

    def test_13_f(j): test(j+1, j+2, j, j+1)

    # a_(j-1), a_j, b_(j-1)
    def test_14_b(j): test(j-2, j, j-2, j+1)

    def test_14_f(j): test(j, j+1, j+1, j+2)

    # b_(j-1), a_j, bj
    def test_15_b(j): test(j-2, j+1, j-2, j-1)

    def test_15_f(j): test(j+1, j+2, j-1, j+1)

    # a_(j-1), a_j, bj
    def test_16_b(j): test(j-2, j-1, j-2, j+1)

    def test_16_f(j): test(j-1, j+1, j+1, j+2)

    # a_j, b_(j-1), b_(j+1)
    def test_17_b(j): test(j-2, j, j-2, j-1)

    def test_17_f(j): test(j, j+2, j-1, j+1)

    # a_(j-1), a_(j+1), b_j
    def test_18_b(j): test(j-2, j-1, j-2, j)

    def test_18_f(j): test(j-1, j+1, j, j+2)

    # the filtering logic should go here

    return src, dst
