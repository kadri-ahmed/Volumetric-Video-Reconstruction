@echo off

set SCRIPT_PATH="C:/Users/ahmed/AppData/Local/ov/pkg/isaac_sim-2022.2.1/tools/composer/src/main.py"
set WORKSPACE_PATH="C:/Users/ahmed/Documents/vvreconstruction/python/NvidiaOmniverse/IsaacSim/composer-workspace"
set PYTHON_ENV_ISAAC= "C:/Users/ahmed/AppData/Local/ov/pkg/isaac_sim-2022.2.1/python.bat"

@REM call %PYTHON_ENV_ISAAC% %SCRIPT_PATH% --input */parameters/tutorial.yaml --output */dataset/tutorial_1 --mount %WORKSPACE_PATH% --num-scenes 10 --nucleus-server localhost/NVIDIA/Assets/Isaac/2022.2.1/Isaac
@REM call %PYTHON_ENV_ISAAC% %SCRIPT_PATH% --input */parameters/tutorial.yaml --output */dataset/tutorial_1 --mount %WORKSPACE_PATH% 
@REM call %PYTHON_ENV_ISAAC% %SCRIPT_PATH% --output */dataset/warehouse --mount %WORKSPACE_PATH% --num-scenes 10 --overwrite
@REM call %PYTHON_ENV_ISAAC% gen_data.py 
call %PYTHON_ENV_ISAAC% %SCRIPT_PATH% --input */parameters/narvis_gen.yaml --output */dataset/narvis --mount %WORKSPACE_PATH% --overwrite --headless