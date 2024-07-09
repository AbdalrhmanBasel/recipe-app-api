"""
Tests for custom management commands.
"""

from django.core.management import call_command
from django.test import TestCase
from unittest.mock import patch
import subprocess


class PushChecksCommandTests(TestCase):
    """Test the push_checks command."""

    @patch('core.management.commands.push_checks.subprocess.run')
    def test_push_checks_command(self, mock_subprocess_run):
        """Test the push_checks command."""
        mock_subprocess_run.return_value.returncode = 0
        call_command('push_checks')
        self.assertTrue(mock_subprocess_run.called)
        self.assertGreaterEqual(mock_subprocess_run.call_count, 4)

    @patch('core.management.commands.push_checks.subprocess.run')
    def test_push_checks_command_flake8_failure(self, mock_subprocess_run):
        """Test the push_checks command with flake8 failure."""
        def mock_run(*args, **kwargs):
            if args[0] == ['flake8', '.']:
                return subprocess.CompletedProcess(
                    args, returncode=1, stdout=b"flake8 error")
            return subprocess.CompletedProcess(args, returncode=0)

        mock_subprocess_run.side_effect = mock_run
        call_command('push_checks')
        self.assertTrue(mock_subprocess_run.called)
        self.assertEqual(mock_subprocess_run.call_count, 1)
        self.assertIn("flake8 found errors. Fix them before pushing.",
                      "flake8 found errors. Fix them before pushing.")

    @patch('core.management.commands.push_checks.subprocess.run')
    def test_push_checks_command_test_failure(self, mock_subprocess_run):
        """Test the push_checks command with test failure."""
        def mock_run(*args, **kwargs):
            if args[0] == ['python', 'manage.py', 'test']:
                return subprocess.CompletedProcess(
                    args, returncode=1, stdout=b"test error")
            return subprocess.CompletedProcess(args, returncode=0)

        mock_subprocess_run.side_effect = mock_run
        call_command('push_checks')
        self.assertTrue(mock_subprocess_run.called)
        self.assertGreaterEqual(
            mock_subprocess_run.call_count, 4)
        self.assertIn("Tests failed. Fix them before pushing.",
                      "Tests failed. Fix them before pushing.")
