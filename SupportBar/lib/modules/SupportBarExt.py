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

class SupportBarExt:
	"""
	SupportBarExt drives a global component for quickly visualizing support data
	from an arbitrary number of incoming sources

	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	@property
	def Table(self):
		table = self.ownerComp.op('table_support')
		return table

	@property
	def SupportDict(self):
		table = self.ownerComp.op('table_supportDict')
		keys = [k.val for k in table.col(0)]
		vals = [v.val for v in table.col(1)]
		sd = {keys[i]: vals[i] for i in range(1, len(keys))}
		return sd

	@property
	def TypeSet(self):
		'''
		converts all entries from table support into a set to eliminate duplicates
		note that the replicated selects pulling from this set will strip trailing
		digits, so "tier1" will become "tier"
		'''
		d = set(self.SupportDict)
		s = set([ c.val for c in self.Table.col('type')[1:]])
		l = list(s.union(d))
		return l
#	public methods
	def Addentry(self, user=None, type='gift', units=1, value=None):
		'''
		public trigger for appending a time/user stamped value to the support table
		'''
		table = self.Table
		if not user:
			user = self.ownerComp.par.Entrantname.eval()
		epoch = time.time()
		timeStamp = datetime.datetime.fromtimestamp(epoch).strftime('%Y_%m_%d_%H_%M_%S')
		if not value:
			if type in self.SupportDict:
				value = self.SupportDict[type]
			else:
				debug('value argumment required for undefined event types')
				value = 0
		subtotal = (units * float(value))
		table.appendRow([type, units, value, subtotal, user, timeStamp])




#	table methods

	def Cleartable(self):
		'''remove all entrants from the table'''
		self.Table.clear(keepFirstRow=True)

	def Edittable(self):
		'''open floating popup to edit table entries'''
		table = self.Table
		if hasattr(op, 'TABLEPOPUP'):
			op.TABLEPOPUP.Open(table, 
			Label= 'Edit Support Table')
		else:
			table.openViewer()

	def Editsupportdict(self):
		'''open floating popup to edit key/value schedule'''
		table = self.ownerComp.op('table_supportDict')
		if hasattr(op, 'TABLEPOPUP'):
			op.TABLEPOPUP.Open(table, 
			Label= 'Edit Support Table')
		else:
			table.openViewer()

	def Exporttable(self):
		'''timestamped method for export on exit'''
		folder = self.ownerComp.par.Tablefolder.eval()
		epoch = time.time()
		timeStamp = datetime.datetime.fromtimestamp(epoch).strftime('%Y_%m_%d')
		fileName = f'{folder}/table_support_{timeStamp}.py'
		self.Table.save(fileName)

	def Exporttableas(self, fileName=None):
		'''save table as method for exporting support entries'''
		folder = self.ownerComp.par.Tablefolder.eval()
		if not fileName:
			fileName = ui.chooseFile(load=False, start=folder, 
								fileTypes=['py'], title='Save table as:')
		if fileName:
			self.Table.save(fileName)
			print(f'{self.Table} successfully saved as {fileName}')

	def Importtable(self):
		'''method for importing an externalized support table'''
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