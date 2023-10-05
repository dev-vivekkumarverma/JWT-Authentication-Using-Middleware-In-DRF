from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from .models import CustomUser
from .helpers import generate_jwt_token,validate_jwt_token
# Create your views here.

@api_view(["GET"])
def register_user(request):
    print("user:",request.user)
    return Response(data={"result":"new user will be created...."},status=status.HTTP_200_OK)




@api_view(["POST"])
def auth_user(request):
    try:
        # print("request:",dir(request))
        username=request.data.get('username',None)
        password=request.data.get('password',None)
        
        if all([username,password]) and CustomUser.objects.filter(username=username).exists():
            user = CustomUser.objects.get(username=username)
            # print("password:",password,"\n username:",username)
            if user.validate_password(password=password):
                # print("uservalidated##############")
                token=generate_jwt_token(username=username)
                return Response(data={"token":token}, status= status.HTTP_201_CREATED)
            else:
                raise Exception('Invalid username/password')
        else:
            raise Exception('Invalid username/password')

    except Exception as e:
        raise Exception (str(e))