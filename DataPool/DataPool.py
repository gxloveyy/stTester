
#############################################################################################################################
#
# Provide an interface to get the information about data. Currently only Future is supported.
# Including: query each kind of Future, query the contract of each Future, query the current active contract,
#   query daily infomation about each contract,
#   and provide a virtual long-hot contract.
#
#############################################################################################################################



class FutureDataManager:
    def __init__(self):
        pass

    def allVariaties(self):
        pass

    def allContracts(self, variaty):
        pass

    def allActiveContracts(self, variaty):
        '''return a list of contract name, like: SR1509, SR1601'''
        pass

    def contractDaily(self, contract):
        '''return a dict, {'20150401':{'open':xxx, 'close':xxx, xxx}, xxx}'''
        pass

    def hotContractDaily(self, variaty):
        '''return a dict like contractDaily'''
        pass

