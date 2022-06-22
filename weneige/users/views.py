from ctypes import addressof
import json
from unicodedata import name
import bcrypt
import jwt

from django.core.exceptions import ValidationError
from django.shortcuts       import render
from django.http            import JsonResponse
from django.views           import View

from .validation            import validate_email, validate_password
from .models                import User
from weneige.settings     import SECRET_KEY, ALGORITHM

class SignUp(View):
    def post(self, request):
        try :
            data = json.loads(request.body)
            name          = data['name']
            email         = data['email']
            password      = data['password']
            user_name     = data['user_name']
            address       = data['address']
            mobile_number = data['mobile_number']

            validate_email(email)
            validate_password(password)
            
            if User.objects.filter(email = email).exists():
                return JsonResponse({'MESSAGE' : 'ALREADY_EXISTS_EMAIL'}, status=400)
            
            if User.objects.filter(user_name = user_name).exists():
                return JsonResponse({'MESSAGE' : 'ALREADY_EXISTS_USER_NAME'}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_password = hashed_password.decode('utf-8')

            User.objects.create(
                name          = first_name,
                email         = last_name,
                password      = user_name,
                user_name     = email,
                address       = decoded_password,
                mobile_number = mobile_number
            )
        
            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status = 201)
        
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)

        except ValidationError as e:
            return JsonResponse({"MESSAGE" : (e.message)}, status = 400)

class LogIn(View):
    def post(self, request):
        
        try :
            data = json.loads(request.body)
            user_email         = data['email']
            user_password      = data['password']

            if not User.objects.filter(email = user_email).exists():
                return JsonResponse({'MESSAGE' : 'INVALID_EMAIL'}, status = 401)

            user = User.objects.get(email = user_email)

            encoded_user_password = user_password.encode('utf-8')
            encoded_db_password = user.password.encode('utf-8')

            if not bcrypt.checkpw( encoded_user_password, encoded_db_password ):
                return JsonResponse({'MESSAGE' : 'INVALID_PASSWORD'}, status = 401)

            token = jwt.encode({'user_id' : user.id}, SECRET_KEY, ALGORITHM)
            return JsonResponse({'token' : token}, status = 200)
                
        except KeyError :
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)