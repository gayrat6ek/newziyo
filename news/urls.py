from django.urls import path 
from .views import AdminNewsAddView, BulkDeleteNewView,  UpdateDestroyApiView, AdminListFilterWithPagination, AdminListCustomPagination, AdminListNewsApi, UserNewListView, UserNewsGetDetailView
from .views import AdminListNewsSearchApi, RecommendationView, RecommendationActivateView, RecommendationListView, UserGetListReCommend, AdminListGetRecommend, AdminRecommendfilterPagination, AdminRecommendOnlyPagination
from .views import UserGetListDistrict,Usergetversion
urlpatterns = [
    #admin
    path('add/news/admin/',AdminNewsAddView.as_view(),name='news_add'),
    path('update/destroy/api/<int:pk>',UpdateDestroyApiView.as_view(), name='update destroy'),
    path('admin/list/filter/paginate/<int:paginate>/<str:order>',AdminListFilterWithPagination.as_view()),
    path('admin/list/filter/paginate/<int:paginate>',AdminListCustomPagination.as_view()),
    path('admin/list/filter/paginate', AdminListNewsApi.as_view()),
    path('admin/list/filter/paginate/search/<str:s>',AdminListNewsSearchApi.as_view()),
    path('admin/news/delete/bulk',BulkDeleteNewView.as_view()),
    path('admin/recommendation/add',RecommendationView.as_view()),
    path('admin/v1/active/recommend/<int:pk>',RecommendationActivateView.as_view()),
    path('admin/v2/list/get/recommend', RecommendationListView.as_view()),
    path('admin/v2/list/get/recommend/search/<str:s>',AdminListGetRecommend.as_view()),
    path('admin/v2/list/get/recommend/<int:paginate>/<str:status>',AdminRecommendfilterPagination.as_view()),
    path('admin/v2/list/get/recommend/<int:paginate>',AdminRecommendOnlyPagination.as_view()),
    #   USER---------------------

    path('user/list/v1/news', UserNewListView.as_view()),
    path('user/detail/v1/news/<int:pk>', UserNewsGetDetailView.as_view()),
    path('user/v1/get/list/recommend',UserGetListReCommend.as_view()),
    path('user/v1/get/list/district', UserGetListDistrict.as_view()),
    path('user/v1/version',Usergetversion.as_view())

]