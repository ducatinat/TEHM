pip install -e ..\socialreaper
rmdir build\ /s /q
rmdir dist\reaper /s /q
pyinstaller.exe -w -i ui/icon.ico reaper.py
robocopy ui dist\reaper\ui /mir
robocopy sources dist\reaper\sources /mir
robocopy licenses dist\reaper\licenses /mir
copy LICENSE.txt dist\reaper\LICENSE.txt
copy sources.xml dist\reaper\sources.xml
"C:\Program Files (x86)\Inno Setup 5\ISCC.exe" scripts\setup.iss /DApplicationVersion==%1
