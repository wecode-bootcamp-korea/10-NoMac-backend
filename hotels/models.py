from django.db import models

class Country(models.Model):
    country = models.CharField(max_length=255)

    class Meta:
        db_table = "countries"

class City(models.Model):
    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    city    = models.CharField(max_length=255)

    class Meta:
        db_table = "cities"

class Hotel(models.Model):
    country      = models.ForeignKey(Country,on_delete=models.CASCADE)
    city         = models.ForeignKey(City,on_delete=models.CASCADE)
    name         = models.CharField(max_length=255)
    flat         = models.CharField(max_length=255,default="")
    user_rating  = models.DecimalField(max_digits=10,decimal_places=2)
    hotel_detail = models.ForeignKey("Hotel_Detail",on_delete=models.CASCADE)

    class Meta:
        db_table = "hotels"

class Hotel_Detail(models.Model):
    hotel_rating   = models.DecimalField(max_digits=10,decimal_places=2)
    hotel_special  = models.CharField(max_length=255)
    hotel_special2 = models.CharField(max_length=255)
    english_name   = models.CharField(max_length=255)
    address        = models.CharField(max_length=255)
    content        = models.TextField(max_length=2000)
    price          = models.DecimalField(max_digits=10,decimal_places=2)
    price_sale     = models.DecimalField(max_digits=10,decimal_places=2)
    provider_logo  = models.TextField(max_length=1000,default="")
    label          = models.CharField(max_length=255,default="")
    star_id        = models.ForeignKey("Star",on_delete=models.CASCADE)

    class Meta:
        db_table = "hotels_details"

    
class Star(models.Model):
    place        = models.DecimalField(max_digits=10,decimal_places=2)
    cleanliness  = models.DecimalField(max_digits=10,decimal_places=2)
    service      = models.DecimalField(max_digits=10,decimal_places=2)
    price        = models.DecimalField(max_digits=10,decimal_places=2)

    class Meta:
        db_table = "hotels_stars"

class Hotel_Image(models.Model):
    hotel_detail = models.ForeignKey("Hotel_Detail",on_delete=models.CASCADE)
    image        = models.ForeignKey("Image",on_delete=models.CASCADE)

    class Meta:
        db_table = "hotels_images"

class Image(models.Model):
    name        = models.CharField(max_length=255)
    image_url   = models.CharField(max_length=1000)

    class Meta:
        db_table = "images"

class Hotel_Facility(models.Model):
    hotel_detail = models.ForeignKey("Hotel_Detail",on_delete=models.CASCADE)
    facility     = models.ForeignKey("Facility",on_delete=models.CASCADE)

    class Meta:
        db_table = "hotels_facilities"

class Facility(models.Model):
    name        = models.CharField(max_length=255)

    class Meta:
        db_table = "facilities"

class Hotel_amenity(models.Model):
    hotel_detail = models.ForeignKey("Hotel_Detail",on_delete=models.CASCADE)
    amenity      = models.ForeignKey("Amenity",on_delete=models.CASCADE)

    class Meta:
        db_table = "hotels_amenities"

class Amenity(models.Model):
    name        = models.CharField(max_length=255)

    class Meta:
        db_table = "amenities"


class Hotel_Roomtype(models.Model):
    hotel_detail = models.ForeignKey("Hotel_Detail",on_delete=models.CASCADE)
    roomtype      = models.ForeignKey("Roomtype",on_delete=models.CASCADE,default="")

    class Meta:
        db_table = "hotels_roomtypes"

class Roomtype(models.Model):
    name        = models.CharField(max_length=255,default="")

    class Meta:
        db_table = "roomtypes"
        