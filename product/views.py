from django.db.models import Count
from .serializers import ParamsValSer, ParamsValSerSt
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from datetime import date
from .models import ParamSelectValues
from django.core.files.storage import default_storage
from django.db.models import F
from django.db.models.functions import Abs
from .serializers import UserGetListCategorySerializer, UserGetListAnnounceSerializer
from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import CreateCategorySerializer, AddAnnouncementSerializer, SubCategorySerializer, SubCategoryUpdateSerializer, AdminGetAnnouncementSerializer, CategoryUpdateSerializer, SubCategoryListByIdSer, CreateParamsSerializer
from .serializers import AdminGetAnnounceById, AdminSubcategoryValuesSerializer, UpdateStatusSerializer, NotisificationSerializer, CreateParamsTypeOfValueSeri, GetParamsBySelectSerializer
from .serializers import GetSelectValuesSerializer, UserGetAnnounceById, UserMakeInactiveSer, UserUpdateAnnouncementSer
from .models import CreateCategoryModel, SubCategoryModel, AnnouncementModel, SubCategoryParams, SubCategoryValues, NotisificationModel, ParamSelectValues
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.db.models import Q
import json
from .permissions import IsStaff
# Create your views here.


class MyCustomPagination(PageNumberPagination):
    page_size = 8
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


class CreateCategoryView(generics.ListCreateAPIView):
    queryset = CreateCategoryModel.objects.all()
    serializer_class = CreateCategorySerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    pagination_class = None

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {'success': True, 'data': response.data}
        return response

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {'success': True, 'data': response.data}
        return response


class SubCategoryView(generics.ListCreateAPIView):
    queryset = SubCategoryModel.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    pagination_class = None

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {'success': True, 'data': response.data}
        return response

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {'success': True, 'data': response.data}
        return response


class SubCategoryUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategoryModel.objects.all()
    serializer_class = SubCategoryUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaff]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.data = {'success': True, 'data': response.data}
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {'success': True, 'data': response.data}
        return response

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        response.data = {'success': True, 'data': response.data}
        return response


class CategoryUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CreateCategoryModel.objects.all()
    serializer_class = CategoryUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaff]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.data = {'success': True, 'data': response.data}
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {'success': True, 'data': response.data}
        return response

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        response.data = {'success': True, 'data': response.data}
        return response


class SubcategoryListById(generics.ListAPIView):
    queryset = SubCategoryModel.objects.all()
    serializer_class = SubCategoryListByIdSer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = SubCategoryModel.objects.filter(parent=kwargs['pk'])
        serializer = self.get_serializer(queryset, many=True)
        query = CreateCategoryModel.objects.filter(pk=kwargs['pk'])
        category_serializer = CategoryUpdateSerializer(query, many=True)
        if not serializer.data:
            return Response({'success': True, 'category': category_serializer.data,  'sublist': serializer.data})
        return Response({'success': True, 'category': category_serializer.data, 'sublist': serializer.data})


class ParamsView(generics.ListCreateAPIView):
    queryset = SubCategoryParams.objects.all()
    serializer_class = CreateParamsSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    pagination_class = None

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {'success': True, 'data': response.data}
        return response

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {'success': True, 'data': response.data}
        return response


class CreateParamByTypeOfValueView(generics.CreateAPIView):
    queryset = SubCategoryParams.objects.all()
    serializer_class = CreateParamsTypeOfValueSeri
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        param_id = response.data['pk']
        type_of_value = request.data.get('type_of_value')
        list_of_select = dict(request.data)
        if type_of_value in ['select', 'multiselect']:
            for i in list_of_select['select_values']:
                ParamSelectValues.objects.create(
                    parent_param=SubCategoryParams.objects.get(pk=param_id), value=i)

        return Response({'success': True}, status=status.HTTP_201_CREATED)


class DeleteParamsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategoryParams.objects.all()
    serializer_class = CreateCategorySerializer
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.data = {'success': True, 'data': response.data}
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {'success': True, 'data': response.data}
        return response

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        response.data = {'success': True, 'data': response.data}
        return response


class GetAnnouncementList(generics.ListAPIView):
    queryset = AnnouncementModel.objects.all()
    serializer_class = AdminGetAnnouncementSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = MyCustomPagination

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {'success': True, 'data': response.data}
        return response


