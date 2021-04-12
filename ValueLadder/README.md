# ValueLadder

![Screenshot](/ValueLadder/lib/samples/demo.gif)

This repository contains a global VALUELADDER component that
can be called to pop up a floating menu styled after the form and functionality of TouchDesigner's built in ValueLadder  

# Quickstart  

lselect hold or mselect the example 'holdPanelExec' 
to call op.VALUELADDER.Open()  

ctrl.select valueLadder for PopMenu  
rselect to reset value to default  
type in parValue field to set par.val manually  

functionality is close to the built in ValueLadder,
but requires an extra click action on the chosen
value increment, and the secondary pop menu has
been condensed to a single menu with label and 
value feedback  

Default behavior is for the valueLadder window to close when it
loses focus. Set closeOnClickRelease=True for TD typical behavior
Closeonclickrelease  

op.VALUELADDER.Open(component, parameter, width=48, height=200, displayThousand=False, 
			displayHundred=True, displayTen=True, displayOne=True, 
			displayTenth=True, displayHundredth=True, displayThousandth=True, 
			borders=False, autoClose=True, closeOnClickRelease=True)  

# Parameters  
------------

> component : str  
    The operater path of the parameter owner you wish to target  
> parameter : str  
    the parName of the parameter whose value you wish to affect  
> width : int  
    The width of the valueLadder popMenu   
> height : int  
    The height of the valueLadder popMenu 	 
> displayThousand	: bool  
    display the Thousand multiplier interval in ValueLadder popup  
> displayHundred : bool  
    display the Hundred multiplier interval in ValueLadder popup  
> displayTen : bool  
    display the Ten multiplier interval in ValueLadder popup  
> displayOne : bool 
    display the One multiplier interval in ValueLadder popup  
> displayTenth : bool  
    display the Tenth multiplier interval in ValueLadder popup  
> displayHundredth : bool  
    display the Hundredth multiplier interval in ValueLadder popup  
> displayThousandth : bool  
    display the Thousandth multiplier interval in ValueLadder popup  
> borders : bool  
    display default pane borders(minimize, fullscreen, close,move)  
> closeOnClickRelease : bool 
    closes ValueLadder window on lclick release after interaction  
> autoClose : bool  
    closes ValueLadder window when the popMenu window loses focus  

