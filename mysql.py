# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 11:36:45 2017

@author: d_xuan
"""
import MySQLdb
db = ''

def sql_select (db,sql):
    cursor = db.cursor()
    try:
        cursor.excute(sql)
        results = cursor.fetchall()
        #for row in results:
        db.commit()
    except:
        db.rollback()

def connect_sql(database):
    db = MySQLdb.connect("localhost", "root", "123456", database)
    print 'connected'
    return db

def close_sql(database):
    database.close()

if __name__ == "__main__":
    db = connect_sql("vgiwork")
    