class GetAnnouncementSearchList(generics.ListAPIView):
    queryset = AnnouncementModel.objects.all()
    serializer_class = AdminGetAnnouncementSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = MyCustomPagination

    def list(self, request, *args, **kwargs):
        s = kwargs['s']
        queryset = AnnouncementModel.objects.filter(
            Q(title__icontains=s) | Q(body__icontains=s))
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        response = self.get_paginated_response(serializer.data)
        if not serializer.data:
            return Response({'success': False, "message": 'there is not data', "data": response.data}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'data': response.data}, status=status.HTTP_200_OK)


class GetAnnouncementListByFilterCustomPagination(generics.ListAPIView):
    queryset = AnnouncementModel.objects.all()
    serializer_class = AdminGetAnnouncementSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = MyCustomPagination

    def list(self, request, *args, **kwargs):
        query = AnnouncementModel.objects.all()
        # MyCustomPagination.page_size = kwargs['paginate']
        paginate = MyCustomPagination()
        paginate.page_size = kwargs['paginate']
        page = paginate.paginate_queryset(query, request)
        serializer = self.get_serializer(page, many=True)
        response = paginate.get_paginated_response(serializer.data)
        return Response({'success': True, 'data': response.data}, status=status.HTTP_200_OK)


class GetAnnouncementListByFilterOnlyStatus(generics.ListAPIView):
    queryset = AnnouncementModel.objects.all()
    serializer_class = AdminGetAnnouncementSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = MyCustomPagination

    def list(self, request, *args, **kwargs):
        query = AnnouncementModel.objects.filter(
            status=kwargs['status'])
        # MyCustomPagination.page_size = kwargs['paginate']
        paginate = MyCustomPagination()
        paginate.page_size = kwargs['paginate']
        page = paginate.paginate_queryset(query, request)
        serializer = self.get_serializer(page, many=True)
        response = paginate.get_paginated_response(serializer.data)
        return Response({'success': True, 'data': response.data}, status=status.HTTP_200_OK)


class GetAnnouncementListByFilterOnlyCatid(generics.ListAPIView):
    queryset = AnnouncementModel.objects.all()
    serializer_class = AdminGetAnnouncementSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = MyCustomPagination

    def list(self, request, *args, **kwargs):
        query = AnnouncementModel.objects.filter(
            subcategory__parent=kwargs['cat_id'])
        # MyCustomPagination.page_size = kwargs['paginate']
        paginate = MyCustomPagination()
        paginate.page_size = kwargs['paginate']
        page = paginate.paginate_queryset(query, request)
        serializer = self.get_serializer(page, many=True)
        response = paginate.get_paginated_response(serializer.data)
        return Response({'success': True, 'data': response.data}, status=status.HTTP_200_OK)


class GetAnnouncementListByFilter(generics.ListAPIView):
    queryset = AnnouncementModel.objects.all()
    serializer_class = AdminGetAnnouncementSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = MyCustomPagination

    def list(self, request, *args, **kwargs):
        query = AnnouncementModel.objects.filter(
            subcategory__parent=kwargs['cat_id'], status=kwargs['status'])
        # MyCustomPagination.page_size = kwargs['paginate']
        paginate = MyCustomPagination()
        paginate.page_size = kwargs['paginate']
        page = paginate.paginate_queryset(query, request)
        serializer = self.get_serializer(page, many=True)
        response = paginate.get_paginated_response(serializer.data)
        return Response({'success': True, 'data': response.data}, status=status.HTTP_200_OK)


