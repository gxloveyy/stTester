# test data pool

import historyDataImporter as hdi

importer = hdi.historyDataImporter(db_file="C:\\Projects\\StraTestPlatform\\data\\futures.sqlitedb")
importer.importHisData(sh_dir='C:\\Projects\\StraTestPlatform\\data\\shfe', zz_dir="C:\\Projects\\StraTestPlatform\\data\\czce")


