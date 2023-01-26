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

First run some preliminary Python setup, imports etc ...

```python
# import the top-level Iris package
import iris

# import local routines handling access to some test data
from testdata_fetching import lfric_filepth
```

<!-- #region -->
## Iris unstructured loading
Let's dive right in by taking a look at some mesh content.

"Unstructured" data can be loaded from UGRID files (i.e. netCDF files containing a UGRID-style mesh).  
This is just like normal Iris loading, except that we must *enable* the interpretion of UGRID content,  
roughly like this ...

```python
with PARSE_UGRID_ON_LOAD.context():
    cube_list = iris.load(path [, constraints])
    # ..and/or..
    single_cube = iris.load_cube(path [, constraints])
    # ..and/or..
    selected_cubes = iris.load_cubes(path, cube_constraints)

```

**Exercise : first import the `PARSE_UGRID_ON_LOAD` object from iris.experimental.ugrid.load**
<!-- #endregion -->

```python
from iris.experimental.ugrid.load import PARSE_UGRID_ON_LOAD
```

<!-- #region -->
---

The variable `lfric_filepath` is already set up, pointing to a suitable test file.

**Exercise : Load all data from `lfric_filepath`, with the UGRID loading enabled, and print the first 10 cubes.**  
Use the plain 'load' method, as shown above.  
NOTE : ***expect this to take a few seconds to complete.***

<details><summary>Sample code solution  <b>click to reveal</b></summary>

```python
with PARSE_UGRID_ON_LOAD.context():
    cubes = iris.load(lfric_)

cubes[:10]
```
</details>
<!-- #endregion -->

```python
# ... space for user code ...

with PARSE_UGRID_ON_LOAD.context():
    cubes = iris.load(lfric_filepth)

cubes[:10]
```


**NOTEs :**
  * putting just `cubes` at the end triggers notebook printing output
    * this also means you can click on each cube to "expand" it into a detail view -- try it
  * the effect of `print(cubes)` is different -- try it

<!-- #region -->
## Loading a single cube
You can instead load a single cube directly from the file.  
This is considerably _faster_ in this case, since the whole file contains ~100 data-variables (i.e. diagnostics).

**Load just the cube named `relative_humidity_at_screen_level`, from the same file, and show that.**  
Hint : it's nicer to use the `load_cube` function

<details><summary>Sample code solution  <b>click to reveal</b></summary>

```python
with PARSE_UGRID_ON_LOAD.context():
    lfric_rh = iris.load_cube(lfric_filepth, "relative_humidity_at_screen_level")

lfric_rh
```
---
    
**NOTEs :**
  * putting just `cubes` at the end triggers notebook printing output
  * the effect of `print(cubes)` is different -- try it
</details>
<!-- #endregion -->

```python
with PARSE_UGRID_ON_LOAD.context():
    lfric_rh = iris.load_cube(lfric_filepth, "relative_humidity_at_screen_level")

lfric_rh
```

```python

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
###-------------------------------
### Utility Function
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
