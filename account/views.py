import bcrypt, hashlib, json, jwt, os, requests, sys

from django.http                    import JsonResponse, HttpResponse
from django.views                   import View
from django.core.exceptions         import (
    ValidationError,
    ObjectDoesNotExist
)
from django.core.validators         import validate_email

from my_settings   import (
    SECRET_KEY,
    ALGORITHM
) 
from .models       import User
from account.utils import login_decorator

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            validate_email(data['email'])
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message":"EXISTING_EMAIL"}, status = 400)
            User.objects.create(
                email        = data["email"],
                password     = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt()),
                name         = data["name"],
                login_method = User.LOGIN_USERID
            ).save()
            return JsonResponse({"message":"SUCCESS"}, status = 200)
        except ValidationError:
            return JsonResponse({"message" : "VALIDATION_ERROR"}, status = 400)
        except KeyError:
            return JsonResponse({"message" : "INVALID_KEY"}, status = 400)
        except TypeError:
            return JsonResponse({"message" : "INVALID_TYPE"}, status = 400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            validate_email(data['email'])
            if User.objects.filter(email=data['email']).exists():
                user = User.objects.get(email = data['email'])
                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode({'user':user.id}, SECRET_KEY, algorithm = ALGORITHM).decode('utf-8')
                    return JsonResponse({'token':token}, status = 200)
                return JsonResponse({'message':'WRONG_EMAIL_PASSWORD'},status=400)
            return JsonResponse({'message':'WRONG_EMAIL_PASSWORD'},status=400)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEY'},status=400)
        except ValidationError:
            return JsonResponse({'message':'INVALID_EMAIL'},status=400)

class KakaoLoginView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)
            access_token = data["access_token"]
            profile_request = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            print(profile_request.json())
            profile_json = profile_request.json()
            email = profile_json.get("kakao_account").get("email")
            if email is None:
                return JsonResponse({"message": "이메일을 선택해 주세요."},status=400)
            nickname = profile_json.get("properties").get("nickname")
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
            else:    
                user = User.objects.create(
                    email=email,
                    name=nickname,
                    login_method=User.LOGIN_KAKAO
                )
                user.save()
            if user.login_method != User.LOGIN_KAKAO:
                return JsonResponse({"message": "카카오 로그인이 아닙니다."},status=400)
            access_token = jwt.encode( {"user": user.id}, SECRET_KEY, algorithm="HS256").decode("utf-8")
            return JsonResponse({"message": "SUCESS", "access_token": access_token}, status=200)
        except TypeError:
            return JsonResponse({"message":"TYPE_ERROR"}, status = 400 )
        except ValueError:
            return JsonResponse({"message":"VALUE_ERROR"}, status = 400 )
        except ObjectDoesNotExist:
            return JsonResponse({"message":"DOES_NOT_EXIST"}, status = 400 )

class GoogleLoginView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)
            if User.objects.filter(email=data['email']).exists():
                user = User.objects.get(email=data['email'])
            user = User.objects.create(
                email = data['email'],
                name = data["name"],
                login_method=User.LOGIN_GOOGLE
            )
            access_token = jwt.encode({'user':user.id},SECRET_KEY,algorithm=ALGORITHM).decode('utf-8')
            return JsonResponse({'message':'SUCCESS',"access_token":access_token}, status=200)
        except KeyError:
            return JsonResponse({'message':'INVALID_DATA'}, status=401)

                    