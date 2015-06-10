import sqlite3
import datetime
import re

class dataContext(object):
    """data fetcher for a filter"""
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        #same as daily table define, will be used in select statement and the daily data returned
        self.daily_data_props = ['date',
                                 'last_settlement_price',
                                 'open',
                                 'high',
                                 'low',
                                 'close',
                                 'settlement_price',
                                 'change1',
                                 'change2',
                                 'volume',
                                 'money',
                                 'position']
        pass

    def fetchActiveHotContracts(self):
        '''fetch the hot contracts still in market most recently, return the date and responding contracts name'''
        res_list = []
        day_str = ""
        cur_day = datetime.date.today()
        delta = datetime.timedelta(days=1)
        sql = "select contract, volume from daily where date = ?"
        for i in range(0, 700):
            day_str = cur_day.isoformat().replace("-", "")
            print("checking " + day_str)
            if self.cursor is None:
                break
            self.cursor.execute(sql, (day_str, ))
            results = self.cursor.fetchall()
            if results is not None and len(results) > 0:
                print('got some results:' + day_str)
                con_vol = {con[0]:con[1] for con in results}
                #get the hot contract based on the volume
                max_volume = {}  # ru:17823839
                max_contract = {} # ru:ru201504
                for contract in con_vol.keys():
                    variaty = ''.join([c for c in contract if c > '9'])
                    print('variaty ' + variaty)
                    if variaty not in max_volume:
                        max_volume[variaty] = con_vol[contract]
                        max_contract[variaty] = contract
                    elif max_volume[variaty] < con_vol[contract]:
                        max_volume[variaty] = con_vol[contract]
                        max_contract[variaty] = contract
                res_list = max_contract.values()
                print(max_contract)
                break
            cur_day = cur_day - delta
        return (day_str, res_list)
        
    def correctPriceList(self, prices):
        final_prices = []
        for p in prices:
            if type(p) == type('str'):
                final_prices.append(float(p.replace(',', '')))
            else:
                final_prices.append(p)
        return final_prices
        
    def correctPrice(self, price):
        if type(price) == type('str'):
            return float(price.replace(',', ''))
        return price        

    def fetchContractRecentData(self, contract, number=60):
        '''fetch recent data, return a list, composed of dict
           the first one will be the most recently one.
           [20150521, 20150520,....]'''
        data = []
        if self.cursor is None:
            return data

        sql = "select %s from daily where contract = ?  order by date desc limit ?" % (','.join(self.daily_data_props))
        self.cursor.execute(sql, (contract, number))
        res_list = self.cursor.fetchall()
        data = [ {self.daily_data_props[i]:l[i] for i in range(0, len(self.daily_data_props))} for l in res_list]
        return data
            


