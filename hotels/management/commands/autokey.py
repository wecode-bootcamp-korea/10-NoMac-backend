from django.core.management.base import BaseCommand, no_translations
import csv
import os


class Command(BaseCommand):
    @no_translations
    def handle(self, *args, **options):
        os.system("python manage.py product_menu")
        os.system("python manage.py product_category")
        os.system("python manage.py product_skin")
        os.system("python manage.py product_genre")
        os.system("python manage.py product_line")
        os.system("python manage.py product_online_main")
        os.system("python manage.py product_main")
        os.system("python manage.py product_star")
        os.system("python manage.py product_detail_data")

        os.system("python manage.py review_worry_skintype")
        os.system("python manage.py review_data")

