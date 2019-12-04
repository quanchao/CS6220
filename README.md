# Suggest Me
## DataPreprocessing

In this project, we used two datasets. One is yelp dataset, which url is https://www.yelp.com/dataset/download, another one is food101, which can be downloaded in http://data.vision.ee.ethz.ch/cvl/food-101.tar.gz.

Food101 is a pretty good dataset, so we do not need any preprocess of data, however, in yelp's datasets, there is no food class label. What I did is to generate the file "foodComment.txt". After that, we used the critical term in the comment to label the pictures. Those codes are in the DataPreprocessing.ipynb in the DataPreprocessing folder.

Btw, the food class I have chosen is foodClass = {"cheesecake", "mussels", "waffles", "pizza", "fried_rice", "dumplings",  "steak", "tacos", "donuts", "sushi"}.



## Model traing



