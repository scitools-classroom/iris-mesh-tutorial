# iris-mesh-tutorial

Tutorials for LFRic (unstructured) data handling, using Iris and related tools.  

The content is all written as interactive Jupyter notebooks, 
which combine presenter information and student exercises.

## Get a suitable Python environment to run the notebooks

For guaranteed operation with tested package versions, create a environment from the provided "lockfile", as follows:  
`$ conda create --name meshtut_safelocked_env --file tutorial_conda_env_resolved.lock` 


## Start the tutorial
Run Jupyter lab, in the chosen Python environment.  
**NOTE:** _always_ start it in the `/notebooks` directory.

E.G.  
```
$ conda activate meshtut_safelocked_env
$ cd notebooks
$ jupyter lab
    [I 2023-01-12 15:39:10.730 ServerApp] jupyter_server_terminals | extension was successfully linked.
    [I 2023-01-12 15:39:10.737 ServerApp] jupyterlab | extension was successfully linked.
 . . .
    [I 2023-01-12 15:39:11.114 ServerApp] Serving notebooks from local directory: /net/home/h05/itpp/git/iris-mesh-tutorial
    [I 2023-01-12 15:39:11.114 ServerApp] Jupyter Server 2.0.6 is running at:
    [I 2023-01-12 15:39:11.114 ServerApp] http://localhost:8888/lab?token=c4ece2e59cd8c81779de0f394c421e22f258f50466cc027e
    [I 2023-01-12 15:39:11.114 ServerApp]  or http://127.0.0.1:8888/lab?token=c4ece2e59cd8c81779de0f394c421e22f258f50466cc027e
    [I 2023-01-12 15:39:11.114 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
    [C 2023-01-12 15:39:11.734 ServerApp] 
        
        To access the server, open this file in a browser:
            file:///net/home/h05/itpp/.local/share/jupyter/runtime/jpserver-90840-open.html
        Or copy and paste one of these URLs:
            http://localhost:8888/lab?token=c4ece2e59cd8c81779de0f394c421e22f258f50466cc027e
         or http://127.0.0.1:8888/lab?token=c4ece2e59cd8c81779de0f394c421e22f258f50466cc027e
```
**A window should then appear in your browser.**  
Failing that, visit one of the urls displayed in the terminal output.

### Get Started
Open the notebook `Mesh_Tutorial_Intro.ipynb`.


## Developer notes: to build the lockfile
The lockfile `tutorial_conda_env_resolved.lock` is produced from an actual resolved environment.

To build a working env with all-latest packages, do the following:

**Step 1:** build a fresh env from the spec

  * The env spec is in the file `tutorial_conda_env.yml`
  * use a conda env with "mamba" in it (since conda is likely to take ages and/or run out of memory)
  * resolve the env
    ```bash
    $ conda activate mamba-env
    $ mamba env create -n mesh-tutorial --file tutorial_conda_env.yml
    ```
  * test that this actually _works_, by running all the notebooks


**Step 2:** make a new version of the lockfile

  * use a conda env with 'ssstack' in it (https://github.com/MetOffice/ssstack)
  * snapshot the new env content, and replace web-proxy urls to convert it to a "shareable" lockfile  
    ```bash
    $ conda activate ssstack-env
    $ conda list -n mesh-tutorial --explicit >temp_condalist_explicit.txt
    $ ssstack shareable temp_condalist_explicit.txt >tutorial_conda_env_resolved.lock
    $ rm temp_condalist_explicit.txt
    ```


**Step 3:** upload changes in a PR
