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

# LFRic + Iris tutorial: Unstructured meshes

The tutorial is provided as a set of Jupyter notebooks, best viewed in Juptyer lab.  
Please see list below for the individual topics.


## Tutorial sections (links to individual notebooks):
   * [01 - Load and Examine some LFRic data](./Sec_01_Load_and_Examine.ipynb)
   * [02 - Mesh concepts and Meshes in Iris](./Sec_02_Meshes.ipynb)
   * [03 - Plotting and Visualisation](./Sec_03_Plotting.ipynb)
   * [04 - Regridding and UM data comparison](./Sec_04_Regridding.ipynb)
   * [05 - Regional Extraction](./Sec_05_RegionExtraction.ipynb)

### Bonus and additional material
  * [Bonus 01 - Mesh from Numbers](./Bonus_01_Mesh_from_Numbers.ipynb): Manually construct an Iris mesh
  * [Bonus 02 - Mesh Connectivities Demo](./Bonus_02_Mesh_Connectivities_Demo.ipynb): Investigate some details of the LFRic mesh, as it appears in Iris
  * [Bonus 03 - MeshCube Extraction](./Bonus_03_MeshCube_Extraction.ipynb): Use Geovista to extract a mesh-cube subregion as a new Iris cube

<!-- #region jp-MarkdownHeadingCollapsed=true tags=[] -->
## Jargon: a really brief glossary of terms
  * [**UM**](https://code.metoffice.gov.uk/trac/um): The Unified Model
  * [**LFRic**](https://www.metoffice.gov.uk/research/approach/modelling-systems/lfric): The UM successor model, modelling cells on an unstructured (cube-sphere) mesh
  * **mesh**: Description of arbitrary locations and regions in space
  * **unstructured**: An _irregular_ arrangement of spatial locations (constrast with 'regular grids')
  * **cubesphere**: Mesh of cells on the globe, arranged like a cube with square cells on each face
  * [**CF**](https://cfconventions.org/cf-conventions/cf-conventions.html): Conventions for encoding climate and forecast data in netCDF files
  * [**UGRID**](https://ugrid-conventions.github.io/ugrid-conventions/): Conventions which extend CF to data on unstructured meshes
  * [**XIOS**](https://forge.ipsl.jussieu.fr/ioserver): Software used by LFRic to save model output as UGRID formatted netCDF files
  * [**VTK**](https://vtk.org/): 3D modelling and visualisation package, based in c++
  * [**PyVista**](https://pyvista.org/): Python package providing control of VTK from Python code
  * [**GeoVista**](https://github.com/bjlittle/geovista#readme): Python package adding geo-location support and utilites to PyVista
  * [**ESMF**](https://earthsystemmodeling.org/) Earth System Modelling Framework: modelling support code for regridding, coupling etc, based in FORTRAN
  * [**iris-esmf-regrid**](https://github.com/SciTools-incubator/iris-esmf-regrid#readme): Python package providing ESMF-based mesh regridders for Iris

<!-- #endregion -->


---
## Use and stability of notebooks

A good deal of the content relies on code which is still experimental. We must expect that there are various outstanding problems, and things sometimes crash. A particular problem is getting things working *within notebooks*.  For that purpose, the following may be useful general notes:

### Python environment
When opening a notebook, you may be **prompted** to select the Python environment with which to run it (which must contain Iris, Jupyter, PyVista etc).  
We suggest that you launch the Jupyter server _itself_ in the dedicated (conda) tutorial env. Then you can simply use the _same_ env as the server, i.e. select "`Python 3 (ipykernel)`".

### When something seems to be taking a long time with no result...
   1. ***first*** look at "kernel status" in top-right of the JupyterLab notebook pane  
       meanings as described in its mouse-over text: 
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

```python

```
