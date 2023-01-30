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

```python tags=[]
# Mark all those faces too, distinguishing "outer" and "inner", and re-plot
cube.data[extended_faces] = data_max + data_range * 1.1
cube.data[corner_faces] = data_max + data_range * np.array([1.4, 1.6, 1.8])
pv = pv_from_lfric_cube(cube)
pv.plot(show_edges=True, jupyter_backend='static')
```

```python

```

```python
# Follow-on : take the above info + produce a plot of the (numbered) nodes + faces of
# a tiny section of the LFRic mesh, for use as a diagram in Sec#02
```

```python
# How many faces ?
len(extended_faces)
```

```python
# some random face values ...
import numpy.random
numpy.random.seed(seed=1234)
face_values = np.random.uniform(0, 1.0, 12)
face_values
```

```python
# convert to colours
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as mcm

cmap = mcm.get_cmap('YlGnBu')
cmap
```

```python
import matplotlib.colors
```

```python
cols = matplotlib.colors.get_named_colors_mapping().keys()
print('\n'.join(x for x in cols if 'purp' in x))
```

```python
for x in face_values:
    print(x, cmap(0.5 * x))
```

```python
# Repeat the extended-points search to get all points in extended faces
ex2_points = cube.mesh.face_node_connectivity[extended_faces].indices
ex2_points = sorted(set(ex2_points.flatten()))
print(ex2_points)
```

```python
print(min(xx[ex2_points]), max(xx[ex2_points]))
print(min(yy[ex2_points]), max(yy[ex2_points]))
```

```python
len(extended_faces)
```

```python
numpy.random.seed(seed=12)
face_values = np.random.uniform(0, 1.0, 12)

fig = plt.figure(figsize=(10,8))
ax = plt.axes()
ax.set_xlim((40, 50))
ax.set_ylim((27, 40))
ax.fill([40, 50, 50, 40, 40], [31, 31, 40, 40, 31], color='lightgray')

dotsize = 4.5

# Label all the corners with red text
for i_pt in ex2_points:
    x, y = xx[i_pt], yy[i_pt]
    plt.plot([x], [y], 'o', color='black', markersize=dotsize)
    plt.text(x + 0.1, y, 'n-' + str(i_pt), color='black')

# color all the faces
for i_col, i_fc in enumerate(extended_faces):
    nodes = list(face_nodes[i_fc])
    face_xx, face_yy = xx[nodes], yy[nodes]
    points_x = list(face_xx) + [face_xx[0]]
    points_y = list(face_yy) + [face_yy[0]]
    color = cmap(0.1 + 0.5 * face_values[i_col])
    plt.fill(points_x, points_y, color=color)
    xav, yav = np.mean(points_x), np.mean(points_y)
    plt.plot(xav, yav, 'o', color='red', markersize=dotsize)
    plt.text(xav+0.1, yav, 'F-' + str(i_fc), color='red')

ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

# print-lines
lines = []
lines.append('Some coordinate values :')
lines.append(
    '    node=94 :  x/y=  node_x/y[94] :  ' +
    str(x_nodes_coord.points[94]) +
    ' / ' + str(y_nodes_coord.points[94])
)
lines.append(
    '    node=97 :  x/y=  node_x/y[97] :  ' +
    str(x_nodes_coord.points[97]) +
    ' / ' + str(y_nodes_coord.points[97])
)
lines.append('')
lines.append('Some connectivity values :')
lines.append('    face=95 :  nodes=  face_nodes[95] :  ' + str(face_nodes[95]))
lines.append('    face=47 :  nodes=  face_nodes[47] :  ' + str(face_nodes[47]))
y_space = 0.4
for i_line, line in enumerate(lines):
    y = 30. - i_line * y_space
    plt.text(41., y, line, color='darkblue')
    
plt.title('Some Faces and Nodes of an LFRic mesh.')
plt.savefig('LFRic_mesh.svg')
plt.show()
```

```python
print('Example coordinate + connectivity values ...')
print('')
print(
    'node=94 x//y= node_x//y[94] = ',
    x_nodes_coord.points[94],
    ' //', y_nodes_coord.points[94]
)
print(
    'node=95 x//y= node_x//y[95] = ',
    x_nodes_coord.points[95],
    ' //', y_nodes_coord.points[95]
)
print('')
print('face=46 nodes=face_nodes[46] = ', face_nodes[46])
print('face=46 nodes=face_nodes[46] = ', face_nodes[46])

```

```python
cube.mesh.node_coords[0]
```

```python

```
