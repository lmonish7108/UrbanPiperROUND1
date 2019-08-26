import requests
import datetime
import json
import pytz
from aylienapiclient import textapi

from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.conf import settings

from api.models import NewStories, Content
from api.serializers import ContentSerializer


def need_to_update(threshold=60, request_url="https://hacker-news.firebaseio.com/v0/newstories.json", top_news=False):
	time_1 = NewStories.retrieve()
	utc = pytz.UTC
	time_diff = (utc.localize(datetime.datetime.now()) - NewStories.objects.get().time_value).total_seconds()
	if time_diff > threshold or Content.objects.all().count() == 0:
		NewStories.objects.get().save()
		stories_id_list = json.loads(requests.get(request_url).content)[:10]
		for story_id in stories_id_list:
			try:
				Content.objects.get(pk=story_id)
			except ObjectDoesNotExist:
				story_api = 'https://hacker-news.firebaseio.com/v0/item/'+ str(story_id) +'.json'
				content = json.loads(requests.get(story_api).content)
				sentiment_client = textapi.Client(settings.X_AYLIEN_APP_ID, settings.X_AYLIEN_API_KEY)
				content['sentiment'] = sentiment_client.Sentiment({'text': content['title']})['polarity']
				serializer = ContentSerializer(data=content)
				if serializer.is_valid():
					serializer.save()
	if top_news:
		stories_list = ContentSerializer(Content.objects.all().order_by("-score")[:5], many=True)
	else:
		stories_list = ContentSerializer(Content.objects.all()[:20], many=True)
	return stories_list.data


def landing_page(request):
	if request.method == "GET":
		stories_list = json.dumps(need_to_update(threshold=7200))
		return render(request, "api/LandingPage.html", {"stories_list": stories_list})


def top_news(request):
	if request.method == "GET":
		stories_list = json.dumps(need_to_update(threshold=60, request_url="https://hacker-news.firebaseio.com/v0/topstories.json", top_news=True))
		return render(request, "api/LandingPage.html", {"stories_list": stories_list})


def get_search_title(request, search_str):
	titles_list = list(Content.objects.filter(title__icontains=search_str)[:5].values("title","url"))
	return HttpResponse(json.dumps(titles_list))

