# iris-mesh-tutorial

Tutorials for LFRic (unstructured) data handling, using Iris and related tools.  

The content is all written as interactive Jupyter notebooks, 
which combine presenter information and student exercises.

## Get a suitable Python environment to run the notebooks
A suitable fresh environment can be created from the list of required packages with conda, using :  
e.g. `$ conda env create --name meshtut_newest_env --file tutorial_conda_env.yml` 

However, this may break as newer package versions are released.

So, we also provide a "lockfile" which ties down all package versions, from which a 
known-good environment can be recreated :  
e.g. `$ conda create --name meshtut_savefixed_env --file tutorial_conda_env_resolved.lock` 

## Start the tutorial
E.G.  
```
$ conda activate meshtut_savefixed_env
$ cd iris-mesh-tutorial/notebooks
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
A window should then appear in your browser.  
Failing that, visit one of the urls displayed in the terminal output.

## Developer notes: to build the lockfile
The lockfile "tutorial_conda_env_resolved.lockfile" is produced from an actual environment.
First build the env from the spec file "tutorial_conda_env.yml"
   * first activating a conda env with "mamba" in it
   * `$ conda activate mamba-env`
   * `$ mamba create -n mesh-tutorial --file tutorial_conda_env.yml`
   * `conda list -n mesh-tutorial --explicit >temp_condalist_explicit.txt`
   * then activate a conda env with 'ssstack' in it : see https://github.com/MetOffice/ssstack
   * `$ conda activate ssstack-env`
   * `$ ssstack shareable temp_condalist_explicit.txt >tutorial_conda_env_resolved.lockfile`
   * `$ rm temp_condalist_explicit.txt`
      
