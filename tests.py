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
        m = Parser(bootstrap=None)

        assert m.registry == {}
        assert m.root_options == []
        assert m.bootstrap is None

    def test_register_and_call_no_args(self):
        m = Parser()
        fn = MagicMock()
        m.register('cmd', fn)
        exit_code = m.run(['cmd'])

        fn.assert_called_once_with()
        assert exit_code == 0

    def test_register_and_call_default_args(self):
        def bootstrap(*args, **kwargs):
            return {'foo': 'bar'}

        m = Parser(bootstrap=bootstrap)
        fn = MagicMock()
        m.register('cmd', fn)
        exit_code = m.run(['cmd'])

        fn.assert_called_once_with(foo='bar')
        assert exit_code == 0

    def test_register_and_call_custom_args(self):
        m = Parser()
        fn = MagicMock()
        m.register('cmd', fn, [Option('--param1', type=str, required=True)])
        exit_code = m.run(['cmd', '--param1=X'])

        fn.assert_called_once_with(param1='X')
        assert exit_code == 0

    def test_register_and_call_default_and_custom_args(self):
        def bootstrap(**kwargs):
            kwargs.update({'c': 'd'})
            return kwargs

        m = Parser(bootstrap=bootstrap)
        fn = MagicMock()
        m.register('cmd', fn, [Option('--param1', type=str, required=True)])
        exit_code = m.run(['cmd', '--param1=X'])

        fn.assert_called_once_with(c='d', param1='X')
        assert exit_code == 0

    def test_register_and_call_default_and_opt_custom_args(self):
        def bootstrap(**kwargs):
            kwargs.update({'c': 'd'})
            return kwargs

        m = Parser(bootstrap=bootstrap)
        fn = MagicMock()
        m.register('cmd', fn, [Option('--param1', type=str, required=False)])
        exit_code = m.run(['cmd'])

        fn.assert_called_once_with(c='d', param1=None)
        assert exit_code == 0

    def test_register_and_call_custom_args_int(self):
        m = Parser()
        fn = MagicMock()
        m.register('cmd', fn, [Option('--param1', type=int, required=True)])
        exit_code = m.run(['cmd', '--param1=666'])

        fn.assert_called_once_with(param1=666)
        assert exit_code == 0


if __name__ == '__main__':
    unittest.main()
