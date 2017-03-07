import argparse
import logging


class Option():
    """Wrapper around ArgumentParser's `add_argument(self, *args, **kwargs)`"""
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class Parser():
    def __init__(self, root_options=None, bootstrap=None):
        """Object for executing commands from command line strings.

        :param root_options: root arguments (before subparsers)
        :param bootstrap: callable that processes kwargs before command call

        :returns: Parser object
        """
        self.root_options = root_options or []
        self.bootstrap = bootstrap
        self.registry = {}

    def make_parser(self):
        parser = argparse.ArgumentParser()

        for opt in self.root_options:
            parser.add_argument(*opt.args, **opt.kwargs)

        subparsers = parser.add_subparsers(dest='command_name')
        subparsers.required = True

        for name, command in self.registry.items():
            subparser = subparsers.add_parser(name)
            if command.get('options'):
                for option in command['options']:
                    subparser.add_argument(*option.args, **option.kwargs)

        return parser

    def run(self, args=None, loglevel=logging.INFO):
        """Execute the matching callable passing."""
        parser = self.make_parser()
        args = parser.parse_args(args)

        command_name = args.__dict__.pop('command_name')

        cmd_kwargs = args.__dict__
        if self.bootstrap:
            cmd_kwargs = self.bootstrap(**cmd_kwargs)

        exit_code = 0
        try:
            result = self.registry[command_name]['callable'](**cmd_kwargs)
            if result is not None:
                print(result)

        except SystemExit as e:
            raise

        except Exception as e:
            if loglevel is not None:
                logging.basicConfig(level=loglevel)
                log = logging.getLogger(self.__class__.__name__)
                log.exception(e)
            exit_code = 1

        return exit_code

    def register(self, name, callable, options=None):
        """Registers a callable against a name and argparse options."""
        self.registry[name] = dict(callable=callable, options=options)

    def register_dec(self, options=None):
        def dec(fn):
            self.register(fn.__name__, fn, options)
            def wrapper(*args, **kwargs):
                return fn(*args, **kwargs)
            return wrapper
        return dec
