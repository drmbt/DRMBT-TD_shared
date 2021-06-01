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

class ColorPickerUIExt:
	"""
	ColorPickerUIExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

		# properties
		TDF.createProperty(self, 'MyProperty', value=0, dependable=True,
						   readOnly=False)

	def Get(self, **kwargs):
		for arg in kwargs:
			if arg in [p.name for p in self.ownerComp.customPars]:
				getattr(self.ownerComp.par, arg)


	def Set(self, **kwargs):
		for arg in kwargs:
			if arg in [p.name for p in self.ownerComp.customPars]:
				setattr(self.ownerComp.par, arg, kwargs.get(arg))


	def Open(self, **kwargs):
		#debug(kwargs)
		self.Set(**kwargs)
		self.ownerComp.openViewer(unique=False, borders=False)