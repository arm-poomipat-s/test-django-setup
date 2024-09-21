# mock
from unittest.mock import patch
# simulate db connec error postgresql
from psycopg2 import OperationalError as Psycopg2Error
# allow test to cal wait_for_db
from django.core.management import call_command
# generic db error in django
from django.db.utils import OperationalError
# for write unit test
from django.test import SimpleTestCase


# replace object from check method with mock
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        # set value return from 'check'
        patched_check.return_value = True
        call_command('wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError"""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
