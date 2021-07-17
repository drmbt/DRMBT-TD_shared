"""
	HIVE
	========
	
	Copyright (c) 2021 [Drmbt](https://github.com/drmbt)
	[Vincent Naples](mailto:vincent@drmbt.com)
	[drmbt.com](https://www.drmbt.com)	

	This file is part of HIVE.

	HIVE is a family of global components and ui elements that become
	more powerful when they interface together. HIVE is powerful, dangerous, 
	and	quite possibly full of bugs.

    As this primarily exists as a personal tool and study of TouchDesigner, git,
	Python, and general UI/UX design, it is in this form being distributed in
	hope that others may find it useful, but WITHOUT ANY WARRANTY; without even 
	the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

	I'm releasing it in this form under the [MIT license](https://www.mit.edu/~amini/LICENSE.md)
	in hopes that it might find some use in the TouchDesigner community.

	
	Version: 001.2021.001.11Apr
"""
import TDFunctions as TDF
import webbrowser
class ValueLadder:
	"""
	Global module which when called, opens a popMenu stylized to look and act  
	like TD's built in Value Ladder. This menu requires an extra click to engage   
	an increment value through interaction instead of rollover, and the visual  
	radial feedback is built into a single menu page view.  
	
	Attributes
	----------
		ownerComp : OP
			Reference to the COMP this Class is initiated by.

	Public Methods
	--------------
		Open(component, parameter, label = None, width='', height='', displayThousand=False, 
			displayHundred=True, displayTen=True, displayOne=True, 
			displayTenth=True, displayHundredth=True, displayThousandth=True, 
			borders=False, autoClose=True, closeOnClickRelease=True)

		Open a mouse centered popMenu when provided with an operator
		and parameter argument. Increment display options, window size,
		and close behavior preferences can be set here
	"""

	def __init__(self,ownerComp):
		self.ownerComp = ownerComp

	@property
	def Name(self):
		""" return the name of the ownerComp"""
		return self.ownerComp.name
	@property
	def Pos(self):
		"""get the panel.rollu starting position on interaction"""
		return self.ownerComp.par.Pos.eval()
	@Pos.setter
	def Pos(self, v):
		"""store the panel.rollu starting position on interaction"""
		self.ownerComp.par.Pos= v
	@property
	def ValueMultiplier(self):
		"""an amount to increment or decrement the target par.val"""
		return self.ownerComp.par.Valuemultiplier.eval()
	
	def	setUround(self,v):
		"""round the incoming u val to affect the target in 1/10 increments"""
		self.ownerComp.par.Uround = round(v, 1)

	def setValueMultiplier(self, v):
		"""set the desired interval by which you'd like to affect the target par"""
		p = self.ownerComp.par.Valuemultiplier
		lookup = {	'value_thousand' 	: 1000, 
					'value_hundred' 	: 100,
					'value_ten'			: 10,
					'value_one'			: 1,
					'value_tenth'		: .1,
					'value_hundredth'	: .01,	
					'value_thousandth'	: .001
				}
		
		p.val = lookup[v]

	def	setDefaultValue(self):
		"""reset targeted parameter value to its default"""
		ownerComp 				= self.ownerComp
		p 						= ownerComp.par
		Op						= p.Operator		
		Par						= p.Parameter 		
		op(Op).par[Par].val		= op(Op).par[Par].default

	def Value(self, val):
		if not isinstance(val, float):
			self.ownerComp.op('valueLadder/parValue/field/string')[0,0] = val
		else:
			self.ownerComp.op('valueLadder/parValue/field/string')[0,0] = round(val, 3)
	
	def Open(self, 
			component			: str = '',
			parameter			: str = '',
			label				: str = None,
			width				: int = 48,
			height				: int = 250,
			displayThousand		: bool= '',
			displayHundred		: bool= '',
			displayTen			: bool= '',
			displayOne			: bool= '',
			displayTenth		: bool= '',
			displayHundredth	: bool= '',
			displayThousandth	: bool= '',
			borders				: bool= False,
			closeOnClickRelease : bool= '',
			autoClose			: bool= '',
			):
		'''
  
		Takes a component and parameter argument, sets display options for
		size and value increments, and preferences for winclose behavior.  

		Parameters
		----------
			component : str
				The operater path of the parameter owner you wish to target
			parameter : str
				the parName of the parameter whose value you wish to affect
			width : int
				The width of the valueLadder popMenu 
			height : int
				The height of the valueLadder popMenu 	
			displayThousand	: bool
				display the Thousand multiplier interval in ValueLadder popup
			displayHundred : bool
				display the Hundred multiplier interval in ValueLadder popup
			displayTen : bool
				display the Ten multiplier interval in ValueLadder popup
			displayOne : bool
				display the One multiplier interval in ValueLadder popup
			displayTenth : bool
				display the Tenth multiplier interval in ValueLadder popup
			displayHundredth : bool
				display the Hundredth multiplier interval in ValueLadder popup
			displayThousandth : bool
				display the Thousandth multiplier interval in ValueLadder popup
			borders : bool
				display default pane borders(minimize, fullscreen, close, move)
			closeOnClickRelease : bool
				closes ValueLadder window on lclick release after interaction
			autoClose : bool
				closes ValueLadder window when the popMenu window loses focus

		
		'''
		self.clear()
		p = self.ownerComp.par
		# update to **kwargs?
		if component != '':
			p.Operator				= component
		if parameter != '':
			p.Parameter				= parameter 
		if label:
			p.Label					= label
		if autoClose != '':
			p.Automaticclose		= autoClose
		if closeOnClickRelease != '':
			p.Closeonclickrelease	= closeOnClickRelease
		if borders != '':
			p.Borders				= borders
		if displayThousand != '':
			p.Thousanddisplay		= displayThousand
		if displayHundred != '':
			p.Hundreddisplay		= displayHundred
		if displayTen != '':
			p.Tendisplay			= displayTen
		if displayOne != '':
			p.Onedisplay			= displayOne
		if displayTenth != '':
			p.Tenthdisplay			= displayTenth
		if displayHundredth != '':
			p.Hundredthdisplay		= displayHundredth
		if displayThousandth != '':
			p.Thousandthdisplay		= displayThousandth
		p.Borders					= borders
		p.w							= width
		p.h							= height


		if self.ownerComp.op("window").isOpen: 
			self.ownerComp.op("window").par.winclose.pulse()

		self.ownerComp.op("window").par.winopen.pulse()

	def close(self):
		"""close the ValueLadder popMenu window"""
		self.ownerComp.op("window").par.winclose.pulse()


	def clear(self):
		"""reset values for next interaction"""
		ownerComp 			= self.ownerComp
		p 					= ownerComp.par
		p.Operator			= ''
		p.Parameter 		= ''
		p.Uround			= 0
		p.Pos				= 0
		p.Valuemultiplier	= 0
		
	def parseVal(self, par, prev):
		"""
		callback to push values to the target parameter in increments of
		the selected ValueMultiplier each time the panelValue change passes
		the round threshold from self.Uround

		"""
		ownerComp = self.ownerComp	
		Op = ownerComp.par.Operator
		p = ownerComp.par.Parameter
		if par > prev:
			op(Op).par[p] = round(float(op(Op).par[p]), 3) + self.ValueMultiplier
		if par < prev:
			op(Op).par[p] = round(float(op(Op).par[p]), 3) - self.ValueMultiplier


