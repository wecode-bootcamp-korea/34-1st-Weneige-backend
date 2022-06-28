import jwt

from users.models  import User
from django.conf   import settings
from django.http   import JsonResponse

def login_decorator(func):

    def wrapper(self, request, *args, **kwargs):
        try:
            token         = request.headers.get("Authorization", None)
            token_payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
            user          = User.objects.get(id=token_payload['user_id'])
            request.user  = user

            return func(self, request, *args, **kwargs) 

        except jwt.DecodeError:
            return JsonResponse({'message' : 'INVALID_USER'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status=401)
            
    return wrapper  