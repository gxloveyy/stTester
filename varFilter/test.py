from varFilter import FilterContext
import dataContext as dc

def doFilter():
    data_context = dc.dataContext("..\\data\\future_daily.sqlitedb")
    fc = FilterContext(data_context, filter_db_file="..\\data\\future_filter.sqlitedb")
    if fc.check():
        fc.filter()
    return

if __name__ == "__main__":
    doFilter()