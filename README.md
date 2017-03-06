# Arseparse

Arseparse is a simple Python utility/micro framework for writing command line interfaces. It provides some fluff around argparse that covers common development scenarios.

```
from arseparse import Parser, Option


parser = Parser()


# register a command that returns the square of an int that is passed in
parser.register('square', lambda value, **kwargs: value**2, [Option('value', type=int)])


# register a command that simply returns a string
parser.register('ping', lambda **kwargs: 'pong')


# or with a decorator
@parser.register_dec([Option('value', type=int)])
def cube(value, **kwargs):
    return value**3


sys.exit(parser.run())
```
You can then simply point an application entrypoint to the script or simply execute the file: `your-entrypoint.py square 2`

So far so boring. A more common scenario is to have a config file as the first argument, parse it, create objects that the command depends on, and pass those alongside the argparse attributes.
`root_options` and `bootstrap` allow you to implement a strategy of that kind.
```
from arseparse import Parser, Option
import myapp


# these are options that come before our main command
root_options = [Option('config', type=str, help='path to ini file')]


# this lets us process/modify the kwargs before we execute the callable.
# we can rely on attributes resulting from root_options to be set.
# Here config gets replaced by three objects: settings, db_session and user_svc
# which will be presented as kwargs to the callable, alongside the attributes
# from the callable's own options.
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
You can now provide the path to a config file as the first argument: `your-entrypoint.py config.ini ban_user 23`

Another common requirement is to be able to jump into a shell where some objects have been preconfigured for us.
Here's a simple recipe for that.

```
@parser.register_dec()
def shell(**kwargs):
    import IPython
    IPython.embed(user_ns=kwargs)

```

Calling `your-entrypoint config.ini shell` wil drop you in an ipython shell where `dbsession`, `settings` and `user_svc` are in scope.