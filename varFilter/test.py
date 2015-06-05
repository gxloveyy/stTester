from varFilter import FilterContext
import dataContext as dc

def doFilter():
    data_context = dc.dataContext("..\\data\\futures.sqlitedb")
    fc = FilterContext(data_context, filter_db_file="..\\data\\filter.sqlitedb")
    if fc.check():
        fc.filter()
    return

if __name__ == "__main__":
    doFilter()