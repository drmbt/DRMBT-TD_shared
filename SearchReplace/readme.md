#SEARCHREPLACE  

This ui is a lister hack of Ivan's searchReplace palette tool. in addition to providing a nice UI for
working with searchReplace, this element leverages some powerful and potentially destructive callbacks
in lister to push data from edited cells to the specified OP. This includes moving the OP's path, 
renaming parPageNames, parNames and parLabels, and changing data in the pars.  

care has been taken to prevent accidents and anticipate user behavior. if the length of a list provided
is different then the initial list, all data will push the first item in that string list, separated by
a comma. I'm sure I haven't thought of everything, so be careful

Future todo's include implementing proper undo callbacks for cells edited, and separating replace from
'Go' functionality to allow for a refined table list to be the only thing changed onReplace

known issues are that it doesn't like integers as a search string, but floats will be found, and can be 
updated as Par Data by editing the cell to a new number, which can be an integer