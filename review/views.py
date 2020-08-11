import json, jwt, requests, boto3, os, mimetypes


from django.core.files.base import ContentFile

from wsgiref.util           import FileWrapper
from django.http.response   import StreamingHttpResponse
from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views           import View
from config.settings        import (
    S3URL,
    SECRET_KEY,
    AWS_SECRET_ACCESS_KEY,
    AWS_ACCESS_KEY_ID,
    AWS_STORAGE_BUCKET_NAME
)
from hotels.models          import (
    Hotel,
    Hotel_Detail
)
from .models                import (
    Review,
    Media
)
from .utils                 import (
    RangeFileWrapper,
    range_re
)
from account.models         import User
from account.utils          import (
    login_decorator,
    detoken
)


class ReviewView(View):
    def get(self, request):
        try:
            hotel_name      = request.GET.get("hotel_name",None)
            user            = User.objects.get(name=request.GET.get("user",None))
            reviews         = Review.objects.select_related('user').filter(user = user).all()
            review_list     = [
                {
                    'id'    : review.id,
                    'user'  : review.user.name,
                    'hotel' : review.hotel.name,
                    'star'  : review.star,
                    'title' : review.title,
                    'text'  : review.text,
                    'media' : [media.url for media in review.media_set.all()]
                } for review  in reviews
            ]
            return JsonResponse({"review_list":review_list}, status = 200 )
        except TypeError:
            return JsonResponse({"message":"TYPE_ERROR"}, status = 400 )
        except ValueError:
            return JsonResponse({"message":"VALUE_ERROR"}, status = 400 )
        except ObjectDoesNotExist:
            return JsonResponse({"message":"DOES_NOT_EXIST"}, status = 400 )
    
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    @login_decorator
    def post(self, request):
        try:
            data  = request.POST.dict()
            user  = request.user
            review=Review.objects.create(
                user  = user,
                hotel = Hotel.objects.get(hotel_detail__english_name = data['hotel']),
                star  = data['stars'],
                title = data['title'],
                text  = data['text']
            )
            media = request.FILES['file']
            self.s3_client.upload_fileobj(
                media,
                AWS_STORAGE_BUCKET_NAME,
                media.name,
                ExtraArgs={
                    "ContentType": media.content_type
                }
            )
            media_url = (S3URL+media.name).strip()
            Media(
                url     = media_url,
                review  = review
            ).save()
            return JsonResponse({"message":"SUCCESS"}, status = 200 )
        except TypeError:
            return JsonResponse({"message":"TYPE_ERROR"}, status = 400 )
        except ValueError:
            return JsonResponse({"message":"VALUE_ERROR"}, status = 400 )
        except ObjectDoesNotExist:
            return JsonResponse({"message":"DOES_NOT_EXIST"}, status = 400 )
        
class StreamingView(View):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    def get(self, request): 
        url  = request.GET.get('path',None) 
        video =url.split('/')[-1]
        path = '/home/bjkim/'+video
        self.s3_client.download_file(AWS_STORAGE_BUCKET_NAME,video,path)
        range_header = request.META.get('HTTP_RANGE','').strip()
        range_match  = range_re.match(range_header)
        size         = os.path.getsize(path)
        content_type, encoding = mimetypes.guess_type(path)
        content_type = content_type  or 'application/octet-stream'
        if range_match:
            first_byte, last_byte = range_match.groups()
            first_byte = int(first_byte) if first_byte else 0
            last_byte  = int(last_byte) if last_byte else size - 1
            if last_byte >= size:
                last_byte = size-1
            length = last_byte - first_byte + 1
            resp = StreamingHttpResponse(RangeFileWrapper(open(path,'rb'), offset=first_byte, length=length), status = 206, content_type = content_type)
            resp['Content-Length'] = str(length)
            resp['Content-Range']  = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
        else:
            resp = StreamingHttpResponse(FileWrapper(open(path,'rb')), content_type = content_type)
            resp['Content-Length'] = str(size)
        resp['Accept-Ranges'] = 'bytes'
        return resp