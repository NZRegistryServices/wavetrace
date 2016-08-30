import unittest
from pathlib import Path 
from shapely.geometry import Point

from wavetrace import *


class TestUtilities(unittest.TestCase):

    def test_check_tile_id(self):
        self.assertIsNone(check_tile_id('N03E027'))
        self.assertRaises(ValueError, check_tile_id, 'n03E027')
        self.assertRaises(ValueError, check_tile_id, 'N93E027')

    def test_get_tile_id(self):
        get = get_tile_id(27.5, 3.64)
        expect = 'N03E027'
        self.assertEqual(get, expect)

        get = get_tile_id(27.5, -3.64)
        expect = 'S04E027'
        self.assertEqual(get, expect)

        get = get_tile_id(-27.5, 3.64)
        expect = 'N03W028'
        self.assertEqual(get, expect)

        get = get_tile_id(-27.5, -3.64)
        expect = 'S04W028'
        self.assertEqual(get, expect)

    def test_get_bounds(self):
        get = get_bounds('N03E027')
        expect = [27, 3, 28, 4]
        self.assertSequenceEqual(get, expect)

        get = get_bounds('S03E027')
        expect = [27, -3, 28, -2]
        self.assertSequenceEqual(get, expect)

        get = get_bounds('N03W027')
        expect = [-27, 3, -26, 4]
        self.assertSequenceEqual(get, expect)

        get = get_bounds('S03W027')
        expect = [-27, -3, -26, -2]
        self.assertSequenceEqual(get, expect)

    def test_build_feature(self):
        f = build_feature('N03E027')
        # Should have coordinates of a quadrangle
        coords = f['geometry']['coordinates'][0]
        self.assertEqual(len(coords), 5)
        self.assertSequenceEqual(coords[0], coords[-1])

    def test_build_polygon(self):
        p = build_polygon('N03E027')
        # Should have coordinates of a quadrangle
        coords = list(p.exterior.coords)
        self.assertEqual(len(coords), 5)
        self.assertSequenceEqual(coords[0], coords[-1])

    def test_compute_intersecting_tiles(self):
        geometries = [
          Point((174.3, -35.7)), 
          Point((168.6, -45.2)).buffer(1, 1), # square buffer
          ]
        get = compute_intersecting_tiles(geometries)
        expect = ['S36E174', 
          'S45E167', 'S45E168', 'S45E169', 
          'S46E167', 'S46E168', 'S46E169', 
          'S47E168',
          ]
        self.assertCountEqual(get, expect)

    def test_get_geoid_height(self):
        get = get_geoid_height(-3.01, 16.78)
        expect = 28.7069
        self.assertEqual(get, expect)

    def test_get_center(self):
        bounds = [174, -36, 175, -35]
        get = get_center(tile_id)
        expect = (174.5, -35.5)
        self.assertSequenceEqual(get, expect)

    def test_get_subtile_bounds(self):
        tile_id = 'S36E174'
        n = 3
        bounds_list = get_subtile_bounds(tile_id, n=n)
        # Should be the correct length
        self.assertEqual(len(bounds_list), n**2)
        # Each bounds should be the correct length
        self.assertSequenceEqual([len(b) for b in bounds_list], 
          [4 for i in range(n**2)])
        # Should be correct on an example subtile
        delta = 1/n
        expect = [174, -36 + delta, 174 + delta, -36 + 2*delta]
        self.assertSequenceEqual(bounds_list[n], expect)


if __name__ == '__main__':
    unittest.main()
