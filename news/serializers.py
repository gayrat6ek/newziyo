from rest_framework import serializers
from .models import News, Recommandation
from .transliterate import to_cyrillic

class AdminNewsAddSerializers(serializers.ModelSerializer):
    pk = serializers.ReadOnlyField()
    viewers = serializers.ReadOnlyField(read_only=True)
    class Meta:
        model = News
        fields = ['theme','images','body','date','time','pk','viewers']
    def to_representation(self, instance):
        user = self.context['request'].user
        representation = super().to_representation(instance)
        if user.language == 'cyrill':
            representation['theme'] = to_cyrillic(representation['theme'])
            representation['body'] = to_cyrillic(representation['body'])
        return representation


class UserNewListSerializer(serializers.ModelSerializer):
    pk = serializers.ReadOnlyField()
    viewers = serializers.ReadOnlyField(read_only=True)
    class Meta:
        model = News
        fields = ['theme','images','date','time','pk','viewers']
    def to_representation(self, instance):
        user = self.context['request'].user
        representation = super().to_representation(instance)
        if user.language == 'cyrill':
            representation['theme'] = to_cyrillic(representation['theme'])
        return representation



class RecommendationSerializer(serializers.ModelSerializer):
    pk = serializers.ReadOnlyField()
    class Meta:
        model = Recommandation
        fields = ['pk','start_date','end_date','body','title','image']

class RecommendationActivateSer(serializers.ModelSerializer):
    class Meta:
        model = Recommandation
        fields = ['status']

class RecommendationListSer(serializers.ModelSerializer):
    class Meta:
        model = Recommandation
        fields = ['pk','start_date','end_date','title','status']


class UserGetListRecommendSer(serializers.ModelSerializer):
    class Meta:
        model = Recommandation
        fields = ['pk','title','body','image']
    def to_representation(self, instance):
        user = self.context['request'].user
        representation = super().to_representation(instance)
        if user.language == 'cyrill':
            representation['title'] = to_cyrillic(representation['title'])
            representation['body'] = to_cyrillic(representation['body'])
        return representation


    






