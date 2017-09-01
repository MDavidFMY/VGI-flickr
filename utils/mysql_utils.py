# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 11:36:45 2017

@author: d_xuan
"""
import MySQLdb
db = ''


def connect_sql(db_name):
    try:
        db_obj = MySQLdb.connect("localhost", "root", "123456", db_name)
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
        print '----creat table '+ table_name + '----'
        cursor.execute(sql)
    except Exception as e:
        print e
        db.rollback()

def table_exist(db,tablename,database_name):
    cursor = db.cursor()
    try:
        cursor.execute("SELECT COUNT(*) as num FROM information_schema.TABLES WHERE TABLE_NAME='"+tablename+"' and TABLE_SCHEMA='"+database_name+"'")
        result = cursor.fetchone()
        return result[0]
    except Exception as e:
        print e

def sql_select (db,sql):
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print e

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
        print '<----insert done---->'
    except Exception as e:
        print e
        db.rollback()

if __name__ == "__main__":
    db = connect_sql("vgiwork")
    i =  table_exist(db,'london_2016_1',"vgiwork")
    print i