class GetAnnouncementByIdView(generics.GenericAPIView):
    queryset = AnnouncementModel.objects.all()
    serializer_class = AdminGetAnnounceById
    pagination_class = None
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        announce = AnnouncementModel.objects.filter(pk=kwargs['pk'])
        serializer = AdminGetAnnounceById(announce, many=True)
        string_params = SubCategoryValues.objects.filter(
            announcement=kwargs['pk'], string__isnull=False)
        integer_params = SubCategoryValues.objects.filter(
            announcement=kwargs['pk'], integer__isnull=False)
        selection_params = AnnouncementModel.objects.get(pk=kwargs['pk'])
        query_from_select = selection_params.announcements.filter(
            selecttion__isnull=False)
        # distinct('params')

        selectionnew = []
        list_of_ids = query_from_select.values(
            'selecttion_id__value', 'params', 'announcement', 'params_id__name')

        # serializer = test(integer_params,many=True)

        for name in list_of_ids:
            selectionnew.append({'name': name['params_id__name'], 'values': SubCategoryValues.objects.filter(
                params=name['params'], announcement=name['announcement']).values('id', 'selecttion__value')})
        a = {
            'integer': {integer_params.values('params_id__name', 'integer')},
            'string': string_params.values('params_id__name', 'string'),
            'selection': selectionnew
        }

        return Response({'success': True, 'announce': serializer.data, 'params': a}, status=status.HTTP_200_OK)


class UpdateStatusView(generics.UpdateAPIView):
    queryset = AnnouncementModel.objects.all()
    serializer_class = UpdateStatusSerializer
    permission_classes = [permissions.IsAdminUser]

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {'success': True, 'data': response.data}
        return response


class NotisificationView(generics.CreateAPIView):
    queryset = NotisificationModel.objects.all()
    serializer_class = NotisificationSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {'success': True, 'data': response.data}
        return response


class NotisificationSearchView(generics.ListAPIView):
    queryset = NotisificationModel.objects.all()
    serializer_class = NotisificationSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = MyCustomPagination

    def list(self, request, *args, **kwargs):
        s = kwargs['s']
        queryset = NotisificationModel.objects.filter(
            Q(theme__icontains=s) | Q(value__icontains=s))
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        response = self.get_paginated_response(serializer.data)
        if not serializer.data:
            return Response({'success': False, "message": 'there is not data', "data": response.data}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'data': response.data}, status=status.HTTP_200_OK)


class NotisificationlistApiView(generics.ListAPIView):
    queryset = NotisificationModel.objects.all()
    serializer_class = NotisificationSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = MyCustomPagination

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {'success': True, 'data': response.data}
        return response


class NotisificationCustomPagination(generics.ListAPIView):
    serializer_class = NotisificationSerializer
    queryset = NotisificationModel.objects.all()
    permission_classes = (permissions.IsAdminUser, permissions.IsAuthenticated)
    pagination_class = MyCustomPagination

    def list(self, request, *args, **kwargs):
        query = NotisificationModel.objects.all()
        # MyCustomPagination.page_size = kwargs['paginate']
        paginate = MyCustomPagination()
        paginate.page_size = kwargs['paginate']
        page = paginate.paginate_queryset(query, request)
        serializer = self.get_serializer(page, many=True)
        response = paginate.get_paginated_response(serializer.data)
        return Response({'success': True, 'data': response.data}, status=status.HTTP_200_OK)


class NotisificationFilterPagintion(generics.ListAPIView):
    serializer_class = NotisificationSerializer
    queryset = NotisificationModel.objects.all()
    permission_classes = (permissions.IsAdminUser, permissions.IsAuthenticated)
    pagination_class = MyCustomPagination

    def list(self, request, *args, **kwargs):
        if kwargs['order'] == 'new':
            query = NotisificationModel.objects.all().order_by('-date', '-time')
        elif kwargs['order'] == 'old':
            query = NotisificationModel.objects.all().order_by('date', 'time')
        else:
            query = NotisificationModel.objects.all().order_by('?')
        # MyCustomPagination.page_size = kwargs['paginate']
        paginate = MyCustomPagination()
        paginate.page_size = kwargs['paginate']
        page = paginate.paginate_queryset(query, request)
        serializer = self.get_serializer(page, many=True)
        response = paginate.get_paginated_response(serializer.data)
        return Response({'success': True, 'data': response.data}, status=status.HTTP_200_OK)


class BulkDeleteNotisificationView(generics.DestroyAPIView):
    queryset = NotisificationModel.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        data = NotisificationModel.objects.filter(
            pk__in=self.request.data['pk'])
        data.delete()

        return Response({'success': True, "message": 'all data has been delated'}, status=status.HTTP_204_NO_CONTENT)


# search apis

