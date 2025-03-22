# Run Isaac Environment
Find the local path to the following ```python.bat``` in the isaac_sim install directory: 
```bat
set PYTHON_ENV_ISAAC="$LocalPath/AppData/Local/ov/pkg/isaac_sim-2022.2.1/python.bat"
```

To execute a code snippet in isaac sim headless mode:
```bat
set SNIPPETS_PATH="C:/Users/ahmed/Documents/vvreconstruction/python/NvidiaOmniverse/IsaacSim/snippets/%1"
```
where you give ```your_script_name.py``` as an argument like follows:
```
./run_isaac_env.bat your_script_name.py
```
