#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis
def getredis():
    pool = redis.ConnectionPool(host='127.0.0.1', password='magicnian', port=6379)
    r = redis.Redis(connection_pool=pool)
    return r


if __name__ == '__main__':
    r = getredis()

    print(r.get('PROXY'))