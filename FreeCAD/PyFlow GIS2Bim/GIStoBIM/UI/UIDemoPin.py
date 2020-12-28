from PyFlow.Packages.GIStoBIM import PACKAGE_NAME
from PyFlow.UI.Canvas.UIPinBase import UIPinBase


class UIDemoPin(UIPinBase):
    def __init__(self, owningNode, raw_pin):
        super(UIDemoPin, self).__init__(owningNode, raw_pin)
