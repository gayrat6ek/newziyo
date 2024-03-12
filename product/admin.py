from django.contrib import admin
from .models import SubCategoryModel,AnnouncementModel,SubCategoryParams
# Register your models here.
admin.site.register((SubCategoryModel,AnnouncementModel,SubCategoryParams))