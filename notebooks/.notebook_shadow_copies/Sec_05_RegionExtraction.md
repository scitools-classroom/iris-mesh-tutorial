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
( *TODO: picture of this ?* )

So we must use geographical calculations to extract mesh data within a required region.  
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

---

Now we will create a tool to extract over a desired region.


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

**Now "apply" the BBox to the global mesh data, by passing it to the `BBox.enclosed` method.**  
And show the resulting object printout.

```python
# 'Apply' the region to the PolyData object.
pv_regional_rh = bbox.enclosed(pv_global_rh)
pv_regional_rh
```

You can see that this new (regional) PolyData has fewer cells than the original (global) one.

---
**Now plot this to see what it looks like.**  
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
# Temporary : show static plot for notebook review
plotter.show(jupyter_backend='static')
```

<!-- #region -->
---
## Get an Iris cube for an extracted region.

While GeoVista provides the efficient tools for mesh region extraction, it and Iris know nothing about one another.  
So, to calculate a regionally-extracted _Iris cube_, GeoVista can do the hard work of determining the subset of cells required, but you must then "reconstruct" an Iris cube from that information.  
For now, at least, there are no ready-made tools for this (either in Iris or Geovista).  

So, this task is rather involved at present, but for those interested a working code example is provided as bonus content in a [separate notebook (broken link!)](to-link-here).


## DEVELOPER-TODO : relegate all this to a separate "bonus content" notebook


While GeoVista provides the efficient tools for mesh region extraction, it and Iris know nothing about one another.  
So, to calculate a regionally-extracted _Iris cube_, GeoVista can do the hard work of determining the subset of cells required, but you must then "reconstruct" an Iris cube from that information.  
For now, at least, there are no ready-made tools for this (either in Iris or Geovista).  

The process requires a few steps, which we can summarise as :
  1. record, on the original global PolyData, the original face indices of each of the cells
  1. perform extraction (by BBox or otherwise) to get a regional PolyData
  1. get the face-indices of the selected cells from the regional PolyData  
  1. index the Iris cube with the selected indices, on the mesh dimension, to extract the regional parts
  1. construct and attach a suitable Iris mesh to represent the extracted region

( Note: the last step itself is not strictly necessary. It may be sufficent to have a regional data cube with a notional "mesh dimension", but which does not possess an actual Iris mesh. )

---
Let's show that operation ...

**Step 1 : First, add an auxiliary array to the global PolyData, recording the original (face) index of each cell.**  
Note : use numpy.arange() to construct a counting sequence, and assign to a named index on the PolyData object.
<!-- #endregion -->

```python
import numpy as np
face_inds = np.arange(pv_global_rh.n_cells)
pv_global_rh.cell_data['original_face_indices'] = face_inds
```

---

**Step 2 : Extract with your Bbox to get a regional PolyData, and show the result.**  
This code is exactly the same as the previous time we did this.

```python
pv_regional_rh = bbox.enclosed(pv_global_rh)
pv_regional_rh
```

You can see that the new version of the extracted (regional) data now has an ***extra*** attached data array, derived from the one we added to the global data, and which holds the selected face indices.

---

**Step 3 : Fetch the indices array from the regional PolyData, by indexing with the array name.**  
and show the result.

```python
# Get the remaining face indices, to use for indexing the Cube.
region_indices = pv_regional_rh["original_face_indices"]
region_indices
```

This contains the original face-indices of all the cells which fall within the region, _i.e. which faces those were in the global mesh_.

We can now apply these indices, to select only those cells *from the Iris cube*.

**Step 4 : Apply these cells as an index to the 'mesh dimension' of the original Iris lfric-rh cube**  
.. and print that out.

```python
lfric_rh_region = lfric_rh[..., region_indices]
lfric_rh_region
```

This new cube contains the mesh data within our selected region.

However, there is a catch here :  Once indexed, our cube ***no longer has a mesh***.  
You can see this in the printout, which lists "Auxiliary coordinates" but no "Mesh coordinates".

This problem will probably be fixed in future.  See [here in the Iris docs](https://scitools-iris.readthedocs.io/en/latest/further_topics/ugrid/operations.html#region-extraction) for a discussion.

For now, what we need to do is to re-create a mesh for the regional cube.
We do that in a few further steps ...

---

**Step 5a : Get the X and Y-axis coordinates from the region cube.**
Use `Cube.coords('longitude')` etc.

```python
x_coord = lfric_rh_region.coord('longitude')
y_coord = lfric_rh_region.coord('latitude')
```

**Step 5b : Create a new `iris.experimental.ugrid.Mesh`-class object, passing the X,Y coords as arguments**

```python
from iris.experimental.ugrid.mesh import Mesh
mesh = Mesh.from_coords(x_coord, y_coord)
```

( Step 2a : **`print()` the Mesh object**  
Note : `Mesh` does not provide a notebook display method.  
)

```python
print(mesh)
```

---
**Step 5c :  Call `Mesh.to_MeshCoords` to create a pair of `MeshCoord`s containing this mesh**  
Note : you must specify the keyword `location="face"` :  This matches the data location of the original data -- i.e. the data cells are faces.

```python
mesh_coords = mesh.to_MeshCoords(location="face")
mesh_coords
```

---
**Step 5d : (finally!!)  
Use `Cube.remove_coord` and `Cube.add_aux_coord` to replace each AuxCoord with its corresponding `MeshCoord` from the previous step.** Note : for 'add_aux_coord', you also need to specify the relevant cube dimension(s) : See [`Cube.add_aux_coord` in the Iris docs](https://scitools-iris.readthedocs.io/en/latest/generated/api/iris/cube.html?highlight=add_aux_coord#iris.cube.Cube.add_aux_coord)  
.. and show the cube ..

```python
lfric_rh_region.remove_coord('longitude')
```

```python
lfric_rh_region.remove_coord('latitude')
```

```python
xco, yco = mesh_coords

lfric_rh_region.add_aux_coord(xco, 0)
lfric_rh_region.add_aux_coord(yco, 0)

# Result : a regional Mesh-Cube with a subset of the original faces.
lfric_rh_region
```

---

**Lastly, plot this to see what we got.**  
Use the techniques as above, converting with `pv_from_lfric_cube` and plotting.


```python
pv = pv_from_lfric_cube(lfric_rh_region)
pv.plot()
```

----

**Investigation:** It is useful to add some extra background information to make this more visible.

As a minimum you can use `plotter.add_coastlines()`.

Another useful one is `plotter.add_base_layer()`  
**Question :  what does that actually do ?**

```python
plotter.add_coastlines()
plotter.add_base_layer()
plotter.show()
```

```python

```
