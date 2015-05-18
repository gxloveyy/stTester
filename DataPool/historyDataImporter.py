
####################################################################################################################
#
# Import history data into databases
#
####################################################################################################################

import sqlite3
import csv
import os
import re
import urllib.request
import io
import zipfile
import time

class historyDataImporter(object):
    """Import history data into databases"""
    def __init__(self, db_file = ''):
        self.db_file = db_file
        self.conn = None
        self.cursor = None
        self.contract_re = re.compile("(?P<variaty>[a-zA-Z]*)(?P<date>[0-9]*)")
        self.insert_daily_sql = "insert or replace into daily values (?,?,?,?,?,?,?,?,?,?,?,?,?)"
        pass

    def checkDB(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        if self.cursor is not None:
            # create each table
            tbl_variaty = '''create table if not exists variaty(
                name text, code text, fe text,
                min_price_change real, min_money_change real, size real, ratio real, primary key(code, fe))'''
            tbl_contract = "create table if not exists contract(variaty, contract, primary key(variaty, contract))"
            tbl_daily = '''create table if not exists daily(
                contract text, date text, 
                last_settlement_price real, 
                open real, high real, low real, close real, settlement_price real,
                change1 real, change2 real, volume number, money number, position number,
                primary key(contract, date))'''
            self.cursor.execute(tbl_variaty)
            self.cursor.execute(tbl_contract)
            self.cursor.execute(tbl_daily)
            self.conn.commit()
        pass

    def importContracts(self, fe, variaties, contracts):
        # variaties is [], and contracts is {}, key is the variaty, value is a list of each contracts        
        for var in variaties:
            self.cursor.execute("insert or replace into variaty(code, fe) values(?,?)", (var, fe))
        for var in contracts:
            for con in contracts[var]:
                self.cursor.execute("insert or replace into contract values(?,?)", (var, con))
        self.conn.commit()

    def importSHFE(self, csvF):
        variaties = []
        contracts = {}
        with open(csvF) as hisF:
            reader = csv.reader(hisF, delimiter='\t')
            cur_contract = None
            insert_sql = "insert or replace into daily values (?,?,?,?,?,?,?,?,?,?,?,?,?)"
            for row in reader:
                if row[0] != '' and not (row[0][0] <= '9' and row[0][0] >= '0'):
                    cur_contract = row[0]
                    m = self.contract_re.match(cur_contract)
                    if m is not None:
                        variaty = m.group("variaty")
                        if variaty not in variaties:
                            variaties.append(variaty)
                            contracts[variaty] = []
                        contracts[variaty].append(cur_contract)
                    else:
                        print("An invalid contract in SHFE? %s" % cur_contract)
                self.cursor.execute(self.insert_daily_sql, (cur_contract, row[1], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13]))
            self.conn.commit()
        self.importContracts("shfe", variaties, contracts)

    def importCZCE(self, csvF):
        variaties = []
        contracts = {}
        with open(csvF) as hisF:
            reader = csv.reader(hisF, delimiter='|')
            cur_contract = None
            row_num = 0
            for row in reader:
                if row_num < 2:
                    row_num = row_num + 1
                    continue
                row = [f.strip(" \t") for f in row]
                if len(row) <= 14:
                    print("invalid row in CZCE: %s" % "|".join(row))
                    continue
                cur_contract = row[1]
                m = self.contract_re.match(cur_contract)
                if m is not None:
                    variaty = m.group("variaty")
                    if variaty not in variaties:
                        variaties.append(variaty)
                        contracts[variaty] = []
                    contracts[variaty].append(cur_contract)
                else:
                    print("An invalid contract in CZCE? %s" % cur_contract)
                self.cursor.execute(self.insert_daily_sql, (cur_contract, row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[13], row[11]))
            self.conn.commit()
        self.importContracts("czce", variaties, contracts)

    def importDCE(self):
        '''analyzing from http://www.dce.com.cn/portal/cate?cid=1277712956100 '''
        variaties = ('a', 'b', 'c','m', 'y', 'l', 'p', 'v', 'j', 'jd', 'jm', 'i', 'fb', 'bb', 'pp', 'cs')
        years = range(2006, 2015)
        contracts = {}
        download_url = "http://www.dce.com.cn/portal/uploadFiles/lssj/%d/%s.zip"
        for y in years:
            for var in variaties:
                time.sleep(5)
                cur_url = download_url % (y, var)
                try:
                    response  = urllib.request.urlopen(cur_url)
                    data = response.read()
                    buffer = io.BytesIO(data)
                    zf = zipfile.ZipFile(buffer)
                    for f in zf.namelist():
                        row_num = 0
                        with zf.open(f, "r") as csvF:
                            con = csvF.read()
                            reader = csv.reader(io.StringIO(str(con, encoding='gb2312')), delimiter=",")
                            for row in reader:
                                if row_num < 1:
                                    row_num = row_num + 1
                                    continue
                                row = [f.strip("\"") for f in row]
                                cur_contract = row[1]
                                m = self.contract_re.match(cur_contract)
                                if m is not None:
                                    variaty = m.group("variaty")
                                    if variaty not in variaties:
                                        variaties.append(variaty)
                                    if variaty not in contracts:
                                        contracts[variaty] = []
                                    contracts[variaty].append(cur_contract)
                                else:
                                    print("An invalid contract in DCE? %s" % cur_contract)
                                self.cursor.execute(self.insert_daily_sql, (cur_contract, row[2], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14]))
                            self.conn.commit()
                except urllib.error.HTTPError:
                    # some variaty may does not exist in some year, this is normal
                    print("Error while handle %s" % cur_url)
        self.importContracts("dce", variaties, contracts)

    def importHisData(self, sh_dir='', zz_dir=''):
        self.checkDB()
        # for ShangHai Future Exchange
        files = os.listdir(sh_dir)
        files.sort()
        for f in files:
            self.importSHFE("%s/%s" % (sh_dir, f))
        # for Zhengzhou Future Exchange
        files = os.listdir(zz_dir)
        files.sort()
        for f in files:
            self.importCZCE("%s/%s" % (zz_dir, f))
        # for DaLian Futrue Exchange
        self.importDCE()




