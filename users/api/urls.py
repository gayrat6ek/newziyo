from django.urls import path
from .views import RegistrationAPIView, AdminLogin, GetUserListView, GetUserListByCustomPaginationAndFilter, GetUserListByCustomPagination, SetPasswordView, AdminVerifyOTPAPIView, LoginUserView, GetUserDataView, VerifyOTPAPIView, LogoutBlacklistTokenUpdateView, ResetPasswordConfirmView, ResetPasswordView, UpdateProfileView
from .views import GetUserListSearchView, ChatView,ChatGetList,ChangeLanguageView,GoogleLoginView,FacebookLoginView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path('verify', VerifyOTPAPIView.as_view(), name='verify-otp'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout', LogoutBlacklistTokenUpdateView.as_view(), name='logout'),
    path('register', RegistrationAPIView.as_view(), name='registration'),
    path('setpassword',SetPasswordView.as_view(),name='setpassword'),
    path('resetpassword',ResetPasswordView.as_view(),name='resetpassword'),    
    path('resetpassword/confirm',ResetPasswordConfirmView.as_view(),name='resetpasswordconfirm'),
    path('login',LoginUserView.as_view(),name='loginuser'),
    path('update/profile',UpdateProfileView.as_view(),name='profile'),
    path('getuserinfo',GetUserDataView.as_view(),name='data'),
    path('user/add/chat/data',ChatView.as_view()),
    path('user/get/list/chat/history',ChatGetList.as_view()),
    path('user/update/language/own', ChangeLanguageView.as_view()),
    #admin verify login
    path('admin/',AdminLogin.as_view(),name='admin_login'),
    path('verify/otp/',AdminVerifyOTPAPIView.as_view(),name='admin_verify'),
    path('admin/get/user/list',GetUserListView.as_view()),
    path('admin/get/user/list/search/<str:s>', GetUserListSearchView.as_view()),
    path('admin/get/user/list/<int:paginate>', GetUserListByCustomPagination.as_view()),
    path('admin/get/user/list/<int:paginate>/<str:tarif>',GetUserListByCustomPaginationAndFilter.as_view()),
    path('google/login',GoogleLoginView.as_view()),
    path('facebook/login',FacebookLoginView.as_view())
]
