import redis

client = redis.Redis.from_url('redis://3.88.32.1:6379')
print(client.ping())

print(client.get('x'))

print(client.get_encoder())
# from redis.cluster import RedisCluster
# rc = RedisCluster(host='inwaydb2.shrvtq.ng.0001.use1.cache.amazonaws.com', port=6379)

# print(rc.get_nodes())
# [[host=127.0.0.1,port=16379,name=127.0.0.1:16379,server_type=primary,redis_connection=Redis<ConnectionPool<Connection<host=127.0.0.1,port=16379,db=0>>>], ...

# rc.set('foo', 'bar')
# True

# rc.get('foo')
# b'bar'