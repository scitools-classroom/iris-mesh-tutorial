---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.0
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

```python
print('trial...')
```

```python
# setup
%matplotlib inline
import pyvista as pv
pv.rcParams["use_ipyvtk"] = True
```

```python
# Trial

import geovista as gv
```

```python
from geovista.pantry import um_orca2
import geovista.theme
```

```python
# Copied from : https://github.com/bjlittle/geovista/blob/main/src/geovista/examples/from_2d__orca.py

def trial_main() -> None:
    # load sample data
    sample = um_orca2()

    # create the mesh from the sample data
    mesh = gv.Transform.from_2d(sample.lons, sample.lats, data=sample.data)

    # remove cells from the mesh with nan values
    mesh = mesh.threshold()

    # plot the mesh
    plotter = gv.GeoPlotter()
    sargs = dict(title=f"{sample.name} / {sample.units}", shadow=True)
    plotter.add_mesh(mesh, show_edges=True, scalar_bar_args=sargs)
    plotter.add_base_layer(texture=gv.natural_earth_1())
    plotter.add_coastlines()
    plotter.add_axes()
    plotter.add_text(
        "ORCA (10m Coastlines)",
        position="upper_left",
        font_size=10,
        shadow=True,
    )
    plotter.show()
```

```python
trial_main()
```

```python

```
