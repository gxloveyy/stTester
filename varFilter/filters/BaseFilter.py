###############################################################################################
# base class for future filter
###############################################################################################
class BaseFilter():
    def __init__(self, data_context):
        self.data_context = data_context
        self.name = 'base'
        pass

    def check(self, contract):
        # True means this contract is qualified today. Return buy/sell and the index value(100 means strongy recommended, 0 means very weak
        # if this contract is not qualified, then return 'none' for the first one of result
        return ('none', 0)
