@echo off

set PYTHON_ENV_ISAAC= "C:/Users/ahmed/AppData/Local/ov/pkg/isaac_sim-2022.2.1/python.bat"
set SNIPPETS_PATH="C:/Users/ahmed/Documents/vvreconstruction/python/NvidiaOmniverse/IsaacSim/snippets/%1"
call %PYTHON_ENV_ISAAC%  %SNIPPETS_PATH%

:: call for usd_converter.py 
:: %2 = --folders 
:: %3 = folder_path 
@REM call %PYTHON_ENV_ISAAC%  %SNIPPETS_PATH% %2 %3
