import json
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header
import jwt
import os
import re
from datetime import datetime,timezone,timedelta
from rest_framework import status
from user_app.models import CustomUser
from django.http import JsonResponse
class JWTAuthMiddleWar:

    def __init__(self,get_response) -> None:
        self.get_response=get_response
        self.ignore_url_list=[r'/auth/*',r'/admin/*',r'/user/login/*']

    def __call__(self,request):
        if not any([re.match(urlpattern,request.path) for urlpattern in self.ignore_url_list])  :
            auth_header=get_authorization_header(request=request)
            token= str(auth_header).split(' ')[-1]
            payload=validate_jwt_token(token=token[:-1])
            print("payload:", payload==None, payload is None, payload is not None)
            if payload is None:
                # Response(data={"error":"error Has occured"},status=status.HTTP_400_BAD_REQUEST)
                return JsonResponse(data={"error":"Invalid token.."},status=status.HTTP_400_BAD_REQUEST)
            else:
                request.user= CustomUser(username=payload["username"])
        
        respone = self.get_response(request)
        return respone
         



def generate_jwt_token(username:str):
    key=os.getenv("TOKEN_SECRET_KEY")
    algorithm=os.getenv("ALGORITHMS")  
    payload={
                "username":username,
                "exp":datetime.now(tz=timezone.utc)+timedelta(days=1)
            }
    token=jwt.encode(payload=payload,key=key,algorithm=algorithm)
    return token

def validate_jwt_token(token:str):
    key=os.getenv("TOKEN_SECRET_KEY")
    algorithm=os.getenv("ALGORITHMS")
    try:
        payload= jwt.decode(jwt=token, key=key, algorithms=algorithm)
        return payload
    except Exception as e:
        return None
            