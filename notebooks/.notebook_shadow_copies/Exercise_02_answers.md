---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.4
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

<!-- #region tags=[] -->
# LFRic Iris data manipulation and visualisation practical

Let's apply what we've learned about data processing and visualisation of LFRic data in Iris and PyVista with the two exercises. \

The aim is to use the prompts to write the code yourself, but we have also provided a separate notebook containing the answers if you are stuck \

All the information needed to write the code for this practical can be found in the notebooks in the first part of this practical \

Note: this is delivered in Jupyter labs, but sometime the PyVista and GeoVista plotting is laggy in labs. If you prefer you can run in ipython.


<!-- #endregion -->

## Exercise 2 - Regrid UM data to LFRic and plot using PyVista


Now you can do a similar exercise compared to the previous Exercise 1, but regrid UM data onto a LFRic mesh and plot the data using PyVista


**Step 1** To begin, we need to import the neccesary packages that we will need for this exercise.

```python
%matplotlib inline
import pyvista as pv
import geovista as gv
import geovista.theme
import iris.quickplot as qplt
import iris
from geovista import GeoPlotter
from esmf_regrid.experimental.unstructured_scheme import MeshToGridESMFRegridder, GridToMeshESMFRegridder
from iris.experimental.ugrid.load import PARSE_UGRID_ON_LOAD
pv.rcParams["use_ipyvtk"] = True
iris.FUTURE.datum_support = True  # avoids some warnings
```

The pv_conversions script contains two functions which convert LFRic cubes to pyvista objects. Load these two functions:

```python
from pv_conversions import pv_from_lfric_cube
from pv_conversions import pv_from_um_cube
```

**Step 2** Lets chose a different diagnostic, 'surface_temperature' and load both the UM data, as well LFRic data to use as reference grid.

```python
# Define the location of the data and file names
data_path = '../example_data/'
lfric_path = data_path + 'u-ct674_20210324T0000Z_lf_ugrid.nc'
um_path = data_path + 'u-ct674_20210324T0000Z_um_latlon.nc'

with PARSE_UGRID_ON_LOAD.context():
    lfric_rho = iris.load_cube(lfric_path, 'surface_air_pressure')
    
um_temp = iris.load_cube(um_path, 'surface_temperature')
um_temp_t0 = um_temp[0]
```

**Step 3** Initialise the regridder 'GridToMeshESMFRegridder' \
Then use the regridder to regrid the new UM cube created earlier. Print your result and notice the mesh characterisics.

```python
g2m_regridder = GridToMeshESMFRegridder(um_temp_t0, lfric_rho)
regridded_um = g2m_regridder(um_temp_t0)
print(regridded_um)
```

**Step 4** Plot the regridded UM data with PyVista. \
(hint: before you can do this you will need to convert you mesh to polydata using pv_from_lfric_cube)

```python
pv = pv_from_lfric_cube(regridded_um)
pv.plot()
```

**Step 5** Plot the native UM data with PyVista. \
(hint: before you can do this you will need to convert you mesh to polydata using pv_from_um_cube)

```python
um_pv = pv_from_um_cube(um_temp_t0)
um_pv.plot()
```

**Step 6** Now we can plot this data side by side \
(hints: start by using plotter = GeoPlotter(shape=(1,2)), then create your subplots, add your coastlines, add a base layer, and add you mesh) \
note: PyVista and GeoVista can be slow in jupyter labs, but try and move the plots, look at the poles - you might notice the polar sigularity problem of the lat-lon grid.

```python
plotter = GeoPlotter(shape=(1, 2))

plotter.subplot(0, 0)
plotter.add_coastlines()
plotter.add_base_layer(texture=gv.natural_earth_1())
plotter.add_mesh(pv, show_edges=True)

plotter.subplot(0, 1)
plotter.add_coastlines()
#plotter.add_base_layer(texture=gv.natural_earth_1())
plotter.add_mesh(um_pv, show_edges=True)

# Make left+right move together
plotter.link_views()

# Try to rationalise the global view a little.
plotter.view_xz()
    
plotter.show()
```

**Step 7** In notebook Section 3, we see how to use the plotter.camera_position = viewpoint functionality. Try this out with the surface temperature data. 

```python
viewpoint = [
    (0.9550352379408845, 0.9378277371075855, 0.9637172962958191),
    (0.0, 0.0, 0.0),
    (-0.3202752464164225, -0.5004192729867466, 0.8043657860428399)
]

plotter.camera_position = viewpoint

plotter.show()
```

**Finished!?** These two exercises were just the beginning. If you have time try adding some cells below and extract a zonal mean, or try to select a region of data. 
