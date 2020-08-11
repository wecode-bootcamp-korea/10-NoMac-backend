from django.db import models

from hotels.models  import Hotel
from account.models import User

class Review(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel   = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    star    = models.DecimalField(max_digits=2, decimal_places=1)
    title   = models.CharField(max_length=250)
    text    = models.TextField()

    class Meta:
        db_table = 'reviews'

class Media(models.Model):
    url     = models.URLField()
    review  = models.ForeignKey(Review, on_delete=models.CASCADE)

    class Meta:
        db_table = 'media'


