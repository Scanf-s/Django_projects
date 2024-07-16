"""
Test custom Django management commands.
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2OPsycopgpError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('django.db.utils.ConnectionHandler.__getitem__')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_getitem):
        """스크립트 작동 여부 확인"""
        patched_getitem.return_value = True

        call_command('wait_for_db')

        self.assertEqual(patched_getitem.call_count, 1)

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_getitem):
        """Psycopg2 에러 3회 발생 및 OperationalError 2회 발생, 마지막에 True 반환"""
        patched_getitem.side_effect = [Psycopg2OPsycopgpError] * 3 + \
            [OperationalError] * 2 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_getitem.call_count, 6)
        patched_sleep.assert_called_with(1)
