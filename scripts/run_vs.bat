@echo off

set activate_env_path= "C:\Users\ahmed\Documents\vvreconstruction\cpp\dracocompressionplugin\build\activate_run.bat"
set vs_2022_path= "C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\devenv.exe"
set solution_path= "C:\Users\ahmed\Documents\vvreconstruction\cpp\dracocompressionplugin\build\DracoCompressionPlugin.sln" 

call %activate_env_path%
call %vs_2022_path% %solution_path%