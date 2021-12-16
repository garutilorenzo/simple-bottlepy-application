import functools
import json, hashlib, redis
from bottle import request, response
from datetime import datetime, timedelta

# RedisCache Object

class RedisCache(object):
    """
    Cache bottle results using Redis backend

    :param config: Dict or None. Valid config keys are:
        redis_host: Redis hostname or ip address. Default redis (Docker container)
        redis_port: Redis port. Default 6379
        redis_db: Redis db. Default 0
        cache_expiry: Redis cache expiry. Default 3600 seconds
    
    # Example
    # If config is not provided redis will try to connect on the redis container 
    # specified in docker-compose.yml

    from bottle_cache import RedisCache
    config = {'redis_host': '<redis_hostname'>, 'redis_port': 6379, 'redis_db': 0}
    cache = RedisCache(config=config)
    """

    def __init__(self, config={}):
        if not (config is None or isinstance(config, dict)):
            raise ValueError("`config` must be an instance of dict or None")

        self.config = config
        self.cache_expiry = config.get('cache_expiry', 3600)

    def get_redis_cli(self):
        redis_cli = redis.Redis(
            host=self.config.get('redis_host', 'redis'),
            port=self.config.get('redis_port', 6379),
            db=self.config.get('redis_db', 0),)
        return redis_cli

    def set_cache(self, cache_key, rv, expiry):
        redis_cli = self.get_redis_cli()
        json_rv = json.dumps(rv)
        redis_cli.setex(cache_key, timedelta(seconds=expiry), json_rv)
    
    def get_cache(self, cache_key):
        redis_cli = self.get_redis_cli()
        cache_result = redis_cli.get(cache_key)
        if cache_result:
            cache_decoded = cache_result.decode('utf-8')
            rv = json.loads(cache_decoded)
            return rv
        else:
            return None

    def invalidate_cache(self, cache_key):
        redis_cli = self.get_redis_cli()
        cache_result = redis_cli.delete(cache_key)

    def cached(self, expiry=None, key_prefix='bottle_cache_%s', content_type='text/html; charset=UTF-8'):
        """ 
            :param expiry: Default None. Default Redis expiry time in seconds. 
                           If not specified in config the default is 3600 secondss
            :param key_prefix: Redis key prefix
            :param content_type: Content-Type to be returned, default: text/html; charset=UTF-8

            Example:
                # Long cache result
                @app.route('/users')
                @app.route('/users/<page_nr:int>')
                @bottle_cache.cached(expiry='86400')
                @view('users')
                def get_users(db, page=1):
                    result = db.get_users()
                    res = dict(result=result)
                
                # Json output
                @app.route('/api/get/tags', method='POST')
                @bottle_cache.cached(content_type='application/json')
                def api_get_tags(db):
                    result = db.get_tags()
                    response.set_header("Content-Type", 'application/json')
                    return json.dumps(result, indent=4, sort_keys=True)
        """
        def decorator(f):
            @functools.wraps(f)
            def decorated_function(*args, **kwargs):

                url = request.url
                body = request.body.getvalue().decode('utf-8')
                query_string = request.query_string
                cache_key = decorated_function.get_cache_key(key_prefix, url, body, query_string)

                if 'skip_cache' in url\
                or 'skip_cache' in body:
                    return f(*args, **kwargs)

                if 'invalidate_cache' in url\
                or 'invalidate_cache' in body:
                    self.invalidate_cache(cache_key)
                    return f(*args, **kwargs)

                try:
                    rv = self.get_cache(cache_key)
                except Exception as e:
                    print("Exception possibly due to cache backend.")
                    return f(*args, **kwargs)

                if rv is None:
                    rv = f(*args, **kwargs)
                    try:
                        expiry_time = expiry if expiry else self.cache_expiry
                        self.set_cache(cache_key, rv, expiry_time)
                    except Exception as e:
                        print("Exception possibly due to cache backend.")
                        return f(*args, **kwargs)

                response.set_header("Content-Type", content_type)
                return rv

            def get_cache_key(key_prefix, url, body, query_string):
                if body:
                    cache_key = '{}/{}'.format(url, json.dumps(body))
                else:
                    cache_key = url
                hash_key = hashlib.md5(cache_key.encode('utf-8')).hexdigest()
                return key_prefix % hash_key

            decorated_function.uncached = f
            decorated_function.cache_expiry = expiry
            decorated_function.content_type = content_type
            decorated_function.get_cache_key = get_cache_key

            return decorated_function
        return decorator