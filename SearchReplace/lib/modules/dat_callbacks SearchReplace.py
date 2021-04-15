#Shared Use License: This file is owned by Derivative Inc. (â€œDerivativeï¿½) 
#and can only be used, and/or modified for use, in conjunction with 
#Derivativeâ€™s TouchDesigner software, and only if you are a licensee who 
#has accepted Derivativeâ€™s TouchDesigner license or assignment agreement 
#(which also governs the use of this file).  You may share a modified version 
#of this file with another authorized licensee of Derivativeâ€™s TouchDesigner 
#software.  Otherwise, no redistribution or sharing of this file, with or 
#without modification, is permitted.

"""
All callbacks for this lister go in this DAT. For a list of available callbacks,
see:

https://docs.derivative.ca/Palette:lister#Custom_Callbacks
"""

"""
See also:
https://docs.derivative.ca/PopDialog_Custom_COMP_Examples
"""
import string
import TDFunctions as TDF
#_______ General selection callbacks ________#
table = op(op(parent().dock).par.Inputtabledat)
def clearTable(info):
	
	if info['button'] == 'OK':
		table.clear(keepFirstRow=True)
	return

def Refresh():	
	parent().dock.par.Refresh.pulse()

def updateTable(row, col, cellText):
	table[row, col] = cellText
	Refresh()

def generalSelection(info):
	selection = info['item']
	# if selection == 'Clear Row':
	# 	table.replaceRow(info['details'], '', entireRow=True)
	# elif selection == 'Delete Row':
	# 	table.deleteRow(info['details'])
	# elif selection == 'Add Row':
	# 	table.appendRow()
	# elif selection == 'Insert Row':
	# 	#debug(info)
	# 	table.insertRow('', info['details'])
	# elif selection == 'Clear Table':
	# 	clearDialog(info)


	# elif selection == 'Export Mappings':
	# 	parent.Mapper.par.Exportmappings.pulse()
	# elif selection == 'Import Mappings':
	# 	parent.Mapper.par.Importmappings.pulse()	
	# return	

#_________ General methods ___________

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

def onClick(info):
	if info['ownerComp'].panel.alt:
		menuItems = ['Clear Row', 'Delete Row', 'Add Row', 'Insert Row', 'Clear Table'] #, 'Export Mappings', 'Import Mappings']
		op.TDResources.op('popMenu').Open(
		items=menuItems,
		callback=generalSelection,
		callbackDetails=info['row'],
		disabledItems=[],
		dividersAfterItems=['Delete Row', 'Insert Row'],
		checkedItems=[],
		subMenuItems=[],
		autoClose=True)

def onClickRight(info):  
	data = info.get('rowData', None)
	#if not data:
	name = op(info['rowData']['OP']).name
	menuItems = [f'{name} Parameters', 'Viewer', 'Network', 'Network Inherit', 'Customize Component'] #, 'Export Mappings', 'Import Mappings']
	op.TDResources.op('popMenu').Open(
	items=menuItems,
	callback=onPopMenu,
	callbackDetails=info['rowData']['OP'],
	disabledItems=[],
	dividersAfterItems=['Network Inherit'],
	checkedItems=[],
	subMenuItems=[],
	autoClose=True)

# def PopMenu(info):
# 	path = info
# 	name = op(info).name

# 	if parent.TablePopup.par.Popmenu:
# 		op.TDResources.op('popMenu').Open(
# 			items=[	f'{name} Parameters', 
# 					'Viewer', 
# 					'Network', 
# 					'Network Inherit'
# 					'Customize Component', 

# 					],
# 			dividersAfterItems=[
# 					'Customize Component', 
# 					],
# 			callback=onPopMenu,
# 			callbackDetails=''
# 			)

def onPopMenu(info):
	selection = info['item']
	path = info['details']
	name = op(path).name

	if selection == f'{name} Parameters':
		OpenParameters(op(path))
	elif selection == 'Viewer':
		OpenViewer(op(path))
	elif selection == 'Network':
		OpenNetwork(op(path))
	elif selection == 'Network Inherit':
		NetworkInherit(op(path))
	elif selection == 'Customize Component':
		CustomizeParameters(op(path))


def OpenParameters(comp=''):
	if not comp:
		comp = parent()
	if hasattr(op, 'PARPOPUP'):
		op.PARPOPUP.Open(comp, 
						label=comp.name, 
						header=False, 
						height=750)
	else:
		comp.openParameters()
def OpenNetwork(comp):
	if hasattr(op, 'INSPECTORGADGET'):
		op.INSPECTORGADGET.Opennetwork(op(comp))
	else:
		pane = TDF.showInPane(op(comp))
		pane.showParameters = True

