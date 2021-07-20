"""
	THE DANDI LINE
	==============
	
	Copyright (c) 2021 [Drmbt](https://github.com/drmbt)
	[Vincent Naples](mailto:vincent@drmbt.com)
	[drmbt.com](https://www.drmbt.com)	

	This file was commissioned by [DandiDoesIt](https://www.twitch.tv/dandidoesit),
	powering The Dandi Line, a Live Performance Video Game (LPVG) leveraging the
	Twitch platform as a vehicle for interactive theater. 
	
	non proprietary components are released under the
	Creative Commons Attribution-NonCommercial 4.0 International license, a
	copy of which should have been provided with this distribution, but can 
	be found at [CreativeCommons.org](https://creativecommons.org/licenses/by-nc/4.0/legalcode)

	this license allows for an individual to copy and redistribute the material 
	in any medium or format, to Adapt, remix, transform, and build upon the material. 

	For commercial use cases or licensing, contact the creator.
	
	Version: 001.2021.001.17July
"""

import TDFunctions as TDF
import webbrowser
import datetime
import time

class LotteryExt:
	"""
	LotteryExt drives a global component for quickly adding entrants to a
	lottery pool and selecting a random winner by rotating through the entrants
	wheel of fortune style.
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	@property
	def Table(self):
		table = self.ownerComp.op('table_lottery')
		return table

#	public methods
	def Addentrant(self, user=None):
		'''
		specify a user and add a time stamped entry to the table. 
		if no user is specified, add entry from ownerComp customPar['Entrantname']
		'''
		table = self.Table
		if not user:
			user = self.ownerComp.par.Entrantname.eval()
		epoch = time.time()
		timeStamp = datetime.datetime.fromtimestamp(epoch).strftime('%Y_%m_%d_%H_%M_%S')
		table.appendRow([user, timeStamp])
		self.ownerComp.par.Entrantname = ''

	def Selectwinner(self, length : float=None):
		'''
		trigger for winner selection process. if no length is specified,
		get length from ownerComp customPar['Selectionlength']
		'''
		randNum = tdu.remap(tdu.rand(absTime.frame),0, 1, 0, self.Table.numRows-2)
		self.ownerComp.op('speed1').par.resetvalue = randNum
		self.ownerComp.op('speed1').par.resetpulse.pulse()
		self.ownerComp.op('count1').par.resetvalue = int(randNum)
		self.ownerComp.op('count1').par.resetpulse.pulse()
		self.ownerComp.op('trigger1').par.triggerpulse.pulse()
		op('audiofilein1').par.play = 1
		

	def Cleartable(self):
		'''remove all entrants from the table'''
		self.Table.clear(keepFirstRow=True)


	def Exporttable(self):
		'''timestamped method for export on exit'''
		folder = self.ownerComp.par.Tablefolder.eval()
		epoch = time.time()
		timeStamp = datetime.datetime.fromtimestamp(epoch).strftime('%Y_%m_%d')
		fileName = f'{folder}/table_lotto_{timeStamp}.py'
		self.Table.save(fileName)

	def Exporttableas(self, fileName=None):
		'''save table as method for exporting lotto entrants'''
		folder = self.ownerComp.par.Tablefolder.eval()
		if not fileName:
			fileName = ui.chooseFile(load=False, start=folder, 
								fileTypes=['py'], title='Save table as:')
		if fileName:
			self.Table.save(fileName)
			print(f'{self.Table} successfully saved as {fileName}')

	def Importtable(self):
		'''method for importing an externalized lotto table'''
		folder = self.ownerComp.par.Tablefolder.eval()
		fileName = ui.chooseFile(load=True, start=folder, 
								fileTypes=['py'], title='Load table:')
		importProxy = self.ownerComp.op('importProxy')
		if fileName != None:
			ui.undo.startBlock(f'undo {self.Table} import from {fileName}')
			importProxy.clear()
			importProxy.par.file = fileName
			importProxy.par.loadonstartpulse.pulse()
			self.Table.copy(importProxy)
			ui.undo.endBlock()
			debug(f'{self.Table} successfully imported from {fileName}')

# support methods

	def Readme(self):
		"""Pulse to open a floating Readme document"""
		self.ownerComp.op('readme').openViewer()
		debug('readme')

	def Support(self):
		'''partronize the creator'''
		url = self.ownerComp.par.Supporturl.eval()
		webbrowser.open(url)

	def Git(self):
		'''navigate browser to git repo'''
		webbrowser.open(self.ownerComp.par.Github.val)

# region callbacks

# parexec_passThru callbacks
	def onParValueChange(self, par, prev):
		"""parexec_passThru value change callbacks to condense logic to ext"""
		if par.name == 'Test':
			debug('Test')

	def onParPulse(self, par):
		"""parexec_passThru pulse callbacks to condense logic to ext"""
		ownerComp = self.ownerComp
		if par.name == 'Help':
			print(help(self))
			ui.messageBox('Help', 'help printed to textport', buttons=['ok'])
		else: 
			try:
				getattr(ownerComp, par.name)()
			except Exception as e:
				debug(e)


# end region