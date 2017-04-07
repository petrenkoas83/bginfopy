==================
bginfopy
==================
 
Agreement of project structure
-------------------------------

https://packaging.python.org/distributing

https://github.com/pypa/sampleproject

Use stdeb to create deb-package
--------------------------------

https://pypi.python.org/pypi/stdeb

Just run next command to build deb-package:

python setup.py --command-packages=stdeb.command sdist_dsc --depends imagemagick bdist_deb
