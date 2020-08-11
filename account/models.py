from django.db import models

class User(models.Model):
    LOGIN_USERID = "user"
    LOGIN_KAKAO = "kakao"
    LOGIN_GOOGLE = "google"
    LOGIN_CHOICES = (
        (LOGIN_USERID, "user"),
        (LOGIN_KAKAO, "Kakao"),
        (LOGIN_KAKAO, "google"),
    )
    name            = models.CharField(max_length=255)
    password        = models.CharField(max_length=255, null=True)
    email           = models.EmailField(max_length=255,null=True,blank=True)
    login_method    = models.CharField(max_length=50, choices=LOGIN_CHOICES, default=LOGIN_USERID)
    created_at      = models.DateTimeField(auto_now_add = True)
    updated_at      = models.DateTimeField(auto_now = True)


    class Meta:
        db_table = 'users'