# -----------------User---------------------User--------------------------------


today = date.today()
year = today.year
month = today.month
day = today.day


class AddAnnouncementView(generics.CreateAPIView):
    queryset = AnnouncementModel.objects.all()
    serializer_class = AddAnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)

    def create(self, request, *args, **kwargs):

        a = dict(request.POST)
        a = a['params']
        a = json.loads(a[0])
        # a = {'select':[],
        #     'multiselect':[],
        #     'string':[],
        #     'integer':[]}
        files = request.FILES.getlist('image')
        image_list = []
        for file in files:
            default_storage.save(
                f"photos/{year}/{month}/{day}/{file.name}", file)
            link = f"/media/photos/{year}/{month}/{day}/{file.name}"
            image_list.append(link)
        image_list = json.dumps(image_list)
        request = super().create(request, *args, **kwargs)
        announcement_pk = request.data['pk']
        n = AnnouncementModel.objects.filter(pk=announcement_pk)
        n.update(images=image_list)
        # input_value = a['string']
        #
        # multiselect = a['multiselect']
        # select = a['select']
        for key, value in a.items():
            val = a[key]
            for data in val:
                if key in ['select', 'multiselect']:

                    subcategory_value = SubCategoryValues.objects.create(params=SubCategoryParams.objects.get(
                        pk=data[0]), announcement=AnnouncementModel.objects.get(pk=announcement_pk), selecttion=ParamSelectValues.objects.get(pk=data[1]))
                    subcategory_value.save()
                if key == 'string':
                    subcategory_value = SubCategoryValues.objects.create(params=SubCategoryParams.objects.get(
                        pk=data[0]), announcement=AnnouncementModel.objects.get(pk=announcement_pk), string=data[1])
                    subcategory_value.save()
                if key == 'integer':
                    subcategory_value = SubCategoryValues.objects.create(params=SubCategoryParams.objects.get(
                        pk=data[0]), announcement=AnnouncementModel.objects.get(pk=announcement_pk), integer=data[1])
                    subcategory_value.save()
        return Response({'success': True, 'Message': 'all data has been sanded'}, status=status.HTTP_201_CREATED)


class GetListOfParamsView(generics.ListAPIView):
    queryset = SubCategoryParams.objects.all()
    serializer_class = CreateParamsSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = SubCategoryParams.objects.filter(subcategory=kwargs['pk'])
        serializer = CreateParamsSerializer(queryset, many=True)
        if not serializer.data:
            return Response({'success': True, 'data': serializer.data})
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)


class UserGetListOfCategory(generics.ListAPIView):
    queryset = CreateCategoryModel.objects.all()
    serializer_class = UserGetListCategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {'success': True, 'data': response.data}
        return Response(response.data, content_type='application/json; charset=utf-8')


class UserSubcategoryListById(generics.ListAPIView):
    queryset = SubCategoryModel.objects.all()
    serializer_class = SubCategoryListByIdSer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = SubCategoryModel.objects.filter(parent=kwargs['pk'])
        # a = SubCategoryModel.objects.get(pk=kwargs['pk'])

        serializer = self.get_serializer(queryset, many=True)
        # query = CreateCategoryModel.objects.filter(pk=kwargs['pk'])
        # category_serializer = CategoryUpdateSerializer(query, many=True)
        # if not serializer.data:
        #    return Response({'success': True, 'category': category_serializer.data,  'sublist': serializer.data})
        return Response({'success': True, 'data': serializer.data}, content_type='application/json; charset=utf-8')


class UserGetListOfAnnounce(generics.ListAPIView):
    # status=puplished
    queryset = AnnouncementModel.objects.filter(
        user_controller='active', status='published')
    serializer_class = UserGetListAnnounceSerializer
    pagination_class = MyCustomPagination

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {'success': True, 'data': response.data}
        return Response(response.data, content_type='application/json; charset=utf-8')


