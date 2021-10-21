from django.core.management.base import BaseCommand
from django.db import connection, migrations

import os

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        try:
            file_path = os.path.join(os.path.dirname(__file__), '../../../', 'triggers.sql')
            sql_statement = open(file_path).read()
        except:
            print("Can't find the triggers.sql file!")

        with connection.cursor() as c:
            c.execute(sql_statement)

        # return 1