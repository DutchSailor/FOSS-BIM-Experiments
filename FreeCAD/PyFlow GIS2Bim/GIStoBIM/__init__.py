PACKAGE_NAME = 'GIStoBIM'

from collections import OrderedDict
from PyFlow.UI.UIInterfaces import IPackage

# Pins
from PyFlow.Packages.GIStoBIM.Pins.DemoPin import DemoPin

# Function based nodes
from PyFlow.Packages.GIStoBIM.FunctionLibraries.DemoLib import DemoLib

# Class based nodes
from PyFlow.Packages.GIStoBIM.Nodes.DemoNode import DemoNode

# Tools
from PyFlow.Packages.GIStoBIM.Tools.DemoShelfTool import DemoShelfTool
from PyFlow.Packages.GIStoBIM.Tools.DemoDockTool import DemoDockTool

# Exporters
from PyFlow.Packages.GIStoBIM.Exporters.DemoExporter import DemoExporter

# Factories
from PyFlow.Packages.GIStoBIM.Factories.UIPinFactory import createUIPin
from PyFlow.Packages.GIStoBIM.Factories.UINodeFactory import createUINode
from PyFlow.Packages.GIStoBIM.Factories.PinInputWidgetFactory import getInputWidget
# Prefs widgets
from PyFlow.Packages.GIStoBIM.PrefsWidgets.DemoPrefs import DemoPrefs

_FOO_LIBS = {}
_NODES = {}
_PINS = {}
_TOOLS = OrderedDict()
_PREFS_WIDGETS = OrderedDict()
_EXPORTERS = OrderedDict()

_FOO_LIBS[DemoLib.__name__] = DemoLib(PACKAGE_NAME)

_NODES[DemoNode.__name__] = DemoNode

_PINS[DemoPin.__name__] = DemoPin

_TOOLS[DemoShelfTool.__name__] = DemoShelfTool
_TOOLS[DemoDockTool.__name__] = DemoDockTool

_EXPORTERS[DemoExporter.__name__] = DemoExporter

_PREFS_WIDGETS["Demo"] = DemoPrefs


class GIStoBIM(IPackage):
	def __init__(self):
		super(GIStoBIM, self).__init__()

	@staticmethod
	def GetExporters():
		return _EXPORTERS

	@staticmethod
	def GetFunctionLibraries():
		return _FOO_LIBS

	@staticmethod
	def GetNodeClasses():
		return _NODES

	@staticmethod
	def GetPinClasses():
		return _PINS

	@staticmethod
	def GetToolClasses():
		return _TOOLS

	@staticmethod
	def UIPinsFactory():
		return createUIPin

	@staticmethod
	def UINodesFactory():
		return createUINode

	@staticmethod
	def PinsInputWidgetFactory():
		return getInputWidget

	@staticmethod
	def PrefsWidgets():
		return _PREFS_WIDGETS

