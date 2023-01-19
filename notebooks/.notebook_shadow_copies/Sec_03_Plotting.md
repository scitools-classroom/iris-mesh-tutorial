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

# Section 3 : 3d visualisation and plotting

Schema :
  * Introduce Geovista
  * Explain context of 3D and "traditional" matplotlib-based plotting


# 3D visualisation

While LFRic data can be presented in 2D plots with a map projection, it is often more profitable way to explore it with a 3D viewer.  

There are a few reasons for this :
  1. the LFRic model grid does not follow a 2d, lat-lon aligned structure (unlike UM)
  2. LFRic data is now tending to be too large for matplotlib-style plotting (~6 million cells)


```python

```

```python tags=[]
# Essential setup
%matplotlib inline
import pyvista as pv
pv.rcParams["use_ipyvtk"] = True
```

### What Geovista is for

  * **VTK** : highly mature 3D visualisation library (C++)
  * **PyVista** : VTK for normal humans (in Python)
  * **Geovista** : geolocation for PyVista
     * map projections + transforms
     * geolocated data and regions
     * coastlines



```python
# Import things from Geovista
import geovista as gv
import geovista.theme
```

```python
# Copied from : https://github.com/bjlittle/geovista/blob/main/src/geovista/examples/from_2d__orca.py
from geovista.pantry import um_orca2

sample = um_orca2()
```

```python
# Handy routine

def trial_display(xx, yy, data, title="") -> None:
    # create the mesh from the sample data
    mesh = gv.Transform.from_2d(xx, yy, data=data)

    # remove cells from the mesh with nan values
    mesh = mesh.threshold()

    # plot the mesh
    plotter = gv.GeoPlotter()
    sargs = dict(title=f"{sample.name} / {sample.units}", shadow=True)
    plotter.add_mesh(mesh, show_edges=True, scalar_bar_args=sargs)
    plotter.add_base_layer(texture=gv.natural_earth_1())
    plotter.add_coastlines()
    plotter.add_axes()
    plotter.add_text(
        title,
        position="upper_left",
        font_size=10,
        shadow=True,
    )
    plotter.show()
```

#### Geovista basic demo : an interactive plot of ocean data

```python
trial_display(sample.data, sample.lats, sample.lons, "ORCA test data")
```

sdsadas&





**NOTE**
  * Geovista is not Iris-dependent
  * Iris does not (yet) fully integrate Geovista
  * .. therefore user code is currently needed to bridge the two
  * .. **but** the gap is fairly small, and this makes Geovista more generally useful



