from re import L
from rest_framework import serializers
from cwn.models import Profile, Character, Campaign

class ProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.DjangoModelField(read_only=True)
    username = serializers.CharField(read_only=False)

    def create(self, validated_data):
        return Profile.objects.create(**validated_data)
    