## Pop Menu functionality 

	def PopMenu(self):
		"""Pop Menu functionality with ctrl.select and True parameter"""
		ownerComp = self.ownerComp
		p = ownerComp.par
		Op = p.Operator
		if self.ownerComp.par.Popmenu:
			op.TDResources.op('popMenu').Open(
							items=[	f'{op(Op).name} Parameters', 
									'Viewer', 
									'Network', 
									'Customize Component', 
									f'{self.Name} Config', 
									],
							dividersAfterItems=[
									f'{op(Op).name} Parameters', 
									'Customize Component'
									],
							callback=self.onPopMenu
							)

	def onPopMenu(self, info):
		"""	Pop Menu Callbacks"""
		ownerComp = self.ownerComp
		p = ownerComp.par
		Op = p.Operator
		if info['item'] == f'{op(Op).name} Parameters':
			debug(op(Op))
			self.OpenParameters(op(Op))
		elif info['item'] == f'{self.Name} Config':
			self.OpenParameters(ownerComp)
		elif info['item'] == 'Viewer':
			self.OpenViewer(op(Op))
		elif info['item'] == 'Network':
			self.OpenNetwork(op(Op))
		elif info['item'] == 'Customize Component':
			self.CustomizeParameters(op(Op))

	def ParMenu(self):	
		"""Open popMenu to select a new Parameter target"""
		parList = [p.name for p in op(self.ownerComp.par.Operator).customPars]
		op.TDResources.op('popMenu').Open(
			items=parList,
			dividersAfterItems=[],
			callback=self.setParameter
							)
	def setParameter(self, info):
		"""ParMenu callbacks"""
		self.ownerComp.par.Parameter = info['item']
		if not self.ownerComp.op('window').isOpen:
			self.ownerComp.op('window').par.winopen.pulse()
		#self.ownerComp.par.Parameter = info['items'][0]

	def ValMenu(self):
		"""Open popMenu to select a new Parameter value for Menu datatypes"""
		valList = [p for p in op(self.ownerComp.par.Operator).par[self.ownerComp.par.Parameter].menuNames]
		op.TDResources.op('popMenu').Open(
			items=valList,
			dividersAfterItems=[],
			callback=self.setParVal
		)
	def setParVal(self, info):
		"""ValMenu callbacks"""
		op(self.ownerComp.par.Operator).par[self.ownerComp.par.Parameter].val = info['item']
							
