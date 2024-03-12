from django.urls import path,re_path
from .views import CreateCategoryView, AddAnnouncementView, SubCategoryView, SubCategoryUpdateView, CategoryUpdateView, SubcategoryListById, ParamsView, GetAnnouncementList, GetAnnouncementListByFilterOnlyStatus
from .views import GetListOfParamsView, DeleteParamsView, GetAnnouncementByIdView, UpdateStatusView, NotisificationView, GetAnnouncementListByFilter, GetAnnouncementListByFilterOnlyCatid
from .views import GetAnnouncementListByFilterCustomPagination, NotisificationlistApiView, NotisificationCustomPagination, NotisificationCustomPagination, NotisificationFilterPagintion
from .views import UserGetListOfCategory, UserSubcategoryListById, UserGetListOfAnnounce, BulkDeleteNotisificationView, GetAnnouncementSearchList, NotisificationSearchView, CreateParamByTypeOfValueView
from .views import GetListOfParamsBySelectView, UserGetAnnouncementByIdView, AdminGetListOfParamsBySelectView, UserGetOwnAnnounce, UserUpdateAnnounceInactive
from .views import UserGetAnnouncementSearchList, LikeButtonView, UnLikeButtonView, GetListOfLikedAnnounce, UserAnnounceFilter, UserGetListOfAnnounceBySub, UpdateAnnounceById
urlpatterns = [
    path('admin/category/',CreateCategoryView.as_view(),name='category'),
    path('admin/subcategory/',SubCategoryView.as_view(),name='subcategory'),
    path('admin/subcategory/<int:pk>/', SubCategoryUpdateView.as_view()),
    path('admin/category/<int:pk>/', CategoryUpdateView.as_view()),
    path('admin/subcategory/list/bycategory/<int:pk>/', SubcategoryListById.as_view()),
    path('admin/announcement/param/api',ParamsView.as_view()),
    path('admin/get/announcement/list/<int:paginate>/<int:cat_id>/<str:status>', GetAnnouncementListByFilter.as_view()),
    path('admin/get/announcement/list/<int:paginate>/<int:cat_id>',GetAnnouncementListByFilterOnlyCatid.as_view()),
    path('admin/get/announcement/list/<int:paginate>/<str:status>',GetAnnouncementListByFilterOnlyStatus.as_view()),
    path('admin/get/announcement/list/<int:paginate>', GetAnnouncementListByFilterCustomPagination.as_view()),
    path('admin/get/announcement/list/',GetAnnouncementList.as_view()),
    path('admin/get/announcement/list/search/<str:s>', GetAnnouncementSearchList.as_view()),
    path('admin/delete/params/<int:pk>',DeleteParamsView.as_view()),
    path('admin/get/list/params/<int:pk>', GetListOfParamsView.as_view()),
    path('admin/get/announce/byid/<int:pk>', GetAnnouncementByIdView.as_view()),
    path('admin/update/status/<int:pk>', UpdateStatusView.as_view()),
    path('admin/create/notisification',NotisificationView.as_view()),
    path('admin/list/notisification', NotisificationlistApiView.as_view()),
    path('admin/list/notisification/search/<str:s>',NotisificationSearchView.as_view()),
    path('admin/list/notisification/<int:paginate>',NotisificationCustomPagination.as_view()),
    path('admin/list/notisification/<int:paginate>/<str:order>',NotisificationFilterPagintion.as_view()),
    path('admin/delete/multiple/notisification/',BulkDeleteNotisificationView.as_view()),

    path('admin/create/params/by/v1/value',CreateParamByTypeOfValueView.as_view()),
    path('admin/get/list/v2/params/<int:pk>',AdminGetListOfParamsBySelectView.as_view()),
    


    #-------User---------------------User--------------------

    
    path('user/add/announcement',AddAnnouncementView.as_view()),
    path('user/get/list/params/<int:pk>',GetListOfParamsView.as_view()),
    path('user/get/list/category', UserGetListOfCategory.as_view()),
    path('user/get/list/subcategory/<int:pk>',UserSubcategoryListById.as_view()),
    path('user/get/list/announcement',UserGetListOfAnnounce.as_view()),
    path('user/get/list/v2/params/<int:pk>',GetListOfParamsBySelectView.as_view()),
    path('user/get/full/data/announce/<int:pk>',UserGetAnnouncementByIdView.as_view()),
    path('user/get/own/announce/<str:activity>',UserGetOwnAnnounce.as_view()),
    path('user/update/delete/retrieve/own/<int:pk>',UserUpdateAnnounceInactive.as_view()),
    path('user/search/announce/by/all/<str:s>',UserGetAnnouncementSearchList.as_view()),
    path('user/like/announcement/by/true/<int:pk>', LikeButtonView.as_view()),
    path('user/like/announcement/by/false/<int:pk>', UnLikeButtonView.as_view()),
    path('user/get/list/of/liked/announce', GetListOfLikedAnnounce.as_view()),
    path('user/announce/get/list/filter',UserAnnounceFilter.as_view()),
    path('user/get/list/announcement/<int:pk>',UserGetListOfAnnounceBySub.as_view()),
    path('user/update/announcement/<int:pk>', UpdateAnnounceById.as_view())
]   