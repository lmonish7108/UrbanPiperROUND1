from django.db import models
import datetime

# Create your models here.
class Content(models.Model):
	"""
	Content Model where all the stories will be stored.
	"""
	id = models.IntegerField(primary_key=True)
	title = models.CharField(max_length=512, blank=False)
	by = models.CharField(max_length=64, blank=False)
	url = models.CharField(max_length=512, blank=False)
	score = models.IntegerField()
	sentiment = models.CharField(default="neutral", max_length=16, blank=False)


class NewStories(models.Model):
	"""
	Singleton Module to compare time difference for updation of Stories with HackerNews.
	"""
	time_value = models.DateTimeField(auto_now=True)

	def save(self, *args, **kwargs):
		self.pk = 1
		super(NewStories, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		pass

	@classmethod
	def retrieve(cls):
		obj, created = cls.objects.get_or_create(pk=1)
		return obj
