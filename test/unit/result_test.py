from nose.tools import *
from mock import patch

import mock

import nose_helper

from kiwi.result import Result
from kiwi.exceptions import *


class TestResult(object):
    def setup(self):
        self.result = Result()

    def test_add(self):
        self.result.add('foo', 'bar')
        assert self.result.get_results() == {'foo': 'bar'}

    @patch('kiwi.logger.log.info')
    def test_print_results_no_data(self, mock_info):
        self.result.print_results()
        assert mock_info.called == 0

    @patch('kiwi.logger.log.info')
    def test_print_results_data(self, mock_info):
        self.result.add('foo', 'bar')
        self.result.print_results()
        assert mock_info.called

    @patch('marshal.dump')
    def test_dump(self, mock_marshal_dump):
        self.result.dump('kiwi.result')
        mock_marshal_dump.assert_called_once_with(
            self.result, 'kiwi.result'
        )

    @patch('marshal.dump')
    @raises(KiwiResultError)
    def test_dump_failed(self, mock_marshal_dump):
        mock_marshal_dump.side_effect = Exception
        self.result.dump('kiwi.result')

    @patch('marshal.load')
    @patch('os.path.exists')
    def test_load(self, mock_exists, mock_marshal_load):
        mock_exists.return_value = True
        Result.load('kiwi.result')
        mock_marshal_load.assert_called_once_with('kiwi.result')

    @patch('os.path.exists')
    @raises(KiwiResultError)
    def test_load_result_not_present(self, mock_exists):
        mock_exists.return_value = False
        Result.load('kiwi.result')

    @patch('marshal.load')
    @patch('os.path.exists')
    @raises(KiwiResultError)
    def test_load_failed(self, mock_exists, mock_marshal_load):
        mock_exists.return_value = True
        mock_marshal_load.side_effect = Exception
        Result.load('kiwi.result')