class UserGetListOfAnnounceBySub(generics.ListAPIView):
    # status=puplished
    queryset = AnnouncementModel.objects.filter(user_controller='active')
    serializer_class = UserGetListAnnounceSerializer
    pagination_class = MyCustomPagination

    def list(self, request, *args, **kwargs):
        query = AnnouncementModel.objects.filter(
            subcategory=kwargs['pk'], user_controller='active', status='published')
        paginate = MyCustomPagination()
        page = paginate.paginate_queryset(query, request)
        serializer = self.get_serializer(page, many=True)
        response = paginate.get_paginated_response(serializer.data)
        return Response({'success': True, 'data': response.data}, content_type='application/json; charset=utf-8')


class UserGetOwnAnnounce(generics.ListAPIView):
    queryset = AnnouncementModel.objects.all()
    serializer_class = UserGetListAnnounceSerializer
    pagination_class = MyCustomPagination

    def list(self, request, *args, **kwargs):
        response = AnnouncementModel.objects.filter(
            user=self.request.user, user_controller=kwargs['activity'])
        response = self.get_serializer(response, many=True)
        return Response({'success': True, 'data': response.data}, content_type='application/json; charset=utf-8')


class isOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class UserUpdateAnnounceInactive(generics.RetrieveUpdateDestroyAPIView):
    queryset = AnnouncementModel.objects.all()
    serializer_class = UserMakeInactiveSer
    permission_classes = [isOwner]

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {"success": True, 'data': response.data}
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        response.data = {"success": True, 'data': response.data}
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data = {"success": True, 'data': response.data}
        return response


class AdminGetListOfParamsBySelectView(generics.ListAPIView):
    queryset = SubCategoryParams.objects.all()
    serializer_class = GetParamsBySelectSerializer

    def list(self, request, *args, **kwargs):
        request_id = kwargs['pk']
        request_data = SubCategoryParams.objects.filter(subcategory=request_id)

        select = []
        multiselect = []
        input_value = []
        filter_data = SubCategoryModel.objects.filter(pk=kwargs['pk'])
        category_and_sub = filter_data.values('parent_id__name', 'name', 'pk')
        selectvalues = {}
        request_ids = request_data.values()
        try:
            for isselect in request_ids:
                a = SubCategoryParams.objects.get(pk=int(isselect['id']))
                query = a.children.all().values('pk', 'value', 'parent_param')
                type_of_value = isselect['type_of_value']
                if type_of_value == 'select':
                    select.append({
                        'name': str(isselect['name']),
                        'pk': isselect['id'],
                        'input_type': 'select',
                        'values': query
                    })
                if type_of_value == 'multiselect':
                    multiselect.append({
                        'name': str(isselect['name']),
                        'pk': isselect['id'],
                        'input_type': 'multiselect',
                        'values': query
                    })

                if type_of_value in 'string':
                    input_value.append(
                        {'pk': isselect['id'], 'name': isselect['name'], 'input_type': 'string'})
                if type_of_value in 'integer':
                    input_value.append(
                        {'pk': isselect['id'], 'name': isselect['name'], 'input_type': 'integer'})
            selectvalues['category_name'] = category_and_sub[0]
            selectvalues['select'] = select
            selectvalues['multiselect'] = multiselect
            selectvalues['input_value'] = input_value
        except:
            return Response({'success': True, 'select': [], 'multiselect': [], 'input_value': [], 'category_name': {'parent_id__name': '', 'name': ''}})

        return Response(selectvalues)


from .transliterate import to_cyrillic

class GetListOfParamsBySelectView(generics.ListAPIView):
    queryset = SubCategoryParams.objects.all()
    serializer_class = GetParamsBySelectSerializer

    def list(self, request, *args, **kwargs):
        request_id = kwargs['pk']
        request_data = SubCategoryParams.objects.filter(subcategory=request_id)

        select = []
        multiselect = []
        input_value = []
        filter_data = SubCategoryModel.objects.filter(pk=kwargs['pk'])
        category_and_sub = filter_data.values('parent_id__name', 'name')
        selectvalues = {}
        request_ids = request_data.values()
        request.user.language
        try:
            for isselect in request_ids:
                a = SubCategoryParams.objects.get(pk=int(isselect['id']))
                query = a.children.all().values('pk', 'value', 'parent_param')
                type_of_value = isselect['type_of_value']
                if type_of_value == 'select':
                    select.append({
                        'name': str(isselect['name']),
                        'value': query
                    })
                if type_of_value == 'multiselect':
                    multiselect.append({
                        'name': str(isselect['name']),
                        'value': query
                    })
                if type_of_value in 'string':
                    input_value.append(
                        {'pk': isselect['id'], 'value': isselect['name'], 'input_type': 'string'})
                if type_of_value in 'integer':
                    input_value.append(
                        {'pk': isselect['id'], 'value': isselect['name'], 'input_type': 'integer'})
            selectvalues['category_name'] = category_and_sub[0]
            selectvalues['select'] = select
            selectvalues['multiselect'] = multiselect
            selectvalues['input_value'] = input_value
        except:
            return Response({'success': True, 'select': [], 'multiselect': [], 'input_value': [], 'category_name': {'parent_id__name': '', 'name': ''}})

        return Response(selectvalues, content_type='application/json; charset=utf-8')


