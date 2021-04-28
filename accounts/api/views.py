from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_jwt.authentication import  JSONWebTokenAuthentication
from .serializers import *
from accounts.models import *


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    def post(self,request,*args,**kwargs):
        data=request.data
        serializer=LoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data=serializer._validated_data
            return Response({'success':'True','message':'Successfully logged in',
                            'data':new_data},status=200)
        return Response(serializer.errors, status=400)
