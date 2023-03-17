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

# Extract a regional mesh-cube with Iris

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

**First, we just repeat some of the imports + code from 'Sec_04_Region_Extraction'**

To get a global mesh-cube and a PolyData derived from it.

```python
# Fetch a single cube of test data
from testdata_fetching import lfric_rh_singletime_2d
lfric_rh = lfric_rh_singletime_2d()
lfric_rh
```

```python
# Convert to a PyVista.PolyData
from pv_conversions import pv_from_lfric_cube
pv_global_rh = pv_from_lfric_cube(lfric_rh)
```

```python
# Define a lat-lon region to extract -- EXACTLY AS BEFORE
from geovista.geodesic import BBox
bbox = BBox(lons=[0, 70, 70, 0], lats=[-25, -25, 45, 45])
```

```python
# 'Apply' the region to the PolyData object.
pv_regional_rh = bbox.enclosed(pv_global_rh)
pv_regional_rh
```

<!-- #region -->
---
## Now the meshcube extraction, as a sequence of steps ...


### Step 1 : Add an auxiliary array to our _global_ PolyData
This is to record, for each PolyData cell, the original (face) index which that cell has.

Note : we use numpy.arange() to construct a counting sequence, and make this a new array on the PolyData object, by assigning to a index-name.
<!-- #endregion -->

```python
import numpy as np
face_inds = np.arange(pv_global_rh.n_cells)
# Assign PolyData[<a-string>] to create a new attached array.
pv_global_rh.cell_data['original_face_indices'] = face_inds
```

---

### Step 2 : Extract with your Bbox to get a regional PolyData, and show the result.
This code is exactly the same as the previous time we did this.

```python
pv_regional_rh = bbox.enclosed(pv_global_rh)
pv_regional_rh
```

You can see that the new version of the extracted (regional) data now has an ***extra*** attached data array, "`original_face_indices`", which is derived from the one we added to the global data, and which holds the face indices of the _selected_ cells.

---

**Step 3 : Fetch the indices array from the regional PolyData, by indexing with the array name.**  
and show the result.

```python
# Get the remaining face indices, to use for indexing the Cube.
region_indices = pv_regional_rh["original_face_indices"]
region_indices
```

This contains the original face-indices of all the cells which fall within the region, _i.e. which faces those were in the global mesh_.

We can now apply these via indexing, to select only those cells *from the Iris cube*.

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
from geovista import GeoPlotter
plotter = GeoPlotter()
plotter.add_mesh(pv)
plotter.add_coastlines()
plotter.add_base_layer()
plotter.show()
```

```python

```
