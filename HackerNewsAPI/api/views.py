import requests
import datetime
import json
import pytz
from aylienapiclient import textapi

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.conf import settings

from api.models import NewStories, Content
from api.serializers import ContentSerializer


def need_to_update(threshold=86400, request_url="https://hacker-news.firebaseio.com/v0/newstories.json", top_news=False):
	"""
	This method gets the Stories.
	If the DB is empty it will fetch from HackerNews and store and display.
	You can have manual update of news Stories from HackerNews by providing proper threshold.
	"""
	# Get or create NewStories time threshold record.
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

				# Sentiment analysis flow
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
	"""
	Home Page gets updated with new stories from HackerNews every 1 hour.
	"""
	if request.method == "GET":
		stories_list = json.dumps(need_to_update(threshold=3600))
		return render(request, "api/LandingPage.html", {"stories_list": stories_list})


def top_news(request):
	"""
	Top News as per the upvotes.
	Gets updated with new Top stories from Hacker news every 5 minutes.
	"""
	if request.method == "GET":
		stories_list = json.dumps(need_to_update(threshold=300, request_url="https://hacker-news.firebaseio.com/v0/topstories.json", top_news=True))
		return render(request, "api/LandingPage.html", {"stories_list": stories_list})


def get_search_title(request, search_str):
	"""
	Provides the list of Content as per the search string criteria.
	"""
	titles_list = list(Content.objects.filter(title__icontains=search_str)[:5].values("title","url"))
	return HttpResponse(json.dumps(titles_list))

