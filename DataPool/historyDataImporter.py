
####################################################################################################################
#
# Import history data into databases
#
####################################################################################################################

import sqlite3
import csv
import os
import re

class historyDataImporter(object):
    """Import history data into databases"""
    def __init__(self, db_file = ''):
        self.db_file = db_file
        self.conn = None
        self.cursor = None
        self.variaties = {}
        self.contracts = {}
        self.contract_re = re.compile("(?P<variaty>[a-zA-Z]*)(?P<date>[0-9]*)")
        pass

    def checkDB(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        if self.cursor is not None:
            # create each table
            tbl_variaty = '''create table if not exists variaty(
                id number, name text, code text, fe text,
                min_price_change real, min_money_change real, size real, ratio real)'''
            tbl_contract = "create table if not exists contract(name text, variaty)"
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

    def importSHFE(self, csvF):
        self.variaties["shfe"] = []
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
                        if variaty not in self.variaties["shfe"]:
                            self.variaties["shfe"].append(variaty)
                            self.contracts[variaty] = []
                        self.contracts[variaty].append(cur_contract)
                    else:
                        print("An invalid contract in SHFE? %s" % cur_contract)
                self.cursor.execute(insert_sql, (cur_contract, row[1], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13]))
            self.conn.commit()
        pass

    def importCZCE(self, csvF):
        self.variaties["czce"] = []
        with open(csvF) as hisF:
            reader = csv.reader(hisF, delimiter='|')
            cur_contract = None
            insert_sql = "insert or replace into daily values (?,?,?,?,?,?,?,?,?,?,?,?,?)"
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
                    if variaty not in self.variaties["czce"]:
                        self.variaties["czce"].append(variaty)
                        self.contracts[variaty] = []
                    self.contracts[variaty].append(cur_contract)
                else:
                    print("An invalid contract in CZCE? %s" % cur_contract)
                self.cursor.execute(insert_sql, (cur_contract, row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[13], row[11]))
            self.conn.commit()
        pass

    def importDCE(self):
        pass


    def importHisData(self, sh_dir='', zz_dir=''):
        self.checkDB()
        # for ShangHai Future Exchange
        files = os.listdir(sh_dir)
        files.sort()
        #for f in files:
        #    self.importSHFE("%s/%s" % (sh_dir, f))
        # for Zhengzhou Future Exchange
        files = os.listdir(zz_dir)
        files.sort()
        for f in files:
            self.importCZCE("%s/%s" % (zz_dir, f))
        
        # for DaLian Futrue Exchange




