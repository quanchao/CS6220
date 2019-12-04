from django.http import HttpResponse
from django.shortcuts import render
from SuggestMe.models import IMG
import json
from urllib.parse import quote
import sys
import requests
from pprint import pprint
import sys
from keras.models import load_model
import numpy as np
import argparse
import imutils
import cv2
import os
from keras import backend as K

MAX_INT = sys.maxsize
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'
DEFAULT_TERM = 'burger'
DEFAULT_LOCATION = 'Atlanta, GA'
SEARCH_LIMIT = 3

API_KEY = "lAaHwPwcL0STM1IIjXwfTz7H5PyrXbSCHMgPQs5zsuciD5HPeyHcl2c8ABD4iG1cUg0x_Gk1OqXBOyIBVhkKKgZNswO2Q3hCsJhXhynbifYYT1hs-ouOvT6n06rcXXYx"
COMMENT_SIZE = 83

base_dir = 'C:/Users/wiki/Desktop/gatech/CS6220/project/SuggestMe'
img_path = 'background2.jpg'
CLASSES = ["cheesecake", "pancake","sashimi", "steak", "ice_cream", 
"pizza", "other_sandwich", "wings", "burrito", "dumpling", "fried_chicken", 
"pasta", "waffle", "curry", "fried_rice", "sushi", "waffle", "omelette", 
"spring_rolls", "ramen"]

def predict(path):
    K.clear_session()
    image = cv2.imread(base_dir+path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))
    image = image.astype("float32")
    mean = np.array([123.68, 116.779, 103.939][::1], dtype="float32")
    image -= mean
    model = load_model(base_dir+'/moreData_IV3_warm.model')
    preds = model.predict(np.expand_dims(image, axis=0))[0]
    i = np.argmax(preds)
    label = CLASSES[i]
    K.clear_session()
    return label

def businessRequest(url_params):
	headers = {
			'Authorization': 'Bearer %s' % API_KEY,
	}
	host = API_HOST
	path = SEARCH_PATH
	url = "%s%s"%(host, quote(path.encode('utf8')))
	response = requests.request('GET', url, headers=headers, params=url_params)
	return response.json()


def getBusinessComment(business_id):
	headers = {
				'Authorization': 'Bearer %s' % API_KEY,
		}
	host = API_HOST
	path = BUSINESS_PATH
	path = path + business_id+ "/reviews"
	url = "%s%s"%(host, quote(path.encode('utf8')))
	response = requests.request('GET', url, headers=headers, params={})
	response = response.json()
	if not response:
		return None
	else:
		reviewTextList = []
		for i in range(len(response["reviews"])):
			reviewTextList.append(response["reviews"][i]["text"])
		minDistance =  MAX_INT
		bestReview = None
		for reviewText in reviewTextList:
			reviewText = reviewText.replace("\n"," ")
			reviewText = reviewText.replace("\r"," ")
			reviewText = reviewText.replace("\r\n"," ")
			if abs(len(reviewText) - COMMENT_SIZE)< minDistance:
				minDistance = abs(len(reviewText) - COMMENT_SIZE)
				bestReview = reviewText
		if len(reviewText)<COMMENT_SIZE :
			return reviewText
		else:
			for i in range(80, -1, -1):
				if reviewText[i] == " ":
					pos = i
					break
			reviewText = reviewText[:pos+1] + "..."
		return reviewText

def search_api(term):
	restaurant_list  = []
	latlng = []
	location = DEFAULT_LOCATION
	url_params = {
			'term': term.replace(' ', '+'),
			'location': location.replace(' ', '+'),
			'limit': SEARCH_LIMIT
	}
	businesses = businessRequest(url_params)
	businessesKey = businesses['businesses']
	for business in businessesKey:
		business_id = business["id"] 
		restaurant={}
		restaurant["name"] = business["name"]
		restaurant["photo_id"] = business["image_url"]
		restaurant["address"] = business["location"]["address1"]
		restaurant["comment"] = getBusinessComment(business_id)
		restaurant["city"] = "%s, %s"%(business["location"]["city"],business["location"]["state"])
		categoryString = business["categories"][0]["title"]
		for categoryName in business["categories"][1:]:
			categoryString = categoryString+ ", "+ categoryName["title"]
		restaurant["category"] = categoryString
		restaurant["rating"] = business["rating"]
		restaurant["url"] = business["url"]
		restaurant_list.append(restaurant)
		latlng.append(business['coordinates'])
	return restaurant_list,latlng

def index(request):
    return render(request, 'index.html')

def login(request):
	return render(request,'login.html')

def user_login(request):
	return render(request, 'user_index.html')

def search(request):
	return render(request, 'search.html')

def results(request):
	#get the image file from post data
	new_img = IMG(img=request.FILES.get('img'))
	new_img.save()
	
	#predict the name of the food
	
	label = predict(new_img.img.url)
	#give recommendation based on the label
	restaurant_list,latlng = search_api(label)

	content = {
		'aaa':new_img,
		'label':label,
		'restaurant_list':restaurant_list,
		'latlng':json.dumps(latlng),
	}
	return render(request,'results.html',content)