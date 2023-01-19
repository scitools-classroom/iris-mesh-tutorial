"""Routines providing a simple interface to load matching UM and LFRic test data as Iris cubes."""

from pathlib import Path
datadir = Path('/scratch/sworsley/lfric_data')

import iris
iris.FUTURE.datum_support = True  # avoids some irritating warnings

from iris.experimental.ugrid.load import PARSE_UGRID_ON_LOAD


um_filepth = datadir / '20210324T0000Z_um_latlon.nc'
lfric_filepth = datadir / '20210324T0000Z_lf_ugrid.nc'

def um_all_datacubes():
    return iris.load(um_filepth)

def um_rh_alltimes_3d():
    return iris.load_cube(um_filepth, 'relative_humidity')

def um_rh_singletime_2d():
    cube = um_rh_alltimes_3d()
    return cube[0]

def lfric_all_datacubes():
    with PARSE_UGRID_ON_LOAD.context():
        cubes = iris.load(lfric_filepth)
    return cubes

def lfric_rh_alltimes_3d():
    with PARSE_UGRID_ON_LOAD.context():
        rh_cube = iris.load_cube(lfric_filepth, 'relative_humidity_at_screen_level')
    return rh_cube

def lfric_rh_singletime_2d():
    cube = lfric_rh_alltimes_3d()
    return cube[0]

