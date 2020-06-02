import numpy as np


class ArrayMethods:
    @staticmethod
    def array(array):
        return np.array(array)

    @staticmethod
    def float(num):
        return np.float(num)

    @staticmethod
    def mgrid(ss, se, es, ee):
        return np.mgrid[ss:se, es:ee]

    @staticmethod
    def zeros(num, shape):
        return np.zeros((num, shape), np.float32)

    @staticmethod
    def save(file, src):
        np.save(file, src)

    @staticmethod
    def dot(mtx1, mtx2):
        return np.dot(mtx1, mtx2)

    @staticmethod
    def inv(mtx):
        return np.linalg.inv(mtx)

    @staticmethod
    def argmax(args):
        return np.argmax(args)

    @staticmethod
    def argmin(args):
        return np.argmin(args)

    @staticmethod
    def expand_dims(arg, axis):
        return np.expand_dims(arg, axis=axis)

    @staticmethod
    def arange(_from, _to):
        return np.arange(_from, _to)

    @staticmethod
    def random(_from, _to, size):
        return np.random.uniform(_from, _to, size=size)