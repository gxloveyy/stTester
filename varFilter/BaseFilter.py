###############################################################################################
# base class for future filter
###############################################################################################
class BaseFilter():
    def __init__(self, data_context):
        self.data_context = data_context
        self.name = 'base'
        pass

    def check(self, contract):
        # True means this contract is qualified today
        return False
