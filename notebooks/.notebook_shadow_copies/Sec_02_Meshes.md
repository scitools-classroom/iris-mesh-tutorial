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

**Print the cube**

```python tags=[]
lfric_rh
```

### What is special about "mesh cubes" ?

Compare the above to some UM data (e.g. `testdata_fetching.um_temp()`).

You should find that an 'unstructured' cube has some extra properties : `cube.mesh`, `cube.location` and `cube.mesh_dim()`  


```python
print("cube.mesh :")
print(lfric_rh.mesh)
print("\n-------")
print("cube.location = ", lfric_rh.location)
print(lfric_rh.mesh_dim())
print("\n-------")
help(lfric_rh.mesh_dim)
print("cube.mesh_dim() = ", lfric_rh.mesh_dim())
```

---
**Additional Note:**  
As previously mentioned, every Iris mesh cube has a "mesh dimension".
This is often the last cube dimension, and is typically "anonymous" -- i.e. it has no dimension coordinate.


## Details of the Iris mesh content

Exactly ***how*** Iris represents a mesh is not usually very relevant to working with cube data in Iris, nor to plotting it with PyVista.  
So that is beyond the scope of an introductory tutorial.  

However, for those interested, there is a bonus notebook showing some of this : ["Mesh_Connectivities_demo.ipynb"](./Mesh_Connectivities_demo.ipynb)


<!-- #region tags=[] -->
---

## Exercises : mesh data

### Ex.1 : How to check whether a cube has structured or mesh-based data
<!-- #endregion -->

```python tags=[]
# ... space for user solution ...
```

```python tags=[]
#
# SAMPLE CODE SOLUTION
#


# Utility Function
#
def is_meshcube(cube):
    return cube.mesh is not None

#-------------------------------
### Testing ...
#
from iris.tests.stock import realistic_3d
nonmesh_cube = realistic_3d()
print('Cube: ', repr(nonmesh_cube), '\n  - is_meshcube ?', is_meshcube(nonmesh_cube))

print()
from iris.tests.stock.mesh import sample_mesh_cube
mesh_cube = sample_mesh_cube()
print('Cube: ', repr(mesh_cube), '\n  - is_meshcube ?', is_meshcube(mesh_cube))
```

<!-- #region tags=[] -->
---
***try this also*** with the 'lfric_rh' cube
<!-- #endregion -->

```python

```

### Question : what is `cube.mesh_dim` for ?


<details><summary>Sample Answer : <b>click to reveal</b></summary>
It is a function which you call, returning an integer.
<br/>The result tells you which cube dimension is the mesh dimension  -- that is, the cube dimension which indexes the individual elements of the mesh

See [Iris API docs for `Cube.mesh_dim`](https://scitools-iris.readthedocs.io/en/latest/generated/api/iris/cube.html#iris.cube.Cube.mesh_dim)

</details>


### Question : what does `cube.location` mean ?

<details><summary>Sample answer : <b>click to reveal</b></summary>
It returns a string, "node", "edge" or "face", indicating the type of mesh element which the cube data is mapped to.

See in [Iris "Mesh Support" docs](https://scitools-iris.readthedocs.io/en/latest/further_topics/ugrid/data_model.html?highlight=location#the-basics)

</details>


### Additional questions to consider ...

  * what does `cube.mesh_dim` do when a cube *has* no mesh ?
        <details><summary>Sample answer : <b>click to reveal</b></summary>
    It returns `None`.
    </details>
  * what happens if there is more than one mesh, or mesh dimension ?
    <details><summary>Sample answer : <b>click to reveal</b></summary>
    A bit of a "trick question" !  
    </br>In UGRID, a data-variable can have at most <i>one</i> location and mesh.  Therefore, since each Iris cube represents a CF data-variable, it can only have one mesh, and one mesh dimension -- that of its location in the mesh.
    </details>


## Next notebook
See the next section : [03 - Plotting and Visualisation](./Sec_03_Plotting.ipynb)

```python

```
