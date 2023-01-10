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

# LFRic + Iris tutorial : Unstructured meshes

<!-- #region tags=[] -->
---

Some important initial setup (always do first) ..
<!-- #endregion -->

```python
# Make PyVista (VTK 3d output) appears an interactive window in the notebook.
# (NOTE: without this, VTK output appears as static embedded images)
import pyvista as pv
pv.rcParams["use_ipyvtk"] = True
```

# Important : use + stability of notebooks

A good deal of the content relies on code which is still experimental.
We must expect that there are various outstanding problems, and things sometimes crash.

A particular problem is getting things working *within notebooks*.  For that purpose, the following may be useful general notes :

whenever something seems to be taking a long time with no result...
   1. ***first*** look at "kernel status" in top-right of the JupyterLab notebook pane  
       meanings as described in its mouse-over text : 
       * white circle = "idle" (ok, done)
       * grey circle = "busy"
       * "electric zap" icon = "connecting"  ***-- this one often means "crashed"***
   2. if stuck, you can always "restart the kernel"  
      (the arrow-round-a-circle icon, in controls at top left of notebook pane)  
      but note :
        1. this will destroy the entire session :  you need to rerun all notebook cells from the start again
        2. after resetting, **do not attempt anything further** until the kernel state shows "idle" again
   3. sometimes gets *really* stuck
      - e.g. after restart, kernel status persists in "connecting" / "restarting" state
      then *close* the JupyterLab window + restart
      * i.e. `$ jupyter-lab`


---
Create generally useful imports

```python
from geovista.pantry import um_orca2
import geovista.theme

import iris
```

---

# **EXAMPLES OF FORMAT**

Some ideas of how we may present...  
And (later) a **list of topics for discussion** ...



# 3D visualisation

While LFRic data can be presented in 2D plots with a map projection, it is often more profitable way to explore it with a 3D viewer.  

There are a few reasons for this :
  1. the LFRic model grid does not follow a 2d, lat-lon aligned structure (unlike UM)
  2. LFRic data is now tending to be too large for matplotlib-style plotting (~6 million cells)

Simple Pyvista testcase


# Ongoing structure question
how to organise / sectionalise / navigate the tutorial ?

### 1. Links to other notebooks
["trial" notebook](./trial.ipynb)

### 2. TOC provision
TBD, not yet tried.  See : https://github.com/jupyterlab/jupyterlab-toc#readme


## Reference : terminology (probably, a separate linked glossary ??)
  * LFRic
  * cubesphere
  * mesh
  * unstructured
  * ugrid
  * VTK
  * geovista
  * pyvista
  * iris-esmf-regrid


<!-- #region -->
# **TOPICS LIST?**

A draft list of topics for discussion.  
NOTE : all these basically need re-casting as interactive sections lead by task questions.  
E.G. (a) "how can you tell this is mesh data ?". (b) "

  1. Basics
     * concepts
       * unstructured (LFRic)
       * UGRID
     * terminology to be covered (PLUS probably, a separate glossary ? -- see above section)


  1. Iris existing features, ***extended***
     * cf Iris docs : https://scitools-iris.readthedocs.io/en/stable/further_topics/ugrid/operations.html#working-with-mesh-data
     * BASICS ..
       * loading
       * printing (cubes)
          * beginnings of questions
       * saving

  1. plotting
     * 3d plotting ((see beginnings of discussion section ..above))
     * 2d plots (projections)

  1. Exploring / comparing UM and LFRIc data
       * cube printouts -- similarity + difference
       * regridding
       * side-by-side inspection (linked 3d plots)

  1. region extraction
     * cf Iris docs : https://scitools-iris.readthedocs.io/en/stable/further_topics/ugrid/operations.html#region-extraction  
       (expand the example code section)

  1. working with connectivity (API)

  1. regridding
     * cf Iris docs : https://scitools-iris.readthedocs.io/en/stable/further_topics/ugrid/operations.html#regridding  
       (expand the example code section)
     * Iris support (extended existing features)
     * iris-esmf-regrid

  1. zonal means via regridding
     * cf : https://iris-esmf-regrid.readthedocs.io/en/latest/_api_generated/esmf_regrid.experimental.unstructured_scheme.html#esmf_regrid.experimental.unstructured_scheme.MeshToGridESMFRegridder  
       look at : `latitude`
<!-- #endregion -->

```python

```

```python

```
