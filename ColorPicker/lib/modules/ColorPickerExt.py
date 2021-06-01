"""
Extension classes enhance TouchDesigner components with python. An
extension is accessed via ext.ExtensionClassName from any operator
within the extended component. If the extension is promoted via its
Promote Extension parameter, all its attributes with capitalized names
can be accessed externally, e.g. op('yourComp').PromotedFunction().

Help: search "Extensions" in wiki
"""

from TDStoreTools import StorageManager
import TDFunctions as TDF
import colorsys
import string
class ColorPickerExt:
	"""
	ColorPickerExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.CustomPars = [p.name for p in self.ownerComp.customPars]
		# properties
		TDF.createProperty(self, 'MyProperty', value=0, dependable=True,
						   readOnly=False)


	def Get(self, *args):
		dict = {}
		for arg in args:
			if arg in self.CustomPars:
				dict[arg] = getattr(self.ownerComp.par, arg)
		return dict

	def Set(self, **kwargs):
		for arg in kwargs:
			if arg in self.CustomPars:
				setattr(self.ownerComp.par, arg, kwargs.get(arg))

#	Public parexec_passThru methods

	def Addtopalette(self):
		ownerComp=self.ownerComp
		p = ownerComp.par
		table = self.ownerComp.op('table_colors')
		table.appendRow([
			1,								# pos
			round(p.Colorr.val, 3),			# r
			round(p.Colorg.val, 3),			# g
			round(p.Colorb.val, 3),			# b
			round(p.Alpha.val, 3),	 		# a
			round(p.Huerotate.val, 3),		# h
			round(p.Saturation.val, 3),		# s
			round(p.Value.val, 3)			# v
		])

	def Updateselectedcolor(self):
		ownerComp = self.ownerComp
		p = ownerComp.par
		table = ownerComp.op('table_colors')
		index = p.Selectedcolorindex
		pos = table[index, 'pos'].val
		table.replaceRow(p.Selectedcolorindex,
			[pos, p.Colorr, p.Colorg, p.Colorb, p.Alpha])
			
	def Clearpalette(self):
		table = self.ownerComp.op('table_colors')
		table.clear(keepFirstRow=True)
	
	def Distributerampkeys(self, curve='linear'):
		table = self.ownerComp.op('table_colors')
		if curve == 'linear':
			for r in range(1, table.numRows):
				table[r, 'pos'] = tdu.remap(r, 1, table.numRows-1, 0, 1)

	def calculateHsv(self, r, g, b):
		hsv = colorsys.rgb_to_hsv(r, g, b)
		return hsv

	def calculateRgb(self, h, s, v):
		rgb = colorsys.hsv_to_rgb(h, s, v)
		return rgb

	def Recalculatehsv(self):
		table = self.ownerComp.op('table_colors')
		if not table[0, 'h']: table.appendCol('h')
		if not table[0, 's']: table.appendCol('s')
		if not table[0, 'v']: table.appendCol('v')
			
		for r in range(1, table.numRows):
			hsv = self.calculateHsv(table[r, 'r'], table[r, 'g'], table[r, 'b'],)
			table[r, 'h'] = hsv[0]
			table[r, 's'] = hsv[1]
			table[r, 'v'] = hsv[2]
	
	def Recalculatergb(self):
		table = self.ownerComp.op('table_colors')
		if not table[0, 'r']: table.appendCol('r')
		if not table[0, 'g']: table.appendCol('g')
		if not table[0, 'b']: table.appendCol('b')
		if not table[0, 'a']: table.appendCol('a')
		for r in range(1, table.numRows):
			rgb = self.calculateRgb(table[r, 'h'], table[r, 's'], table[r, 'v'],)
			table[r, 'r'] = rgb[0]
			table[r, 'g'] = rgb[1]
			table[r, 'b'] = rgb[2]
			if table[r, 'a'] == '': table[r, 'a'] = 1
	def Updaterampkeys(self):
		self.Resamplerampkeys(self.ownerComp.op('table_colors').numRows-1)

	def Resamplerampkeys(self, v=''):
		
		ownerComp = self.ownerComp
		if v != '': ownerComp.par.Keys = v
		table = self.ownerComp.op('table_colors')
		rampDat = self.ownerComp.op('chopto1') 
		self.ownerComp.op('ramp1').lock = True
		ui.undo.startBlock('undo resample')
		table.clear(keepFirstRow=True)
		for r in range(0, rampDat.numRows): table.appendRow([c for c in rampDat.row(r)])
		script = f"op('{self.ownerComp.op('ramp1')}').lock = False"
	#	self.Distributerampkeys()
		self.Recalculatehsv()
		run(script, delayFrames=60)
		debug('resample')
		#run(f"op('{switch}').par.index = 0", delayFrames = 120)
		ui.undo.endBlock()

	def SetPushColor(self, r):
		owner = r.owner
		name = r.name
		name = name[:-1]
		ownerComp = self.ownerComp
		try:		
			ownerComp.par.Pushcolorr.expr = f"op('{owner}').par['{name}r']"
			ownerComp.par.Pushcolorg.expr = f"op('{owner}').par['{name}g']"
			ownerComp.par.Pushcolorb.expr = f"op('{owner}').par['{name}b']"
			if hasattr(op(owner).par, f"{name}a"):
				ownerComp.par.Pushcolora.expr = f"op('{owner}').par['{name}a']"
			ownerComp.par.Pushactive = True
		except:
			pass

	def Exportpalette(self, fileName=None):
		Table = self.ownerComp.op('table_colors')
		if fileName == None:
			fileName = ui.chooseFile(load=False, start='local/mappings', 
								fileTypes=['py'], title='Save table as:')
		if fileName:
			Table.save(fileName)
			print(f'{Table} successfully saved as {fileName}')

	def Importpalette(self, fileName=None):
		if fileName == None:
			fileName = ui.chooseFile(load=True, start='local/mappings', 
								fileTypes=['py'], title='Load table:')

		Table = self.ownerComp.op('table_colors')
		Table.par.file = fileName
		Table.par.loadonstartpulse.pulse()
		Table.par.file = ''
		debug(f'{Table} successfully imported from {fileName}')

	def Importlut(self, fileName=None):
		if fileName == None:
			fileName = ui.chooseFile(load=True, start='local/mappings ', 
								title='Load table:')
		if fileName != None:
			ocio = self.ownerComp.op('ocio1')
			switch = self.ownerComp.op('switch_LUT')
			ocio.par.usefiletransform = True
			ocio.par.filesource = fileName
			switch.par.index = 1
		#	run(f"op('{switch}').par.index = 0", delayFrames =520)
			run(self.Resamplerampkeys(), delayFrames =0)
		#	ocio.par.filesource = ''
		#	ocio.par.usefiletransform = False
	
			
		#	debug(f'LUT successfully imported from {fileName}')


	def Openui(self, **kwargs):
		self.ownerComp.op('ColorPickerUI').Open(**kwargs)

	def Generateui(self):
		"""
		Generates a basic UI as a starting point to access IG functions
		"""
		# table = self.ownerComp.op('table_colors')
		# #table.lock = True
		ColorPickerUI = self.ownerComp.parent().copy(self.ownerComp.op('ColorPickerUI'), name='ColorPickerUI', includeDocked=True)
		ColorPickerUI.allowCooking = ColorPickerUI.display = ColorPickerUI.par.display = True
		ColorPickerUI.par.Colorpickercomp.expr = f"op('{self.ownerComp.path}')"
		ColorPickerUI.cook(force=True, recurse=True)

#	Push Color rules


	def Colorr(self, par, val, prev):
		ownerComp = self.ownerComp
		if ownerComp.par.Pushactive:
			r = ownerComp.par.Pushcolorr.expr
			script = f"{r} = {val}"
			run(script)
	def Colorg(self, par, val, prev):
		ownerComp = self.ownerComp
		if ownerComp.par.Pushactive:
			g = ownerComp.par.Pushcolorg.expr
			script = f"{g} = {val}"
			run(script)
	def Colorb(self, par, val, prev):
		ownerComp = self.ownerComp
		if ownerComp.par.Pushactive:
			b = ownerComp.par.Pushcolorb.expr
			script = f"{b} = {val}"
			run(script)
	def Alpha(self, par, val, prev):
		ownerComp = self.ownerComp
		if ownerComp.par.Pushactive:
			a = ownerComp.par.Pushcolora.expr
			try:
				script = f"{a} = {val}"
				run(script)
			except:
				pass