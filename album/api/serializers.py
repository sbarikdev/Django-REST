
from django.db.models import Q
from rest_framework.exceptions import APIException
from rest_framework.serializers import *
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from accounts.exceptions import APIException400
from ..models import *

from django.db.models import Q
import uuid

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER



class CreateAlbumMusicSerializer(ModelSerializer):
    title = CharField(error_messages={'required':'title key is required', 'blank':'title is required'})
    dance_ability = CharField(allow_blank=True)
    energy = CharField(allow_blank=True)
    mode = CharField(allow_blank=True)
    acousticness = CharField(allow_blank=True)
    tempo = CharField(allow_blank=True)
    Duration_ms = serializers.CharField(allow_blank=True)
    Num_sections = serializers.CharField(allow_blank=True)
    Num_segments = CharField(allow_blank=True)
    
    class Meta:
        model = Music
        fields= ['title','dance_ability','energy','mode','acousticness','tempo',
        'Duration_ms','Num_sections','Num_segments']

    def validate(self,data):
        title       = data['title']
        dance_ability               = data['dance_ability']
        energy                      = data['energy']
        mode                        = data['mode']
        acousticness                = data['acousticness']

        if not title or title == "":
            raise APIException400({"message":"Please provide title"})
        return data        
      
    def create(self,validated_data):
        title                       = validated_data['title']
        dance_ability               = validated_data['dance_ability']
        energy                      = validated_data['energy']
        mode                        = validated_data['mode']
        acousticness                = validated_data['acousticness']
        tempo                       = validated_data['tempo']
        Duration_ms                 = validated_data['Duration_ms']
        Num_sections                = validated_data['Num_sections']
        Num_segments                = validated_data['Num_segments']

        restaurant_obj = Music.objects.create(
            title=title,
            dance_ability=dance_ability,
            energy=energy,
            mode=mode,
            acousticness=acousticness,
            tempo=tempo,
            Duration_ms=Duration_ms,
            Num_sections=Num_sections,
            Num_segments=Num_segments,) 
        return validated_data    



class AlbumMusicSerializer(ModelSerializer):
    class Meta:
        model = Music
        fields = "__all__"


class CreateRatingsSerializer(ModelSerializer):
    rating = CharField(error_messages={'required':'rating key is required', 'blank':'rating is required'})
    music_id = CharField(error_messages={'required':'music_id key is required', 'blank':'music_id is required'})
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Music
        fields= ['rating','music_id','user']

    def validate(self,data):
        rating                 = data['rating']
        music_id               = data['music_id']

        if not rating or rating == "":
            raise APIException400({"message":"Please provide rating"})
        if rating:
            # if not rating.isdigit():
            #     raise ValidationError({"message": "please provide valid rating"})
            if float(rating) > 5.0:
                raise ValidationError({"message": "maximum rating is 5"})
        if not music_id or music_id == "":
            raise APIException400({"message":"Please provide music"})
        if music_id:
            if not music_id.isdigit():
                raise ValidationError({"message": "Invalid music ID"})
            qs = Music.objects.filter(id=music_id)
            if not qs.exists():
                raise APIException400({
                'success' : 'False',
                'message' : 'music ID does not exist'})
        return data        
      
    def create(self,validated_data):
        rating              = validated_data['rating']
        music_id               = validated_data['music_id']
        validated_data['user'] = User.objects.get(id=self.context['request'].user.id)

        restaurant_obj = Ratings.objects.create(
            rating=rating,
            music_id=music_id,
            user=validated_data['user'],) 
        return validated_data    