##  Pane / Op / Dialogs

	def OpenParameters(self, comp=''):
		"""Takes an argument to open a floating parameter window"""
		if not comp:
			comp = self.ownerComp
		if hasattr(op, 'PARPOPUP'):
			op.PARPOPUP.Open(comp, 
							label=comp.name, 
							header=False, 
							height=750)
		else:
			comp.openParameters()
	def OpenNetwork(self, comp=''):
		"""Takes an argument to open a floating network"""
		if not comp:
			comp = self.ownerComp
		if hasattr(op, 'INSPECTORGADGET'):
			op.INSPECTORGADGET.Opennetwork(comp)
		else:
			pane = TDF.showInPane(op(comp))
			pane.showParameters = True

	def OpenViewer(self, comp=''):
		"""Takes an argument to open a floating viewer"""
		if not comp:
			comp = self.ownerComp
		comp.openViewer()

	def CustomizeParameters(self, comp=''):
		"""Pulse to open a floating par editor dialog"""
		if not comp:
			comp = self.ownerComp
		op.TDDialogs.op('CompEditor').EditComp(comp)

	def Readme(self):
		"""Pulse to open a floating Readme document"""
		self.OpenViewer(self.ownerComp.op('code/readme'))
		debug('readme')
	def Support(self):
		webbrowser.open('https://drmbt.com/projects/about/')

	def Git(self):
		webbrowser.open(self.ownerComp.par.Github.val)
	def Helpgit(self):
		"""Pulse to open a floating network"""
		ui.viewFile(self.ownerComp.par.Helpurl)

# region callbacks

# panelexec_passThru   
	def onPanelEvent(self, event, panelValue):
		"""panelexec_passThru callbacks to condense logic to the extension"""
		ownerComp	= self.ownerComp
		owner		= panelValue.owner
		ownerName	= owner.name
		name		= panelValue.name
		v			= panelValue.val
##  Local Keyboard Shortcuts / Hotkeys 	                
		if hasattr(op, 'KEYMACROS'):
			ctrl 	= op.KEYMACROS.par.Ctrl
			shift	= op.KEYMACROS.par.Shift
			alt 	= op.KEYMACROS.par.Alt
		else:
			ctrl	= owner.panel.ctrl
			shift	= owner.panel.shift
			alt 	= owner.panel.alt

		if event == 'valueChange':
			if name == 'u':
				self.setUround(v-self.Pos)
	
		if event == 'onToOff':
			if name == 'select':
				if ownerComp.par.Closeonclickrelease == True:
					self.clear()
					self.close()
			if name == 'focusselect' and ownerComp.par.Automaticclose == True:
				if owner == ownerComp.op('valueLadder'):
					self.close()
		if event == 'offToOn':

			if name == 'select':
				if 'value' in owner.name:
					self.setValueMultiplier(ownerName)
					v = owner.panel.rollu.val
					self.Pos = v
				if owner.name == 'parMenu':
					self.ParMenu()
				if owner.name == 'field':
					if self.ownerComp.par.Type == 'Menu':
						self.ValMenu()

			if name == 'rselect' and not ctrl:
				if ownerComp.par.Rclicksetdefault:
					self.setDefaultValue()
					ownerComp.par.Uround			= 0
					ownerComp.par.Pos				= 0
					ownerComp.par.Valuemultiplier	= 0
			if ctrl == 1 and alt == 0:
				if name == 'rselect' or name == 'lselect':
					self.PopMenu()
		return
			
# parexec_passThru callbacks
	def onParValueChange(self, par, prev):
		"""panelexec_passThru value change callbacks to condense logic to ext"""
		if par.name == 'Uround':
			self.parseVal(par.val, prev)
		if par.name == 'Value':
			self.Value(par.eval())

	def onParPulse(self, par):
		"""panelexec_passThru pulse callbacks to condense logic to ext"""
		ownerComp = self.ownerComp
		if par.name == 'Help':
			print(help(ValueLadder))
		else: 
			try:
				getattr(ownerComp, par.name)()
			except Exception as e:
				debug(e)
# end region