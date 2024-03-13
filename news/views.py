from django.shortcuts import render
from .models import News,Recommandation
from rest_framework import permissions
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .serializers import AdminNewsAddSerializers, UserNewListSerializer, RecommendationSerializer, RecommendationActivateSer, RecommendationListSer, UserGetListRecommendSer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
# Create your views here.


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


class AdminListNewsApi(generics.ListAPIView):
    serializer_class = AdminNewsAddSerializers
    queryset = News.objects.all()
    permission_classes = (permissions.IsAdminUser, permissions.IsAuthenticated)
    pagination_class = MyCustomPagination
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {'success': True, "data": response.data}
        return response


class AdminListNewsSearchApi(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = AdminNewsAddSerializers
    permission_classes = [permissions.IsAdminUser]
    pagination_class = MyCustomPagination

    def list(self, request, *args, **kwargs):
        s = kwargs['s']
        queryset = News.objects.filter(
            Q(theme__icontains=s) | Q(body__icontains=s))
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        response = self.get_paginated_response(serializer.data)
        if not serializer.data:
            return Response({'success': False, "message": 'there is not data', "data": response.data}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'data': response.data}, status=status.HTTP_200_OK)





class AdminListCustomPagination(generics.ListAPIView):
    serializer_class = AdminNewsAddSerializers
    queryset = News.objects.all()
    permission_classes = (permissions.IsAdminUser, permissions.IsAuthenticated)
    pagination_class = MyCustomPagination

    def list(self, request, *args, **kwargs):
        query = News.objects.all()
        # MyCustomPagination.page_size = kwargs['paginate']
        paginate = MyCustomPagination()
        paginate.page_size = kwargs['paginate']
        page = paginate.paginate_queryset(query, request)
        serializer = self.get_serializer(page, many=True)
        response = paginate.get_paginated_response(serializer.data)
        return Response({'success': True, 'data': response.data}, status=status.HTTP_200_OK)


class AdminListFilterWithPagination(generics.ListAPIView):
    serializer_class = AdminNewsAddSerializers
    queryset = News.objects.all()
    permission_classes = (permissions.IsAdminUser, permissions.IsAuthenticated)
    pagination_class = MyCustomPagination

    def list(self, request, *args, **kwargs):
        if kwargs['order']=='new':
            query = News.objects.all().order_by('-date','-time')
        elif kwargs['order'] == 'old':
            query = News.objects.all().order_by('date', 'time')
        else:
            query = News.objects.all().order_by('?')
        # MyCustomPagination.page_size = kwargs['paginate']
        paginate = MyCustomPagination()
        paginate.page_size = kwargs['paginate']
        page = paginate.paginate_queryset(query, request)
        serializer = self.get_serializer(page, many=True)
        response = paginate.get_paginated_response(serializer.data)
        return Response({'success': True, 'data': response.data}, status=status.HTTP_200_OK)

class AdminNewsAddView(generics.CreateAPIView):
    serializer_class = AdminNewsAddSerializers
    queryset = News.objects.all()
    permission_classes = (permissions.IsAdminUser,permissions.IsAuthenticated)
    pagination_class = MyCustomPagination
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.data = {'success': True, "data": response.data}
        return response

class UpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdminNewsAddSerializers
    queryset = News.objects.all()
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data = {'success': True, "data": response.data}
        return response
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        response.data = {'success': True, "data": response.data}
        return response
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {'success': True, "data": response.data}
        return response

class BulkDeleteNewView(generics.DestroyAPIView): 
    queryset = News.objects.all()
    permission_classes = [permissions.IsAdminUser]
    def destroy(self, request, *args, **kwargs):
        data = News.objects.filter(pk__in=self.request.data['pk'])
        data.delete()
        
        return Response({'success':True,"message":'all data has been delated'},status=status.HTTP_204_NO_CONTENT)



class RecommendationView(generics.CreateAPIView):
    queryset = Recommandation.objects.all()
    serializer_class = RecommendationSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {'success':True,'data':response.data}
        return response


class RecommendationActivateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recommandation.objects.all()
    serializer_class = RecommendationActivateSer
    permission_classes = [permissions.IsAdminUser]
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data = {'status':True,'data':response.data}

        return response
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {'status':True,'data':response.data}
        return response
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        response.data = {'status': True, 'data': response.data}
        return response



class RecommendationListView(generics.ListAPIView):
    queryset = Recommandation.objects.all()
    serializer_class = RecommendationListSer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = MyCustomPagination
    def list(self, request, *args, **kwargs):
        response = super().list(request,*args,**kwargs)
        response.data = {'success':True,'data':response.data}
        return response


class AdminListGetRecommend(generics.ListAPIView):
    queryset = Recommandation.objects.all()
    serializer_class = RecommendationListSer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = MyCustomPagination

    def list(self, request, *args, **kwargs):
        s = kwargs['s']
        queryset = Recommandation.objects.filter(
            Q(title__icontains=s) | Q(body__icontains=s))
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        response = self.get_paginated_response(serializer.data)
        if not serializer.data:
            return Response({'success': True, "message": 'there is not data', "data": response.data}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'data': response.data}, status=status.HTTP_200_OK)


class AdminRecommendfilterPagination(generics.ListAPIView):
    serializer_class = RecommendationListSer
    queryset = Recommandation.objects.all()
    permission_classes = (permissions.IsAdminUser, permissions.IsAuthenticated)
    pagination_class = MyCustomPagination

    def list(self, request, *args, **kwargs):
        if kwargs['status'] == 'inactive':
            query = Recommandation.objects.filter(status='inactive')
        elif kwargs['status'] == 'active':
            query = Recommandation.objects.filter(status='active')
        else:
            query = Recommandation.objects.all().order_by('?')
        # MyCustomPagination.page_size = kwargs['paginate']
        paginate = MyCustomPagination()
        paginate.page_size = kwargs['paginate']
        page = paginate.paginate_queryset(query, request)
        serializer = self.get_serializer(page, many=True)
        response = paginate.get_paginated_response(serializer.data)
        return Response({'success': True, 'data': response.data}, status=status.HTTP_200_OK)


class AdminRecommendOnlyPagination(generics.ListAPIView):
    serializer_class = RecommendationListSer
    queryset = Recommandation.objects.all()
    permission_classes = (permissions.IsAdminUser, permissions.IsAuthenticated)
    pagination_class = MyCustomPagination

    def list(self, request, *args, **kwargs):
        query = Recommandation.objects.all()
        # MyCustomPagination.page_size = kwargs['paginate']
        paginate = MyCustomPagination()
        paginate.page_size = kwargs['paginate']
        page = paginate.paginate_queryset(query, request)
        serializer = self.get_serializer(page, many=True)
        response = paginate.get_paginated_response(serializer.data)
        return Response({'success': True, 'data': response.data}, status=status.HTTP_200_OK)


# ----------------------USER----------------------------------------------USER------------------------------------




from datetime import datetime
import pytz
tz = pytz.timezone("Asia/Tashkent")
now_hour = datetime.now(tz).time().strftime('%H:%M:%S')
now_year = datetime.now(tz).today()
from django.db.models import Q

class UserNewListView(generics.ListAPIView):
    serializer_class = UserNewListSerializer
    queryset = News.objects.filter(Q(date__lt=now_year) | (Q(time__lt=now_hour) & Q(date__lt=now_year)))
    pagination_class = MyCustomPagination
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {'success': True, "data": response.data}
        return response

import os


def calculate_similarity(s1, s2):
    common_prefix = os.path.commonprefix([s1, s2])
    return len(common_prefix) / max(len(s1), len(s2))