class UserGetAnnouncementByIdView(generics.GenericAPIView):
    queryset = AnnouncementModel.objects.all()
    serializer_class = UserGetAnnounceById
    pagination_class = None

    def get(self, request, *args, **kwargs):
        announce = AnnouncementModel.objects.filter(pk=kwargs['pk'])
        serializer = UserGetAnnounceById(
            announce,    context={'request': request}, many=True)
        string_params = SubCategoryValues.objects.filter(
            announcement=kwargs['pk'], string__isnull=False)
        integer_params = SubCategoryValues.objects.filter(
            announcement=kwargs['pk'], integer__isnull=False)
        selection_params = AnnouncementModel.objects.get(pk=kwargs['pk'])
        query_from_select = selection_params.announcements.filter(
            selecttion__isnull=False)
        #query_from_select = query_from_select.values_list('params',flat=True)
        # add distinct('params')
        #print(query_from_select.values())
        selectionnew = []
        values_dict = []
        list_of_ids = query_from_select.values(
            'selecttion_id__value', 'params', 'announcement', 'params_id__name')
        for name in list_of_ids:
            if int(name['params']) not in values_dict:
                values_dict.append(int(name['params']))
                selectionnew.append({'name': name['params_id__name'], 'values': SubCategoryValues.objects.filter(params=name['params'], announcement=name['announcement']).values('id', 'selecttion__value')})


        serialiser = ParamsValSer(integer_params, many=True)
        serialiserst = ParamsValSerSt(string_params, many=True)
        a = list(serialiserst.data)
        a = a+list(serialiser.data)

        if serializer.data[0]['viewers'] is not None:
            viewers = serializer.data[0]['viewers']+1

            announce[0].viewers = viewers
            announce[0].save()
        else:
            viewers = 1

            announce[0].viewers = viewers
            announce[0].save()
        query = AnnouncementModel.objects.annotate(similarity=Abs(F('price') - serializer.data[0]['price'])).filter(
            ~Q(pk=serializer.data[0]['pk']), status='published', subcategory=serializer.data[0]['subcategory'], currency=serializer.data[0]['currency']).order_by('-similarity')[:5]
        data = self.get_serializer(query, many=True)
        return Response({'success': True, 'announce': serializer.data[0], 'input_values': a, 'selection': selectionnew, 'similar': data.data}, status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')


class UserGetAnnouncementSearchList(generics.ListAPIView):
    queryset = AnnouncementModel.objects.all()
    serializer_class = UserGetListAnnounceSerializer
    pagination_class = MyCustomPagination

    def list(self, request, *args, **kwargs):
        s = kwargs['s']
        queryset = AnnouncementModel.objects.filter(Q(title__icontains=s) | Q(body__icontains=s) | Q(
            subcategory__name__icontains=s) | Q(subcategory__parent__name__icontains=s), status='published')
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        response = self.get_paginated_response(serializer.data)
        if not serializer.data:
            return Response({'success': True, "message": 'there is not data', "data": response.data}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'data': response.data}, status=status.HTTP_200_OK)


class LikeButtonView(generics.UpdateAPIView):
    queryset = AnnouncementModel.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        obekt = get_object_or_404(
            AnnouncementModel.objects.all(), pk=kwargs['pk'])
        obekt.likers.add(request.user)
        return Response({'success': True, 'message': 'you liked this announcement'})


