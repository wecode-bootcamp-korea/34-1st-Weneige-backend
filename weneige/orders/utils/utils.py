import jwt

from users.models  import User
from django.conf   import settings
from django.http   import JsonResponse

def login_decorator(func):

    def wrapper(self, request, *args, **kwargs):

        if "Authorization" not in request.headers:
            return JsonResponse({"message" : "INVALID_LOGIN"}, status=401)

        token = request.headers.get("Authorization", None)

        try:
            if token:
                token_payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
                user          = User.objects.get(id=token_payload['user_id'])
                request.user = user

                return func(self, request, *args, **kwargs) 

            return JsonResponse({'message' : "NEED_LOGIN"}, status=401)

        except jwt.DecodeError:
            return JsonResponse({'message' : 'INVALID_USER'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status=401)
            
    return wrapper      