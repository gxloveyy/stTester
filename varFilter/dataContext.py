import sqlite3
import datetime

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

    def fetchActiveContracts(self):
        '''fetch the contracts still in market most recently, return the date and responding contracts name'''
        res_list = []
        day_str = ""
        cur_day = datetime.date.today()
        delta = datetime.timedelta(days=1)
        sql = "select contract from daily where date = ?"
        for i in range(0, 700):
            day_str = cur_day.isoformat().replace("-", "")
            if self.cursor is None:
                break
            self.cursor.execute(sql, (day_str, ))
            res_list = self.cursor.fetchall()
            if res_list is not None and len(res_list) > 0:
                res_list = [con[0] for con in res_list]
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
            


