# coding:utf-8

from urllib.parse import quote
import sys
import requests
from pprint import pprint
import sys
MAX_INT = sys.maxsize
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'
DEFAULT_TERM = 'burger'
DEFAULT_LOCATION = 'Atlanta, GA'
SEARCH_LIMIT = 3

API_KEY = "lAaHwPwcL0STM1IIjXwfTz7H5PyrXbSCHMgPQs5zsuciD5HPeyHcl2c8ABD4iG1cUg0x_Gk1OqXBOyIBVhkKKgZNswO2Q3hCsJhXhynbifYYT1hs-ouOvT6n06rcXXYx"
COMMENT_SIZE = 83
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

def search(term = DEFAULT_TERM):
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
		#print(business)
		business_id = business["id"] 
		restaurant={}
		restaurant["url"] = business["url"]
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
		
		restaurant_list.append(restaurant)
		latlng.append(business['coordinates'])
	return restaurant_list,latlng


restaurant_list,latlng = search("china")
print(restaurant_list)
print(latlng)
	


