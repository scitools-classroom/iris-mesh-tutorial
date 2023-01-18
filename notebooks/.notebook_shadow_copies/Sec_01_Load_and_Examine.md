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

# Section 1 : Loading and Examining some LFRic data

Let's dive right in by taking a look at some output file contents.

**TODO: data needs to be available somewhere sensible**

```python tags=[]
from pathlib import Path
datadir = Path('/scratch/sworsley/lfric_data')
datadir.exists()
```

```python
%ls -1l {datadir}
```

```python
# !ncdump -h /scratch/sworsley/lfric_data/latlon_surface.nc | head -n 100
```

```python
!ncdump -h /scratch/sworsley/lfric_data/20210324T0000Z_lf_ugrid.nc | head -n 100
```

## Relationship to existing Iris usage

Much the same ...


```python
import iris
iris.FUTURE.datum_support = True  # avoids some irritating warnings
```

```python
# From these, grab one UM and one LFRic datafile, which roughly correspond

um_filepth = datadir / '20210324T0000Z_um_latlon.nc'
lfric_filepth = datadir / '20210324T0000Z_lf_ugrid.nc'
```

<!-- #region tags=[] -->
## Just for reference : some UM data, and what that looks like in Iris ...
<!-- #endregion -->

```python
um_cubes = iris.load(um_filepth)
```

```python
print("n(UM-cubes) = ", len(um_cubes))
print("first 10 cubes ...")
um_cubes[:10]
```

```python
um_rh = um_cubes.extract_cube('relative_humidity')
um_rh
```

<!-- #region -->
### NOTE: loading a single cube
You could instead load a single cube directly from the file.  
```python
um_rh = iris.load_cube(um_filepth, 'relative_humidity')
```
This is in fact rather faster, from a file like this with lots of data-variables (i.e. diagnostics).
<!-- #endregion -->

```python

```

## What's in the LFRic files ?

Let's start with a quick look at a dump of the file  
 -- but not actually all of it, as there are ***dozens*** of disagnostic variables ...
 

```python
!ncdump -h {lfric_filepth} | head -n 120
```

The mesh metadata alone can be better viewed using the "ugrid checker" program, which knows how to interpret it ...
( NOTE:  this is a public utility, also designed here in AVD : see https://github.com/pp-mo/ugrid-checks#readme )

```python
!ugrid-checker -sqe {lfric_filepth} | head -n 24
```

---

Let's not bother any more with that : Instead, we can load it into Iris which does a reasonable job of interpreting the mesh-structured data.


```python
# Load the LFRic single datafile 

from iris.experimental.ugrid.load import PARSE_UGRID_ON_LOAD
# Note the use of the special context.  This is basically because the Iris mesh functionality is still 'experimental'
with PARSE_UGRID_ON_LOAD.context():
    lfric_cubes = iris.load(lfric_filepth)
```

```python
print("n(LFRic-cubes) = ", len(lfric_cubes))
print("first 10 cubes ...")
lfric_cubes[:10]
```

```python
lfric_rh = lfric_cubes.extract_cube('relative_humidity_at_screen_level')

lfric_rh
```

---
Or, just to show a faster selective loading ...

```python
with PARSE_UGRID_ON_LOAD.context():
    lfric_rh = iris.load_cube(lfric_filepth, 'relative_humidity_at_screen_level')

lfric_rh
```

## What you initially notice about "mesh cubes"

The cube printout has a "Mesh" section, which displays the mesh info.

The cube itself now has some extra properties : `cube.mesh`, `cube.location` and `cube.mesh_dim()`  
(these are otherwise all `None`)

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

```python

```

<!-- #region tags=[] -->
---

## Exercise: identifying mesh data
**How, in your code, could you check whether a cube has structured or mesh-based data ?**

---

<details><summary><b>Sample code solution :</b> "check whether cube has structured data ?" <b>click to reveal</b></summary>

<br>

```python
#-------------------------------
# Utility Function
#
def is_meshcube(cube):
    return cube.mesh is not None

#-------------------------------
# Testing ...
#
from iris.tests.stock import realistic_3d
nonmesh_cube = realistic_3d()
print('Cube: ', repr(nonmesh_cube), '\n  - is_meshcube ?', is_meshcube(nonmesh_cube))

print()
from iris.tests.stock.mesh import sample_mesh_cube
mesh_cube = sample_mesh_cube()
print('Cube: ', repr(mesh_cube), '\n  - is_meshcube ?', is_meshcube(mesh_cube))

```
---
    
**NOTE :**
  * **Try this code**, by pasting it into a code cell + running ...
  * try it also with the 'lfric_rh' cube
</details>
<!-- #endregion -->

```python
# (space for user commands)
#  . . .
```

## Question : what is `cube.mesh_dim` for ?


<details><summary><b>Sample Answer :</b> what is cube.mesh_dim for ? <b>click to reveal</b></summary>
It is a function which you call, returning an integer.
<br/>The result tells you which cube dimension is the mesh dimension  -- that is, the cube dimension which indexes the individual elements of the mesh

See [Iris API docs for `Cube.mesh_dim`](https://scitools-iris.readthedocs.io/en/latest/generated/api/iris/cube.html#iris.cube.Cube.mesh_dim)

</details>


## Question : what does `cube.location` mean ?

<details><summary>Sample answer : <b>click to reveal</b></summary>
It returns a string, "node", "edge" or "face", indicating the type of mesh element which the cube data is mapped to.

See in [Iris "Mesh Support" docs](https://scitools-iris.readthedocs.io/en/latest/further_topics/ugrid/data_model.html?highlight=location#the-basics)

</details>


## Additional questions to consider ...

  * what does `cube.mesh_dim` do when a cube *has* no mesh ?
        <details><summary>Sample answer : <b>click to reveal</b></summary>
    It returns `None`.
    </details>
  * what happens if there is more than one mesh, or mesh dimension ?
    <details><summary>Sample answer : <b>click to reveal</b></summary>
    A bit of a "trick question" !  
    </br>In UGRID, a data-variable can have at most <i>one</i> location and mesh.  Therefore, since each Iris cube represents a CF data-variable, it can only have one mesh, and one mesh dimension -- that of its location in the mesh.
    </details>

```python

```

```python

```
