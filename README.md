# Simple python Bottle application

[![docker swarm ingress CI](https://github.com/garutilorenzo/simple-bottlepy-application/actions/workflows/ci.yml/badge.svg)](https://github.com/garutilorenzo/simple-bottlepy-application/actions/workflows/ci.yml)
[![GitHub issues](https://img.shields.io/github/issues/garutilorenzo/simple-bottlepy-application)](https://github.com/garutilorenzo/simple-bottlepy-application/issues)
![GitHub](https://img.shields.io/github/license/garutilorenzo/simple-bottlepy-application)
[![GitHub forks](https://img.shields.io/github/forks/garutilorenzo/simple-bottlepy-application)](https://github.com/garutilorenzo/simple-bottlepy-application/network)
[![GitHub stars](https://img.shields.io/github/stars/garutilorenzo/simple-bottlepy-application)](https://github.com/garutilorenzo/simple-bottlepy-application/stargazers)

A very simple web application written in python.

# Table of Contents

* [Requirements](#requirements)
* [The application stack](#the-application-stack)
* [Data used in this example site](#data-used)
* [Setup the environmant](#setup-the-environmant)
* [Download sample data](#download-sample-data)
* [Start the environment](#start-the-environment)
* [Application Overview](#application-overview)
* [App configuration](#app-configuration)
* [DB configuration](#db-configuration)
* [SQLAlchemy plugin](#sqlalchemy-plugin)
* [Redis Cache](#redis-cache)
* [Data export](#data-export)
* [Data import](#data-import)

## Requirements 

To use this environment you need [Docker](https://docs.docker.com/get-docker/) an [Docker compose](https://docs.docker.com/compose/install/) installed.

## The application stack

Backend:

* [BottlePy](https://bottlepy.org/docs/dev/)
* [SQLAlchemy](https://www.sqlalchemy.org/)

Frontend:

* [Bootstrap 5](https://getbootstrap.com/)
* [jQuery](https://jquery.com/)

Database:

* [PostgreSQL](https://www.postgresql.org/)
* [Redis](https://redis.io/)

Webserver:

* [Nginx](https://www.nginx.com/) - Only Prod env.

## Data used

To use this example application we need to import some example data. This example application use the "Stack Exchange Data Dump" available on [archive.org](https://archive.org/details/stackexchange).

All the data used by this site is under the [cc-by-sa 4.0](https://creativecommons.org/licenses/by-sa/4.0/) license.

## Setup the environmant

We are now ready to setup our environment. For dev purposes link the docker-compose-dev.yml do docker-compose.yml

```bash
ln -s docker-compose-dev.yml docker-compose.yml
```

For prod environments:

```bash
ln -s docker-compose-dev.yml docker-compose.yml
```

The difference between dev and prod envs are:

|   Prod   |   Dev   |
| -------- | ------- |
| Nginx is used to expose our example application | Built-in HTTP development server |
| Http port 80 | Http port 8080 |
| Debug mode is disabled | Debug mode is enabled |
| Reloader is disabled | Reloader is enabled |

Now we can download some sample data.

## Download sample data

To dwonload some example data run:

```bash
./download_samples.sh
```

By default the archive with the 'meta' attribute will be downloaded. If you want more data remove in download_samples.sh 'meta' form the archive name.

Small data:

```bash
for sample in workplace.meta.stackexchange.com.7z unix.meta.stackexchange.com.7z
```

Big data:


```bash
for sample in workplace.stackexchange.com.7z unix.stackexchange.com.7z
```

**Note** not all the stackexchange sites where imported on this example. After you choose the archives you will download adjust the network.py schema under src/schema/

```python
class Sites(enum.Enum):
    vi = 'vi.stackexchange.com'
    workplace = 'workplace.stackexchange.com'
    wordpress = 'wordpress.stackexchange.com'
    unix = 'unix.stackexchange.com'
    tex = 'tex.stackexchange.com'
```

Onche the data is downloaded we can import the data:

```bash
docker-compose run --rm bottle bash

web@4edf053b7e4f:~/src$  python init_db.py # <- Initialize DB
web@4edf053b7e4f:~/src$  python import_data.py # <- Import sample data
```

Now for each data sample you have downloaded (Eg. tex, unix, vi) a python subprocess is started and will import in order:

* all the tags
* all the users
* all the posts
* all the post history events

Once the import is finished we can start our environment

## Start the environment

With our DB populated we can now start our web application:

```bash
docker-compose up -d

Creating network "bottle-exchange_default" with the default driver
Creating postgres ... done
Creating redis    ... done
Creating bottle   ... done
```

The application will be available at http://localhost:8080 for the dev and http://localhost for the prod

## Application Overview

### Index

Home page with a search form. On every change on the "Network" select, the "Tags" select is populated by an ajax call on /api/autocomplete/form/get_tags (POST) (for more details see src/bottle/static/asset/js/custom.js).

The POST call is authenticated with a random hard coded string (see src/bottle/app.py, api_get_tags)

### Tags

List of all available tags with a pagination nav.
Clicking on the tag name the application will search all questions matching the tag you have selected, by clicking the site name the application will search all questions matching the tag and the site you ave selected.

### Users

Table view of all available users with a pagination nav.

Clicking on the username, we enter on the detail's page of the user. In the details user page we see: UP Votes,Views,Down Votes. If the user has populated the "About me" field, we see a button that trigger a modal with the about me details.
If the user ha asked or answered some question we see a list of question in the "Post" section.

### Posts

List of all posts with a pagination nav

### API/REST endpoint

This application expose one api/rest route: /api/get/tags. You can query this route making a POST call, you have to make the call using a json payload:

```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"auth_key":"dd4d5ff1c13!28356236c402d7ada.aed8b797ebd299b942291bc66,f804492be2009f14"}' \
  http://localhost:8080/api/get/tags | jq

 {
  "data": [
    {
      "clean_name": "html5",
      "created_time": "2021-12-29 11:33:06.517152+00:00",
      "id": "1",
      "name": "html5",
      "network_sites": "Sites.wordpress",
      "questions": "91",
      "tag_id": "2",
      "updated_time": "None"
    },
    ...
    ],
  "errors": [],
  "items": 5431,
  "last_page": 27
}
```

The auth_key is hard coded in src/bottle/app.py

## App configuration

The application's configuration are loaded by the load_config module (src/load_config.py).

This module will load a .yml file under:

```
/app/src/<BOTTLE_APP_NAME>/config/<BOTTLE_APP_ENVIRONMENT>
```

*BOTTLE_APP_NAME* and *BOTTLE_APP_ENVIRONMENT* are environment variables.

BOTTLE_APP_NAME is the name of the path where our bottle application lives, in this case *bottle*. BOTTLE_APP_ENVIRONMENT value is prod or env.

An example configuration is:

```yaml
---
enable_debug: True
enable_reloader: True
http_port: 8080
pgsql_username: "bottle"
pgsql_password: "b0tTl3_Be#"
pgsql_db: "bottle_exchange"
pgsql_host: "pgsql"
pgsql_port: 5432
create_db_schema: True
default_result_limit: 50
```

## DB configuration

The database configuration is defined under the src/schema module.

The base.py file contains the engine configuration:

```python
import load_config # <- See App configuration

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

main_config = load_config.load_config()
conn_string = 'postgresql+psycopg2://{pgsql_username}:{pgsql_password}@{pgsql_host}:{pgsql_port}/{pgsql_db}'.format(**main_config)

engine = create_engine(conn_string, pool_size=80, pool_recycle=60)
Session = sessionmaker(bind=engine)

Base = declarative_base()
```

All the tables are defined in a separate file always under schema:

| schema  |  Tables  | Description |
| ------- | ------- | ----------- |
| `network.py` | None | Sites class is not a SQLAlchemy object, but is an Enum used by all the other tables |
| `posts.py` | posts,post_history | Table definition for post and post_history tables. This module contains also three enum definitions: PostType, PostHistoryType, CloseReason |
| `tags.py` | tags | Tags table |
| `users.py` | users | Users table |


## SQLAlchemy plugin

In this example application is used and insalled a SQLAlchemy plugin (src/bottle/bottle_sa.py). This plugin is used to handle the SQLAlchemy session:

```python
from schema.base import Base, engine # <- Base and engine are defined in the schema module, see "DB configuration"
from bottle_sa import SQLAlchemyPlugin
import load_config

main_config = load_config.load_config()

# Main Bottle app/application
app = application = Bottle()

# DB Plugin
saPlugin = SQLAlchemyPlugin(
    engine=engine, metadata=Base.metadata, 
    create=main_config['create_db_schema'], 
    config=main_config,
)
application.install(saPlugin)
```

This plugin pass an extra parameter on each function defined in src/bottle/app.py. By default this parameter is 'db', but it can be changed by passing the extra parameter 'keyword' on the SQLAlchemyPlugin init.

So an example function will be:

```python
@app.route('/docs')
@view('docs')
def index(db): # <- db is our SQLAlchemy session
    return dict(page_name='docs')
```

## Redis Cache

In this example application we use redis to cache some pages. The caching "approach" is very useful if you have:

* a site with few updates
* a slow page/route 
* you have to decrease the load of your DB

The RedisCache is defined in src/bottle/bottle_cache.py and this is an example usage:

```python
from bottle_cache import RedisCache

# Cache
cache = RedisCache()

@app.route('/tags')
@app.route('/tags/<page_nr:int>')
@cache.cached()
@view('tags')
def get_tags(db, page_nr=1):
    do_something()
    return something
```

You can init RedisCache class with an extra parameter config:

```python
config = {'redis_host': '<redis_hostname'>, 'redis_port': 6379, 'redis_db': 0, 'cache_expiry': 86400}
cache = RedisCache(config=config)
```

By default the configurations are:

| Param   | Default | Description |
| ------- | ------- | ----------- |
| `redis_host` | `redis` | Redis FQDN or ip address |
| `redis_port` | `6379` | Redis listen port |
| `redis_db` | `0` | Redis database |
| `cache_expiry` | `3600` | Global cache expiry time in seconds |

The @cached decorator can accept some arguments:

| Param   | Default | Description |
| ------- | ------- | ----------- |
| `expiry` | `None` | Route cache expiry time. If not defined is the same value as the global expiry time |
| `key_prefix` | `bottle_cache_%s` | Redis key prefix |
| `content_type` | `text/html; charset=UTF-8` | Default content type |

### Caching json requests

A json caching example would be:

```python
@app.route('/api/get/tags', method='POST')
@cache.cached(content_type='application/json')
def api_get_tags(db):
    do_something()
    return something
```

### Invalidate cache

To invalidate the cache pass **invalidate_cache** key as query parameter or in the body request if you make a POST call

### Skip/bypass cache

To skip or bypass the cache pass **skip_cache** key as query parameter or in the body request if you make a POST call

## Data export

To backup PgSQL data run dump_db.sh

```bash
./dump_db.sh
```

the dump will be placed in the root directory of this repository, the file will be named dump.sql.gz (Gzipped format)

## Data import

To import an existing DB uncomment the following line in the docker-compose.yml:

```yaml
volumes:
    - type: volume
      source: postgres
      target: /var/lib/postgresql/data
    - ./sql:/docker-entrypoint-initdb.d # <- uncomment this line
```

and plache your dump in gzip or plain text format under sql/ (create the directory first)

## Stop the environment

To stop the environment run

```bash
docker-compose down

Stopping bottle   ... done
Stopping postgres ... done
Stopping redis    ... done
Removing bottle   ... done
Removing postgres ... done
Removing redis    ... done
Removing network bottle-exchange_default
```

To clean up all the data (pgsql data) pass the extra argument "-v" to docker-compose down. With this parameter the pgsql volume will be deleted.