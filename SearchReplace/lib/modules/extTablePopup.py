"""
	HIVE
	========
	
	Copyright (c) 2021 Vincent Naples
	vincent@drmbt.com
	https://www.drmbt.com	

	This file is part of HIVE.

	HIVE is a family of global components and ui elements that become
	more powerful when they interface together. HIVE is powerful, dangerous, 
	and	quite possibly full of bugs.

    As this primarily exists as a personal tool and study of TouchDesigner, git,
	Python, and general UI/UX design, it is in this form being distributed in
	hope that others may find it useful, but WITHOUT ANY WARRANTY; without even 
	the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
	
	Version: 001.2021.001.11Apr
"""
# Version: 001.2021.001.11Apr
#
# _END_HEADER_

from TDStoreTools import StorageManager
import TDFunctions as TDF

class extTablePopup:
	"""
	extTablePopup description

	The TablePopup tool is a global or local component that accepts arguments 
	to create a popup DAT editor leveraging the powerful callbacks from Lister.

	Any valid table with header will be properly configured for bi-directional
	editing, including reordering. Custom menus in the callbacks allow for 
	adding, inserting, clearing and deleting rows. Because autoDefining columns
	doesn't allow for custom buttons and behaviors, the rules below dictate how 
	one we treat common values for a specific table

	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

		# properties
		TDF.createProperty(self, 'MyProperty', value=0, dependable=True,
						   readOnly=False)

		# attributes:
		self.a = 0 # attribute
		self.B = 1 # promoted attribute

		# stored items (persistent across saves and re-initialization):
		storedItems = [
			# Only 'name' is required...
			{'name': 'StoredProperty', 'default': None, 'readOnly': False,
			 						'property': True, 'dependable': True},
		]
		# Uncomment the line below to store StoredProperty. To clear stored
		# 	items, use the Storage section of the Component Editor
		
		# self.stored = StorageManager(self, ownerComp, storedItems)

	def Winopen(self):
		"""Open a floating version of the table"""
		self.ownerComp.op('window').par.winopen.pulse()
	def Colupdate(self):
		"""Pulse passThru to update the column definitions"""
		self.ColDefine()

	def Open(self, table, label='', width=1350, height=540,	borders=False, 
			autoClose=''):
		"""
		Takes a table component argument, and sets display options for 
		label, borders, size and closing behaviors

		Parameters
		----------

		table : op
			The tableDAT operator you wish to open
		label : str
			a label for the floating window
		width : int
			width of the TablePopup window 
		height L int
			height of the TablePopup window
		borders : bool
			option to enable or disable popup window default borders
		autoClose : bool
			if enabled, this windows will close after losing panel focus

		"""
		comp = self.ownerComp
		p = comp.par

		# check if table
		if table.type == 'table':			
			p.Table = table.path 

			if label == '':
				label = op(table).name
			p.Label	= label
			p.Borders = borders
			if autoClose != '':
				p.Automaticclose = autoClose
			comp.op('TableLister').par.w = width
			comp.op('TableLister').par.h = height
			# configure Column definitions
			self.ColDefine(table)

			if comp.op("window").isOpen: 
				comp.op("window").par.winclose.pulse()	
			comp.op("window").par.winopen.pulse()

		else:
			debug('Selectedop not a valid table')

		# if dragdrop != '':
		# 	comp.op('TableLister').par.dragdropcallbacks = dragdrop

	def Close(self):
		""" Close the floating TablePopup window"""
		comp = self.ownerComp
		if comp.op("window").isOpen: 
			comp.op("window").par.winclose.pulse()

	def ColDefine(self, table=''):
		"""
		Rules for setting the column definitions from incoming table's
		header. Since we can't rely on autoconfiguration, column behavior
		and layout can be set positionally here. More information on the 
		lister definitions at the url below:

		https://docs.derivative.ca/Palette:lister

		column
		columnLabel
		sourceData
		sourceDataMode
		cellLook
		topPath
		help
		width
		stretch
		editable
		selectRow
		justify
		draggable
		clickOnDrag

		"""
		comp = self.ownerComp
		if not table:
			table = op(comp.par.Table)
		target = comp.op('TableLister/listConfig/colDefine')
		target.clear(keepFirstCol=True)

		# parse the header row and give them default positional values

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

		# specify rules for common column headers 

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
		if 'max' in table.row(0):
			target['width','max'] = 50
			target['stretch', 'max'] = 0
		if 'default' in table.row(0):
			target['width','default'] = 100
			target['stretch', 'default'] = 0
		if 'parameter' in table.row(0):
			target['width','parameter'] = 180
			target['stretch', 'parameter'] = 0
		if 'shortcut' in table.row(0):
			target['width','shortcut'] = 120
			target['stretch', 'shortcut'] = 0
		if 'path' in table.row(0):
			target['width','path'] = 450
			target['stretch', 'path'] = 1
		if 'OP' in table.row(0):
			target['width','OP'] = 450
			target['stretch', 'OP'] = 0
		if 'comment' in table.row(0):
			target['width','comment'] = 400
			target['stretch', 'comment'] = 1
		if 'execute' in table.row(0):
			target['width','execute'] = 500
			target['stretch', 'execute'] = 1
		if 'name' in table.row(0):
			target['width','name'] = 180
			target['stretch', 'name'] = 0
		if 'type' in table.row(0):
			target['width','type'] = 150
			target['stretch', 'type'] = 0

		# add a Delete Column
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
		"""parexec_passThru value change callbacks to condense logic to ext"""

		ownerComp = self.ownerComp
		name = par.name

		# selected value update
	
	def onParPulse(self, par):
		"""parexec_passThru pulse callbacks to condense logic to ext"""
		ownerComp = self.ownerComp
		if par.name == 'Test':
			print('test')
		else: 
			try:
				getattr(ownerComp, par.name)()
			except Exception as e:
				debug(e)
	