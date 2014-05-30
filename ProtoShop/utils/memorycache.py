# -*- coding:utf8 -*-

"""
@Item   :  redis API
@Author :  Anselz
@Group  :  NeoWork
@Date   :  2014-05-08
@Funtion:
        redis_set : Redis in the form of pipe insert data, json hash as a string print
        redis_get : Redis inprintion, and json string into the original print
"""
import sys,os,time,redis,traceback,json
import ProtoShop.conf.global_settings as conf

class redising(object):
    ''' Establish redis session connection pool '''
    def __new__(cls,host,port,db):
    	if not hasattr(cls, '_instance'):  
            orig = super(redising, cls)  
            cls._instance = orig.__new__(cls,host,port,db)  
        return cls._instance

    def __init__(self,host,port,db):
    	self.host = host
        self.port = port
        self.db = db
        try:
            pool = redis.ConnectionPool(host = self.host, port = self.port, db = self.db)
            self.conn  = redis.Redis(connection_pool=pool)
            self.pipe = self.conn.pipeline()
        except:
            return traceback.format_exc()

    def redis_set(self,key=None ,values=None):
        ''' Insert redis databases,keys = key ,values = value'''
        try:
            self.conn.set(key,values)
            # self.pipe.execute()
            self.conn.expire(key,10)
            return True
        except:
            return False
            # return traceback.format_exc()
    def redis_hset(self, key, field, values):
        '''insert redis key, field ,values'''
        try:
            self.pipe.hset(key, field, json.dumps(values))
            self.pipe.execute()

        except:
            return traceback.format_exc()
    def redis_hget(self, key, field = None):
        '''get by key, return the dict'''
        try:
            fields = []
            if field:
                fields.append(field)
            else:
                fields = self.conn.hkeys(key)
            for f in fields:
                self.pipe.hget(key, f)
            values = self.pipe.execute()
            values = [json.loads(i) for i in values]
            return dict(zip(fields, values))
        except:
            return key
    def redis_get(self,key):
        ''' Getting single KYES values ,argv : is keys'''
        try:
            # self.pipe.get(argv)
            # return json.loads( self.pipe.execute()[0])

            return self.conn.get(key)
        except:
            return traceback.format_exc()
    def redis_getkeys(self):
        ''' Getting all keys '''
        try:
            self.pipe.keys('*')
            return self.pipe.execute()[0]
        except:
            return traceback.format_exc()
    def redis_delete(self,keys):
        try:
            self.pipe.delete(keys)
            self.pipe.execute()
            return True
        except:
            return False

    def redis_exist(self,key):
        return self.conn.exists(key)
        



