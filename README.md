# Arseparse
[![CircleCI](https://img.shields.io/circleci/project/github/sgarcez/arseparse/master.svg)](https://circleci.com/gh/sgarcez/arseparse) [![codecov](https://img.shields.io/codecov/c/github/sgarcez/arseparse.svg)](https://codecov.io/gh/sgarcez/arseparse/) [![PyPI version](https://badge.fury.io/py/arseparse.svg)](https://pypi.python.org/pypi/arseparse) [![PyPI format](https://img.shields.io/pypi/format/arseparse.svg)](https://pypi.python.org/pypi/arseparse)


Arseparse is a simple Python utility/micro framework for writing command line interfaces. It provides some functionality around [argparse](https://docs.python.org/3/library/argparse.html) to dispatch a command handler and pre-process its arguments.

 
```
<entrypoint> root_args... command_name command_args...
```
For example:
```
<entrypoint> config.ini create_user foo@bar.xyz s3cr3t
```
Would execute this handler:
```
@parser.register_dec([Option('username', type=str), Option('secret', type=str)])
def create_user(username, secret, user_svc, **kwargs):
    user_svc.create_user(username, secret)
```
Where `user_svc` argument depends on the `config` root argument. More on that later.

Installation:
```
pip install arseparse
```

Basic usage (without root args):
```
from arseparse import Parser, Option


parser = Parser()


# register handler
@parser.register_dec([Option('value', type=int)])
def cube(value):
    return value**3


# register without a decorator
parser.register('square', lambda value: value**2, [Option('value', type=int)])


# register a command with no args
parser.register('ping', lambda: 'pong')


if __name__ == '__main__':
    sys.exit(parser.run())
```
Execute your `entry_point` or the file directly: `your-entrypoint[.py] square 2`

A more common scenario is to pass a config file as the first argument, parse it, create objects depend on the configuration, and pass those along to the handler.
The `root_options` and `bootstrap` constructor args to `Parser` allow us to do this:
```
from arseparse import Parser, Option
import myapp


root_options = [Option('config', type=str, help='path to ini file')]


# this lets us process/modify the kwargs before we execute the callable.
def bootstrap(**kwargs):
    config_uri = kwargs.pop('config')
    settings = myapp.parse_app_config(config_uri)
    dbsession = myapp.get_sessionmaker(settings)()
    user_svc = myapp.UserService(dbsession)
    kwargs.update(dict(settings=settings, dbsession=dbsession, user_svc=user_svc))
    return kwargs


parser = Parser(root_options, bootstrap)


@parser.register_dec([Option('username', type=str), Option('secret', type=str)])
def create_user(username, secret, user_svc, **kwargs):
    user_svc.create_user(username, secret)
    
 
@parser.register_dec([Option('user_id', type=int)])
def ban_user(user_id, user_svc, **kwargs):
    user_svc.ban_user(user_id)


@parser.register_dec()
def print_settings(settings, **kwargs):
    print(settings)

```
You can now provide the path to a config file as the first argument: `your-entrypoint[.py] config.ini ban_user 23`

Another common requirement is to be able to jump into a shell where some objects have been preconfigured for us.
Here's a simple recipe for that.

```
@parser.register_dec()
def shell(**kwargs):
    import IPython
    IPython.embed(user_ns=kwargs)

```

Calling `your-entrypoint.py config.ini shell` will drop you in an ipython shell where `dbsession`, `settings` and `user_svc` are available.
