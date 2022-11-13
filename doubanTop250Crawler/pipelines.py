# Define your item pipelines here

import MySQLdb.cursors
from twisted.enterprise import adbapi


class MysqlTwistedPipeline:
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            password=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._insert, item)
        query.addErrback(self._handle_error, item, spider)

    def _insert(self, cursor, item):
        try:
            cursor.execute(*item.insert_sql())
        except Exception as e:
            print(e)

    def _handle_error(self, failure, item, spider):
        print(failure)
        import codecs
        import time
        f = codecs.open("error.txt", "a", "utf-8")
        f.write('\n'.join([
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            str(failure)
        ]))
        f.close()