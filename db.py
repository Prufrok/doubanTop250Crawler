import MySQLdb
from scrapy.utils.project import get_project_settings

def create_table():
    settings = get_project_settings()
    dbparms = dict(
        host=settings["MYSQL_HOST"],
        db=settings["MYSQL_DBNAME"],
        user=settings["MYSQL_USER"],
        password=settings["MYSQL_PASSWORD"],
        charset='utf8',
    )

    conn = MySQLdb.connect(**dbparms)
    cur = conn.cursor()

    table_name, var_info = table_input()
    sql = '\n'.join([
        f'DROP TABLE IF EXISTS {table_name};\n',
        
        f'CREATE TABLE {table_name} (',
        ',\n'.join([' '*4 + f'{l}' for l in var_info]),
        ');'
    ])
    
    cur.execute(sql)
    cur.close()
    conn.close()

def table_input():
    table_name = input('Table name:')

    var_info = []
    print("Enter/Paste contents here. Press `enter` to save it.")
    while True:
        line = input()
        if not line: break
        var_info.append(line)
    return table_name, var_info

if __name__ == '__main__':
    create_table()
    
title VARCHAR(255) PRIMARY KEY
url VARCHAR(255)
img_url VARCHAR(255)
author VARCHAR(255)
rate FLOAT
votes_num INT
comments_num INT