def NetworkInherit(comp):
	debug('inherit')
	ui.panes[0].owner = comp
def OpenViewer(comp=''):
	if not comp:
		comp = parent()
	comp.openViewer()

def CustomizeParameters(comp=''):
	if not comp:
		comp = parent()
	op.TDDialogs.op('CompEditor').EditComp(comp)

def Readme(comp):
	self.OpenViewer(comp)

def Helpgit(url):
	ui.viewFile(url)

#_______ Per cell callbacks ________#

def deleteRow(info):
	if info['button'] == 'OK':
		ui.undo.startBlock(
			'Delete row from table')
		table.deleteRow(info['details']['row'])
		ui.undo.endBlock()
	return	
#_________ Per cell methods _________#

def onClickDelete(info):
	op.TDResources.op('popDialog').Open(
	text='Are you sure you want to delete this row?',
	title='Delete',
	buttons=['OK', 'Cancel'],
	callback=deleteRow,
	details=info,
	textEntry=False,
	escButton=2,
	enterButton=1,
	escOnClickAway=True)	


def onDataChanged(info):
#	debug(info)
	return

def onEditEnd(info):
#	Refresh()

	searchString= parent.SearchReplace.par.Searchstring.eval()
	prevText	= info['prevText']
	cellText	= info['cellText']
	row			= info['row']
	col			= info['col']
	colName		= info['colName']
	opName		= str(table[row, "OP Names"])
	lenStrip	= -(len(opName) + 1)
	OP 			=  str(table[row, "OP"])
	
#	SearchReplace callbacks	
	if colName == 'OP':
		opName = prevText.rsplit('/', 1)[-1]
		print(opName)
		if str(table[row,'OP']).endswith('/'):
			OP = str(table[row,'OP'])[:-1]
		elif str(table[row,'OP']).endswith(opName):
			OP = str(table[row,'OP'])[:lenStrip]
		else:
			OP	= str(table[row, 'OP'])
		try:
			ui.undo.startBlock('change op path')
			if op(OP).valid:	
				pPath		= op(OP).parent().path
				newPath		= f'{OP}/{opName}'
				updateTable(row, col, newPath)

				if pPath != newPath:	
					try:
						
						new = op(OP).copy(op(prevText))
						op(prevText).destroy()
						updateTable(row,col, cellText.rstrip('/') +'/' + new.name)
						
					except:
						debug('Filepath does not exist')
						updateTable(row, col, prevText)
				else:
					debug('same path')
					updateTable(row, col, prevText)
			ui.undo.endBlock()
		except:
			debug('Filepath does not exist')
			updateTable(row, col, prevText)

	elif colName == 'OP Names':
		try:
			newName = tdu.legalName(str(table[row,'OP Names']))
			newPath = f'{op(OP).parent().path}/{newName}'
			updateTable(row, col, newName)
			op(OP).name = newName
			updateTable(row, 'OP', newPath)
		except Exception as e:
			debug(e)
	elif colName == 'Par Page Names':
		prevList = prevText.split(', ')
		list = cellText.split(', ')	
		pageList = op(OP).customPages
		if op(OP).isCOMP:
			for newName in list:
				try:
					if newName in pageList:
						debug('page already exists')
						#updateTable(row, col, prevText)
					elif newName not in pageList:
						if prevList != ['']:
							debug(f'rename {prevList[0]} to {newName}')
							index = pageList.index(prevList[0])
							pageList[index].name = newName
						elif newName not in prevList and newName not in pageList:
							debug(f'append "{newName}" customPage to {op(OP)}')
							op(OP).appendCustomPage(newName)			
				except Exception as e:
					debug(e)
		else:
			debug('this operator is not a valid customPage target')
			updateTable(row, col, prevText)

	elif colName == 'Par Labels':
		prevList = prevText.split(', ')
		list = cellText.split(', ')		
		parList = op(OP).customPars
		# labelList = []
		# for l in parList:
		# 	labelList.append(l.label)
		try:
			for p in parList:
				if p.label in prevList:
					if len(list) == len(prevList):
						newLabel = list[prevList.index(p.label)]
						op(OP).par[p.name].label = newLabel
						debug(f"rename op{OP} par labels[{prevList}] to [{list}]")
					else:
						newLabel = list[0]
						op(OP).par[p.name].label = newLabel
						debug(f"rename op{OP} par labels[{prevList}] to [{list[0]}]")

					updateTable(row, col, cellText)
		except Exception as e:
			debug(e)
			updateTable(row, col, prevText)
