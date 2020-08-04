import random

from django.test import TestCase
from django.test import Client

from .utils      import facilities_path
from .models     import (
    Hotel, 
    HotelAmenity,
    HotelDetail,
    HotelImage,
    HotelFacility,
    HotelRoomtype,
    Facility,
    Image,
    Star,
    Amenity,
    Roomtype,
    Country,
    City
)

def create_data():
    country = Country.objects.create(id=1,country="미국")
    City.objects.create(id=1,country_id=country.id,name="하와이 섬")
     
    Amenity.objects.create(id=1,name="목욕 가운")
    Amenity.objects.create(id=2,name="벽난로")
    Amenity.objects.create(id=3,name="하우스키핑")
    Amenity.objects.create(id=4,name="옷장/벽장")

    Facility.objects.create(id=1,name="무료 주차")
    Facility.objects.create(id=2,name="무료 초고속 인터넷(Wi-Fi)")
    Facility.objects.create(id=3,name="온수 욕조")
    Facility.objects.create(id=4,name="무료 조식")

    Roomtype.objects.create(id=1,name="금연실")
    Roomtype.objects.create(id=2,name="스위트")
    Roomtype.objects.create(id=3,name="패밀리 룸")
    Roomtype.objects.create(id=4,name="바다 전망")

    star = Star.objects.create(
        id          = 1,
        place       = 5.0,
        cleanliness = 5.0,
        service     = 5.0,
        price       = 5.0
    )
    star2 = Star.objects.create(
        id          = 2,
        place       = 4.0,
        cleanliness = 4.0,
        service     = 4.0,
        price       = 4.0
    )

    hotel_detail = HotelDetail.objects.create(
        id                   = 1,
        hotel_rating         = 5,
        hotel_special        = "오늘만 특가",
        hotel_special2       = "내일도 특가",
        english_name         = "Gold Hotel",
        address              = "하와이 섬",
        content              = "니가가라 하와이",
        price                = 100000,
        price_sale           = 0,
        provider_logo        = "www.google.com/image",
        label                = "구글",
        star_id              = star.id,
        reservation_start_at = "2020-08-01",
        reservation_end_at   = "2020-08-11",
    )

    hotel_detail2 = HotelDetail.objects.create(
        id                   = 2,
        hotel_rating         = 4,
        hotel_special        = "오늘만 특가",
        hotel_special2       = "내일도 특가",
        english_name         = "Yello Hotel",
        address              = "하와이 섬",
        content              = "니가가라 하와이 동쪽으로",
        price                = 200000,
        price_sale           = 0,
        provider_logo        = "www.naver.com/image",
        label                = "네이버",
        star_id              = star2.id,
        reservation_start_at = "2020-08-15",
        reservation_end_at   = "2020-08-21",
    )

    hotel = Hotel.objects.create(
        id           = 1,
        country_id   = 1,
        city_id      = 1,
        name         = "골드 호텔",
        user_rating  = 5.0,
        flat         = "조식 포함",
        hotel_detail = hotel_detail,
    )
    hotel2 = Hotel.objects.create(
        id           = 2,
        country_id   = 1,
        city_id      = 1,
        name         = "엘로우 호텔",
        user_rating  = 4.0,
        flat         = "",
        hotel_detail = hotel_detail2,
    )
    image = Image.objects.create(
        id        = 1,
        image_url = "www.google.com/image"
    )
    image2 = Image.objects.create(
        id        = 2,
        image_url = "www.naver.com/image"
    )

    HotelImage.objects.create(
        id           = 1,
        hotel_detail = hotel_detail,
        image        = image
    )
    HotelImage.objects.create(
        id           = 2,
        hotel_detail = hotel_detail2,
        image        = image2
    )

    HotelFacility.objects.create(
        id           = 1,
        facility     = Facility.objects.get(pk=1),
        hotel_detail = hotel_detail
    )
    HotelFacility.objects.create(
        id           = 2,
        facility     = Facility.objects.get(pk=2),
        hotel_detail = hotel_detail
    )
    HotelFacility.objects.create(
        id           = 3,
        facility     = Facility.objects.get(pk=3),
        hotel_detail = hotel_detail
    )

    HotelAmenity.objects.create(
        id           = 1,
        amenity      = Amenity.objects.get(pk=1),
        hotel_detail = hotel_detail
    )
    HotelAmenity.objects.create(
        id           = 2,
        amenity      = Amenity.objects.get(pk=2),
        hotel_detail = hotel_detail
    )
    HotelAmenity.objects.create(
        id           = 3,
        amenity      = Amenity.objects.get(pk=3),
        hotel_detail = hotel_detail
    )
    HotelRoomtype.objects.create(
        id            = 1,
        roomtype      = Roomtype.objects.get(pk=1),
        hotel_detail  = hotel_detail
    )
    HotelRoomtype.objects.create(
        id           = 2,
        roomtype      = Roomtype.objects.get(pk=2),
        hotel_detail = hotel_detail
    )
    HotelRoomtype.objects.create(
        id            = 3,
        roomtype      = Roomtype.objects.get(pk=3),
        hotel_detail  = hotel_detail
    )

