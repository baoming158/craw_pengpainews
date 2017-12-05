import pymysql

con = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                passwd='root1234',
                db='craw_data',
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor
            )