class UserNewsGetDetailView(generics.RetrieveAPIView):
    serializer_class = AdminNewsAddSerializers
    queryset = News.objects.all()
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        news_obj = News.objects.filter(pk=kwargs['pk'])
        serializer = self.get_serializer(news_obj,many=True)
        if not serializer.data:
            return Response({'success': False, 'Message': "there is not data related to this key"})
        if serializer.data[0]['viewers'] is not None:
            viewers = serializer.data[0]['viewers']+1

            news_obj[0].viewers = viewers
            news_obj[0].save()
        else:
            viewers = 1

            news_obj[0].viewers = viewers

        query = News.objects.filter(~Q(pk=response.data['pk'])).order_by('-date','-time')[:5]
        data = self.get_serializer(query,many=True) 
        return Response({'success': True, 'data': response.data,'similar':data.data})




class UserGetListReCommend(generics.ListAPIView):
    serializer_class = UserGetListRecommendSer
    queryset = Recommandation.objects.filter(Q(start_date__lte=now_year)&Q(end_date__gte=now_year),status='active')
    pagination_class = None
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {'success': True, "data": response.data}
        return response



data = [
    {'region': 'Andijon viloyati', 'district': [
        'Andijon', 'Asaka', 'Baliqchi', 'Bo`z', 'Oltinko`l', 'Shahrixon', 'Ulug`nor']},
    {'region': 'Buxoro viloyati', 'district': ['Alat', 'Beshariq', 'G`ijduvon', 'Jondor',
        'Karakul', 'Kogon', 'Olot', 'Paxtakor', 'Qorako`l', 'Romitan', 'Shofirkon', 'Vobkent']},
    {'region': 'Farg`ona viloyati', 'district': ['Beshkent', 'Buvayda', 'Dang`ara', 'Farg`ona',
        'Forish', 'Qo`qon', 'Quva', 'Rishton', 'So`x', 'Toshloq', 'Uchko`prik', 'O`zbekiston']},
    {'region': 'Jizzax viloyati', 'district': [
        'Arnasoy', 'Baxmal', 'Do`stlik', 'Forish', 'Gallaorol', 'Mirzachul', 'Paxtachi', 'Sharof Rashidov', 'Zafarobod']},
    {'region': 'Xorazm viloyati', 'district': [
        'Bog`ot', 'Gurlan', 'Xiva', 'Shovot', 'Urganch', 'Vurg`on']},
    {'region': 'Namangan viloyati', 'district': [
        'Chartak', 'Chust', 'Kosonsoy', 'Namangan', 'Norin', 'Pop', 'To`raqo`rg`on', 'Uychi', 'Yangiqo`rg`on']},
    {'region': 'Navoiy viloyati', 'district': [
        'Xatirchi', 'Karmana', 'Konimeh', 'Navbahor', 'Nurota', 'Tomdi', 'Uchquduq']},
    {'region': 'Qashqadaryo viloyati', 'district': ['Chiroqchi', 'Dehqonobod', 'G`uzor', 'Kamashi',
        'Kasbi', 'Kitob', 'Koson', 'Muborak', 'Nishon', 'Qarshi', 'Shaxrisabz', 'Yakkabog`']},
    {'region': 'Samarqand viloyati', 'district': ['Bulung`ur','Oqdaryo', 'Ishtixon', 'Jomboy', 'Kattaqo`rg`on',
        'Narpay', 'Nurobod', 'Oqdaryo', 'Paxtachi', 'Payariq', 'Pastdarg`om', 'Samarqand', 'Toyloq']},
    {'region': 'Sirdaryo viloyati', 'district': [
        'Akaltyn', 'Bayavut', 'Boyovut', 'Farish', 'G`uliston', 'Mirzaobod', 'Sardoba', 'Sayxunobod', 'Shirin']},
    {'region': 'Qoraqalpog`iston Respublikasi', 'district': [
        'Beruniy', 'Ellikqal`a', 'Kegeyli', 'Mo`ynoq', 'Nukus', 'Qarao`zek', 'Qonliko`l', 'Qo`ng`irot', 'Qo`shko`pir', 'Taxiatosh']},
    {'region': 'Surxondaryo viloyati', 'district': [
        'Angor', 'Boysun', 'Denov', 'Jarqo`rg`on', 'Muzrabot', 'Oltinsoy', 'Qiziriq', 'Sherobod', 'Sho`rchi', 'Sariosiyo']},
    {'region': 'Toshkent shahri', 'district': ['Mirzo Ulug`bek', 'Yunusobod', 'Mirobod', 'Shayxontohur',
                                               'Sergeli', 'Chilonzor', 'Olmazor', 'Uchtepa', 'Yakkasaroy', 'Shayhontohur', 'O`rtachirchiq', 'Bektemir']},
    {'region': 'Toshkent viloyati', 'district': ['Ahangaron', 'Bekobod', 'Bostanliq', 'Bo`ka', 'Yangiyo`l', 'Zangiota',
                                                 'Zarafshon', 'Ohangaron', 'O`rta Chirchiq', 'Parkent', 'Piskent', 'Quyi Chirchiq', 'Chinoz', 'Chirchiq']}
    ]


