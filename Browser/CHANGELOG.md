# Changelog
All notable changes to this project will _hopefully_ be documented in this file.

The format is _loosely_ based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project _tries to_ adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


### [1.1.3] 2021-6-1
clicking invalid files clears tmpViewer
epoch conversion handled in extension and treeLister, not as eval mod

# To Do  
Wrap send2trash, eliminate td-pip implementation

### [1.1.2] 2021-5-19

- Add Refreshfolder() to treeLister r click menu
- Add rollover help to clarify delete function, ambiguous customPars
## experimental 
addition of project.paths to folder list on init. Adding a folder now automatically adds that folder to project.paths, and adding something to project.paths should dynamically create the folder. Known issues with cooking stem from dependability monitoring len(project.paths), will investigate ways to get that to cook. shouldn't really be a problem most anyone encounters, but we'll see



### [1.1.1] 2021-5-12
hour minute second granularity for epoch time conversion added
rollover help updated to accurately reflect path for folders

### [1.1] 2021-5-12
carve out loophole for epoch conversion errors on mac

### [1.0] 2021-5-12
initial commit
