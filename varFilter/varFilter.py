############################################################################################################
#
# this function scan each packages under this directory, and run each filter, save the result to database 
#
############################################################################################################
import sqlite3
import os
import datetime

import filters.allFilters as ff

###############################################################################################
# base class for future filter
###############################################################################################
class FilterContext():
    def __init__(self, data_context, filter_db_file):
        self.data_context = data_context
        # init each filters
        self.filters = ff.instances(self.data_context)
        # database handle
        self.filter_conn = sqlite3.connect(filter_db_file)
        self.filter_cursor = self.filter_conn.cursor()
        self.filter_sql = '''insert into filter_result values(?,?,?,?,?)'''
        pass

    def check(self):
        # create the filter table if not exist
        if self.filter_cursor is None:
            return False
        sql = '''create table if not exists filter_result (
                    filter_name,
                    date asc,
                    contract,
                    index_v,
                    direction,
                    primary key (filter_name, date asc, contract))'''
        self.filter_cursor.execute(sql)
        self.filter_conn.commit()
        return True
    
    def filter(self):
        day, active_contracts = self.data_context.fetchActiveHotContracts()
        for filter in self.filters:
            for contract in active_contracts:
                (order,index) = filter.check(contract)
                if order != 'none':
                    # import qualified into databases
                    try:
                        self.filter_cursor.execute(self.filter_sql, (filter.name, day, contract, index, order))
                        self.filter_conn.commit()
                    except Exception, e:
                        print('Exception caught while insert a filter result record')
        return
