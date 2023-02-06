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

# Section 5 : Extracting a region from mesh-based data

This process is considerably more involved than with "structured" data like UM.

For instance, UM data has data and coordinates with X and Y dimensions, corresponding to cell indices in the model arrays, and longitudes and latitudes of cells on the globe.  
Therefore, we can slice out a rectangular range of X and Y indices, e.g. `my_datacube[..., 10:40, 4:77]` and the result is some contiguous region of the globe within a defined range of latitude+longitude.

However, the unstructured mesh does not visit locations on the globe in any particular, simple regular pattern.  So crucially, a slice of data from the (now 1-D) arrays is not a contiguous geographical region.  And conversely a contiguous region of the data is generally not contained in a contiguous range of data indices.  
***For a demonstration of that :*** see the previous diagram showing numbering of nodes+faces around an LFRic cubesphere corner, [here](./LFRic_mesh.svg).

---

So, we must use geographical calculations to extract mesh data within a required region.  
Since this is a geographical concept, Geovista provides support for it.  
This is also a good match since, with larger data this can become quite compute-intensive :
Processing via VTK should be performant and scalable, and can benefit from GPU accelaration.

Here's an example of how to extract the mesh falling within a defined lat-lon region ...  
**NOTE: as with the plotting example, there are no Iris utility functions for this, so a fair amount of user code is currently required to mediate between the Iris and Geovista/PyVista worlds.**


---

**First, import the utility function `lfric_rh_datacube` from `testdata_fetching`, and call it to get a global LFRic test cube.**

```python
from testdata_fetching import lfric_rh_singletime_2d
lfric_rh = lfric_rh_singletime_2d()
lfric_rh
```

**Create a Polydata object from this.**  
Use the routine `pv_from_lfric_cube` from the package `pv_conversions`, which we used in the plotting section.

```python
from pv_conversions import pv_from_lfric_cube
pv_global_rh = pv_from_lfric_cube(lfric_rh)
```


## Create a 'BBox' tool to extract over a desired region.


**Import the class `BBox` from `geovista.geodesic`, and make one...**  

```python
from geovista.geodesic import BBox
```

Note: the name here is short for "Bounding Box".

**Use the notebook "?" command to display the function signature of its constructor : `?BBox.__init__`**

```python
?BBox.__init__
```

---

**Create a BBox to specify a bounding rectangle in lat-lon space.**  
Give it `lons` and `lats` arguments which specify the points of a bounding rectangle,
in lat-lon space, from 0..70 in longitude and -24..+45 in latitude.  
( *Note:* do ***not*** supply a duplicate 'end' point -- a closed loop is automatically generated. )

```python
bbox = BBox(lons=[0, 70, 70, 0], lats=[-25, -25, 45, 45])
```

---

## Apply the BBox to data
Operate on the global mesh data, by passing it to the `BBox.enclosed` method.**  
And show the resulting object printout.

```python
# 'Apply' the region to the PolyData object.
pv_regional_rh = bbox.enclosed(pv_global_rh)
pv_regional_rh
```

You can see that this new (regional) PolyData has fewer cells than the original (global) one.

---

### Plot this to see what it looks like.
Note : in this case, it will be very useful to add coastlines for reference.
Use the techniques from [Sec#2 Plotting - Additional features](./Sec_03_Plotting.ipynb#Additional-features).

```python
from geovista import GeoPlotter
plotter = GeoPlotter()
plotter.add_mesh(pv_regional_rh)
plotter.add_coastlines()
plotter.show()
```

```python
# Additional : static plot for notebook review
plotter.show(jupyter_backend='static')
```

---
## Get an Iris cube for an extracted region.

While GeoVista provides the efficient tools for mesh region extraction, it and Iris know nothing about one another.  
So, to calculate a regionally-extracted _Iris cube_, GeoVista can do the hard work of determining the subset of cells required, but you must then "reconstruct" an Iris cube from that information.

For now, at least, there are no ready-made tools for this (in either Iris or Geovista).  

However, the operation is possible, and may be instructive.  
So, for those interested, there is an extra notebook ["MeshCube_Extraction.ipynb"](./MeshCube_Extraction.ipynb), showing how this is done.


```python

```

## Next notebook

This is the end of the standard tutorial content.  
There is also some more detailed bonus content which you might be interested in : [see list here](./Mesh_Tutorial_Intro.ipynb#bonus_and_additional_material)

```python

```
