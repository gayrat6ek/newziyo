from .serializers import RegistrationSerializer, AdminLoginSerializer, GetUserListSerializer, SetPasswordSerializer, GetUserDataSerializer, LoginUserSerializer, VerifyOTPSerializer, ResetPasswordSerializer, ResetPasswordConfirmView, UpdateProfileSerializer
from .serializers import ChangeLanguageSerializer, GoogleLoginSer,FacebookLoginSer
from rest_framework import generics,status
from .serializers import ChatSerializer
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from users.emails import phone_or_mail
from users.models import User,Chat
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q


class MyCustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'page_size': self.page_size,
            'total_objects': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page_number': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })





usr = get_user_model()

class UpdateProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UpdateProfileSerializer
    queryset = usr.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.data = {'success':True,'userdata':response.data}
        return response
    def update(self, request, *args, **kwargs):

        response = super().update(request, *args, **kwargs)
        response.data = {"success":True,"userdata":response.data}
        return response


class LoginUserView(generics.GenericAPIView):
    serializer_class = AdminLoginSerializer
    def post(self, request):
        phone_number = request.data['phone_number']
        password = request.data['password']
        user = authenticate(phone_number=phone_number, password=password)
        if not user:
            return Response({"Message": 'Incorrect authentication details', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        user_data = User.objects.filter(phone_number=phone_number)
        serializer = LoginUserSerializer(user_data,many=True)
        
        #statuss = str(user_data.status)
        statuss = serializer.data[0]['status']
        if statuss=='inactive':
            return Response({"Message": 'Incorrect authentication details', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        access = str(AccessToken.for_user(user))
        return Response({"Message":'Authentication method is correct','access':access,'success':True,'userdata':serializer.data[0]},status=status.HTTP_200_OK)






class RegistrationAPIView(generics.GenericAPIView):
    '''Registers user'''
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        #data = {}
        user_status = ''
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            data = serializer.data['phone_number']
            user_obj = User.objects.get(phone_number=data)
            user_obj.status = 'inactive'
            user_obj.save()
            issended = phone_or_mail(serializer.data['phone_number'])
            if issended is False:
                return Response({"Message":'invalid phone or phone_number','success':False},status=status.HTTP_400_BAD_REQUEST)
            return Response({"Message":'Registration Successful. Otp sended to your mail please verify it and login','success':True},status=status.HTTP_200_OK)

        elif user_status=='active':
            return Response({"Message":'Status active please login','success':False},status=status.HTTP_404_NOT_FOUND)
        else:
            phone_or_mail(serializer.data['phone_number'])
            return Response({"Message":'User exist but not active, Otp is sended','success':True},status=status.HTTP_200_OK)
    



    
class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.filter(phone_number=serializer.data['phone_number'])
            
            if list(user.values()):
                issended = phone_or_mail(serializer.data['phone_number'])
                if issended is False:
                    return Response({"Message":'invalid phone or phone_number','success':False},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'Message':'there is no user with this phone number ','success':False},status=status.HTTP_204_NO_CONTENT)
            #issended = phone_or_mail(serializer.data['phone_number'])
            #if issended is False:
            #    return Response({"Message":'invalid phone or phone_number','success':False},status=status.HTTP_400_BAD_REQUEST)
            return Response({"Message":'Otp is sended to your number','success':True},status=status.HTTP_200_OK)

class ResetPasswordConfirmView(generics.GenericAPIView):
    serializer_class = ResetPasswordConfirmView
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.data['phone_number']
            otp = serializer.data['otp']
            try:
                user_obj = User.objects.get(phone_number=phone_number)
                data = {}
                if user_obj.otp == otp:
                    user_obj.status = 'active'
                    user_obj.save()
                    
                    refresh = RefreshToken.for_user(user=user_obj)
                    data['refresh'] = str(refresh)
                    data['access'] = str(refresh.access_token)
                    return Response({"refresh":data['refresh'],"access":data['access'],'success':True},status=status.HTTP_200_OK)
                return Response({"Message":'Otp doesnot match','success':False},status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"Message":'Bad request','success':False},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Message":'Incorrect Auth methods','success':False},status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPAPIView(generics.GenericAPIView):
    serializer_class = VerifyOTPSerializer
    def post(self, request, *args, **kwargs):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.data['phone_number']
            otp = serializer.data['otp']
            try:
                user_obj = User.objects.get(phone_number=phone_number)
                data = {}
                userser = LoginUserSerializer(user_obj)
                if user_obj.otp == otp:
                    user_obj.status = 'active'
                    user_obj.save()
                    refresh = RefreshToken.for_user(user=user_obj)
                    data['access'] = str(refresh.access_token)
                    return Response({"access":data['access'],'success':True,'userdata':userser.data},status=status.HTTP_200_OK)
                return Response({"Message":'Otp doesnot match','success':False},status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"Message":'Bad request','success':False},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Message":'Incorrect Auth methods','success':False},status=status.HTTP_400_BAD_REQUEST)

class SetPasswordView(generics.GenericAPIView):
    serializer_class = SetPasswordSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            password1 = request.data['password']
            user = request.user
            user.set_password(password1)
            user.save()
        return Response({"Message":'Password set succesful','success':True},status=status.HTTP_200_OK)


class GetUserDataView(generics.ListAPIView):
    serializer_class = GetUserDataSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response({"userdata":serializer.data,'success':True},status=status.HTTP_200_OK)





class LogoutBlacklistTokenUpdateView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:

            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"Message":'Your are logged out','success':False},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            
            return Response({"Message":'token invalid','success':False},status=status.HTTP_404_NOT_FOUND)


class AdminLogin(generics.GenericAPIView):
    serializer_class = AdminLoginSerializer
    def post(self, request):
        phone_number = request.data['phone_number']
        password = request.data['password']
        try:
            user = User.objects.get(phone_number=phone_number)
            user = authenticate(phone_number=phone_number,password=password)
            if not user:
                return Response({'message':'you cannot login to this page','success':False},status=status.HTTP_404_NOT_FOUND)
            if user.is_superuser|user.is_staff is False:
                return Response({'message':'you are not super user','success':False},status=status.HTTP_400_BAD_REQUEST)
            issended = phone_or_mail(phone_number)
            if issended is False:
                return Response({"Message": 'invalid phone or email', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"Message": 'Message has been send successfull','success':True},status=status.HTTP_200_OK)
            #refresh = RefreshToken.for_user(user=user)
            #data['refresh'] = str(refresh)
            #data['access'] = str(refresh.access_token)
            
            
        except:
            return Response({'Message':'given cridentials is not True','success':False},status=status.HTTP_400_BAD_REQUEST)


class AdminVerifyOTPAPIView(generics.GenericAPIView):
    serializer_class = VerifyOTPSerializer
    def post(self, request, *args, **kwargs):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.data['phone_number']
            otp = serializer.data['otp']
            try:
                user_obj = User.objects.get(phone_number=phone_number)
                data = {}
                #need to add --> user_obj.otp
                if user_obj.otp == otp and user_obj.is_superuser|user_obj.is_staff:
                    user_obj.status = 'active'
                    user_obj.save()
                    refresh = RefreshToken.for_user(user=user_obj)
                    data['refresh'] = str(refresh)
                    data['access'] = str(refresh.access_token)
                    return Response({"refresh":data['refresh'],"access":data['access'],'success':True},status=status.HTTP_200_OK)
                return Response({"Message":'Otp doesnot match','success':False},status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"Message":'Bad request','success':False},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Message":'Incorrect Auth methods','success':False},status=status.HTTP_400_BAD_REQUEST)


class GetUserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = GetUserListSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = MyCustomPagination
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.data = {'success': True,'data': response.data}
        return response




class GetUserListSearchView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = GetUserListSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = MyCustomPagination

    def list(self, request, *args, **kwargs):
        s = kwargs['s']
        queryset = User.objects.filter(Q(full_name__icontains=s) | Q(phone_number__icontains=s))
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        response = self.get_paginated_response(serializer.data)
        if not serializer.data:
            return Response({'success': False, "message": 'there is not data', "data": response.data}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'data': response.data}, status=status.HTTP_200_OK)


class GetUserListByCustomPagination(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = GetUserListSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = MyCustomPagination

    def list(self, request, *args, **kwargs):
        query = User.objects.all()
        # MyCustomPagination.page_size = kwargs['paginate']
        paginate = MyCustomPagination()
        paginate.page_size = kwargs['paginate']
        page = paginate.paginate_queryset(query, request)
        serializer = self.get_serializer(page, many=True)
        response = paginate.get_paginated_response(serializer.data)
        return Response({'success': True, 'data': response.data}, status=status.HTTP_200_OK)


class GetUserListByCustomPaginationAndFilter(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = GetUserListSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = MyCustomPagination

    def list(self, request, *args, **kwargs):
        query = User.objects.filter(tarif=kwargs['tarif'])
        # MyCustomPagination.page_size = kwargs['paginate']
        paginate = MyCustomPagination()
        paginate.page_size = kwargs['paginate']
        page = paginate.paginate_queryset(query, request)
        serializer = self.get_serializer(page, many=True)
        response = paginate.get_paginated_response(serializer.data)
        return Response({'success': True, 'data': response.data}, status=status.HTTP_200_OK)


class ChatView(generics.CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(from_user = self.request.user)
        
        return super().perform_create(serializer)
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {'success':True,'data':response.data}
        
        return response



class ChatGetList(generics.ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]
    def list(self, request, *args, **kwargs):

        query = Chat.objects.filter(from_user=self.request.user).order_by('-date_field')
        #serializer = ChatSerializer(query,many=True)
        return Response({'success': True, 'data': query.values_list('text_body', 'time_created')},content_type='application/json; charset=utf-8')
class ChangeLanguageView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ChangeLanguageSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data = {'success':True,'data':response.data}
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {'success': True, 'data': response.data}
        return response
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        response.data = {'success': True, 'data': response.data}
        return response
        
import requests
class GoogleLoginView(generics.CreateAPIView):
    serializer_class = GoogleLoginSer
    def post(self, request, *args, **kwargs):
        try:
            google_token = request.data['token']
            urldata = f"https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token={google_token}"
            email = requests.get(urldata).json()['email']
            user,created = User.objects.get_or_create(phone_number=email)
            if created:
                query = User.objects.filter(phone_number=email)
                query.update(is_active=True)
            accesstoken = AccessToken.for_user(user=user)
            return Response({'access':str(accesstoken),'email':str(user),'success':True},status=status.HTTP_200_OK)
        except:
            return Response({'message':'token expired','success':False},status=status.HTTP_400_BAD_REQUEST)


class FacebookLoginView(generics.CreateAPIView):
    serializer_class = GoogleLoginSer
    def post(self, request, *args, **kwargs):
        try:
            google_token = request.data['token']
            urldata = f"https://graph.facebook.com/me?access_token={google_token}"
            data = requests.get(urldata).json()
            email = data['id']
            full_name=data['name']
            user,created = User.objects.get_or_create(phone_number=email,full_name=full_name)
            if created:
                query = User.objects.filter(phone_number=email)
                query.update(is_active=True)
            accesstoken = AccessToken.for_user(user=user)
            return Response({'access':str(accesstoken),'facebook_id':str(user),'success':True},status=status.HTTP_200_OK)
        except:
            return Response({'message':'token expired','success':False},status=status.HTTP_400_BAD_REQUEST)