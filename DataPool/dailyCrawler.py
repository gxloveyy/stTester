
####################################################################################################################
#
# Crawle daily informatin from each Futrues Exchange-s
#
####################################################################################################################

import datetime
import urllib.request
import json
import csv
import sqlite3
import re
import io

class dailyCrawler(object):
    """description of class"""
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
        if self.conn is not None:
            self.cursor = self.conn.cursor()
        self.isOK = self.conn is not None
        self.insert_daily_sql = "insert or replace into daily values (?,?,?,?,?,?,?,?,?,?,?,?,?)"

    def ready(self):
        return self.isOK

    def fetchUrlContent(self, base_url, encoding="utf-8"):
        cur_day = datetime.date.today()
        day_str = ""
        str_con = None
        delta = datetime.timedelta(days=1)
        for i in range(0, 7):
            try:
                day_str = cur_day.isoformat().replace("-", "")
                url = base_url % day_str
                url_con = urllib.request.urlopen(url).read()
                str_con = str(url_con, encoding=encoding)
                break
            except urllib.error.HTTPError:
                print("No content for %s" % cur_day)
                cur_day = cur_day - delta
                continue
        return day_str, str_con

    def fetchCZCE(self):
        day_str, str_con = self.fetchUrlContent("http://www.czce.com.cn/portal/exchange/%d/datadaily" % datetime.date.today().year + "/%s.txt",
                                                encoding="gb2312")
        if str_con is None:
            print("Can not fetch content for CSCE")
            return
        got = 0
        csv_f = csv.reader(io.StringIO(str_con), delimiter=",")
        if csv_f is not None:
            for row in csv_f:
                if len(row) >= 14 and re.match("[a-zA-Z0-9]+", row[0]):
                    got = got + 1
                    self.cursor.execute(self.insert_daily_sql, (row[0], day_str, row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[12], row[10]))
            self.conn.commit()
        if got == 0:
            print("Can not fetch data for CACE")
        pass

    def fetchDCE(self):
        pass

    def fetchSHFE(self):
        day_str, str_con = self.fetchUrlContent("http://www.shfe.com.cn/data/dailydata/kx/kx%s.dat?isAjax=true")
        if str_con is None:
            print("Can not fetch content for SHFE")
            return
        v = json.loads(str_con)
        if "o_curinstrument" in v:
            vs = v["o_curinstrument"]
            # vs is a list
            for var in vs:
                # var is a dict
                variaty = var['PRODUCTID'].strip()
                if variaty.endswith("_f"):
                    variaty = variaty[:-2]
                if re.match("[\d]+", var['DELIVERYMONTH']):
                    self.cursor.execute(self.insert_daily_sql, (variaty + var['DELIVERYMONTH'], day_str, 
                                                                var['PRESETTLEMENTPRICE'],
                                                                var['OPENPRICE'], var['HIGHESTPRICE'], var['LOWESTPRICE'], var['CLOSEPRICE'], var['SETTLEMENTPRICE'], var['ZD1_CHG'], var['ZD2_CHG'],
                                                                var['VOLUME'], '0', var['VOLUME']))
                # check if variaty or contract is not in database
                #
            self.conn.commit()
        else:
            print("website contect changed for SHFE")
        pass
