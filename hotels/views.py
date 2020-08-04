import random

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Prefetch
from django.shortcuts import render

from .utils           import facilities_path
from .models          import (
    Hotel, 
    HotelAmenity,
    HotelDetail,
    HotelImage,
    Facility,
    Image
)



class HotelListView(View):
    def get(self, request):
        page = int(request.GET.get("page", 1))
        s_facilities = request.GET.get("facilities","all").split(",")
        s_price = request.GET.get("price",-1)
        s_user_rating = request.GET.get("user_rating","all")
        s_row_price = request.GET.get("row_price","all")
        s_check_in_date = request.GET.get("checkin","2020-08-01")
        s_check_out_date = request.GET.get("checkout","9999-01-01")
        page_size = 30
        end_offset = page_size * page
        start_offset = end_offset - page_size

        filter_args = {}
        exclude_args = {}
        order_by = str()
        
        filter_args["hotel_detail__reservation_start_at__gte"] = s_check_in_date
        filter_args["hotel_detail__reservation_end_at__lte"] = s_check_out_date

        if s_facilities[0] != "all" :
            filter_args["hotel_detail__hotelfacility__facility__name__in"] = s_facilities
        
        if s_price != -1:
                filter_args["hotel_detail__price__range"] = (1,s_price)

        if s_user_rating != "all":
            order_by = "-user_rating"

        if s_row_price != "all":
            order_by = "hotel_detail__price"
            exclude_args["hotel_detail__price"] = 0

        if order_by == "":
            order_by = "id"
        hotels = Hotel.objects.prefetch_related(
            Prefetch("hotel_detail__hotelimage_set"),
            Prefetch("hotel_detail__hotelfacility_set"),
            Prefetch("review_set"),
        ).filter(**filter_args).order_by(order_by,"id").exclude(**exclude_args).distinct()

        if hotels.count() == 0:
            return JsonResponse({"message": "NotExistData"}, status=401)

        hotel_total_count = hotels.count()

        data = [{
            "id"                  : hotel.hotel_detail.id,
            "image"               :[img.image.image_url.replace("w=100","w=300") for img in hotel.hotel_detail.hotelimage_set.select_related("image").all()[:5]],
            "facilities"          :[facility.facility.name for facility in hotel.hotel_detail.hotelfacility_set.select_related("facility").all()[:5]],
            "facilities_path"     :[facilities_path(facility.facility.name) for facility in hotel.hotel_detail.hotelfacility_set.select_related("facility").all()[:5]],
            "flat"                : hotel.flat,
            "name"                : hotel.name,
            "provider_logo"       : hotel.hotel_detail.provider_logo,
            "price"               : hotel.hotel_detail.price,
            "price_sale"          : hotel.hotel_detail.price_sale,
            "hotel_special"       : hotel.hotel_detail.hotel_special,
            "hotel_special2"      : hotel.hotel_detail.hotel_special2,
            "label"               : hotel.hotel_detail.label,
            "hotel_rating"        : float(hotel.hotel_detail.hotel_rating),
            "review_count_msg"    : f"{hotel.review_set.count()}건의 리뷰",
            "user_rating"         : hotel.user_rating,
            "reservation_start_at": hotel.hotel_detail.reservation_start_at,
            "reservation_end_at"  : hotel.hotel_detail.reservation_end_at,
            "hotels_count"        : hotels.count(),
        } for hotel in hotels[start_offset:end_offset]]

        return JsonResponse({"data": data,"hotel_count":hotel_total_count}, status=200)

class HotelDetailView(View):
    def get(self, request, pk):
        hotels = Hotel.objects.prefetch_related(
            "hotel_detail__hotelimage_set",
            "hotel_detail__hotelfacility_set",
            "hotel_detail__hotelamenity_set",
            "hotel_detail__hotelroomtype_set",
            ).filter(id=pk)

        data = [{
            "id"                 : hotel.hotel_detail.id,
            "image"              :[img.image.image_url.replace("w=100","w=500") for img in hotel.hotel_detail.hotelimage_set.select_related("image").all()],
            "facilities"         :[facility.facility.name for facility in hotel.hotel_detail.hotelfacility_set.select_related("facility").all()],
            "amanities"          :[amenity.amenity.name for amenity in hotel.hotel_detail.hotelamenity_set.select_related("amenity").all()],
            "roomtypes"          :[roomtype.roomtype.name for roomtype in hotel.hotel_detail.hotelroomtype_set.select_related("roomtype").all()],
            "name"               : hotel.name,
            "english_name"       : hotel.hotel_detail.english_name,
            "provider_logo"      : hotel.hotel_detail.provider_logo,
            "hotel_rating"       : hotel.hotel_detail.hotel_rating,
            "review_count_msg"    : f"{hotel.review_set.count()}건의 리뷰",
            "place"              : hotel.hotel_detail.star.place,
            "cleanliness"        : hotel.hotel_detail.star.cleanliness,
            "service"            : hotel.hotel_detail.star.service,
            "price"              : hotel.hotel_detail.star.price,
            "hotelclassification": random.randint(3,5),
            "content"            : hotel.hotel_detail.content,
            "address"            : hotel.hotel_detail.address,
        } for hotel in hotels]

        return JsonResponse({"data": data}, status=200)

class MapView(View):
    def get(self, request):
        s_user_rating = request.GET.get("user_rating",1)

        filter_args = {}
        exclude_args = {}

        if s_user_rating == "1":
            filter_args["user_rating__range"] = (s_user_rating,int(s_user_rating)+1)
        elif s_user_rating == "2":
            filter_args["user_rating__range"] = (int(s_user_rating)-1,int(s_user_rating)+1)
        else:
            print(int(s_user_rating)+0.5)
            filter_args["user_rating__range"] = (int(s_user_rating)+0.5,int(s_user_rating)+1)

        exclude_args["hotel_detail__price"] = 0

        hotels = Hotel.objects.prefetch_related(
            "hotel_detail__hotelimage_set",
            ).filter(**filter_args).order_by("id").exclude(**exclude_args).distinct()

        data = [{
            "id"                 : hotel.hotel_detail.id,
            "image"              :[img.image.image_url.replace("w=100","w=500") for img in hotel.hotel_detail.hotelimage_set.select_related("image")[:1]],
            "hotel_rating"       : hotel.hotel_detail.hotel_rating,
            "user_rating"        : hotel.user_rating,
            "name"               : hotel.name,
            "review_count_msg"   : f"{hotel.review_set.count()}건의 리뷰",
            "price"               : hotel.hotel_detail.price,
            "lat"                : hotel.hotel_detail.lat,
            "lng"                : hotel.hotel_detail.lng,
        } for hotel in hotels]
        return JsonResponse({"data": data}, status=200)
