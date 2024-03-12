from django.core.files.storage import default_storage
from rest_framework import serializers
from .models import CreateCategoryModel, SubCategoryModel, SubCategoryParams, SubCategoryValues, AnnouncementModel, NotisificationModel,ParamSelectValues
from cyrtranslit import to_cyrillic

from .transliterate import to_cyrillic
class CreateCategorySerializer(serializers.ModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = CreateCategoryModel
        fields = ['pk','name','icon']

class SubCategorySerializer(serializers.ModelSerializer):
    parent_name = serializers.ReadOnlyField(source='parent.name')
    pk = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = SubCategoryModel
        fields = ['name','parent',"parent_name",'pk']



class SubCategoryUpdateSerializer(serializers.ModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = SubCategoryModel
        fields = ['name','parent','pk']


class CategoryUpdateSerializer(serializers.ModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = CreateCategoryModel
        fields = ['name', 'icon','pk']
        

class SubCategoryListByIdSer(serializers.ModelSerializer): 
    parent_name = serializers.ReadOnlyField(source='parent.name')   
    count_announce = serializers.SerializerMethodField()    
    pk = serializers.PrimaryKeyRelatedField(read_only=True) 
    class Meta:
        model = SubCategoryModel
        fields = ['name', 'parent', "parent_name", 'pk','count_announce']
    def get_count_announce(self,obj):
        return AnnouncementModel.objects.filter(subcategory=obj.pk, status='published').count()
    def to_representation(self, instance):
        user = self.context['request'].user
        representation = super().to_representation(instance)
        if user.language == 'cyrill':
            representation['name'] =to_cyrillic(representation['name'])
            representation['parent_name'] = to_cyrillic(representation['parent_name'])
        return representation

class CreateParamsSerializer(serializers.ModelSerializer):
    pk = serializers.ReadOnlyField(read_only=True)
    class Meta:
        model = SubCategoryParams
        fields = ['pk', 'subcategory', 'name']


class AdminGetAnnouncementSerializer(serializers.ModelSerializer):
    pk = serializers.ReadOnlyField()
    category = serializers.CharField(source='subcategory.parent.name')
    subcategory = serializers.CharField(source='subcategory.name')
    user = serializers.CharField(source='user.phone_number')
    class Meta:
        model = AnnouncementModel
        fields = ['pk', 'title', 'district',
                  'subcategory', 'status', 'category', 'user']

class AdminSubcategoryValuesSerializer(serializers.ModelSerializer):
    params = serializers.CharField(source ='params.name')
    class Meta:
        model = SubCategoryValues
        fields = ['pk','params','value']


class AdminGetAnnounceById(serializers.ModelSerializer):
    pk = serializers.ReadOnlyField()
    category = serializers.CharField(source='subcategory.parent.name')
    subcategory = serializers.CharField(source='subcategory.name')
    phone_number = serializers.CharField(source='user.phone_number')
    user_image = serializers.ImageField(source='user.image')
    full_name = serializers.CharField(source='user.full_name')
    user_tarif = serializers.CharField(source='user.tarif')
    title = serializers.CharField()
    class Meta:
        model = AnnouncementModel
        fields = ['pk', 'title', 'subcategory', 'district', 'status', 'category', 'body', 'price', 'location',
                  'currency', 'images', 'phone_number', 'user_image', 'user_tarif', 'full_name', 'kelishuv']
        


class UpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementModel
        fields = ['status','notisification']



class NotisificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotisificationModel
        fields = ['pk','theme','value','date','time']


class CreateParamsTypeOfValueSeri(serializers.ModelSerializer):
    pk =serializers.ReadOnlyField()
    class Meta:
        model = SubCategoryParams
        fields = ['pk','subcategory','name','type_of_value']

    

#------------------User-------------------User------------------User----------------- 
from datetime import date
today = date.today()
year = today.year
month = today.month
day = today.day
import json
#class AddAnnouncementSerializer(serializers.Serializer):
#    subcategory = serializers.IntegerField()
#    currency = serializers.ChoiceField(
#        choices=(('Dollar', 'dollar'), ('Som', 'som')))
#    price = serializers.FloatField()
#    location = serializers.URLField()
#    image = serializers.FileField()
#    user = serializers.
class AddAnnouncementSerializer(serializers.ModelSerializer):
    #params = serializers.CharField(write_only=True)
   #image = serializers.ListField(
   #    child=serializers.ImageField(max_length=100000,allow_empty_file=False,use_url=False),write_only=True
   #)
    images= serializers.ReadOnlyField()
    pk = serializers.ReadOnlyField()
    class Meta:
        model = AnnouncementModel
        fields = ['pk', 'title', 'subcategory', 'district', 'currency', 'price', 'location',
                  'image', 'images', 'body', 'contact_name', 'contact_number', 'kelishuv']
    def create(self, validated_data):
        return super().create(validated_data)



class UserGetListCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateCategoryModel
        fields = ['pk','name','icon']
    def to_representation(self, instance):
        user = self.context['request'].user
        representation = super().to_representation(instance)
        if user.language == 'cyrill':
            representation['name'] =to_cyrillic(representation['name'])
        return representation



class UserGetListAnnounceSerializer(serializers.ModelSerializer):
    likers_count = serializers.SerializerMethodField()
    is_top = serializers.SerializerMethodField()
    class Meta:
        model = AnnouncementModel
        fields = ['pk', 'images', 'title', 'time', 'date', 'district', 'viewers', 'likers_count',
                  'price', 'currency', 'location', 'is_top', 'user', 'user_controller', 'kelishuv']
    def to_representation(self, instance):
        user = self.context['request'].user
        representation = super().to_representation(instance)
        if user.language == 'cyrill':
            representation['title'] =to_cyrillic(str(representation['title']))
            representation['currency'] = to_cyrillic(representation['currency'])
        return representation

    def get_likers_count(self,obj):
        return obj.likers.all().count()
    def get_is_top(self,obj):
        if obj.user.tarif in ['turbo','premium']:
            return True
        return False
        
class UserMakeInactiveSer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementModel
        fields = ['user_controller']
        



class GetParamsBySelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategoryParams
        fields = ['pk','subcategory','name','type_of_value']

class GetSelectValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParamSelectValues
        fields = ['pk','parent_param','value']


class UserGetAnnounceById(serializers.ModelSerializer):
    pk = serializers.ReadOnlyField()
    category = serializers.CharField(source='subcategory.parent.name')
    subcategory_name = serializers.CharField(source='subcategory.name')
    user_image = serializers.ImageField(source='user.image')
    is_liked = serializers.SerializerMethodField()
    class Meta:
        model = AnnouncementModel
        fields = ['pk', 'title', 'is_liked', 'date', 'district', 'time', 'subcategory', 'user_image', 'status', 'category', 'body',
                  'price', 'location', 'currency', 'images', 'viewers', 'subcategory_name', 'contact_name', 'contact_number', 'kelishuv']
         
    def get_is_liked(self,obj):
        a = self.context.get('request',None)
        try:
            is_null = obj.likers.filter(phone_number=a.user)
        except:
            return False
        if not list(is_null):
            return False
        return True
    def to_representation(self, instance):
        user = self.context['request'].user
        representation = super().to_representation(instance)
        representation['title'] =to_cyrillic(representation['title'])
        representation['category'] = to_cyrillic(representation['category'])
        representation['body'] = to_cyrillic(representation['body'])
        representation['subcategory_name'] = to_cyrillic(representation['subcategory_name'])
        representation['contact_name'] = to_cyrillic(representation['contact_name'])
        representation['title'] = to_cyrillic(representation['title'])
        representation['currency'] = to_cyrillic(representation['currency'])
        return representation

class ParamsValSer(serializers.Serializer):
    name = serializers.ReadOnlyField(source='params.name')
    values = serializers.CharField(source = 'integer')
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['name'] = to_cyrillic(representation['name'])
        return representation
class ParamsValSerSt(serializers.Serializer):
    name = serializers.ReadOnlyField(source='params.name')
    values = serializers.ReadOnlyField(source = 'string')
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['name'] = to_cyrillic(representation['name'])
        representation['values'] = to_cyrillic(representation['values'])
        return representation

class UserUpdateAnnouncementSer(serializers.ModelSerializer):
    images= serializers.ReadOnlyField()
    pk = serializers.ReadOnlyField()
    subcategory = serializers.ReadOnlyField(source='subcategory.pk')
    class Meta:
        model = AnnouncementModel
        fields = ['pk','title','subcategory','currency','district','body','price','location','image','images','contact_name','contact_number','kelishuv']