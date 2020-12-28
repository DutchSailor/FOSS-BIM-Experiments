from PyFlow.Core.Common import *
from PyFlow.Core import FunctionLibraryBase
from PyFlow.Core import IMPLEMENT_NODE


class DemoLib(FunctionLibraryBase):
    '''list functions'''

    def __init__(self, packageName):
        super(DemoLib, self).__init__(packageName)


    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', ""), meta={NodeMeta.CATEGORY: 'List|Read', NodeMeta.KEYWORDS: ['list']})
    def listGetItemAtIndex(list=('AnyPin', ""), index=('IntPin', 0)):
        '''return an item from a given list at the specific index'''
        Result = list[index]
        return Result

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', ""), meta={NodeMeta.CATEGORY: 'List|Read', NodeMeta.KEYWORDS: ['list']})
    def listFirstItem(list=('AnyPin', "")):
        '''return an item from a given list at the specific index'''
        Result = list[0]
        return Result
		
    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', ""), meta={NodeMeta.CATEGORY: 'List|Read', NodeMeta.KEYWORDS: ['list']})
    def listLastItem(list=('AnyPin', "")):
        '''return an item from a given list at the specific index'''
        Result = list[-1]
        return Result

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', ""), meta={NodeMeta.CATEGORY: 'List|Modify', NodeMeta.KEYWORDS: ['list']})
    def listDropFirstItem(list=('AnyPin', "")):
        '''return an item from a given list at the specific index'''
        Result = list.pop[0]
        return Result
		
    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', ""), meta={NodeMeta.CATEGORY: 'List|Modify', NodeMeta.KEYWORDS: ['list']})
    def listDropLastItem(list=('AnyPin', "")):
        '''return an item from a given list at the specific index'''
        Result = list.pop[-1]
        return Result
		
    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', ""), meta={NodeMeta.CATEGORY: 'List|Modify', NodeMeta.KEYWORDS: ['list']})
    def listDropItemAtIndex(list=('AnyPin', ""), index=('IntPin', 0)):
        '''return an item from a given list at the specific index'''
        Result = list.pop[index]
        return Result

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', ""), meta={NodeMeta.CATEGORY: 'List|Modify', NodeMeta.KEYWORDS: ['list']})
    def listAddItemAtStart(list=('AnyPin', ""), item=('AnyPin', "")):
        '''return an item from a given list at the specific index'''
        Result = list.insert(0,item)
        return Result
		
    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', ""), meta={NodeMeta.CATEGORY: 'List|Modify', NodeMeta.KEYWORDS: ['list']})
    def listAddItemAtEnd(list=('AnyPin', ""), item=('AnyPin', "")):
        '''return an item from a given list at the specific index'''
        Result = list.insert(max(list),item)
        return Result

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', ""), meta={NodeMeta.CATEGORY: 'List|Modify', NodeMeta.KEYWORDS: ['list']})
    def listAddItemAtIndex(list=('AnyPin', ""), item=('AnyPin', ""), index=('IntPin', "")):
        '''return an item from a given list at the specific index'''
        Result = list.insert(index,item)
        return Result
			
    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', ""), meta={NodeMeta.CATEGORY: 'List|Read', NodeMeta.KEYWORDS: ['list']})
    def listMaximumItem(list=('AnyPin', "")):
        '''return an item from a given list at the specific index'''
        Result = max(list)
        return Result
		
    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', ""), meta={NodeMeta.CATEGORY: 'List|Read', NodeMeta.KEYWORDS: ['list']})
    def listMinimumItem(list=('AnyPin', "")):
        '''return an item from a given list at the specific index'''
        Result = min(list)
        return Result
		
    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', ""), meta={NodeMeta.CATEGORY: 'Primitives|String', NodeMeta.KEYWORDS: ['string','float']})
    def stringToFloat(string=('StringPin', "")):
        '''return an item from a given list at the specific index'''
        Result = float(string)
        return Result

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', ""), meta={NodeMeta.CATEGORY: 'Primitives|String', NodeMeta.KEYWORDS: ['string','length']})
    def stringLength(string=('StringPin', "")):
        '''return an item from a given list at the specific index'''
        Result = len(string)
        return Result

    @staticmethod
    @IMPLEMENT_NODE(returns=('IntPin', ""), meta={NodeMeta.CATEGORY: 'Webrequest', NodeMeta.KEYWORDS: ['string','length']})
    def openWebbrowser(url=('StringPin', "")):
        '''return an item from a given list at the specific index'''
        import webbrowser
        webbrowser.open_new_tab(url)
        Result = URL
        return Result
