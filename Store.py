from pymemcache.client import base

class Store:
    instance = None

    def __init__(self, config):
        self.config = config
        self.use_memcached = config.use_memcached
        self.users = {}
        if self.use_memcached:
            self.client = base.Client((self.config.memcached_host, self.config.memcached_port))

    
    def set(self, key, value):
        if self.use_memcached:
            self.client.set(key, value, 86400)
        else:
            self.users[key] = value


    def get(self, key):
        ret = None
        if self.use_memcached:
            ret = self.client.get(key)
        else:
            ret = self.users[key] if self.users.has_key(key) else None
        return ret


    def delete(self, key):
        if self.use_memcached:
            ret = self.client.delete(key)
        else:
            if key in self.users:
                del self.users[key]

    @classmethod
    def get_store(cls, config=None): 
        if cls.instance is None: 
             cls.instance = Store(config) 
        return cls.instance
