# Browser

![Screenshot](/Browser/lib/samples/demo.jpg)

This repository contains a global BROWSER component that
can be called to pop up a floating file explorer for navigating, managing, importing and accessing assets and tox files external to TouchDesigner

# Version
built in TouchDesigner build 12380.

# Known Issues
Works on mac, but td-pip install isn't currently supported, so rclick delete will be caught in an error exception and nothing will happen. Completely borked in 2020 td build, will not support

# Quickstart  
Drop BROWSER.tox into a TouchDesigner session. Local cache and pip dependancy folders are created in the project folder location.

If Initfoldersoncreate is True, folder definitions will be updated when the tox is created to the current machine when you drop the tox into a session. Folder init definitions can be edited by the user in the BrowserExt. Folder labels and references can be updated by double clicking the desired lister cell

Right click menus return expected menu items for a file explorer

Users can add or delete their own folders via the right click menu of the left most folder lister. By default the folder depth is limited to 4 children to avoid stalls in loading massive fileTrees, but this parameter can be changed in the Browser options

A search bar uses case insensitive regular expressions to filter through the returned folder results. If the Livesearch parameter of SearchFilter is True, the results are dynamically fuzzy found, otherwise enter will return the filter results

The browser can be sorted by its headers, including size(kb), name, path and date modified. Filetypes are color coded via a series of background TOPs that can be user defined in the treeListerConfig base.

Icons are imported on selection by loading a single frame to the sys/quiet folder. This folder is bypassed and global op shortcuts are disabled. Files in this folder are automatically deleted on quit. If the 'Export Cache on Save' and 'Import Cache on Start' parameters are True, a local cache directory can be made persistent across saves by storing these files to disk.  

When the listCOMP gets 2021 dragdrop standards, dragging operators to the network will be supported. In the meantime, 'Place in Network' from the right click menu, or dragging from the 'Drag Surrogate' panel will allow for this functionality.

Shift/ctrl clicking to select a range of files is supported, and icons can be batch loaded via the right click menu

File and folder deletion is supported via a dynamically pip installed library called send2trash downloaded on the first delete attempt... this will cause a brief hang the first time its engaged while the package installs. This process is based on td-pip by Alphamoonbase and was adapted from the [Olib utility](https://olib.amb-service.net/)  

This package allows for files to be sent to trash/recycle bin across platforms. While it adds a non-negligable file size overhead to the package, its a feature I really wanted but was too dangerous with just the os.remove() method that deletes items from the disk without ability for recovery


# Parameters  
------------

All public parameters are accessible in some form from as customPars
