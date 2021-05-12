# Browser

![Screenshot](/Browser/lib/samples/demo.jpg)

This repository contains a global BROWSER component that
can be called to pop up a floating file explorer for navigating and
accessing assets and tox files external to TouchDesigner

# Quickstart  
call op.BROWSER.Openbrowser() to pop up a floating browser UI
call Initfolderlist() to reset to a default set of paths for this filesystem
- these folder definitions can be edited by the user in the BrowserExt
right click menus return expected menu items for a file explorer

users can add or delete their own folders via the right click menu of the left most folder lister. By default the folder depth is limited to 4 children to avoid stalls in loading massive fileTrees, but this parameter can be changed in the Browser options

a search filter uses case insensitive regular expressions to filter through the returned folder results. If the Livesearch parameter of SearchFilter is True, the results are dynamically fuzzy found, otherwise enter will return the filter results

The browser can be sorted by its headers, including size(kb), name, path and date modified. Filetypes are color coded via a series of background TOPs that can be user defined in the treeListerConfig base.

icons are imported on selection by loading a single frame to the sys/quiet folder. This folder is bypassed and global op shortcuts are disabled. Files in this folder are automatically deleted on quit. If the 'Export Cache on Save' and 'Import Cache on Start' parameters are True, a cache directory can be persistant across saves by storing these icons in a local directory.  

When the listCOMP gets 2021 dragdrop standards, dragging operators to the network will be supported. in the meantime, 'Place in Network' from the right click menu, or dragging from the 'Drag Surrogate' panel will allow for this functionality.

shift clicking to select a range of files is supported, and icons can be batch loaded via the right click menu

file and folder deletion is supported via a dynamically pip installed library called send2trash downloaded and installed on first delete attempt. This process is based on td-pip by Alphamoonbase and was adapted from the [Olib utility](https://olib.amb-service.net/)  
This package allows for files to be sent to trash/recycle bin across platforms. While it adds a non-negligable file size overhead to the package, its a feature I really wanted but was too dangerous with just the os.remove() method that hard removes items from the disk


# Parameters  
------------

All public parameters are accessible in some form from as customPars
