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

# LFRic + Iris tutorial : Unstructured meshes


## Important Preliminary : use + stability of notebooks

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
      -- e.g. after restart, kernel status persists in "connecting" / "restarting" state  
      In such cases, *close* the JupyterLab window + restart
      * i.e. `$ jupyter-lab`


---
## Tutorial sections : --> individual notebooks
   * [01 - Load and Examine some LFRic data](./Sec_01_Load_and_Examine.ipynb)
   * [02 - Mesh concepts and Meshes in Iris](./Sec_02_Meshes.ipynb)
   * [03 - Plotting and Visualisation](./Sec_03_Plotting.ipynb)
   * [04 - Regional Extraction](./Sec_04_RegionExtraction.ipynb)
   * [05 - Regridding and UM data comparison](./Sec_05_Regridding.ipynb)
   


## Reference : terminology (probably, a separate linked glossary ??)
  * LFRic
  * cubesphere
  * mesh
  * unstructured
  * ugrid
  * xios
  * VTK
  * geovista
  * pyvista
  * iris-esmf-regrid


<!-- #region -->
# Work To Do : **TOPICS LIST**

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
     * assume basic Iris knowledge (but maybe no more)
        * but would like to focus initially on LFRic, not UM ?
     * BASICS ..
       * loading
          * BRIEFLY show UM/structured loading
          * then LFRic -- highlight differences
       * printing (cubes)
          * beginnings of questions
          * cube.mesh, cube.mesh_dim ?
       * saving

  1. plotting
     * 3d plotting ((see beginnings of discussion section ..above))
     * 2d plots (projections)

  1. Exploring / comparing UM and LFRIc data
       * "back out" to details of the differences
          * ?MAYBE? split extra info from this section to the 2nd session (post 1st hour)
       * cube printouts -- similarity + difference
       * regridding
         * cf Iris docs : https://scitools-iris.readthedocs.io/en/stable/further_topics/ugrid/operations.html#regridding  
           (expand the example code section)
         * Iris support (extended existing features)
         * iris-esmf-regrid
       * side-by-side inspection (linked 3d plots)

  1. ??first hour finishes here ??

  1. region extraction
     * cf Iris docs : https://scitools-iris.readthedocs.io/en/stable/further_topics/ugrid/operations.html#region-extraction  
       (expand the example code section)

  1. zonal means via regridding
     * possibly BONUS material?
     * cf : https://iris-esmf-regrid.readthedocs.io/en/latest/_api_generated/esmf_regrid.experimental.unstructured_scheme.html#esmf_regrid.experimental.unstructured_scheme.MeshToGridESMFRegridder  
       look at : `latitude`
       
  1. working with connectivity (API)
     * possibly BONUS material?


<!-- #endregion -->

```python
# NOTE: some random changes : to check Jupytext automation
```

```python

```
