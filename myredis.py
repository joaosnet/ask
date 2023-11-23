import redis

# client = redis.Redis.from_url('redis://3.88.32.1:6379')
# print(client.ping())

# print(client.get('x'))

# print(client.get_encoder())

rc = redis.Redis.from_url('redis://waywaydb2.shrvtq.ng.0001.use1.cache.amazonaws.com:6379')

print(rc.ping())

rc.set('foo', 'bar')
# True

print(rc.get('foo'))
# b'bar'