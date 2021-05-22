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
import webbrowser
class SearchReplaceUIExt:
	"""
	SearchReplaceUIExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def OpenViewer(self, comp=''):
		"""Takes an argument to open a floating viewer"""
		if not comp:
			comp = self.ownerComp
		comp.openViewer()

	def Readme(self):
		"""Pulse to open a floating Readme document"""
		self.OpenViewer(self.ownerComp.op('code/readme'))
		debug('readme')
	def Support(self):
		webbrowser.open('https://drmbt.com/projects/about/')

	def Git(self):
		"""Open git repo"""
		webbrowser.open(self.ownerComp.par.Github.val)

	def Helpgit(self):
		"""Pulse to open a floating network"""
		ui.viewFile(self.ownerComp.par.Helpurl)

	def Help(self):
		"""print python class help"""
		print(help(self))
