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

# Section 4 : Extracting a region from a mesh

This process is considerably more involved than with "structured" data like UM.

For instance, UM data has data and coordinates with X and Y dimensions, corresponding to cell indices in the model arrays, and longitudes and latitudes of cells on the globe.  
Therefore, we can slice out a rectangular range of X and Y indices, e.g. `my_datacube[..., 10:40, 4:77]` and the result is some contiguous region of the globe within a defined range of latitude+longitude.

However, the unstructured mesh does not visit locations on the globe in any particular, simple regular pattern.  So crucially, a slice of data from the (now 1-D) arrays is not a contiguous geographical region.  And conversely a contiguous region of the data is generally not contained in a contiguous range of data indices.  
( *TODO: picture of this ?* )

So we must use geographical calculations to extract mesh data within a required region.  
Since this is a geographical concept, Geovista provides support for it.

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
And show the resulting object.

```python
# 'Apply' the region to the PolyData object.
pv_regional_rh = bbox.enclosed(pv_global_rh)
pv_regional_rh
```

You can see that the new (regional) polydata has fewer cells than the original (global) one.

---

**Now index the regional PolyData with `pv["vtkOriginalCellIds"]`, to get an array of cell indexes**  
and show the result.

```python
# Get the remaining face indices, to use for indexing the Cube.
region_indices = pv_regional_rh["vtkOriginalCellIds"]
region_indices
```

**Note:** This shows the original cell indices of the cells which fall within the region.

Now we can use these to select only those cell *from the Iris cube*.

**Apply these cells as an index to the 'mesh dimension' of the original Iris lfric-rh cube**  
and show that

```python
lfric_rh_region = lfric_rh[..., region_indices]
lfric_rh_region
```

This cube contains the mesh data within our selected region.

However, there is a catch here :  Once indexed, our cube ***no longer has a mesh***.  
You can see this in the printout, which lists "Auxiliary coordinates" but no "Mesh coordinates".
This problem will probably be fixed in future.  See [here in the Iris docs](https://scitools-iris.readthedocs.io/en/latest/further_topics/ugrid/operations.html#region-extraction) for a discussion.

For now, what we need to do is to re-create a mesh for the regional cube.
We do that in a few steps ...

---

Step 1 : **Get the X and Y-axis coordinates from the region cube.**
Use `Cube.coords('longitude')` etc.

```python
x_coord = lfric_rh_region.coord('longitude')
y_coord = lfric_rh_region.coord('latitude')
```

Step 2 : **Create a new `iris.experimental.ugrid.Mesh`-class object, passing the X,Y coords as arguments**

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
Step 3 : **call `Mesh.to_MeshCoords` to create a pair of `MeshCoord`s containing this mesh**  
Note : you must specify the keyword `location="face"` :  This matches the data location of the original data -- i.e. the data cells are faces.

```python
mesh_coords = mesh.to_MeshCoords(location="face")
mesh_coords
```

---
Step 4 : (finally!!)  
**Use `Cube.remove_coord` and `Cube.add_aux_coord` to replace each AuxCoord with its corresponding `MeshCoord` from the previous step.** Note : for 'add_aux_coord', you also need to specify the relevant cube dimension(s) : See [`Cube.add_aux_coord` in the Iris docs](https://scitools-iris.readthedocs.io/en/latest/generated/api/iris/cube.html?highlight=add_aux_coord#iris.cube.Cube.add_aux_coord)  

And show the cube ..

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

Lastly, plot this to see what we get.

The following steps ...
  * create a PolyData from the regional cube with `pv_conversions.pv_from_lfric_cube`
  * follow the steps shown in the Plotting section

```python
pv = pv_from_lfric_cube(lfric_rh_region)
from geovista import GeoPlotter
plotter = GeoPlotter()
plotter.add_mesh(pv)
plotter.show()
```

----

**Investigation:** It is useful to add some extra background information to make this more visible.

As a minimum you can use `plotter.add_coastlines()`.

Another useful one is `plotter.add_base_layer()`
**What does that do ?**

```python
plotter.add_coastlines()
plotter.add_base_layer()
plotter.show()

```

----

**Investigation:** 
If you rotate the above images, you will see they don't behave liekt e

As a minimum you can use `plotter.add_coastlines()`.

Another useful one is `plotter.add_base_layer()`
**What does that do ?**

```python

```
