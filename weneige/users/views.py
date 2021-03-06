import json
import bcrypt
import jwt

from django.core.exceptions import ValidationError
from django.http            import JsonResponse
from django.views           import View
from django.conf            import settings

from .validation            import validate_email, validate_password
from .models                import User

class SignUpView(View):
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

            hashed_password  = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_password = hashed_password.decode('utf-8')

            User.objects.create(
                name          = name,
                email         = email,
                password      = decoded_password,
                user_name     = user_name,
                address       = address,
                mobile_number = mobile_number
            )
        
            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status = 201)
        
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)

        except ValidationError as e:
            return JsonResponse({'MESSAGE' : (e.message)}, status = 400)

class LogInView(View):
    def post(self, request):
        try :
            data          = json.loads(request.body)
            user_email    = data['email']
            user_password = data['password']

            if not User.objects.filter(email = user_email).exists():
                return JsonResponse({'MESSAGE' : 'INVALID_EMAIL'}, status = 401)

            user = User.objects.get(email = user_email)

            encoded_user_password = user_password.encode('utf-8')
            encoded_db_password   = user.password.encode('utf-8')

            if not bcrypt.checkpw( encoded_user_password, encoded_db_password ):
                return JsonResponse({'MESSAGE' : 'INVALID_PASSWORD'}, status = 401)

            token = jwt.encode({'user_id' : user.id}, settings.SECRET_KEY, settings.ALGORITHM)
            return JsonResponse({'token' : token}, status = 200)
                
        except KeyError :
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)