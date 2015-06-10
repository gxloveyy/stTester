from BaseFilter import BaseFilter

class Volume_Filter(BaseFilter):
    def __init__(self, data_context):
        BaseFilter.__init__(self, data_context)
        self.threshold = 1.5
        self.name = 'Volume_change_1.5'
    
    def check(self, contract):
        data = self.data_context.fetchContractRecentData(contract, number=2)
        if len(data) < 2:
            return ('none', 0)
        volumes = self.data_context.correctPriceList([d['volume'] for d in data])
        closes = self.data_context.correctPriceList([d['close'] for d in data])
        if volumes[1] == 0 or volumes[0] == 0:
            return ('none', 0)
        ratio = volumes[1] / volumes[0]
        if ratio >= self.threshold and closes[1] > closes[0]:
            return ('buy', ratio*10)
        if ratio >= self.threshold and closes[1] < closes[0]:
            return ('sell', ratio*10)
        return ('none', 0)
        