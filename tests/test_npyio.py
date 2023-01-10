#!/usr/bin/env python
"""
This is the unittest for npyio module.

python -m unittest -v tests/test_npyio.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_npyio.py

"""
import unittest


class TestNpyio(unittest.TestCase):
    """
    Tests for npyio.py
    """

    def test_updatez(self):
        import os
        from io import BytesIO
        from tempfile import mkstemp
        import numpy as np
        import pyjams as pj
        from numpy.ma.testutils import assert_equal
        from numpy.testing import temppath

        x = np.zeros((2, 2))
        y = np.zeros((3, 3))
        xnew = np.zeros((4, 4))
        updatez_list = [pj.updatez, pj.updatez_compressed]

        # filename

        # append array
        for updatez in updatez_list:
            with temppath(prefix="np_test_updatez_", suffix=".npz") as tmp:
                np.savez(tmp, x=x)
                ll = np.load(tmp)
                assert 'x' in ll.keys()
                assert_equal(x, ll['x'])
                updatez(tmp, y=y)
                ll = np.load(tmp)
                assert 'x' in ll.keys()
                assert 'y' in ll.keys()
                assert_equal(x, ll['x'])
                assert_equal(y, ll['y'])

        # update array and append array
        for updatez in updatez_list:
            with temppath(prefix="np_test_updatez_", suffix=".npz") as tmp:
                np.savez(tmp, x=x)
                ll = np.load(tmp)
                assert 'x' in ll.keys()
                assert_equal(x, ll['x'])
                updatez(tmp, x=xnew, y=y)
                ll = np.load(tmp)
                assert 'x' in ll.keys()
                assert 'y' in ll.keys()
                assert_equal(xnew, ll['x'])
                assert_equal(y, ll['y'])

        # file is not zipfile
        for updatez in updatez_list:
            with temppath(prefix="np_test_updatez_", suffix=".npz") as tmp:
                updatez(tmp, x=x)
                ll = np.load(tmp)
                assert 'x' in ll.keys()
                assert_equal(x, ll['x'])
                updatez(tmp, x=xnew, y=y)
                ll = np.load(tmp)
                assert 'x' in ll.keys()
                assert 'y' in ll.keys()
                assert_equal(xnew, ll['x'])
                assert_equal(y, ll['y'])

        # array passed as arg
        for updatez in updatez_list:
            with temppath(prefix="np_test_updatez_", suffix=".npz") as tmp:
                updatez(tmp, x=x)
                ll = np.load(tmp)
                assert 'x' in ll.keys()
                assert_equal(x, ll['x'])
                updatez(tmp, xnew, x=xnew, y=y)
                ll = np.load(tmp)
                assert 'x' in ll.keys()
                assert 'y' in ll.keys()
                assert 'arr_0' in ll.keys()
                assert_equal(xnew, ll['x'])
                assert_equal(y, ll['y'])
                assert_equal(xnew, ll['arr_0'])

        # file does not exist yet
        for updatez in updatez_list:
            fd, tmp = mkstemp('.npz')
            os.close(fd)
            os.remove(tmp)
            updatez(tmp, x=x)
            ll = np.load(tmp)
            assert 'x' in ll.keys()
            assert_equal(x, ll['x'])
            updatez(tmp, x=xnew, y=y)
            ll = np.load(tmp)
            assert 'x' in ll.keys()
            assert 'y' in ll.keys()
            assert_equal(xnew, ll['x'])
            assert_equal(y, ll['y'])
            os.remove(tmp)

        # file without .npz suffix
        for updatez in updatez_list:
            fd, tmp = mkstemp()
            os.close(fd)
            os.remove(tmp)
            updatez(tmp, x=x)
            tmpz = tmp + '.npz'
            ll = np.load(tmpz)
            assert 'x' in ll.keys()
            assert_equal(x, ll['x'])
            updatez(tmpz, x=xnew, y=y)
            ll = np.load(tmpz)
            assert 'x' in ll.keys()
            assert 'y' in ll.keys()
            assert_equal(xnew, ll['x'])
            assert_equal(y, ll['y'])
            os.remove(tmpz)

        # Errors

        # path-like objects
        for updatez in updatez_list:
            tmp = BytesIO()
            self.assertRaises(ValueError, updatez, tmp, x=x)

        # un-named variable and keyword have name 'arr_0'
        for updatez in updatez_list:
            with temppath(prefix="np_test_updatez_", suffix=".npz") as tmp:
                # savez raises error
                self.assertRaises(ValueError, updatez, tmp, x, arr_0=x)
                updatez(tmp, x)
                ll = np.load(tmp)
                assert 'arr_0' in ll.keys()
                assert_equal(x, ll['arr_0'])
                # updatez raises error
                self.assertRaises(ValueError, updatez, tmp, x, arr_0=x)


if __name__ == "__main__":
    unittest.main()
