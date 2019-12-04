# CS 6220 
## DataPreprocessing

In this project, we used two datasets. One is yelp dataset, which url is https://www.yelp.com/dataset/download, another one is food101, which can be downloaded in http://data.vision.ee.ethz.ch/cvl/food-101.tar.gz.

Food101 is a pretty good dataset, so we do not need any kind of preprocessing, however, in yelp's datasets, there is no food class label. What I did is to generate the file "foodComment.txt". After that, we used the critical term in the comments to label the pictures. Those codes are in the DataPreprocessing.ipynb in the DataPreprocessing folder.

Btw, the food class I have chosen is foodClass = {"cheesecake", "mussels", "waffles", "pizza", "fried_rice", "dumplings",  "steak", "tacos", "donuts", "sushi"}.



## Model training

I used two models in this project. The first one is Inceptionv3 model.  


###Reference
1.https://colab.research.google.com/github/theimgclist/examples/blob/MultiClassTF2.0/community/en/multi_class_classification/food_classifier.ipynb

2.




##Recommendation System

This part is the fronted_End of the previous part. What we are going to do here is to upload any picture, after that, we used our models to produce a label for that picture. SearchAPI.py is what I wrote to search for a nearby reasturant using the returned food label by Yelp's API. A website was developed to display the results.


To run this part, please go to the directory recommendationSystem, In the terminate, input
***python manage.py runserver***


##Future Work

The future work was designed to predict a person's resturant preference base on his friends's historical data, we generated two files, one is user's friendShip, the other one is the history data of user. Those files are in the folder futureWork. This did not work because in this data, a user has very small amount of friends, the information is simply not enough to do predictions. 