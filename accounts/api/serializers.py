from rest_framework.serializers import *
from rest_framework import serializers
from accounts.exceptions import *
from accounts.models import *
from django.db.models import Subquery,Q, Max

from django.contrib.auth import get_user_model
User = get_user_model()



from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler  = api_settings.JWT_ENCODE_HANDLER

class LoginSerializer(ModelSerializer):
    password            =   serializers.CharField(allow_blank=True,label='Password',style={'input_type':'password'},write_only=True)
    email               =   serializers.CharField(allow_blank=True)
    token               =   serializers.CharField(read_only=True)
    
    class Meta:
        model  = User
        fields = ['email','password','token']    
        
    def validate(self,data):
        email            =  data['email']
        password         =  data['password']
            
        if not email or email =='':
            raise APIException400({
                'success' : 'False',
                'message' : 'Please provide email'}) 
        if not password or password == '':
            raise APIException400({
                'success' : 'False',
                'message' : 'Password is required'})    

        user_obj = ''
      
        #Email Validation
        if email:            
            user_qs =  User.objects.filter(email__iexact = email)
            if user_qs.exists() and user_qs.count() == 1:
                user_obj =  user_qs.first()
            else:
                raise APIException400({
                    'success' : 'False',
                    'message' : 'User with this email does not exist'})

        # password Validation
        # if len(password)<8:
        #     raise APIException400({
        #         'success':"False",
        #         'message':'Password must be at least 8 characters',
        #     })
        
        if user_obj:
            if not user_obj.check_password(password):
                raise APIException400({
                    'success'  : 'False',
                    'message'  : 'Wrong Password'})
                

        payload = jwt_payload_handler(user_obj)
        token   = jwt_encode_handler(payload)
        data['token']           = 'JWT '+str(token)        
        data['email']           = user_obj.email
        password = data.pop('password', None)
    
        return data 

