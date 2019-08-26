from rest_framework import serializers
from api.models import NewStories, Content


class ContentSerializer(serializers.Serializer):
	id = serializers.IntegerField(required=True)
	title = serializers.CharField(required=True, allow_blank=False, max_length=512)
	by = serializers.CharField(required=True, allow_blank=False, max_length=64)
	url = serializers.CharField(required=True, allow_blank=False, max_length=512)
	score = serializers.IntegerField(required=False)
	sentiment = serializers.CharField(required=True, allow_blank=False, max_length=16)

	def create(self, validated_data):
		"""
		Create and return a new `Snippet` instance, given the validated data.
		"""
		return Content.objects.create(**validated_data)

	def update(self, instance, validated_data):
		"""
		Update and return an existing `Snippet` instance, given the validated data.
		"""
		instance.id = validated_data.get('id', instance.id)
		instance.title = validated_data.get('title', instance.title)
		instance.by = validated_data.get('by', instance.by)
		instance.url = validated_data.get('url', instance.url)
		instance.score = validated_data.get('score', instance.score)
		instance.save()
		return instance
