import os
import django
import csv
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE","config.settings")
django.setup()

from hotels.models import *
from account.models import *
from review.models import *

CSV_PATH = ['../hawaii.csv']
CSV_PATH.append('../hawaii2.csv')
CSV_PATH.append('../hawaii3.csv')
CSV_PATH.append('../hawaii4.csv')
CSV_PATH.append('../hawaii5.csv')
CSV_PATH.append('../hawaii6.csv')


for CSV in CSV_PATH:
    with open(CSV) as in_file:
        data_reader = csv.reader(in_file)
        for row in data_reader:
            english_name = row[0]
            user_name    = row[1]
            stars        = row[2]
            review_title = row[3]
            review_text  = row[4]  
            
            if Hotel.objects.filter(hotel_detail__english_name = english_name).exists():
                print(english_name,user_name,stars,review_title,review_text)
                try:
                    user = User.objects.get(name = user_name)
                except:
                    User(
                        name= user_name
                    ).save()
                Review(
                    user=User.objects.get(name=user_name),
                    hotel=Hotel.objects.filter(hotel_detail__english_name=english_name)[0],
                    star=stars,
                    title=review_title,
                    text=review_text
                ).save()
            

                
