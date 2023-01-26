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

# Demonstrating Iris mesh concepts

Goals :
  * introduce mesh coordinates + connectivities
  * show real LFRic mesh structure on plots

```python
import numpy as np
from pv_conversions import pv_from_lfric_cube
```

```python
## TODO : remove later -- this bit is temporary, for initial testing with C48 data
from testdata_fetching import switch_data
switch_data(use_newer_smaller_c48_data=True)
```

```python
from testdata_fetching import lfric_rh_singletime_2d
cube = lfric_rh_singletime_2d()
print(cube)
```

```python
# Snapshot the original data range -- this is useful below
data_min, data_max = cube.data.min(), cube.data.max()
data_range = data_max - data_min
```

```python
# Calculate the coordinates of a cubesphere corner
x_corner = 45.0
y_corner = np.rad2deg(np.arctan(1.0 / np.sqrt(2)))
y_corner, x_corner
```

```python
# Get node coordinates from the mesh
x_nodes_coord = cube.mesh.coord(axis='x', include_nodes=True)
y_nodes_coord = cube.mesh.coord(axis='y', include_nodes=True)
x_nodes_coord
```

```python
# Find the number of the node nearest the cubesphere corner
xx = x_nodes_coord.points
yy = y_nodes_coord.points
xy_dists = (xx -  x_corner) ** 2 + (yy - y_corner) ** 2
closest = np.min(xy_dists)
i_node_nearest_corner = np.argmin(xy_dists)

# show the results
print(
    'corner index :',
    i_node_nearest_corner
)
print('Some corner-distances around the corner node.. : ')
print('   ', xy_dists[i_node_nearest_corner - 2:i_node_nearest_corner + 3]
)
```

```python
# Now find the faces which touch that corner
# (spoiler alert : if we specced the corner right, there are probably 3 of them)
face_nodes = cube.mesh.face_node_connectivity.indices
assert face_nodes.ndim == 2 and face_nodes.shape[1] == 4
```

```python
face_on_corner = np.any(face_nodes == i_node_nearest_corner, axis=1)
corner_faces = np.where(face_on_corner)[0]
print('corner face indices :', corner_faces)
```

```python
# Go back to the cube data, "mark" those faces visibly, and display
marks = data_max + data_range * np.array([1.2, 1.3, 1.4])
cube.data[corner_faces] = marks

# Plot the cube
pv = pv_from_lfric_cube(cube)
pv.plot(show_edges=True, jupyter_backend='static')
```

---

Now "expand" this face selection outwards   
-- to include all the faces adjacent to these ones ...

```python
# **First** find all points which are corners of those faces
extended_points = cube.mesh.face_node_connectivity[corner_faces].indices
extended_points
```

```python
# Tidy to get sorted + unique point indices
extended_points = sorted(set(extended_points.flatten()))
print(extended_points)
```

```python
# ... **Then** find all faces which use those points (as before)
extended_faces = []
for i_point in extended_points:
    face_touches_point = np.any(face_nodes == i_point, axis=1)
    extended_faces.extend(np.where(face_touches_point)[0])

# tidy for sorted + unique, again
extended_faces = sorted(set(extended_faces))
print(extended_faces)
```

```python
# Mark all those faces too, distinguishing "outer" and "inner", and re-plot
cube.data[extended_faces] = data_max + data_range * 1.1
cube.data[corner_faces] = data_max + data_range * np.array([1.4, 1.6, 1.8])
pv = pv_from_lfric_cube(cube)
pv.plot(show_edges=True, jupyter_backend='static')
```

```python

```

```python

```
