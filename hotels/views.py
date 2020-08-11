from django.views import View
from django.http import JsonResponse

from .models import (
    Hotel, 
    Hotel_amenity,
    Hotel_Detail,
    Hotel_Image,
    Image
)
class HotelListViwe(View):
    def get(self, request):
        querydatas = Hotel.objects.prefetch_related("hotel_detail__image_set")[:30]
        data = []
        for querydata in querydatas:
            print(dir(querydata))
            data_dic = {
                "id": querydata.hotel_detail.id,
                'image':[img.image_url for img in Image.objects.filter(id=querydata.image_id)]
            }
            data.append(data_dic)
        return JsonResponse({"data": data}, status=200)

        # hotels = Hotel.objects.prefetch_related('hotel_detail__hotels_image_set').all()
        # hotel_list =[
        #     {
        #         'id':hotel.id,
        #         'name':hotel.name,
        #         'image':[img.image for img in hotel.hotel_detail.hotel_image__set.object.filter(id=t)]
        #     } for hotel in hotels[:30]
        # ]

