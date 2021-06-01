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


from TDStoreTools import StorageManager
import TDFunctions as TDF
import os

class extTablePopup:
	"""
	extTablePopup description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
	@property
	def Table(self):
		return self.ownerComp.par.Table.eval()

	@Table.setter
	def Table(self, comp):
		self.ownerComp.par.Table = comp

	def Winopen(self):
		self.ownerComp.op('window').par.winopen.pulse()
	def Colupdate(self):
		self.ColDefine()

	def Exporttable(self):
		fileName = ui.chooseFile(load=False, start='local/mappings', 
								fileTypes=['py'], title='Save table as:')
		if fileName:
			self.Table.save(fileName)
			print(f'{self.Table} successfully saved as {fileName}')

	def Importtable(self):
		fileName = ui.chooseFile(load=True, start='local/mappings ', 
								fileTypes=['py'], title='Load table:')
		importProxy = self.ownerComp.op('code/importProxy')
	#	if fileName != self.Table.par.file:
		ui.undo.startBlock(f'undo {self.Table} import from {fileName}')
		importProxy.clear()
		importProxy.par.file = fileName
		importProxy.par.loadonstartpulse.pulse()
		self.Table.copy(importProxy)
		ui.undo.endBlock()
		debug(f'{self.Table} successfully imported from {fileName}')
			#importProxy.clear()
	def Appendtable(self, table=''):
		if table != '':
			self.Table = table
		fileName = ui.chooseFile(load=True, start='local/mappings ', 
								fileTypes=['py'], title='Append table:')
		importProxy = self.ownerComp.op('code/importProxy')
		ui.undo.startBlock(f'undo append{fileName} to {self.Table}')
		importProxy.par.file = tdu.collapsePath(fileName)
		op(self.Table).appendRows(importProxy.rows()[1:])
		ui.undo.endBlock()
		debug(f'{fileName} successfully appended to {self.Table}')

	def Cleartable(self):
		self.clearDialog()

	def clearDialog(info):
		op.TDResources.op('popDialog').Open(
		text='Are you sure you want to clear this table?',
		title='Delete',
		buttons=['OK', 'Cancel'],
		callback=clearTable,
		details=info,
		textEntry=False,
		escButton=2,
		enterButton=1,
		escOnClickAway=True)
	
	def clearTable(self, info):	
		if info['button'] == 'OK':
			ui.undo.startBlock('undo Clear Table')
			self.Table.clear(keepFirstRow=True)
			ui.undo.endBlock()
		return

	def Opennetwork(self, comp=''):
		if not comp:
			comp = op(self.Table)
		if hasattr(op, 'INSPECTORGADGET'):
			op.INSPECTORGADGET.Opennetwork(comp)
		else:
			pane = TDF.showInPane(comp)
			pane.showParameters = True

	def Explorer(self, comp):
		os.open(op(self.Table).par.file)


	def Open(self, 
			table, 
			label='', 
			tableHeader=True,
			width = '', 
			height= '',	
			borders=False, 		
			autoClose='', 
			header=True,
			dragdrop=''
			):
		comp = self.ownerComp
		p = comp.par

		# check if table
		if table.type == 'table':			
			p.Table = table.path #self.ownerComp.relativePath(table)
			if label == '':
				label = op(table).name
			p.Label	= label
			p.Borders = borders
			if autoClose != '':
				p.Automaticclose = autoClose

			p.Header = header

			if width != '':
				comp.op('TableLister').par.w = width
			if height != '':
				comp.op('TableLister').par.h = height

			# configure Column definitions
			self.ColDefine(table)

			if not comp.op("window").isOpen: 
				comp.op("window").par.winopen.pulse()
				
		#	comp.op("window").par.winopen.pulse()
		else:
			debug('Selectedop not a valid table')

		if dragdrop != '':
			comp.op('TableLister').par.dragdropcallbacks = dragdrop

	def Close(self):
		comp = self.ownerComp
		if comp.op("window").isOpen: 
			comp.op("window").par.winclose.pulse()

	def ColDefine(self, table=''):
		debug('coldefine')
		comp = self.ownerComp
		if not table:
			table = op(comp.par.Table)
		target = comp.op('TableLister/listConfig/colDefine')
		target.clear(keepFirstCol=True)
		for cell in table.row(0):
			target.appendCol([cell,
							'*',
							cell,
							'string',
							'',
							'',
							'',
							'120',
							'1',
							'2',
							'1',
							'0',
							'1',
							'CENTERLEFT',
							'0',
							'0'
							])

		if 'Invert' in table.row(0):
			target.replaceCol('Invert', ['Invert',
										'*',
										'Invert',
										'blank',
										'button',
										'checkbox*',
										'',
										'50',
										'0',
										'0',
										'0',
										'0',
										'1',
										'CENTERLEFT',
										'0',
										'0'
										])
		if 'Active' in table.row(0):
			target.replaceCol('Active', ['Active',
										'*',
										'Active',
										'blank',
										'button',
										'checkbox*',
										'',
										'50',
										'0',
										'0',
										'0',
										'0',
										'1',
										'CENTERLEFT',
										'0',
										'0'
										])
		if 'Toggle' in table.row(0):
			target.replaceCol('Toggle', ['Toggle',
										'*',
										'Toggle',
										'blank',
										'button',
										'checkbox*',
										'',
										'50',
										'0',
										'0',
										'0',
										'0',
										'1',
										'CENTERLEFT',
										'0',
										'0'
										])
		if 'toggle' in table.row(0):
			target.replaceCol('toggle', ['toggle',
										'*',
										'toggle',
										'blank',
										'button',
										'checkbox*',
										'',
										'50',
										'0',
										'0',
										'0',
										'0',
										'1',
										'CENTERLEFT',
										'0',
										'0'
										])
		if 'Rename' in table.row(0):
			target.replaceCol('Rename', ['Rename',
										'*',
										'Rename',
										'blank',
										'button',
										'checkbox*',
										'',
										'50',
										'0',
										'0',
										'0',
										'0',
										'1',
										'CENTERLEFT',
										'0',
										'0'
										])
		if 'Missing' in table.row(0):
			target.replaceCol('Missing', ['Missing',
										'*',
										'Missing',
										'blank',
										'button',
										'missing*',
										'',
										'60',
										'0',
										'0',
										'0',
										'0',
										'1',
										'CENTERLEFT',
										'0',
										'0'
										])
		if 'Exists' in table.row(0):
			target.replaceCol('Exists', ['Exists',
										'*',
										'Exists',
										'blank',
										'button',
										'exists*',
										'',
										'60',
										'0',
										'0',
										'0',
										'0',
										'1',
										'CENTERLEFT',
										'0',
										'0'
										])
		if 'Delete' in table.row(0):
			target.replaceCol('Delete', ['Delete',
										'*',
										'X',
										'',
										'button',
										'delete',
										'',
										'50',
										'0',
										'0',
										'0',
										'0',
										'0',
										'CENTERLEFT',
										'0',
										'0'
										])
		
		
		# rules for common values

		if 'min' in table.row(0):
			target['width','min'] = 50
			target['stretch', 'min'] = 0
		if 'normMin' in table.row(0):
			target['width','normMin'] = 70
			target['stretch', 'normMin'] = 0
		if 'max' in table.row(0):
			target['width','max'] = 60
			target['stretch', 'max'] = 0
		if 'normMax' in table.row(0):
			target['width','normMax'] = 70
			target['stretch', 'normMax'] = 0
		if 'default' in table.row(0):
			target['width','default'] = 80
			target['stretch', 'default'] = 0
		if 'style' in table.row(0):
			target['width','style'] = 80
			target['stretch', 'default'] = 0
		if 'parameter' in table.row(0):
			target['width','parameter'] = 180
			target['stretch', 'parameter'] = 0
		if 'shortcut' in table.row(0):
			target['width','shortcut'] = 120
			target['stretch', 'shortcut'] = 0
		if 'path' in table.row(0):
			target['width','path'] = 450
		if 'owner' in table.row(0):
			target['width','owner'] = 250
			target['stretch', 'owner'] = 1
		if 'expr' in table.row(0):
			target['width','expr'] = 250
			target['stretch', 'expr'] = 1
		if 'OP' in table.row(0):
			target['width','OP'] = 450
			target['stretch', 'OP'] = 0
		if 'comment' in table.row(0):
			target['width','comment'] = 400
			target['stretch', 'comment'] = 1
		if 'execute' in table.row(0):
			target['width','execute'] = 650
			target['stretch', 'execute'] = 1
		if 'script' in table.row(0):
			target['width','script'] = 650
			target['stretch', 'script'] = 1
		if 'name' in table.row(0):
			target['width','name'] = 150
			target['stretch', 'name'] = 0
		if 'checked' in table.row(0):
			target['width','checked'] = 150
			target['stretch', 'checked'] = 0
		if 'disabled' in table.row(0):
			target['width','disabled'] = 150
			target['stretch', 'disabled'] = 0
		if 'dividers' in table.row(0):
			target['width','dividers'] = 150
			target['stretch', 'dividers'] = 0
		if 'highlight' in table.row(0):
			target['width','highlight'] = 150
			target['stretch', 'highlight'] = 0
		if 'label' in table.row(0):
			target['width','label'] = 150
			target['stretch', 'label'] = 0
		if 'items' in table.row(0):
			target['width','items'] = 150
			target['stretch', 'items'] = 0
		if 'page' in table.row(0):
			target['width','page'] = 80
			target['stretch', 'page'] = 0
		if 'ParMode' in table.row(0):
			target['width','ParMode'] = 120
			target['stretch', 'ParMode'] = 0
		if 'style' in table.row(0):
			target['width','style'] = 80
			target['stretch', 'style'] = 0
		if 'type' in table.row(0):
			target['width','type'] = 150
			target['stretch', 'type'] = 0
		if 'param' in table.row(0):
			target['width','param'] = 150
			target['stretch', 'param'] = 0
		if 'controller' in table.row(0):
			target['width','controller'] = 150
			target['stretch', 'controller'] = 0
		if 'element' in table.row(0):
			target['width','element'] = 150
			target['stretch', 'element'] = 0

		# add a Delete Column
		debug('add delete')
		if 'Delete' not in table.row(0):
			target.appendCol(['Delete',
							'*',
							'X',
							'',
							'button',
							'delete',
							'',
							'50',
							'0',
							'0',
							'0',
							'0',
							'0',
							'CENTERLEFT',
							'0',
							'0'
							])

##	parexec_passThru callbacks

	def onParValueChange(self, par, prev):
		ownerComp = self.ownerComp
		name = par.name

		# selected value update
	
	def onParPulse(self, par):
		ownerComp = self.ownerComp
		if par.name == 'Test':
			print('test')
		else: 
			try:
				getattr(ownerComp, par.name)()
			except Exception as e:
				debug(e)
	