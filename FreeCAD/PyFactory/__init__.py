PACKAGE_NAME = 'PyFactory'

from collections import OrderedDict
from PyFlow.UI.UIInterfaces import IPackage

# Pins
from PyFlow.Packages.PyFactory.Pins.DemoPin import DemoPin

# Function based nodes
from PyFlow.Packages.PyFactory.FunctionLibraries.DemoLib import DemoLib

# Class based nodes
from PyFlow.Packages.PyFactory.Nodes.DemoNode import DemoNode

# Tools
from PyFlow.Packages.PyFactory.Tools.DemoShelfTool import DemoShelfTool
from PyFlow.Packages.PyFactory.Tools.DemoDockTool import DemoDockTool

# Factories
from PyFlow.Packages.PyFactory.Factories.UIPinFactory import createUIPin
from PyFlow.Packages.PyFactory.Factories.UINodeFactory import createUINode
from PyFlow.Packages.PyFactory.Factories.PinInputWidgetFactory import getInputWidget
# Prefs widgets
from PyFlow.Packages.PyFactory.PrefsWidgets.DemoPrefs import DemoPrefs

_FOO_LIBS = {}
_NODES = {}
_PINS = {}
_TOOLS = OrderedDict()
_PREFS_WIDGETS = OrderedDict()

_FOO_LIBS[DemoLib.__name__] = DemoLib(PACKAGE_NAME)

_NODES[DemoNode.__name__] = DemoNode

_PINS[DemoPin.__name__] = DemoPin

_TOOLS[DemoShelfTool.__name__] = DemoShelfTool
_TOOLS[DemoDockTool.__name__] = DemoDockTool

_PREFS_WIDGETS["Demo"] = DemoPrefs


class PyFactory(IPackage):
	def __init__(self):
		super(PyFactory, self).__init__()

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

