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
import glob
import string
import shutil
import subprocess
import importlib
import webbrowser
from zipfile import ZipFile
import tempfile
import sys

class BrowserExt:
	"""
	BROWSER is a file explorer for TouchDesigner, with a number of features 
	designed to speed up working with external files and folders on your disk.
	
	Quick Access folders are defined and accessed via a treeLister. When an item
	is selected, it is loaded into the sys/quiet folder, where a low res icon
	representation is generated and supplied as a background top to the treeListers
	icon column. Quiet loaded files are not persistent in Touchdesigner, so they won't
	be saved to your project by default. If desired, the optional export/import
	cache options will allow one to maintain a persistent library of thumbnails
	local to your project.

	Delete functionality is enhanced with the send2trash 3rd party python library,
	which is loaded on demand using a fork of Alpha Moonbase's TD-PIP tool. 
	This means that instead of relying on os.remove() to hard erase files from 
	the disk on delete, they are instead sent to the trash/recycle bin, with 
	a pop up confirmation. This is still a dangerous feature, since it allows 
	TD to erase files external to the program, so use with caution.
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		#self.InitDependancy()
		self.python_exec = app.binFolder + '/python.exe'	
		self.local_lib_path = ''
		self.init_local_library()
		self.install_pip()		

	@property
	def FolderList(self):
		'''list of folders we're lookin' at '''
		list = [i for i in self.ownerComp.op('table_folders').col('path')[1:]]
		return list

	@property
	def Quiet(self):
		'''reference to derivative's sys/quiet folder'''
		return op('/sys/quiet')
	@property
	def tmpViewer(self):
		'''our opview for these temp files'''
		return self.ownerComp.op('tmp_viewer').par.Previewop.eval()
	@property
	def QuickBrown(self):
		'''a quickbrown statement for previewing fonts'''
		return 'sphinx of black quartz, judge my vow\nSPHINX OF BLACK QUARTZ, JUDGE MY VOW'

	@tmpViewer.setter
	def tmpViewer(self, v):
		self.ownerComp.op('tmp_viewer').par.Previewop = v

	'''fork of td-pip methods from Alphamoonbase https://olib.amb-service.net/'''

	def InstallPackage(self, package):
		try:
			subprocess.check_call([self.python_exec, "-m", "pip", "install", package, "--target", "{}".format(self.local_lib_path.replace('\\', '/'))])
		except: 
			return False
		
		return True

	def TestPackage(self, package, silent = False):
		try:
			importlib.import_module(package)
		except:
			if not silent: ui.messageBox('Does not exist', 'The package is not installed')
			return False
			
		if not silent: ui.messageBox('Does exist', 'The package is installed')
		return True

	def Import_Module(self, module, pip_name = ''):
		if not pip_name: pip_name = module
		if not self.TestPackage(module, silent = True): 
			if not self.InstallPackage(pip_name):
				return False
			
		return importlib.import_module(module)

	def init_local_library(self):
		os.makedirs('lib/pip', exist_ok = True)
		self.local_lib_path = os.path.abspath('lib/pip')
		if self.local_lib_path in sys.path: 
			debug( "Local lib already in paths" )
			return
		sys.path.append(self.local_lib_path)
		os.environ['PYTHONPATH'] = self.local_lib_path
		debug( "Local lib initialized" )
	
	def install_pip(self):
		if self.TestPackage('pip', silent = True): 
			debug( "PIP already installed" )
			return
			
		with tempfile.TemporaryDirectory() as temp_dir:
			pip_zip = self.ownerComp.op('virtualFile').vfs.export(temp_dir)[0]
			try:
				os.makedirs(self.local_lib_path + '/pip')
			except:
				ui.messageBox( 'No Privilege', 'Please Restart TouchDesigner with Administrator privileges. Cannot install PIP' )
				return
			
			with ZipFile(pip_zip, 'r') as zip_file:
				zip_file.extractall(path = self.local_lib_path)

#	end td-pip

#	Browser Methods

	def Initfolderlist(self):
		'''comment out or add rows to customize initial folder paths'''
		table = self.ownerComp.op('table_folders')
		
		initList = [
			['name'		, 'path'],
			['project'	, f"{project.folder}"],
			['desktop'	, f"{app.desktopFolder}"],
			['downloads', f"{str(app.desktopFolder).replace('Desktop', 'Downloads')}"],
			['samples'	, f"{app.samplesFolder}"],
			['palette'	, f"{app.samplesFolder}/Palette"],
			['user palette'	, f"{app.userPaletteFolder}"]
					]
		table.clear()
		for item in initList:
			table.appendRow(item)


		return

	def Openbrowser(self):
		'''pop up a window of BROWSER '''
		self.ownerComp.openViewer()

	def Refreshfolder(self):
		'''call to refresh the folderDAT'''
		self.ownerComp.op('folder').par.refreshpulse.pulse()

	def Refreshfilelister(self):
		'''call to refresh the treeLister'''
		print('refresh files')
		self.ownerComp.op('treeLister_files').Refresh()
		self.ownerComp.op('treeLister_files').Refresh()
	
	def Refreshicons(self):
		'''call to quietLoad treeLister selections'''
		for item in self.GetDragItems():
			try:
				self.ParseType(item[0])
			except:
				pass

	def Addfolder(self, path=''):
		'''Add folder to quick select folder list '''
		table = self.ownerComp.op('table_folders')
		if path !='':
			self.ownerComp.par.Folder = path
		if path == '':
			path = tdu.collapsePath(self.ownerComp.par.Folder)
		if path == '':
			path = tdu.collapsePath(ui.chooseFolder(title='Select Folder', start=project.folder))
		if path != 'None':
			self.ownerComp.par.Folder = path
			name = path.split('/')[-1:][0]
			table.appendRow([name, path])

		self.ownerComp.par.Folder == ''

	def Removefolder(self, path=''):
		'''remove folder from quick select folder list'''
		table = self.ownerComp.op('table_folders')
		if path !='':
			self.ownerComp.par.Folder = path
		path = self.ownerComp.par.Folder 

		if self.ownerComp.par.Folder in self.FolderList:
			op(table).deleteRow(table.findCell(path, cols=['path']).row)

		return
	def Open(self, filePath=''):
		'''python method for opening a file from the browser '''
		ownerComp = self.ownerComp
		FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
		if filePath !='':
			ownerComp.par.File = filePath
		if filePath == '':
			filePath = self.ownerComp.par.File
		if filePath == '':
			filePath = ui.chooseFolder(title='Select Folder', start=project.folder)
		filePath = os.path.normpath(str(filePath))
		if os.path.isfile(filePath):
			subprocess.run([FILEBROWSER_PATH, '/select,', str(filePath)])
			os.system(filePath)
			
	def Openexplorer(self, filePath=''):
		'''python method to open path in windows file explorer '''
		ownerComp = self.ownerComp
		FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
		if filePath !='':
			ownerComp.par.File = filePath
		if filePath == '':
			filePath = self.ownerComp.par.File
		if filePath == '':
			filePath = ui.chooseFolder(title='Select Folder', start=project.folder)
		filePath = os.path.normpath(str(filePath))
		if os.path.isdir(filePath):
			subprocess.run([FILEBROWSER_PATH, str(filePath)])
		elif os.path.isfile(filePath):
			subprocess.run([FILEBROWSER_PATH, '/select,', str(filePath)])
	
	def DeleteDialog(self):
		'''confirmation dialog for send2trash'''
		op.TDResources.op('popDialog').Open(
		text=f'send selected items to the \nRecycle Bin?',
		title='Delete Files',
		buttons=['Delete', 'Cancel'],
		callback=self.DeleteFiles,
		textEntry=False,
		escButton=2,
		enterButton=1,
		escOnClickAway=True)
	
	def DeleteFiles(self, info):
		''' send2trash callback '''
		if info['button'] == 'Delete':
			send2trash = self.Import_Module('send2trash')
			for r in range (0, len(self.SelectedRowObjects())):
				filePath = self.SelectedRowObjects()[r]['path']
				format = os.path.abspath(filePath)	
				try:
					send2trash.send2trash(format)
					print(f"moved to recycle bin: {format}")
				except:
					debug(f"error deleting {format}")
					pass
		self.Refreshfolder()

#	quiet folder methods
	def LoadQuietTox(self, path):
		'''rules for quiet loading files with .tox extension '''
		filebase, fileext = os.path.splitext(path)
		name =  tdu.legalName(filebase.split('/')[-1:][0])

		if name not in [n.name for n in self.Quiet.findChildren(depth=1)]:
			tmp = self.Quiet.loadTox(path)
			self.tmpViewer = f"{tmp.path}/icon"
			tmp.nodeY = len(self.Quiet.findChildren(depth=1)) *100
		try:
			self.tmpViewer = self.Quiet.op(name).op('icon').path
		except:
			self.tmpViewer = ''
			pass

	def LoadQuietMovie(self, path):
		'''rules for quiet loading files with legal movie extensions '''
		filebase, fileext = os.path.splitext(path)
		name =  tdu.legalName(filebase.split('/')[-1:][0])

		if name not in [n.name for n in self.Quiet.findChildren(depth=1)]:
			tmp = self.Quiet.create(moviefileinTOP, name)
			p = tmp.par
			p.play = False
			p.outputresolution = 'limit'

			p.resolutionw = 512
			p.resolutionh = 288
			p.trim = True
			p.tendunit = 'frames'
			p.tend = 1
			p.outputaspect = 'useinput'
			p.file = path	
			p.updateimage = True
			p.alwaysloadinitial = True
			tmp.nodeY = len(self.Quiet.findChildren(depth=1)) *100
		self.tmpViewer = f"{self.Quiet.path}/{name}"
	
	def LoadQuietPoints(self, path):
		'''rules for quiet loading files with legal pointdata extensions '''
		filebase, fileext = os.path.splitext(path)
		name =  tdu.legalName(filebase.split('/')[-1:][0])

		if name not in [n.name for n in self.Quiet.findChildren(depth=1)]:
			tmp = self.Quiet.create(pointfileinTOP, name)
			p = tmp.par
			p.outputresolution = 'limit'
			p.resolutionw = 512
			p.resolutionh = 288
			p.outputaspect = 'useinput'
			p.file = path	
			p.reloadpulse.pulse()
			tmp.nodeY = len(self.Quiet.findChildren(depth=1)) *100
		self.tmpViewer = f"{self.Quiet.path}/{name}"

	def LoadQuietSubstance(self, path):
		'''rules for quiet loading files with legal substance extensions '''
		filebase, fileext = os.path.splitext(path)
		name =  tdu.legalName(filebase.split('/')[-1:][0])
		if name not in [n.name for n in self.Quiet.findChildren(depth=1)]:
			tmp = self.Quiet.create(substanceTOP, name)
			p = tmp.par
			p.outputresolution = 'limit'
			p.resolutionw = 512
			p.resolutionh = 512
			p.outputaspect = 'useinput'
			p.file = path	
			p.reloadconfig.pulse()
			tmp.nodeY = len(self.Quiet.findChildren(depth=1)) *100
		self.tmpViewer = f"{self.Quiet.path}/{name}"

	def LoadQuietObject(self, path):
		'''rules for quiet loading geometry filetypes'''
		filebase, fileext = os.path.splitext(path)
		name =  tdu.legalName(filebase.split('/')[-1:][0])
		if name not in [n.name for n in self.Quiet.findChildren(depth=1)]:

			if fileext == '.fbx':
				tmp = self.Quiet.create(fbxCOMP, name)
				tmp.par.file = path
				tmp.par.imp.pulse()
				tmp.allowCooking=False
				tmp.nodeY = len(self.Quiet.findChildren(depth=1)) *100
				tmp.resetViewer(recurse=True)
			if fileext == '.usda' or fileext == '.usd':
				tmp = self.Quiet.create(usdCOMP, name)
				tmp.par.file = path
				tmp.par.imp.pulse()
				tmp.allowCooking=False
				tmp.nodeY = len(self.Quiet.findChildren(depth=1)) *100
				tmp.resetViewer(recurse=True)
			elif fileext == '.abc':
				tmp = self.Quiet.create(alembicSOP, name)
				tmp.par.file = path
				tmp.nodeY = len(self.Quiet.findChildren(depth=1)) *100
				tmp.resetViewer(recurse=True)
			else:
				debug(path)
				tmp = self.Quiet.create(fileinSOP, name)
				tmp.par.file = path
				tmp.par.refreshpulse.pulse()
				#tmp.allowCooking=False
				tmp.nodeY = len(self.Quiet.findChildren(depth=1)) *100
				tmp.resetViewer(recurse=True)
		self.tmpViewer = f"{self.Quiet.path}/{name}"
		self.Quiet.op(name).resetViewer(recurse=True)

	def LoadQuietChannel(self, path):
		'''rules for quiet loading files with audio extensions '''
		filebase, fileext = os.path.splitext(path)
		name =  tdu.legalName(filebase.split('/')[-1:][0])
		if name not in [n.name for n in self.Quiet.findChildren(depth=1)]:
			tmp = self.Quiet.create(fileinCHOP, name)
			p = tmp.par
			p.file = path
			tmp.nodeY = len(self.Quiet.findChildren(depth=1)) *100
		self.tmpViewer = f"{self.Quiet.path}/{name}"

	def LoadQuietMidi(self, path):
		'''rules for quiet loading files with MIDI extensions '''
		filebase, fileext = os.path.splitext(path)
		name =  tdu.legalName(filebase.split('/')[-1:][0])
		if name not in [n.name for n in self.Quiet.findChildren(depth=1)]:
			tmp = self.Quiet.create(midiinCHOP, name)
			p = tmp.par
			p.source = 'file'
			p.file = path
			tmp.nodeY = len(self.Quiet.findChildren(depth=1)) *100
		self.tmpViewer = f"{self.Quiet.path}/{name}"
		
	def LoadQuietText(self, path):
		'''rules for quiet loading text file extensions'''
		filebase, fileext = os.path.splitext(path)
		name =  tdu.legalName(filebase.split('/')[-1:][0])

		if name not in [n.name for n in self.Quiet.findChildren(depth=1)]:
			tmp = self.Quiet.create(textDAT, name)
			p = tmp.par
			p.file = path
			p.loadonstartpulse.pulse()
			tmp.nodeY = len(self.Quiet.findChildren(depth=1)) *100
		self.tmpViewer = f"{self.Quiet.path}/{name}"
	def LoadQuietFont(self, path):
		'''rules for quiet loading font previews '''
		filebase, fileext = os.path.splitext(path)
		name =  tdu.legalName(filebase.split('/')[-1:][0])

		if name not in [n.name for n in self.Quiet.findChildren(depth=1)]:
			tmp = self.Quiet.create(textTOP, name)
			p = tmp.par
			tmp.nodeY = len(self.Quiet.findChildren(depth=1)) *100
			p.outputresolution = 'custom'
			p.resolutionw = 512
			p.resolutionh = 288
			p.wordwrap = True
			p.text = self.QuickBrown
			p.fontsizex = 24
			p.fontfile = path
		self.tmpViewer = f"{self.Quiet.path}/{name}"
		return name

	def Openquietfolder(self):
		'''Open a network pane to see the sys/quiet folder'''
		pane = TDF.showInPane(self.Quiet, inside=True)
		pane.showParameters = False

	def Clearquietfolder(self):
		'''clear the sys/quiet folder '''
		for child in op('/sys/quiet').findChildren(depth=1):
			child.destroy()

#	cache methods

	def Clearcachefolder(self):
		'''clear the local cache icon file directory'''
		filepath = tdu.expandPath(self.ownerComp.par.Localcachefolder)

		folder = filepath
		for filename in os.listdir(folder):
			file_path = os.path.join(folder, filename)
			try:
				if os.path.isfile(file_path) or os.path.islink(file_path):
					os.unlink(file_path)
				elif os.path.isdir(file_path):
					shutil.rmtree(file_path)
			except Exception as e:
				print('Failed to delete %s. Reason: %s' % (file_path, e))

	def Importcache(self):
		'''load the icon files from the local cache '''
		os.makedirs(self.ownerComp.par.Localcachefolder.eval(), exist_ok = True)
		folder = tdu.expandPath(self.ownerComp.par.Localcachefolder)
		for filename in os.listdir(folder):
			filebase, fileext = os.path.splitext(filename)
			name =  tdu.legalName(filebase.split('/')[-1:][0])
			if name not in [n.name for n in self.Quiet.findChildren(depth=1)]:
				tmp = self.Quiet.create(moviefileinTOP, name)
				p = tmp.par
				p.play = False
				p.file.mode = ParMode.CONSTANT
				p.file = F"{folder}/{filename}"	
				tmp.allowCooking = True
				p.reloadpulse.pulse()
				tmp.nodeY = len(self.Quiet.findChildren(depth=1)) *1000

	def Exportquietcache(self):
		'''export currently loaded quiet folder icons to the local cache folder'''
		os.makedirs(self.ownerComp.par.Localcachefolder.eval(), exist_ok = True)
		filepath = tdu.expandPath(self.ownerComp.par.Localcachefolder)
		i = 0
		cacheList = []
		
		for filename in os.listdir(filepath):
			cacheList.append(filename.split('.')[0])
		
		for image in self.Quiet.findChildren(depth=1, type=TOP):
			if image not in cacheList:
				i = i +1
				print(image)
				pathStr = f"{filepath}/{image.name}.jpg"
				script = f"op('{image}').save('{filepath}/{image.name}.jpg', asynchronous=True, createFolders=True, quality=.3)"
				try:
					run(script, delayFrames = i)
				except:
					debug(image)	
		debug('quiet cache exported')

#	main parsing methods	
	def ParseType(self, path):
		# based on Greg's approach to testing moviefilein validity
		filebase, fileext = os.path.splitext(path)
		name =  tdu.legalName(filebase.split('/')[-1:][0])
		if len(fileext) == 0 :
			return False	
		else :
			fileext2 = fileext[1:]
			if fileext == '.tox':
				self.LoadQuietTox(path)
			elif fileext2.lower() in tdu.fileTypes['movie']:
				self.LoadQuietMovie(path)
			elif fileext2.lower() in tdu.fileTypes['image']:
				self.LoadQuietMovie(path)
			elif fileext2.lower() in tdu.fileTypes['pointdata']:
				self.LoadQuietPoints(path)
			elif fileext == '.sbsar':
				self.LoadQuietSubstance(path)
			elif fileext2.lower() in tdu.fileTypes['object'] or fileext2.lower() in tdu.fileTypes['geometry'] or fileext == '.geo':		
				self.LoadQuietObject(path)
			elif fileext2.lower() in tdu.fileTypes['channel'] or fileext2.lower() in tdu.fileTypes['audio']:
				self.LoadQuietChannel(path)
			elif fileext2.lower() in tdu.fileTypes['text'] or fileext == '.rst':
				self.LoadQuietText(path)
			elif fileext== '.midi':
				self.LoadQuietMidi(path)
			elif fileext == '.ttf' or  fileext == '.otf' or  fileext == '.woff':
				self.LoadQuietFont(path)
		return [filebase, name, fileext]

	def PlaceExternalOperators(self, dragItems):
		tmpList = []
		for item in dragItems:
			#debug(item[0])
			file 	= []
			name 	= []
			tmp = self.ownerComp.op('tmpPlace').copy(op(item[3]))
			# type specific op formatting rules
			if tmp.type == 'moviefilein':
				p = tmp.par
				p.outputresolution = 'input'
				
				p.tendunit = 'fraction'
				p.tend = 1
				p.trim = False
				p.outputaspect = 'useinput'
				p.file = f"{item[0]}{item[2]}"
				p.reloadpulse.pulse()
			''' 
			todo: figure out audio file placement as audiofile and not fileCHOP.
			fileCHOP is desirable to see waveform in quiet preview. too much trouble?
			'''

			# elif tmp.type == 'filein' and tmp.family == 'CHOP':
			# 	debug('chop')
			# 	file.append(op(tmp).par.file)
			# 	name.append(tmp.name)
			# 	debug(file[0])
			# 	debug(name[0])
			# 	tmp.destroy()
			# 	newTmp = self.ownerComp.op('tmpPlace').create(audiofileinCHOP, name[0])
			# 	newTmp.par.file = file[0]
				
			item.append(tmp)
			tmpList.append(tmp)		
		placeOps = ui.panes.current.placeOPs(tmpList)
		for x in tmpList:
			op(ui.panes.current.owner).op(x).viewer = True

	def SelectedRowObjects(self):
		ownerComp = self.ownerComp
		rO = ownerComp.op('treeLister_files/lister').SelectedRowObjects
		return rO

##	region callbacks

#	dragdrop	
	def GetDragItems(self):
		ownerComp = self.ownerComp
		rO = self.SelectedRowObjects()
		dragItems =  []
		for r in rO:
			parse = self.ParseType(r['path'])
			dragItems.append(parse)
			
		return dragItems

	def DragItemQuietFormat(self):
		dragItems = self.GetDragItems()
		for i in dragItems:
			i.append(f"/sys/quiet/{i[1]}")
		return dragItems
		
	def OnDragEnd(self, info):
		dragItems = self.DragItemQuietFormat()
		self.PlaceExternalOperators([dragItems][0])
		
# 	parexec_passThru callbacks
	def onParValueChange(self, par, prev):
		"""panelexec_passThru value change callbacks to condense logic to ext"""
		if par.name == 'Test':
			debug('Test')
	def onParPulse(self, par):
		"""panelexec_passThru pulse callbacks to condense logic to ext"""
		ownerComp = self.ownerComp
		name = par.name
		if name == 'Help':
			print(help(self))
		elif name == 'Readme':
			self.ownerComp.op('readme').openViewer()
		elif name == 'Support':
			webbrowser.open('https://drmbt.com/projects/about/')
		else: 
			try:
				getattr(ownerComp, par.name)()
			except Exception as e:
				debug(e)

#	datexec_passThru callbacks
	def onTableChange(self, dat):
		ownerComp = self.ownerComp
		if dat.numRows > 1:
			path = dat[1, 'path']
			if ownerComp.par.Clearquietonselect:
				self.Clearquietfolder()
			self.ParseType(path.val)

## 	end region
