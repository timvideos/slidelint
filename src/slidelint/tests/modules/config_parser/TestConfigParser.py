import os.path
import unittest
from testfixtures import compare, LogCapture

from slidelint import config_parser

here = os.path.dirname(os.path.abspath(__file__))


class TestSequenceFunctions(unittest.TestCase):

    def test_enables_disables(self):
        _ = config_parser.enables_disables
        compare(_({}),
                ([], []))
        compare(_({'enable': '', 'disable': ''}),
                 ([], []))
        compare(_({'enable': '1\n2', 'disable': '3\n4'}),
                 (['1', '2'], ['3', '4']))

    def test_default_config(self):
        with LogCapture() as l:
            config_parser.LintConfig()
            l.check(('user_messages',
                     'INFO',
                     'No config file found, using default configuration'),)

    def test_dummy_config(self):

        path = os.path.join(
            here, 'simple_enabling_disabling.cfg')
        config = config_parser.LintConfig(path)
        compare(config.categories,
                ['AllCategories'])
        compare(config.disable_categories,
                ['CategoryA'])
        compare(config.checkers,
                [('checker_a', {})])
        compare(config.disable_checkers,
                ['checker_f'])
        compare(config.messages,
                ['W0100'])
        compare(config.disable_messages,
                ['W0110'])

    def test_detailed_config(self):
        path = os.path.join(
            here, 'detailed_config.cfg')
        config = config_parser.LintConfig(path)
        compare(config.categories,
                ['CategoryC'])
        compare(config.checkers,
                [('checker_d', {}),
                 ('checker_e', {'arg1': '10', 'arg2': '20'})])
        compare(config.disable_checkers,
                ['checker_a'])

    def test_mixed_config(self):
        path = os.path.join(here, 'mixed.cfg')
        config = config_parser.LintConfig(path)
        compare(config.categories,
                ['CategoryC'])
        compare(config.disable_categories,
                ['CategoryDummy'])
        compare(config.checkers,
                [('checker_b', {}),
                 ('checker_d', {}),
                 ('checker_e', {'arg1': '10', 'arg2': '20'})])
        compare(config.disable_checkers,
                ['checker_f', 'checker_a'])
        compare(config.messages,
                ['W0100'])
        compare(config.disable_messages,
                ['W0110'])

# TODO: tests for LintConfig.compose
