from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import *
from ..models import *
from accounts.exceptions import *

import datetime
from datetime import timedelta
import uuid


class CreateMusicAPIView(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        # user = request.user
        # print(user)
        data           = request.data
        print(data)
        serializer =  CreateAlbumMusicSerializer(data=data, context = {'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'success' :'True','message' : 'music added successfully','data' : serializer.data},status=200)
        error_keys = list(serializer.errors.keys())
        if error_keys:
            error_msg = serializer.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        #return Response(serializer.errors, status=400)

from django.core.paginator import Paginator

class MusicListView(ListAPIView):
    # permission_classes = (IsAuthenticated,)
    def get(self,request,*args,**kwargs):
        # user = request.user
        _id = self.request.GET.get('id', None)
        if _id:
            try:
                queryset = Music.objects.filter(id=_id)
            except:
                return Response({
                    'success' : 'False',
                    'message' : 'No matched record found'},status=400)
        else:
            queryset = Music.objects.all()
        # print(queryset.query)
        search_result = queryset.count()
        from django.core.paginator import Paginator
        page_number = self.request.query_params.get('page_number ', 1)
        page_size = self.request.query_params.get('page_size ', 10)
        paginator = Paginator(queryset , page_size)
        serializer = AlbumMusicSerializer(paginator.page(page_number) , many=True, context={'request':request})
        # -----------------------------------------------------------
        # serializer = AlbumMusicSerializer(queryset, many=True, context={'request':request})
        data = serializer.data
        # # print(data)
        # # print('data_id', data['id'])
        # for r in data:
        #     qs = Ratings.objects.filter(music__id=r['id'])
        #     if qs:
        #         r['ratings'] = True
        #     else:
        #         r['ratings'] = None

        if data:
            return Response({
                'success' : 'True',
                'message' : 'Data retrieved successfully',
                'search_result': search_result,
                'data'    : data,
            },status=200)
        else:
            return Response({
                'message':'No data to retrieve',
                'success':'False'
            },status=400)


from django.db.models import Q
class CreateRatingsAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        user = request.user
        print(user)
        data           = request.data
        print(data)
        qs = Ratings.objects.filter(Q(user=user)&Q(music=data['music_id']))
        if qs.exists():
            raise APIException({'message':'this user already rated to this music'})
        serializer =  CreateRatingsSerializer(data=data, context = {'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'success' :'True','message' : 'ratings added successfully','data' : serializer.data},status=200)
        error_keys = list(serializer.errors.keys())
        if error_keys:
            error_msg = serializer.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        #return Response(serializer.errors, status=400)

