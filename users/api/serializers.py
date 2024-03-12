from users.models import User,Chat
from rest_framework import serializers
# from rest_framework_simplejwt.serializers import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken


class UpdateProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(read_only=True)
    class Meta:
        model=User
        fields = ['phone_number','full_name','image','birth_date']
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class GetUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['pk','phone_number','full_name','image','birth_date','is_staff','is_superuser']
    


class LoginUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['pk','status','full_name','birth_date','phone_number','image']

 
#class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#    @classmethod
#    
#    def get_token(cls, user):
#        token = super().get_token(user)
#        return token
#    


class RegistrationSerializer(serializers.ModelSerializer):
    #password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields =  ['phone_number','password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def save(self):
        #password = self.validated_data['password']
        #password2 = self.validated_data['password2']
#
        #if password != password2:
        #    raise serializers.ValidationError(
        #        {'error': 'passwords did not match'})
    #            User.objects.create(phone_number=self.validated_data['phone_number'],
        user = User(phone_number=self.validated_data['phone_number'],is_active=True)
        user.set_password(self.validated_data['password'])
        user.save()
        return user


class ResetPasswordSerializer(serializers.Serializer):
    
    phone_number = serializers.CharField()


class ResetPasswordConfirmView(serializers.Serializer):
    phone_number = serializers.CharField()
    otp = serializers.CharField()



        
class SetPasswordSerializer(serializers.ModelSerializer):

    password = serializers.CharField(style={'input_type': 'password'}, write_only=True,required=True)
    class Meta:
        model = User
        fields =  ['password']
    



                    
class VerifyOTPSerializer(serializers.Serializer):

    phone_number = serializers.CharField()
    otp = serializers.CharField()
    #fcm_token = serializers.CharField()



class GetUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'full_name','tarif','birth_date','phone_number']




# class CustomTokenRefreshViewSerializer(TokenRefreshView):
#     def validate(self, attrs):
#         # The default result (access/refresh tokens)
#         data = super(CustomTokenRefreshViewSerializer, self).validate(attrs)
#         # Custom data you want to include
#         data.update({'user': self.user.username})
#         data.update({'id': self.user.id})
#         # and everything else you want to send in the response
#         return data

# class LoginTokenGenerationSerializer(serializers.Serializer):
#     phone_number = serializers.phone_numberField()
#     password = serializers.CharField()
    
    

class AdminLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)
        
class AdminConfirmSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=255)
    otp = serializers.CharField()




class ChatSerializer(serializers.ModelSerializer):
    time_created = serializers.ReadOnlyField(read_only=True)
    class Meta:
        model = Chat
        fields = ['text_body', 'time_created', 'image']


class ChangeLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['language']
class GoogleLoginSer(serializers.Serializer):
    token = serializers.CharField()
class FacebookLoginSer(serializers.Serializer):
    token = serializers.CharField()