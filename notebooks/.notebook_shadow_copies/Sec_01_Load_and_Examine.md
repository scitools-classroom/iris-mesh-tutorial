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

# Section 1: Loading and Examining some LFRic data

This Section uses output from LFRic and UM case study runs to show some basic differences of unstructured mesh (LFRic) and gridded data (UM).  

Example data is available with this tutorial.  
Let's dive right in by taking a look at some output file contents.

<!-- #region -->
## Iris unstructured loading

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
<!-- #endregion -->

### Enable UGRID loading

Most importantly, we need the `PARSE_UGRID_ON_LOAD` object from `iris.experimental.ugrid.load`

```python
from iris.experimental.ugrid.load import PARSE_UGRID_ON_LOAD
```

### Load UGRID data from netCDF files.
The variable `lfric_filepath` is defined in the tutorial helper code `testdata_fetching`: 
It points to a suitable test file.

In this case, we use the plain `iris.load` function, as shown above.  

NOTE : ***There are a lot of cubes:  Expect this to take a few seconds, and only show a few of the cubes.***

```python
# First do some preliminary Python setup, imports etc ...

# import the top-level Iris package
import iris

# import local routines handling access to some test data
from testdata_fetching import lfric_filepth
```


```python
print('loading...')
with PARSE_UGRID_ON_LOAD.context():
    cubes = iris.load(lfric_filepth)

print(f'\n... Loaded {len(cubes)} cubes.')
print('Showing first 4:')
cubes[:4]
```


---
**NOTES:**
  * putting just `cubes` at the end triggers notebook printing output
    * this also means you can click on each cube to "expand" it into a detail view -- ***try this***
  * the effect of `print(cubes)` is different -- ***try this***


## Loading a single cube
You can instead load just a _single_ cube from the file.  
This is considerably _faster_ in many cases, since a typical file may contain 100s data-variables (i.e. diagnostics).

### Load just "relative_humidity_wrt_water" data
(From the same file)  
NOTE: it is nicer to use the `load_cube` function.

```python
with PARSE_UGRID_ON_LOAD.context():
    lfric_rh = iris.load_cube(lfric_filepth, "relative_humidity_wrt_water")

lfric_rh
```

**NOTES:**
  * putting just the `lfric_rh` variable at the end of the Jupyter cell triggers notebook printing output
  * the effect of `print(lfric_rh)` is different -- ***try this***


```python

```

## What is notable about "mesh cubes"

In the cube printout above, _compared to regular UM-style data_, you can see that it has an additional section in the cube printout called "Mesh", which displays the mesh-specific info.  

The cube itself also now has some extra properties : `cube.mesh`, `cube.location` and `cube.mesh_dim()`  
(which are otherwise all `None`)

Cubes with a mesh are known in Iris as "unstructured cubes" or "mesh cubes.  
They also always have a specific "mesh dimension":  In the above example it is the _last_ cube dimension.


```python

```

## Next notebook
See the next section: [02 - Mesh concepts and Meshes in Iris](./Sec_02_Meshes.ipynb)

```python

```