class UnLikeButtonView(generics.UpdateAPIView):
    queryset = AnnouncementModel.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        obekt = get_object_or_404(
            AnnouncementModel.objects.all(), pk=kwargs['pk'])
        obekt.likers.remove(request.user)
        return Response({'success': True, 'message': 'you Unliked this announcement'})


class GetListOfLikedAnnounce(generics.ListAPIView):
    queryset = AnnouncementModel.objects.all()
    serializer_class = UserGetListAnnounceSerializer

    def list(self, request, *args, **kwargs):
        query = AnnouncementModel.objects.filter(likers=request.user)
        serializer = self.get_serializer(query, many=True)
        return Response({'success': True, 'data': serializer.data},content_type='application/json; charset=utf-8')


class UserAnnounceFilter(generics.CreateAPIView):
    serializer_class = UserGetListAnnounceSerializer
    pagination_class = MyCustomPagination

    def post(self, request, *args, **kwargs):
        # a = dict(request.data)
        # a = a['params']
        # a = json.loads(a)
        a = {'multiselect': [],
             'select': [],
             'integer': []}
        multisel = a['multiselect']
        select = a['select']
        integer = a['integer']
        every_all = multisel+select
        every_all_sell = [i[1] for i in every_all]

        integer_list = [i[1] for i in integer]

        sub_id = int(request.data['subcategory'])
        money_from = int(request.data['money_from'])
        money_to = int(request.data['money_to'])
        currency = request.data['currency']
        kelishuv = request.data['kelishuv']
        if integer_list and kelishuv == False:
            b = SubCategoryValues.objects.filter(Q(integer__in=integer_list), Q(announcement__price__gt=money_from) & Q(
                announcement__price__lte=money_to), announcement__currency=currency, params__subcategory=sub_id, announcement__status='published')  # .distinct('announcement')
        elif every_all_sell and kelishuv == False:
            b = SubCategoryValues.objects.filter(Q(selecttion__in=every_all_sell), Q(announcement__price__gt=money_from) & Q(
                announcement__price__lte=money_to), announcement__currency=currency, params__subcategory=sub_id, announcement__status='published')  # .distinct('annonucement')
        elif integer_list and every_all_sell and kelishuv == False:
            b = SubCategoryValues.objects.filter(Q(integer__in=integer_list) | Q(selecttion__in=every_all_sell), Q(announcement__price__gt=money_from) & Q(
                announcement__price__lte=money_to), announcement__currency=currency, params__subcategory=sub_id, announcement__status='published')  # .distinct('announcement')
        elif not (integer_list and every_all_sell) and kelishuv == False:
            b = SubCategoryValues.objects.filter(Q(announcement__price__gt=money_from) & Q(
                announcement__price__lte=money_to), announcement__currency=currency, params__subcategory=sub_id, announcement__status='published')  # .distinct('announcement')
        elif integer_list and kelishuv == True:
            b = SubCategoryValues.objects.filter(Q(integer__in=integer_list), announcement__kelishuv=True, announcement__currency=currency,
                                                 params__subcategory=sub_id, announcement__status='published')  # .distinct('announcement')
        elif every_all_sell and kelishuv == True:
            b = SubCategoryValues.objects.filter(announcement__kelishuv=True, announcement__currency=currency,
                                                 params__subcategory=sub_id, announcement__status='published')  # .distinct('annonucement')
        elif integer_list and every_all_sell and kelishuv == True:

            b = SubCategoryValues.objects.filter(Q(integer__in=integer_list) | Q(selecttion__in=every_all_sell), announcement__kelishuv=True,
                                                 announcement__currency=currency, params__subcategory=sub_id, announcement__status='published')  # .distinct('announcement')
        elif not (integer_list and every_all_sell) and kelishuv == True:

            b = SubCategoryValues.objects.filter(
                announcement__kelishuv=True, params__subcategory=sub_id, announcement__status='published')
        else:
            b = SubCategoryValues.objects.filter(id=0)
        # b = SubCategoryValues.objects.filter(params__subcategory=sub_id)
        # distinct
        list_of_announce = [i[0] for i in list(b.values_list('announcement'))]
        query = AnnouncementModel.objects.filter(
            pk__in=list_of_announce, user_controller='active')
        paginate = MyCustomPagination()
        page = paginate.paginate_queryset(query, request)
        serializer = self.get_serializer(page, many=True)
        response = paginate.get_paginated_response(serializer.data)
        return Response({'success': True, 'data': response.data},content_type='application/json; charset=utf-8')


