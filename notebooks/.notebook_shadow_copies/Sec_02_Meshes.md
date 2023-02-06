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

# Section 2 : Mesh Concepts, and the LFRic mesh

A Mesh is a way of describing spatial regions, which may also have data values associated to them.

Iris uses the [UGRID](http://ugrid-conventions.github.io/ugrid-conventions/) conventions encoding standard as its basis for representing meshes.  
UGRID is an extension of the [CF Conventions](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.10/cf-conventions.html).  It prescribes a CF-compatible way of recording meshes and mesh data in NetCDF files.  

We will briefly explain some UGRID concepts, and then go on to show how this looks in Iris (some of which you've already seen).  
For a more thorough discussion, see the [Iris Mesh Data documentation pages](https://scitools-iris.readthedocs.io/en/latest/further_topics/ugrid/data_model.html#)

<!-- #region tags=[] -->
## Basic constructions

UGRID can describe spatial **points**, **lines** and (polygonal) **faces**.  

Appropriate data can be associated with any of these -- e.g. sampled values at cell corners (points), 
or average values over each cell region (faces).

UGRID's permitted element types are :
  * **node** - a point in space, defined by some M coordinate values
  * **edge** - a line between 2 end nodes
  * **face** - a polygon with some N nodes as its corners

Thus, "edges" and "faces" are defined in terms of "nodes".  
A **mesh** contains -
  * arrays of coordinates which define its **nodes**, plus _optionally_ ..
  * optional node-number arrays which add **edges** and/or **faces**, by listing the nodes which define them (i.e. their ends or corners)

In addition, edges and faces can have associated coordinate values.
These are independent of the nodes defining line-ends/face-vertices, and represent an additional associated
spatial location for each element, often used to represent something like a mid-point.
<!-- #endregion -->

<!-- #region tags=[] -->
Extra Notes: 
  * a file can contain multiple meshes.  Each is self-contained.
  * a file will contain a dimension mapping each component defined by a mesh,  
    e.g. a node dimension and a face dimension.
  * other types of component are also possible and may be present (more rarely).  
    ( See full specs for details. )  

<!-- #endregion -->

### Construction of an abstract Mesh in Iris
This is too complex to cover in detail here.  
For those interested, this is explained in the bonus notebook ["mesh_from_numbers.ipynb"](./mesh_from_numbers.ipynb).


## Actual LFRic meshes

The most common usage (at least in LFRic output), is to have a mesh which defines nodes + faces, 
plus data variables mapped to the face components.

Here is an example of what that looks like :--


![Picture of nodes and faces](LFRic_mesh.svg)


This diagram demonstrates the relationship between face-numbers, node-numbers and node coordinates.
Note that no _edges_ are shown here :  In UGRID, and Iris, mesh faces do not depend on edges, but are built only from nodes.

Technically, the LFRic mesh is a "**cubesphere**".  
  * the surface of the globe is divided into 6 equal 'panels', analagous to the 6 faces of a cube
  * each panel is subdivided into N * N cells, giving 6.N^2 total cells
  * the above view shows the neighbourhood of one cubesphere 'corner'

**We will next load some actual LFRic data and look at how the mesh appears in Iris.**


---

### Fetch some sample unstructured data
As used in Section#01

**Import the data-access routine `lfric_rh_singletime_2d` from `testdata_fetching`, and call it to get a single two-dimensional test cube.**

```python
from testdata_fetching import lfric_rh_singletime_2d
lfric_rh = lfric_rh_singletime_2d()
```

**Print the cube, and its `cube.mesh`**

```python
print(lfric_rh)
print('\n----\n')
print(lfric_rh.mesh)
```

### Details of the Iris mesh content

How Iris represents the mesh is not usually very relevant to working with cube data in Iris, nor to plotting it with PyVista.  
So that is beyond the scope of an introductory tutorial.  

However, for those interested, there is a bonus notebook showing some of this : ["Mesh_Connectivities_demo.ipynb"](./Mesh_Connectivities_demo.ipynb)



### Plotting mesh data : minimal 3D visualisation of a 2D cube


This is just a quick preview of the next section (Sec_03_Plotting), to show a basic 3D plot.


<!-- #region jp-MarkdownHeadingCollapsed=true tags=[] -->
**Convert a cube to PyVista form for plotting**

There are as yet *no* facilities in Iris for plotting unstructed cubes.  
We can do that using PyVista, but we need first to convert the data to a PyVista format.  

So first,  
**Import the routine** `pv_conversions.pv_from_lfric_cube` **(provided here in the tutorial).  
And call that..**

<!-- #endregion -->

```python
from pv_conversions import pv_from_lfric_cube

pv = pv_from_lfric_cube(rh_t0)
```

This produces a PyVista ["PolyData" object](https://docs.pyvista.org/api/core/_autosummary/pyvista.PolyData.html#pyvista-polydata).  
Which is a thing we can plot, by simply calling its `.plot()` method.


---

**Call the `plot` routine of the PolyData object.  An output should appear.**

```python
pv.plot()
```

**NOTES**:
  * this plot is interactive -- try dragging to rotate, and the mouse scroll-wheel to zoom
  * this obviously causes some clutter and uses up some space (e.g. you can't easily scroll past it)  
    * To ***remove*** a plot output, use "Clear Output" from the "Edit" menu (or from right-click on the cell)
  * alternatively, set the keyword `jupyter_backend='static'` in the command, for output as a plain image

There are a lot more keywords available to [the `PolyData.plot()` method](https://docs.pyvista.org/api/core/_autosummary/pyvista.PolyData.plot.html), but it is not ideal to overcomplicate these calls.  
Finer control is better achieved in a different ways :  See more detail on plotting in [the Plotting section](./Sec_03_Plotting.ipynb).


## Next notebook
See the next section : [03 - Plotting and Visualisation](./Sec_03_Plotting.ipynb)

```python

```
