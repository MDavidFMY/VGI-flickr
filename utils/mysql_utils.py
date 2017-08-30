# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 11:36:45 2017

@author: d_xuan
"""
import MySQLdb
db = ''


def connect_sql(db):
    try:
        db_obj = MySQLdb.connect("localhost", "root", "123456", db)
        print 'connected'
    except Exception as e:
        print e
    return db_obj

def close_sql(db):
    try:
        db.close()
    except Exception as e :
        print e

def creat_table(db,sql,table_name):
    cursor = db.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS " + table_name)
        print '----creat table '+ table_name + '----'
        cursor.execute(sql)
    except Exception as e:
        print e
        db.rollback()

def sql_select (db,sql):
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except:
        db.rollback()

def sql_insert_singel(db,sql):
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print e
        db.rollback()

def sql_insert_many(db,sql,values):
    cursor = db.cursor()
    try:
        cursor.executemany(sql,values)
        db.commit()
    except Exception as e:
        print e
        db.rollback()

if __name__ == "__main__":
    db = connect_sql("vgiwork")


