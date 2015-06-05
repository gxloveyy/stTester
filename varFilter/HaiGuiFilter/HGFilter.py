from BaseFilter import BaseFilter

class HGFilter(BaseFilter):
    """report the contract consistent with HG principle"""
    def __init__(self, data_context):
        BaseFilter.__init__(self, data_context)
        self.name = 'HaiGui_20'
        # parameters
        self.days = 20
        return

    def check(self, contract):
        data = self.data_context.fetchContractRecentData(contract, number=self.days + 1)
        today = data[-1]
        close = self.data_context.correctPriceList([d['close'] for d in data])
        if max(close) <= self.data_context.correctPrice(today['close']):
            return True
        return False



