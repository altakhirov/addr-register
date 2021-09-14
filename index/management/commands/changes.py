import subprocess

from django.core.management import BaseCommand

from index import tasks


class Command(BaseCommand):

    def handle(self, **options):
        # subprocess.run(["python", "manage.py", "migrate"])
        subprocess.run(["sudo", "service", "supervisor", "start"])
        subprocess.run(["sudo", "supervisorctl", "reread"])
        subprocess.run(["sudo", "supervisorctl", "update"])
        subprocess.run(["sudo", "supervisorctl", "restart", "celery"])
        subprocess.run(["python", "manage.py", "collectstatic", "--noinput"])
        # tasks.fucking_parser.apply_async()
        # print('Объекты будут добавляться/индексироваться в фоновом режиме.')
