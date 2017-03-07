import unittest
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

from arseparse import (
    Parser,
    Option,
)


class ParserTest(unittest.TestCase):

    def test_default_props(self):
        parser = Parser(bootstrap=None)

        assert parser.registry == {}
        assert parser.root_options == []
        assert parser.bootstrap is None

    def test_register_and_call_no_args(self):
        parser = Parser()
        fn = MagicMock()
        parser.register('cmd', fn)
        exit_code = parser.run(['cmd'])

        fn.assert_called_once_with()
        assert exit_code == 0

    def test_bootstrap(self):
        def bootstrap(**kwargs):
            return {'foo': 'bar'}

        parser = Parser(bootstrap=bootstrap)
        fn = MagicMock()
        parser.register('cmd', fn)
        exit_code = parser.run(['cmd'])

        fn.assert_called_once_with(foo='bar')
        assert exit_code == 0

    def test_bootstrap_root_options(self):
        def bootstrap(**kwargs):
            assert 'config' in kwargs
            return kwargs

        root_options = [Option('config')]
        parser = Parser(bootstrap=bootstrap, root_options=root_options)

        fn = MagicMock()
        parser.register('cmd', fn)
        exit_code = parser.run(['foo.ini', 'cmd'])

        fn.assert_called_once_with(config='foo.ini')
        assert exit_code == 0

    def test_register_and_call_custom_args(self):
        parser = Parser()
        fn = MagicMock()
        parser.register('cmd', fn, [Option('--param1', required=True)])
        exit_code = parser.run(['cmd', '--param1=X'])

        fn.assert_called_once_with(param1='X')
        assert exit_code == 0

    def test_register_and_call_default_and_custom_args(self):
        def bootstrap(**kwargs):
            kwargs.update({'c': 'd'})
            return kwargs

        parser = Parser(bootstrap=bootstrap)
        fn = MagicMock()
        parser.register(
            'cmd', fn, [Option('--param1', type=str, required=True)])
        exit_code = parser.run(['cmd', '--param1=X'])

        fn.assert_called_once_with(c='d', param1='X')
        assert exit_code == 0

    def test_register_and_call_default_and_opt_custom_args(self):
        def bootstrap(**kwargs):
            kwargs.update({'c': 'd'})
            return kwargs

        parser = Parser(bootstrap=bootstrap)
        fn = MagicMock()
        parser.register(
            'cmd', fn, [Option('--param1', type=str, required=False)])
        exit_code = parser.run(['cmd'])

        fn.assert_called_once_with(c='d', param1=None)
        assert exit_code == 0

    def test_register_and_call_custom_args_int(self):
        parser = Parser()
        fn = MagicMock()
        parser.register(
            'cmd', fn, [Option('value', type=int)])
        exit_code = parser.run(['cmd', '23'])

        fn.assert_called_once_with(value=23)
        assert exit_code == 0

    def test_blow_up(self):
        parser = Parser()

        def fn():
            raise ValueError()

        parser.register('cmd', fn)
        exit_code = parser.run(['cmd'])

        assert exit_code == 1

    def test_sys_exit(self):
        parser = Parser()

        def fn():
            raise SystemExit()

        parser.register('cmd', fn)
        with self.assertRaises(SystemExit):
            parser.run(['cmd'])

    def test_decorator(self):
        parser = Parser()

        @parser.register_dec([Option('--value', type=int, required=True)])
        def double(value):
            return value + value

        assert double(2) == 4

        exit_code = parser.run(['double', '--value=2'])

        assert exit_code == 0


if __name__ == '__main__':
    unittest.main()