class UpdateAnnounceById(generics.RetrieveUpdateAPIView):
    queryset = AnnouncementModel.objects.all()
    serializer_class = UserUpdateAnnouncementSer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def update(self, request, *args, **kwargs):
        try:
            a = dict(request.POST)
            a = a['params']
            a = json.loads(a[0])
            SubCategoryValues.objects.filter(
                announcement=kwargs['pk']).delete()
            for key, value in a.items():
                val = a[key]
                for data in val:
                    if key in ['select', 'multiselect']:

                        subcategory_value = SubCategoryValues.objects.create(params=SubCategoryParams.objects.get(
                            pk=data[0]), announcement=AnnouncementModel.objects.get(pk=kwargs['pk']), selecttion=ParamSelectValues.objects.get(pk=data[1]))
                        subcategory_value.save()
                    if key == 'string':
                        subcategory_value = SubCategoryValues.objects.create(params=SubCategoryParams.objects.get(
                            pk=data[0]), announcement=AnnouncementModel.objects.get(pk=kwargs['pk']), string=data[1])
                        subcategory_value.save()
                    if key == 'integer':
                        subcategory_value = SubCategoryValues.objects.create(params=SubCategoryParams.objects.get(
                            pk=data[0]), announcement=AnnouncementModel.objects.get(pk=kwargs['pk']), integer=data[1])
                        subcategory_value.save()
        except:
            pass
        super().update(request, *args, **kwargs)
        query = AnnouncementModel.objects.filter(pk=kwargs['pk'])
        imagelist = query.values('images')
        images = json.loads(imagelist[0]['images'])
        try:
            imagelist = query.values('images')
            files = request.FILES.getlist('image')
            index_of_image = dict(request.POST)
            index_of_image = json.loads(index_of_image['index_of_image'][0])
            index_of_index = 0

            if files:
                for file in files:
                    default_storage.save(
                        f"photos/{year}/{month}/{day}/{file.name}", file)
                    link = f"/media/photos/{year}/{month}/{day}/{file.name}"
                    if index_of_image[index_of_index] >= len(images):
                        images.append(link)
                    else:
                        images[int(index_of_image[index_of_index])] = link
                    index_of_index += 1
                image_list = json.dumps(images)
                query.update(images=image_list, status='inactive')
        except:
            pass

        return Response({'success': True, 'message': 'updated'})

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        request_id = response.data['subcategory']
        request_data = SubCategoryParams.objects.filter(subcategory=request_id)

        select = []
        multiselect = []
        input_value = []
        selectvalues = {}
        request_ids = request_data.values()
        try:
            for isselect in request_ids:
                a = SubCategoryParams.objects.get(pk=int(isselect['id']))
                query = a.children.all().values('pk', 'value', 'parent_param')
                type_of_value = isselect['type_of_value']
                if type_of_value == 'select':
                    select.append({
                        'name': str(isselect['name']),
                        'value': query
                    })
                if type_of_value == 'multiselect':
                    multiselect.append({
                        'name': str(isselect['name']),
                        'value': query
                    })
                if type_of_value in 'string':
                    input_value.append(
                        {'pk': isselect['id'], 'value': isselect['name'], 'input_type': 'string'})
                if type_of_value in 'integer':
                    input_value.append(
                        {'pk': isselect['id'], 'value': isselect['name'], 'input_type': 'integer'})
            selectvalues['select'] = select
            selectvalues['multiselect'] = multiselect
            selectvalues['input_value'] = input_value
        except:
            return Response({'success': False, 'message': "null data"})
            # return Response({'success':True,'select':[],'multiselect':[],'input_value':[],'category_name':{'parent_id__name':'','name':''}})

        responsedata  = {'success': True, 'category_name': response.data, 'select': select,
                         'multiselect': multiselect, 'input_value': input_value}
        return Response(responsedata, content_type='application/json; charset=utf-8')
