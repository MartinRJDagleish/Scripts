# Scripts

This repository is a collection of (mostly) python scripts which I wrote or collected 
as means of automating tasks for numerous projects, such as my bachelor thesis 
and a lot of computational chemistry projects.




# Tips and Tricks
## Python Scripts are not running in Terminal

If your scripts do not run anymore in the Terminal, but 
are opened in VS Code. 

Go to "default apps" in Windows settings and change `.py` association to Python itself and 
not to VS Code. 

→ Scripts should be working then again.  

→ If that (still) does not work, you need to change the association to the correct version of Python. 

→ Open CMD (NOT!!! Powerhshell) and type:

```cmd
assoc | help # to see all available associations
```

If it works then:
```cmd
assoc .py
```
and note the output:
```cmd
.py=Python.File
```
If not the output then:
```cmd
assoc .py=Python.File
```

Now you can change the association to the correct version of Python.
```cmd
ftype Python.File="C:\Python310\python.exe" "%1"
```

Syntax:
```cmd
ftype <FileType>=<Path to executable> "%1"
```
