rmdir dist
rmdir build
pyinstaller -F -w -i levnet.ico ..\src\GUI.py && echo Success!
pause
exit