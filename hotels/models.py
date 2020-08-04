from django.db import models

class Country(models.Model):
    country = models.CharField(max_length=255)

    class Meta:
        db_table = "countries"

class City(models.Model):
    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    name    = models.CharField(max_length=255)

    class Meta:
        db_table = "cities"

class Hotel(models.Model):
    country      = models.ForeignKey(Country,on_delete=models.CASCADE)
    city         = models.ForeignKey(City,on_delete=models.CASCADE)
    name         = models.CharField(max_length=255)
    flat         = models.CharField(max_length=255,default="")
    user_rating  = models.DecimalField(max_digits=10,decimal_places=2)
    hotel_detail = models.OneToOneField("HotelDetail",on_delete=models.CASCADE)

    class Meta:
        db_table = "hotels"

class HotelDetail(models.Model):
    hotel_rating         = models.DecimalField(max_digits=10,decimal_places=2)
    english_name         = models.CharField(max_length=255)
    address              = models.CharField(max_length=255)
    lat                  = models.CharField(max_length=255,default="")
    lng                  = models.CharField(max_length=255,default="")
    content              = models.TextField(max_length=2000)
    price                = models.DecimalField(max_digits=10,decimal_places=2)
    price_sale           = models.DecimalField(max_digits=10,decimal_places=2)
    provider_logo        = models.TextField(max_length=1000,default="")
    label                = models.CharField(max_length=255,default="")
    facility             = models.ManyToManyField("Facility",through="HotelFacility")
    amenity              = models.ManyToManyField("Amenity",through="HotelAmenity")
    roomtype             = models.ManyToManyField("Roomtype",through="HotelRoomtype")
    star                 = models.OneToOneField("Star",on_delete=models.CASCADE)
    reservation_start_at = models.DateField(null=True) 
    reservation_end_at   = models.DateField(null=True)

    class Meta:
        db_table = "hotel_details"

class Star(models.Model):
    place        = models.DecimalField(max_digits=10,decimal_places=2)
    cleanliness  = models.DecimalField(max_digits=10,decimal_places=2)
    service      = models.DecimalField(max_digits=10,decimal_places=2)
    price        = models.DecimalField(max_digits=10,decimal_places=2)

    class Meta:
        db_table = "hotel_stars"

class HotelImage(models.Model):
    hotel_detail = models.ForeignKey("HotelDetail",on_delete=models.CASCADE)
    image        = models.ForeignKey("Image",on_delete=models.CASCADE, default="")

    class Meta:
        db_table = "hotel_images"

class Image(models.Model):
    name        = models.CharField(max_length=255)
    image_url   = models.CharField(max_length=1000)

    class Meta:
        db_table = "images"

class HotelFacility(models.Model):
    hotel_detail = models.ForeignKey("HotelDetail", on_delete=models.CASCADE)
    facility     = models.ForeignKey("Facility",on_delete=models.CASCADE, default="")

    class Meta:
        db_table = "hotel_facilities"

class Facility(models.Model):
    name        = models.CharField(max_length=255)

    class Meta:
        db_table = "facilities"

class HotelAmenity(models.Model):
    hotel_detail = models.ForeignKey("HotelDetail",on_delete=models.CASCADE)
    amenity      = models.ForeignKey("Amenity", on_delete=models.CASCADE, default="")

    class Meta:
        db_table = "hotel_amenities"

class Amenity(models.Model):
    name        = models.CharField(max_length=255)

    class Meta:
        db_table = "amenities"


class HotelRoomtype(models.Model):
    hotel_detail  = models.ForeignKey("HotelDetail",on_delete=models.CASCADE)
    roomtype      = models.ForeignKey("Roomtype", on_delete=models.CASCADE, default="")

    class Meta:
        db_table = "hotel_roomtypes"

class Roomtype(models.Model):
    name = models.CharField(max_length=255, default="")

    class Meta:
        db_table = "roomtypes"