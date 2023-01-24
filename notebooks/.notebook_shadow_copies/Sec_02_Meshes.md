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

## Actual LFRic meshes

The most common usage (at least in LFRic output), is to have a mesh which defines nodes + faces, 
plus data variables mapped to the face components.

Here is an example of what that looks like :--


![Picture of nodes and faces](ugrid_variable_faces.svg)


**NOTE** that, in the above, the faces (polygons) have different numbers of corners.

This does not happen in current LFRic data : the mesh is a "cubesphere" (see later images), and all cells have four corners.


---

## Fetch some sample unstructured data, as used in Section#01

**Import the data-access routine `lfric_rh_singletime_2d` from `testdata_fetching`, and call it to get a single two-dimensional test cube.**

```python
## TODO : remove later -- this bit is temporary, for initial testing with C48 data
from testdata_fetching import switch_data
switch_data(use_newer_smaller_c48_data=True)
```

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

```python
# TODO: work this up for user input

# Simply plot that ..
from pv_conversions import pv_from_lfric_cube
pv = pv_from_lfric_cube(lfric_rh)
pv.plot() #jupyter_backend='static')
```

```python

```

### Todo : examine mesh content + demonstrate APIs


## Plotting mesh data : minimal 3D visualisation of a 2D cube

<!-- #region -->
First, slice the cube to get the first timestep only  
  -- as we can only (easily) plot a 2d cube.

**Ex: Put this in a new cube variable, which is our 2D cube.**
<details><summary>Sample code solution : <b>click to reveal</b></summary>

```python
rh_t0 = lfric_rh[0]
```
</details>
<!-- #endregion -->

```python
from testdata_fetching import lfric_rh_singletime_2d

rh_t0 = lfric_rh_singletime_2d()
```

<!-- #region jp-MarkdownHeadingCollapsed=true tags=[] -->
### Convert a cube to PyVista form for plotting

There are as yet *no* facilities in Iris for plotting unstructed cubes.  
We can do that using PyVista, but we need first to convert the data to a PyVista format.  

So first,  
**Ex: import the routine `pv_from_lfric_cube` from the package `pv_conversions` (provided here in the tutorial).**
<details><summary>Sample code solution : <b>click to reveal</b></summary>

```python
from pv_conversions import pv_from_lfric_cube
```
</details>
<!-- #endregion -->

```python
from pv_conversions import pv_from_lfric_cube
```

<!-- #region -->
**Ex: now call that function, passing it our 2D RH cube, to get a PyVista object.**
<details><summary>Sample code solution : <b>click to reveal</b></summary>

```python
pv = pv_from_lfric_cube(rh_t0)
```
</details>
<!-- #endregion -->

```python
pv = pv_from_lfric_cube(rh_t0)
```

<!-- #region -->
This produces a PyVista ["PolyData" object](https://docs.pyvista.org/api/core/_autosummary/pyvista.PolyData.html#pyvista-polydata).  
Which is a thing we can plot.  

**Now just print that + see what it looks like ...**
<details><summary>Sample code solution : <b>click to reveal</b></summary>

```python
pv
```
</details>
<!-- #endregion -->

```python
pv
```

***TODO:*** some notes here on what the detail means ?


( Note: like `Cube`s + `CubeList`s, these `PolyData` objects are provided with a specific visible within the Jupyter notebooks.  This is displayed when you just enter the variable in a cell.  
You can also use "print(x)" to display the standard string representation of the object, but usually the notebook-style output is a bit more useful. )


---
### Quick 3d plotting

For a really quick, basic plot, you can display a PolyData as a VTK view with PyVista, by simply calling its `.plot` method.

**Call the `plot` routine of the PolyData object.  An output should appear.**

```python
pv.plot()
```

**NOTES**:
  * this plot is interactive -- try dragging to rotate, and the mouse scroll-wheel to zoom
  * this obviously causes some clutter and uses up some space (e.g. you can't easily scroll past it)  
    * To ***remove*** a plot output, use "Clear Output" from the "Edit" menu (or from right-click on the cell)
  * alternatively, set the keyword `jupyter_backend='static'` in the command, for output as a plain image

There are a lot more keywords available to [the `PolyData.plot()` method](https://docs.pyvista.org/api/core/_autosummary/pyvista.PolyData.plot.html), but it is not ideal to overcomplicate these calls.  :  
Finer control is better achieved in a different ways :  See more detail on plotting in [the Plotting section](./Sec_03_Plotting.ipynb).


<!-- #region tags=[] -->
### Create a plotter, and display 3D visualisation

Finally, we will plot the 'PolyData' object via PyVista.  
This requires a few additional steps ...

First, we need a [PyVista "plotter"](https://docs.pyvista.org/api/plotting/_autosummary/pyvista.Plotter.html#pyvista.Plotter) object to display things in 3D.  
Since our data is geo-located, we will use a special type of plotter from [GeoVista](https://github.com/bjlittle/geovista#philisophy) for this.

**Import the class `GeoPlotter` from the `geovista` package, and create one** (with no arguments)
<details><summary>Sample code solution : <b>click to reveal</b></summary>

```python
from geovista import GeoPlotter
plotter = GeoPlotter()
```
</details>
<!-- #endregion -->

```python
from geovista import GeoPlotter
plotter = GeoPlotter()
```

<!-- #region -->
Call the plotter `add_mesh` function, passing in our PolyData object with the Rh cube data in it.  
( **N.B.** don't worry about the object which this passes back -- just discard it ).
<details><summary>Sample code solution : <b>click to reveal</b></summary>

```python
_ = plotter.add_mesh(pv)
```
</details>
<!-- #endregion -->

```python
_ = plotter.add_mesh(pv)
```

<!-- #region -->
Now simply plot this, by calling the plotter function "show" (with no args).
<details><summary>Sample code solution : <b>click to reveal</b></summary>

```python
plotter.show()
```
</details>
<!-- #endregion -->

```python
plotter.show()
```

**Some odd notes:**
  * By default, `plotter.show()` opens an interactive window : **you can rotate and zoom it with the mouse**.
    * you can instead generate static output 
        * in a notebook, you do this with `jupyter_backend='static'`
        * or in a Python session, try `interactive=False`
  * VTK/PyVista doesn't use plot "types".  
    Instead, you add meshes to a plotter + can subsequently control the presentation.
  * GeoVista can also produce more familiar 2D plots (see on ...)



***TODO:*** can suggest some of these as follow-on exercises