#		string = x.capitalize in list

		updateTable(row, col, cellText)
	elif colName == 'Par Names':
		prevList = prevText.split(', ')
		list = cellText.split(', ')		
		capList = [x.capitalize() for x in list]
		nameList = []
		try:
			for p in prevList:
				
				if len(list) == len(prevList):
					newName = capList[prevList.index(p)]
					op(OP).par[p].name = newName
					debug(f"rename op({OP}).par[{p}] to {newName}")
					updateTable(row, col, ", ".join(capList))
					
					print(capList)
		
				else:
					
					newName = capList[0] + str(prevList.index(p)+1)
					nameList.append(newName)
					op(OP).par[p].name = newName
					debug(f"rename op({OP}).par[{p}] to {newName}")
					updateTable(row, col, ", ".join(nameList) )
		except Exception as e:
			debug(e)
			updateTable(row, col, prevText)
	elif colName == 'DAT Text Line #s':
		updateTable(row, col, prevText)
	elif colName == 'Par Data':
		prevList = prevText.split(', ')
		list = cellText.split(', ')	
		p = str(table[row, "Par Data"])
		try:
			for item in prevList:
				if len(prevList) == len(list):
					ui.undo.startBlock('Undo Par Data cell replace')
					op(OP).par[item] = list[prevList.index(item)]
					debug(f"op({OP}).par[{prevList[prevList.index(item)]}].val changed to {list[prevList.index(item)]}")
					updateTable(row, col, prevText)
					ui.undo.endBlock()
				else:
					op(OP).par[item] = list[0]
					debug(f"op({OP}).par[{prevList[prevList.index(item)]}].val changed to {list[0]}")
					updateTable(row, col, prevText)
		except Exception as e:
			debug(e)
			updateTable(row, col, prevText)
	elif colName == 'Par Menu Items':
		prevList = prevText.split(', ')
		list = cellText.split(', ')	
		try:
			for item in prevList:
				ui.undo.startBlock('Undo Par Menu Items cell replace')
				nameList = op(OP).par[item].menuNames
				labelList = op(OP).par[item].menuLabels
				newNames = [sub.replace(searchString, list[0]) for sub in nameList]
				newLabels = [sub.replace(searchString, list[0]) for sub in labelList]
				
				op(OP).par[item].menuNames = newNames
				op(OP).par[item].menuLabels = newLabels
				ui.undo.endBlock()
				debug(f"all instances of '{searchString}' in op({OP}).par[{item}] names and labels replaced with {cellText}")
				
			updateTable(row, col, prevText)
		except Exception as e:
			debug(e)

		updateTable(row, col, prevText)

	elif colName == 'Field Text':

		try:
			ui.undo.startBlock('Undo field text change')
			op(OP).panel.field.val = cellText
			updateTable(row, col, cellText)
			ui.undo.endBlock()
		except Exception as e:
			debug(e)
			updateTable(row, col, prevText)

	return
	
#_________ Sort methods _________ added by drmbt#
# def onSort(info):
# 	input = op('../MappingsList/outList')
# 	output = table
# 	output.text = input.text
	
#_________ Toggle methods _________ added by drmbt#

def onClickInvert(info):
	if table[info['row'], 'Invert'] == 1:
		table[info['row'], 'Invert'] = 0
	elif table[info['row'], 'Invert'] == 0:
		table[info['row'], 'Invert'] = 1
	elif table[info['row'], 'Invert'] == '':
		table[info['row'], 'Invert'] = 1

def onClickToggle(info):
	if table[info['row'], 'Toggle'] == 1:
		table[info['row'], 'Toggle'] = 0
	elif table[info['row'], 'Toggle'] == 0:
		table[info['row'], 'Toggle'] = 1
	elif table[info['row'], 'Toggle'] == '':
		table[info['row'], 'Toggle'] = 1

def onClickActive(info):
	if table[info['row'], 'Active'] == 1:
		table[info['row'], 'Active'] = 0
	elif table[info['row'], 'Active'] == 0:
		table[info['row'], 'Active'] = 1
	elif table[info['row'], 'Active'] == '':
		table[info['row'], 'Active'] = 1
			
def onClickRename(info):
	if table[info['row'], 'Rename'] == 1:
		table[info['row'], 'Rename'] = 0
	elif table[info['row'], 'Rename'] == 0:
		table[info['row'], 'Rename'] = 1
	elif table[info['row'], 'Rename'] == '':
		table[info['row'], 'Rename'] = 1
			
# dragdrop

def onDropHover(info):
	debug(info)
	return True

def onDrop(info):
	print('!!!DROP')
	debug(info)
	print('DROP!!!')
