# ColorPicker

![Screenshot](/ColorPicker/lib/samples/demo.gif)

This repository contains a global ColorPicker component that can be called to pop up a floating ColorPickerUI with a number of useful features: 
- modular, scaleable global pop dialogue for color control
- generate local user interfaces for custom UI design
- dynamic RGB/HSV/HEX conversion
- a sortable ramp assembler DAT lister for fine control of ramps and palettes
- a protocol for importing and exporting color palettes. 

# Version
tested as stable in TouchDesigner build 13610.



# Quickstart  
Check out the sample project for examples of how one might call ColorPicker to generate a temporary UI for a color tuplet  

Generateui():  
Create a copy of the user interface to be worked into larger UI design

SetPushColor(r: parameterR):  

provide the 'r' member of a color paramter tuplet to temporarily link the UI to the specified rgb or rgba tuplet

Openui(**kwargs):  
set an arbitrary number of unordered Parameter values for the popup UI. Same as calling Open(**kwargs) on the ColorPickerUI comp itself.  

This method leaves the previous value as default, so only what you need changed must be specified

example panelexecDAT script:
```
def onOffToOn(panelValue):
	op.COLORPICKER.SetPushColor(op(me.par.panels).par['Rgbar'])
	op.COLORPICKER.Openui(
	Label				= f"Full UI: {op(me.par.panels).path}",  
	Displayheader			= True,  
	Displayhsv			= True,  
	Displayspectrum 		= True,  
	Displaycolorcontrols	        = True,  
	Displaypickerpars		= True,  
	Displaypalette			= True,  
	Displayramplister		= True,  
	W				= 720,  
	H				= 960,  
	Orient				= 'horz',  
	Autoclose			= False,
	    )  

```

		

# Parameters  
------------
All public parameters are accessible in some form from as customPars

# Known Issues
--------------
LUT importing is inconsistent, needs to be switched manually for now
