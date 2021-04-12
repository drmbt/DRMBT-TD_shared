# This file and all related intellectual property rights are
# a part of the Hive family of TD operators by DRMBT.  The use and modification
# of this file is governed by, and only permitted under, the terms
# of the Hive [End-User License Agreement]
# [https://drmbt.com/placeholder/userAgreement.asp]
# (the "License Agreement").  Among other terms, this file can only
# be used, and/or modified for use, with HIVE ops for Derivative's TouchDesigner
# software, and only by employees of the organization that has licensed
# Derivative's TouchDesigner software and [accepted] the License Agreement.
# Any redistribution or sharing of this file, with or without modification,
# to or with any other person is strictly prohibited [(except as expressly
# permitted by the License Agreement)].
#
# Version: 001.2021.001.11Apr
#
# _END_HEADER_

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
		Open(component, parameter, width=48, height=200, displayThousand=False, 
			displayHundred=True, displayTen=True, displayOne=True, 
			displayTenth=True, displayHundredth=True, displayThousandth=True, 
			borders=False, autoClose=True, closeOnClickRelease=True)

		Open a mouse centered popMenu when provided with an operator
		and parameter argument. Increment display options, windos size,
		and close behavior preferences can be set here
	"""

	def __init__(self,ownerComp):
		self.ownerComp = ownerComp

	@property
	def Pos(self):
		"""get the panel.rollu starting position on interaction"""
		return self.ownerComp.par.Pos.eval()
	
	@property
	def ValueMultiplier(self):
		"""an amount to increment or decrement the target par.val"""
		return self.ownerComp.par.Valuemultiplier.eval()

	def setPos(self, v):
		"""store the panel.rollu starting position on interaction"""
		self.ownerComp.par.Pos= v

	def	setUround(self,v):
		"""round the incoming u val to affect the target in 1/10 increments"""
		self.ownerComp.par.Uround = round(v, 1)

	def setValueMultiplier(self, v):
		"""set the desired interval by which you'd like to affect the target par"""
		p = self.ownerComp.par.Valuemultiplier
		if v == 'value_thousand':
			p.val = 1000
		if v == 'value_hundred':
			p.val = 100
		if v == 'value_ten':
			p.val = 10
		if v == 'value_one':
			p.val = 1
		if v == 'value_tenth':
			p.val = .1
		if v == 'value_hundredth':
			p.val = .01
		if v == 'value_thousandth':
			p.val = .001 
	def clear(self):
		"""reset values for next interaction"""
		ownerComp 	= self.ownerComp
		p 			= ownerComp.par
		p.Operator	= ''
		p.Parameter = ''
		p.Uround	= 0
		p.Pos		= 0
		self.close()

	def Open(self, 
			component			: str = None,
			parameter			: str = None,
			width				: int = 48,
			height				: int = 250,
			displayThousand		: bool= False,
			displayHundred		: bool= True,
			displayTen			: bool= True,
			displayOne			: bool= True,
			displayTenth		: bool= True,
			displayHundredth	: bool= True,
			displayThousandth	: bool= True,
			borders				: bool= False,
			closeOnClickRelease : bool= True,
			autoClose			: bool= True,
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
		p						= self.ownerComp.par
		p.Operator				= component
		p.Parameter				= parameter 
		p.Automaticclose		= autoClose
		p.Closeonclickrelease	= closeOnClickRelease
		p.Borders				= borders
		p.Thousanddisplay		= displayThousand
		p.Hundreddisplay		= displayHundred
		p.Tendisplay			= displayTen
		p.Onedisplay			= displayOne
		p.Tenthdisplay			= displayTenth
		p.Hundredthdisplay		= displayHundredth
		p.Thousandthdisplay		= displayThousandth
		p.w						= width
		p.h						= height

		if self.ownerComp.op("window").isOpen: 
			self.ownerComp.op("window").par.winclose.pulse()

		self.ownerComp.op("window").par.winopen.pulse()

	def close(self):
		"""close the ValueLadder popMenu window"""
		self.ownerComp.op("window").par.winclose.pulse()

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
			op(Op).par[p] = op(Op).par[p] + self.ValueMultiplier
		if par < prev:
			op(Op).par[p] = op(Op).par[p] - self.ValueMultiplier

# region callbacks

# panelexec_passThru   
	def onPanelEvent(self, event, panelValue):
		"""panelexec_passThru callbacks to condense logic to the extension"""
		ownerComp	= self.ownerComp
		owner		= panelValue.owner
		ownerName	= owner.name
		name		= panelValue.name
		v			= panelValue.val

		if event == 'valueChange':
			if name == 'u':
				self.setUround(v-self.Pos)
	
		if event == 'onToOff':
			if name == 'focusselect' and ownerComp.par.Automaticclose == True:
				self.close()
			if name == 'select':
				if ownerComp.par.Closeonclickrelease == True:
					self.clear()

		if event == 'offToOn':
			if name == 'select':
				self.setValueMultiplier(ownerName)
				v = owner.panel.rollu.val
				self.setPos(v)

			return
			
# parexec_passThru callbacks
	def onParValueChange(self, par, prev):
		"""panelexec_passThru value change callbacks to condense logic to ext"""
		if par.name == 'Uround':
			self.parseVal(par.val, prev)

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