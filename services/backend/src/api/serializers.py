from re import L
from rest_framework import serializers
from api.models import Profile, Character, Campaign

class CharacterSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    

# class ProfileSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     userid = serializers.PrimaryKeyRelatedField(read_only=True)
#     username = serializers.CharField(read_only=False)

#     def create(self, validated_data):
#         return Profile.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.username = validated_data.get('username', instance.username)
#         instance.save()
#         return instance
    
#     class Meta:
#         model = Profile
#         fields = ['id', 'userid', 'username']
