# test data pool

import historyDataImporter as hdi
import dailyCrawler as dc

def importHistory():
    importer = hdi.historyDataImporter(db_file="C:\\Projects\\StraTestPlatform\\data\\futures.sqlitedb")
    importer.importHisData(sh_dir='C:\\Projects\\StraTestPlatform\\data\\shfe', zz_dir="C:\\Projects\\StraTestPlatform\\data\\czce")
    return

def testDaily():
    crawler = dc.dailyCrawler(db_file="C:\\Projects\\StraTestPlatform\\data\\futures.sqlitedb")
    if crawler.ready():
        crawler.fetchSHFE()
        crawler.fetchCZCE()
    pass


if __name__ == "__main__":
    testDaily()

