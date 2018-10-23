import numpy as np
import numpy.linalg as LA
from filtering import filtering


class SCS():
    """
    Sorting the Correspondence Space Algorithm as described in :
    Assalih, H., 2013. 3D reconstruction and motion estimation using forward
    looking sonar (Doctoral dissertation, Heriot-Watt University).
    """
    def __init__(self, src, dst):
        """
        src {2d np.array} -- starting point set
        dst {2d np.array} -- target point set
        """
        self.src = np.hstack((src, np.ones(src.shape[0])[:, np.newaxis]))
        self.dst = np.hstack((dst, np.ones(dst.shape[0])[:, np.newaxis]))

        assert self.src.shape[0] == self.dst.shape[0]
        assert self.src.shape[1] == 3
        assert self.dst.shape[1] == 3

    def __err(self, a, T):
        """
        error metric given the source matrix a and transformation T
        """
        b = np.matmul(T, a)
        n = len(a)
        err = 0

        for operator in ((1, 1, 0), (1, -1, 0)):
            aa = sorted([np.dot(i, operator) for i in a.T])[:n//2]
            bb = sorted([np.dot(i, operator) for i in b.T])[:n//2]

            err += sum(abs(i-j)**2 for i in aa for j in bb)

        return err/n

    def fit(self, step=10e-2, threshold=10e-8):
        """
        compute the transformation matrix T
        """
        self.dst_sorted_by_beta = sorted(self.dst, key=lambda p: sum(p))
        dst_pinv = LA.pinv(np.transpose(self.dst_sorted_by_beta))

        # constantes necessary in the filtering, computed
        # in advance outside the loop for optimization
        beta = np.array([sum(p) for p in self.dst_sorted_by_beta])
        vand = np.vstack((beta, np.ones(beta.shape[0])))

        min_error = float('inf')
        rate = np.pi/180

        for psi in (i*rate for i in range(-180, 181)):
            y = (np.cos(psi), -np.sin(psi), 0)

            src_by_alpha = sorted(self.src, key=lambda p: np.dot(p, y))
            alpha, beta = filtering(alpha=src_by_alpha, beta=beta, vand=vand, y=y)

            src_sorted = np.transpose(src_by_alpha)
            T = LA.inv(np.matmul(src_sorted, dst_pinv))

            # pruning
            T[np.abs(T) < threshold] = 0

            current_error = self.__err(src_sorted, T)

            if current_error < min_error:
                min_error, self.T = current_error, T

        sx = LA.norm(self.T[0][0:2])

        # parametres of the transformation are computed here for easy access
        # T : translation, subscripte denotes in which direction
        # S : scaling, subscripte denotes in which direction
        # thata : rotation angle, in radians
        self.params = {'Tx': self.T[0, 2], 'Ty': self.T[1, 2],
                       'Sx': sx, 'Sy': LA.norm(self.T[1][0:2]),
                       'theta': np.arccos(self.T[0, 0]/sx) * np.sign(-self.T[0, 1]/sx)}