datacyrill = [
    {'region': 'Андижон вилояти', 'district': ['Андижон', 'Асака', 'Балиқчи', 'Бўз', 'Олтинкўл', 'Шаҳрихон', 'Улугнор']},
    {'region': 'Бухоро вилояти', 'district': ['Алат', 'Бешариқ', 'Ғиждувон', 'Жондор', 'Қоракўл', 'Қогон', 'Олот', 'Пахтачирчиқ']},
    {'region': 'Қашқадарё вилояти', 'district': ['Қарши', 'Қамаши', 'Қаршинский', 'Қасбинский', 'Қарчин', 'Қизириқ', 'Қизилтепа', 'Миришкор', 'Муборак', 'Нишон', 'Қарши', 'Қарчин', 'Қизилтепа']},
    {'region': 'Қорақалпоғистон Республикаси', 'district': ['Беруний', 'Элликқалъа', 'Кегейли', 'Мўйноқ', 'Нукус', 'Қараўзек', 'Қонликўл', 'Қўңирот', 'Қўшкоўпир', 'Тахиаташ']},
    {'region': 'Навоий вилояти', 'district': ['Ғўйтепа', 'Кизириқ', 'Қизилўрда', 'Қўшрўн', 'Навбаҳор', 'Томди', 'Учқудуқ']},
    {'region': 'Наманган вилояти', 'district': ['Наманган', 'Тўракўл', 'Уйчи', 'Чуст', 'Мингбулоқ']},
    {'region': 'Самарқанд вилояти', 'district': ['Пахтачи', 'Оқдарё','Иштихон','Булунғур', 'Жомбой', 'Каттақўрғон', 'Қўшработ', 'Нарпай', 'Нурабод', 'Пайарик', 'Пастдарғом', 'Самарқанд', 'Тойлоқ']},
    {'region': 'Сирдарё вилояти', 'district': ['Гулистон', 'Мирзачўл', 'Оқолтаин', 'Сардоба', 'Ширин', 'Сайхунобод']},
    {'region': 'Сурхондарё вилояти', 'district': ['Ангор', 'Бойсун', 'Денов', 'Жарқўрғон',
                                                  'Кизириқ', 'Қизириш', 'Музробод', 'Оққўрғон', 'Сариасия', 'Термез', 'Узун', 'Шерабод']},
    {'region': 'Тошкент шаҳри', 'district': [
        'Мирабад', 'Мирзо-Улуғбек', 'Сергели', 'Учтепа', 'Шайхонтоҳур', 'Юнусобод', 'Яккасарой']},
    {'region': 'Тошкент вилояти', 'district': ['Бекобод', 'Бўка', 'Бука', 'Зангиота',
                                               'Зафар', 'Кибрай', 'Куйичирчик', 'Паркент', 'Пскент', 'Тойлоқ', 'Янгибозор']}
    ]

class UserGetListDistrict(generics.ListAPIView):
    serializer_class = UserGetListRecommendSer
    permission_classes = [permissions.IsAuthenticated]
    def list(self, request, *args, **kwargs):
        # if self.request.user.language == 'cyrill':
        #     response = {'success':True,'data':datacyrill}
        # else:
        response = {'success':True,'data':data}
        return Response(response,content_type='application/json; charset=utf-8')



class Usergetversion(generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        return Response({'version':2})

