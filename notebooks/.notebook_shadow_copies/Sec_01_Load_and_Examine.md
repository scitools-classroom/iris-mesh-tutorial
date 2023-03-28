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

"Unstructured" data can be loaded from UGRID files (i.e. netCDF files containing a UGRID-style mesh). This is just like normal [Iris](https://scitools-iris.readthedocs.io/en/latest) loading, except that we must *enable* the interpretion of UGRID content like this:

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

To test loading of UGRID files, like demonstrated above, we need to import `iris`, and the `PARSE_UGRID_ON_LOAD` object from [iris.experimental.ugrid.load](https://scitools-iris.readthedocs.io/en/latest/generated/api/iris/experimental/ugrid/load.html#)


```python tags=[]
import iris 

from iris.experimental.ugrid.load import PARSE_UGRID_ON_LOAD
```

### Load UGRID data from netCDF files.
The tutorial helper code `testdata_fetching` defines a variable `lfric_filepath` (and `um_filepath`) which points to suitable a test file.

```python tags=[]
# import tutorial helper routines for handling access to test data
from testdata_fetching import lfric_filepth, um_filepth
print('LFRic data availble from: ' + str(lfric_filepth))
print('UM data availble from' + str(um_filepth))
```


In this case, we use the plain [iris.load](https://scitools-iris.readthedocs.io/en/latest/userguide/loading_iris_cubes.html) function to load the data (but of course with the PARSE_UGRID_ON_LOAD context) from above listed files. 

We show the first few of the cubes. Putting just `cubes` at the end triggers noteboook printing output. You can click on each cube to expand it into detail view. Try this. Try also to use `print(cubes)` instead.

```python tags=[]
print('loading...')
with PARSE_UGRID_ON_LOAD.context():
    cubes = iris.load(lfric_filepth)

print(f'\n... Loaded {len(cubes)} cubes.')
print('Showing first 6:')
cubes[:6]
```


Putting just `cubes` at the end of the code above triggers noteboook printing output. You can click on each cube to expand it into detail view. Try this. Try also to use `print(cubes)` instead. To spot some structual differences between LFRic and UM data also load some cubes from `um_filepath` above. 

<!-- #region -->
## What is notable about "mesh cubes"

In the cube printout above, compared to regular UM-style data (try loading data from `um_filepth`), you can see that it has an additional section in the cube printout called "Mesh", which displays the mesh-specific info. The Mesh has "Mesh coordinates", containing information about latitude and longitude but no dimension coordinates for latitude or longitude. Cubes with a mesh are known in Iris as "unstructured cubes" or "mesh cubes". They also always have a specific "mesh dimension": In the above example it is the _last_ cube dimension.


The cube itself also now has some extra properties : `cube.mesh`, `cube.location` and `cube.mesh_dim()`  
(which are otherwise all `None` if the cube is not a mesh cube)

<!-- #endregion -->

## Loading a single cube
To print the three mentioned extras properties we load just a single cube from the file (This is considerably faster if a file contains 100s variables). Let's load just `relative_humidity_wrt_water` data from the example file (`fric_filepth`) whith the [load_cube](https://scitools-iris.readthedocs.io/en/latest/generated/api/iris.html?highlight=load_cube#iris.load_cube) function and print those properties:

```python tags=[]
with PARSE_UGRID_ON_LOAD.context():
    lfric_rh = iris.load_cube(lfric_filepth,'relative_humidity_wrt_water')

# just uncomment to explore: 
#print(lfric_rh)
#print(lfric_rh.mesh)
#print(lfric_rh.location)
#print(lfric_rh.mesh_dim)

```

If the cube is not a mesh cube these propertise are  `None`, which we can demonstrate with a cube from the "UM file":   

```python tags=[]
um_cube = iris.load_cube(um_filepth,'air_temperature')
#print(um_cube)
print(um_cube.mesh)

```

## Next notebook
See the next section: [02 - Mesh concepts and Meshes in Iris](./Sec_02_Meshes.ipynb)
