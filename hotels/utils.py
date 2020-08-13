from faker import Faker
import datetime
import time

def facilities_path(name):
    icon_name = name.strip()
    if icon_name == "무료 인터넷" or icon_name == "인터넷":
        return "/images/internet.png"
    elif icon_name == "무료 주차" or icon_name == "발렛주차" or icon_name == "호텔 내 호텔 전용 유료 주차장":
        return "/images/parking.png"
    elif icon_name == "안전조치 이행":
        return "/images/safety.png"
    elif icon_name == "해변":
        return "/images/sun.png"
    elif icon_name == "수영장" or icon_name == "풀":
        return "/images/swimmer.png"
    elif icon_name == "무료 와이파이" or icon_name == "무료 초고속 인터넷(Wi-Fi)" or icon_name == "Wi-Fi":
        return "/images/wifi.png"
    elif icon_name == "음식":
        return "/images/food.png"
    elif icon_name == "바/라운지":
        return "/images/bar.png"
    elif icon_name == "헬스장/피트니스 센터":
        return "/images/fitness.png"
    else:
        return "/images/favicon.png"
        
def create_date():
    fake = Faker()

    base_date = datetime.date(year=2020, month=8, day=1)
    
    start_date = fake.date_between(start_date=base_date, end_date='+30d')
    end_date = fake.date_between(start_date=base_date, end_date='+30d')
    temp_date = fake.date_between(start_date=base_date, end_date='+30d')

    if start_date >= end_date:
        temp_date = start_date
        start_date = end_date
        end_date = temp_date
    elif start_date == end_date:
        end_date = fake.date_between(start_date=start_date, end_date='+2d')

    return start_date,end_date