def delete_data():
    Hotel.objects.all().delete()
    HotelAmenity.objects.all().delete()
    HotelDetail.objects.all().delete()
    HotelImage.objects.all().delete()
    HotelFacility.objects.all().delete()
    HotelRoomtype.objects.all().delete()
    Facility.objects.all().delete()
    Image.objects.all().delete()
    Star.objects.all().delete()
    Amenity.objects.all().delete()
    Roomtype.objects.all().delete()
    Country.objects.all().delete()
    City.objects.all().delete()

class HotelListTest(TestCase):
    maxDiff = None

    def setUp(self):
        create_data()
    def tearDown(self):
        delete_data()
    def test_hotel_list_get_success(self):
        client = Client()
        response = client.get("/hotel")

        hotels = Hotel.objects.prefetch_related(
            "hotel_detail__hotelimage_set",
            "hotel_detail__hotelfacility_set"
        )

        data = [{
            "id"                  : hotel.hotel_detail.id,
            "image"               :[img.image.image_url.replace("w=100","w=300") for img in hotel.hotel_detail.hotelimage_set.select_related("image").all()[:5]],
            "facilities"          :[facility.facility.name for facility in hotel.hotel_detail.hotelfacility_set.select_related("facility").all()[:5]],
            "facilities_path"     :[facilities_path(facility.facility.name) for facility in hotel.hotel_detail.hotelfacility_set.select_related("facility").all()[:5]],
            "flat"                : hotel.flat,
            "name"                : hotel.name,
            "provider_logo"       : hotel.hotel_detail.provider_logo,
            "price"               : str(hotel.hotel_detail.price),
            "price_sale"          : str(hotel.hotel_detail.price_sale),
            "hotel_special"       : hotel.hotel_detail.hotel_special,
            "hotel_special2"      : hotel.hotel_detail.hotel_special2,
            "label"               : hotel.hotel_detail.label,
            "hotel_rating"        : str(hotel.hotel_detail.hotel_rating),
            "review_count_msg"    : f"{hotel.review_set.count()}건의 리뷰",
            "reservation_start_at": str(hotel.hotel_detail.reservation_start_at),
            "reservation_end_at"  : str(hotel.hotel_detail.reservation_end_at),

            }
        } for hotel in hotels]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"data": data})

    def test_hotel_list_get_fail(self):
        client = Client()
        delete_data()
        response = client.get("/hotel/",content_type='application/json')

        self.assertEqual(response.status_code, 404)
   
    def test_hotel_list_get_exception(self):
        client = Client()
        delete_data()
        response = client.get("/hotel",content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "NotExistData"})

class HotelDetailtTest(TestCase):
    maxDiff = None

    def setUp(self):
        create_data()
    def tearDown(self):
        delete_data()
    def test_hotel_list_get_success(self):
        client = Client()
        response = client.get("/hotel/1",content_type='application/json')

        hotels = Hotel.objects.prefetch_related(
            "hotel_detail__hotelimage_set",
            "hotel_detail__hotelfacility_set",
            "hotel_detail__hotelamenity_set",
            "hotel_detail__hotelroomtype_set",
            ).filter(id=1)

        data = [{
            "id"                 : hotel.hotel_detail.id,
            "image"              :[img.image.image_url.replace("w=100","w=500") for img in hotel.hotel_detail.hotelimage_set.select_related("image").all()],
            "facilities"         :[facility.facility.name for facility in hotel.hotel_detail.hotelfacility_set.select_related("facility").all()],
            "amanities"          :[amenity.amenity.name for amenity in hotel.hotel_detail.hotelamenity_set.select_related("amenity").all()],
            "roomtypes"          :[roomtype.roomtype.name for roomtype in hotel.hotel_detail.hotelroomtype_set.select_related("roomtype").all()],
            "name"               : hotel.name,
            "english_name"       : hotel.hotel_detail.english_name,
            "provider_logo"      : hotel.hotel_detail.provider_logo,
            "hotel_rating"       : str(hotel.hotel_detail.hotel_rating),
            "review_count_msg"    : f"{hotel.review_set.count()}건의 리뷰",
            "place"              : str(hotel.hotel_detail.star.place),
            "cleanliness"        : str(hotel.hotel_detail.star.cleanliness),
            "service"            : str(hotel.hotel_detail.star.service),
            "price"              : str(hotel.hotel_detail.star.price),
            "hotelclassification": 4,
            "content"            : hotel.hotel_detail.content,
        } for hotel in hotels]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"data": data})

    def test_hotel_list_get_exception(self):
        client = Client()
        response = client.get("/hotel/5555",content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "NotExistData"})

    def test_hotel_list_get_fail(self):
        client = Client()
        response = client.get("/hotel/5/",content_type='application/json')

        self.assertEqual(response.status_code, 404)