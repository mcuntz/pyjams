#!/usr/bin/env python
"""
This is the unittest for pack module.

python -m unittest -v tests/test_pack.py
python -m pytest --cov=pyjams --cov-report term-missing -v tests/test_pack.py

Not covered:
267: Index creation failing is probably not possible
     at that stage of the algorithm

"""
import unittest


class TestPack(unittest.TestCase):
    """
    Tests for pack.py
    """

    def test_pack(self):
        import numpy as np
        from pyjams import pack

        # dimensions
        d0 = 2
        d1 = 3
        d2 = 4
        d3 = 5

        # data arrays
        s2 = (d1, d0)
        data2d = np.arange(np.prod(s2), dtype=float).reshape(s2) + 1.
        s3 = (d2, d1, d0)
        data3d = np.arange(np.prod(s3), dtype=np.float32).reshape(s3) + 1.
        s4 = (d3, d2, d1, d0)
        data4d = np.arange(np.prod(s4), dtype=int).reshape(s4) + 1

        # masked arrays
        mask2d = np.zeros(np.prod(s2), dtype=bool)
        mask2d[::2] = True
        mask2d = mask2d.reshape(s2)

        mask3d = np.zeros(np.prod(s3), dtype=bool)
        mask3d[::2] = True
        mask3d = mask3d.reshape(s3)

        # masked array as values
        imask2d = mask2d.astype(int)
        fmask2d = mask2d.astype(float)

        # data2d, mask2d
        ois = pack(data2d, mask2d)
        ii = np.where(mask2d)
        osoll = data2d[ii]
        assert ois.dtype == data2d.dtype
        assert np.all(ois == osoll)

        # data3d, mask3d
        ois = pack(data3d, mask3d)
        ii = np.where(mask3d)
        osoll = data3d[ii]
        assert ois.dtype == data3d.dtype
        assert np.all(ois == osoll)

        # data3d, mask2d
        ois = pack(data3d, mask2d)
        ii = np.where(mask2d)
        osoll = data3d[:, ii[0], ii[1]]
        assert ois.dtype == data3d.dtype
        assert np.all(ois == osoll)

        # data3d, mask2d as values
        ois = pack(data3d, imask2d)
        ii = np.where(mask2d)
        osoll = data3d[:, ii[0], ii[1]]
        assert ois.dtype == data3d.dtype
        assert np.all(ois == osoll)
        ois = pack(data3d, fmask2d)
        assert ois.dtype == data3d.dtype
        assert np.all(ois == osoll)

        # data4d, mask2d
        ois = pack(data4d, mask2d)
        ii = np.where(mask2d)
        osoll = data4d[..., ii[0], ii[1]]
        assert ois.dtype == data4d.dtype
        assert np.all(ois == osoll)

        # data4d, mask3d
        ois = pack(data4d, mask3d)
        ii = np.where(mask3d)
        osoll = data4d[:, ii[0], ii[1], ii[2]]
        assert ois.dtype == data4d.dtype
        assert np.all(ois == osoll)

    def test_unpack(self):
        import numpy as np
        from pyjams import pack, unpack

        # dimensions
        d0 = 2
        d1 = 3
        d2 = 4
        d3 = 5

        # data arrays
        s2 = (d1, d0)
        data2d = np.arange(np.prod(s2)).reshape(s2) + 1.
        s3 = (d2, d1, d0)
        data3d = np.arange(np.prod(s3)).reshape(s3) + 1.
        s4 = (d3, d2, d1, d0)
        data4d = np.arange(np.prod(s4), dtype=int).reshape(s4) + 1

        # masked arrays
        mask2d = np.zeros(np.prod(s2), dtype=bool)
        mask2d[::2] = True
        mask2d = mask2d.reshape(s2)

        mask3d = np.zeros(np.prod(s3), dtype=bool)
        mask3d[::2] = True
        mask3d = mask3d.reshape(s3)

        # masked array as values
        imask2d = mask2d.astype(int)
        fmask2d = mask2d.astype(float)

        # data2d, mask2d
        ois = pack(data2d, mask2d)
        ii = np.where(mask2d)
        osoll = data2d[ii]
        assert ois.dtype == data2d.dtype
        assert np.all(ois == osoll)
        uis = unpack(ois, mask2d)
        assert uis.dtype == data2d.dtype
        assert np.all(uis[ii] == data2d[ii])
        uis = unpack(ois, mask2d, fill_value=-1)
        jj = np.where(~mask2d)
        assert uis.dtype == data2d.dtype
        assert np.all(uis[ii] == data2d[ii])
        assert np.all(uis[jj] == -1)

        # data3d, mask3d
        ois = pack(data3d, mask3d)
        ii = np.where(mask3d)
        osoll = data3d[ii]
        assert ois.dtype == data3d.dtype
        assert np.all(ois == osoll)
        uis = unpack(ois, mask3d)
        assert uis.dtype == data3d.dtype
        assert np.all(uis[ii] == data3d[ii])
        uis = unpack(ois, mask3d, -1)
        jj = np.where(~mask3d)
        assert uis.dtype == data3d.dtype
        assert np.all(uis[ii] == data3d[ii])
        assert np.all(uis[jj] == -1)

        # data3d, mask2d
        ois = pack(data3d, mask2d)
        ii = np.where(mask2d)
        osoll = data3d[:, ii[0], ii[1]]
        assert ois.dtype == data3d.dtype
        assert np.all(ois == osoll)
        uis = unpack(ois, mask2d)
        assert uis.dtype == data3d.dtype
        assert np.all(uis[:, ii[0], ii[1]] == data3d[:, ii[0], ii[1]])
        uis = unpack(ois, mask2d, -1)
        jj = np.where(~mask2d)
        assert uis.dtype == data3d.dtype
        assert np.all(uis[:, ii[0], ii[1]] == data3d[:, ii[0], ii[1]])
        assert np.all(uis[:, jj[0], jj[1]] == -1)

        # data3d, mask2d as values
        ois = pack(data3d, imask2d)
        ii = np.where(mask2d)
        osoll = data3d[:, ii[0], ii[1]]
        assert ois.dtype == data3d.dtype
        assert np.all(ois == osoll)
        uis = unpack(ois, imask2d)
        assert uis.dtype == data3d.dtype
        assert np.all(uis[:, ii[0], ii[1]] == data3d[:, ii[0], ii[1]])
        uis = unpack(ois, imask2d, -1)
        jj = np.where(~mask2d)
        assert uis.dtype == data3d.dtype
        assert np.all(uis[:, ii[0], ii[1]] == data3d[:, ii[0], ii[1]])
        assert np.all(uis[:, jj[0], jj[1]] == -1)
        ois = pack(data3d, fmask2d)
        assert ois.dtype == data3d.dtype
        assert np.all(ois == osoll)
        uis = unpack(ois, fmask2d)
        assert uis.dtype == data3d.dtype
        assert np.all(uis[:, ii[0], ii[1]] == data3d[:, ii[0], ii[1]])
        uis = unpack(ois, fmask2d, -1)
        jj = np.where(~mask2d)
        assert uis.dtype == data3d.dtype
        assert np.all(uis[:, ii[0], ii[1]] == data3d[:, ii[0], ii[1]])
        assert np.all(uis[:, jj[0], jj[1]] == -1)

        # data4d, mask2d
        ois = pack(data4d, mask2d)
        ii = np.where(mask2d)
        osoll = data4d[..., ii[0], ii[1]]
        assert ois.dtype == data4d.dtype
        assert np.all(ois == osoll)
        uis = unpack(ois, mask2d)
        assert uis.dtype == data4d.dtype
        assert np.all(uis[..., ii[0], ii[1]] == data4d[..., ii[0], ii[1]])
        uis = unpack(ois, mask2d, -1)
        jj = np.where(~mask2d)
        assert uis.dtype == data4d.dtype
        assert np.all(uis[..., ii[0], ii[1]] == data4d[..., ii[0], ii[1]])
        assert np.all(uis[..., jj[0], jj[1]] == -1)

        # data4d, mask3d
        ois = pack(data4d, mask3d)
        ii = np.where(mask3d)
        osoll = data4d[:, ii[0], ii[1], ii[2]]
        assert ois.dtype == data4d.dtype
        assert np.all(ois == osoll)
        uis = unpack(ois, mask3d)
        assert uis.dtype == data4d.dtype
        assert np.all(uis[:, ii[0], ii[1], ii[2]] == (
            data4d[:, ii[0], ii[1], ii[2]] ))
        uis = unpack(ois, mask3d, -1)
        jj = np.where(~mask3d)
        assert uis.dtype == data4d.dtype
        assert np.all(uis[:, ii[0], ii[1], ii[2]] == (
            data4d[:, ii[0], ii[1], ii[2]] ))
        assert np.all(uis[:, jj[0], jj[1], jj[2]] == -1)


if __name__ == "__main__":
    unittest.main()
