# Selenium WebDriver Wrapper

## Packaging
Exceute cookiecut.sh and fill out forms appropriately. (mostly project(/repo) name (python-)selenium_wrapper )

Add contents of src to the src directory of the newly created subdirectory. Maybe there is another subdirectory within. Files should be at same level as the automatically create ```cli.py```/```__main__.py```.

Add ```include src/selenium_wrapper/driver/*``` to the 'MANIFEST.in' file. Path may vary but should be point to the driver directory within the newly created folder.

Go to selenium_wrapper subdirectory (created by cookiecutter), and install via ```python3 -m pip install .```
