"""
Custom Django command to run checks before pushing to GitHub.
This command performs the following checks:

1. Runs flake8 to check for PEP 8 compliance and code style issues.
2. Waits for the database to be available.
3. Applies database migrations.
4. Runs all Django tests.

If any of these steps fail, the command reports errors and
suggests fixing them before pushing.
"""

import subprocess
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Custom Django command to run checks before pushing to GitHub."

    def handle(self, *args, **options):
        self.stdout.write(
            "Running flake8 to check for code style issues...")
        flake8_process = subprocess.run(['flake8', '.'],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        if flake8_process.returncode != 0:
            self.stdout.write(self.style.ERROR(
                "flake8 found errors. Fix them before pushing."))
            self.stdout.write(flake8_process.stdout.decode('utf-8')
                              if flake8_process.stdout else "")
            self.stdout.write(flake8_process.stderr.decode('utf-8')
                              if flake8_process.stderr else "")
            return

        self.stdout.write("Waiting for the database to be available...")
        subprocess.run(['python', 'manage.py', 'wait_for_db'])

        self.stdout.write("Applying database migrations...")
        subprocess.run(['python', 'manage.py', 'migrate'])

        self.stdout.write("Running Django tests...")
        test_process = subprocess.run(
            ['python', 'manage.py', 'test'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if test_process.returncode != 0:
            self.stdout.write(
                self.style.ERROR("Tests failed. Fix them before pushing."))
            self.stdout.write(
                test_process.stdout.decode('utf-8') if test_process.stdout else "")
            self.stdout.write(
                test_process.stderr.decode('utf-8') if test_process.stderr else "")
            return

        self.stdout.write(self.style.SUCCESS("All checks passed! Ready to push."))
