import json
import collections
import matplotlib
import matplotlib.pyplot as plt
import random

userSet = set()
businessSet = set()
userBusinessDict = collections.defaultdict(list)
userFriendDict = collections.defaultdict(list)


userDict = dict()
businessDict = dict()


def userBusinessRelation(tipFile, userBusiness,topUserBusiness,topNum):
    print("0")
    with open('./yelp_dataset/user.json') as user_file:
        for line in user_file.readlines():
            data = json.loads(line)
            user = data["user_id"]
            friends = data["friends"]
            friends = friends.split(",")
            for friend in friends:
                userFriendDict[user].append(friend)
                
    print("1")
    with open(tipFile) as json_file, open(userBusiness, "w") as userBusinessFile:
        for line in json_file.readlines():
            data = json.loads(line)
            userBusinessDict[data["user_id"]].append(data["business_id"])
            if not data["user_id"] in userSet:
                userSet.add(data["user_id"])
            if not data["business_id"] in businessSet:
                businessSet.add(data["business_id"])
            userBusinessFile.write(data["user_id"]+"\t")
            userBusinessFile.write(data["business_id"]+"\t1\n")
    print("Num of User",len(userSet))
    print("Num of Business", len(businessSet))
    
    
    print("\n\npick top Business\n\n")
    userList = list(userBusinessDict.keys())
    topbusinessSet = set() 
    userList.sort (key = lambda x:len(userFriendDict[x]), reverse = True)
    userList = userList[:topNum]
    topUserSet = set(userList)
    valList = [len(userFriendDict[user]) for user in userList]
    
    
    for i, user in enumerate(userList):
        userDict[user] = i
        for business in userBusinessDict[user]:
            topbusinessSet.add(business)
    for i, business in enumerate(list(topbusinessSet)):
        businessDict[business] = i
    lines = []
    for i, user in enumerate(userList):
        for business in userBusinessDict[user]:
            lines.append(str(i)+","+str(businessDict[business])+",1\n")
    random.shuffle(lines)
    split = int(0.75*len(lines))
    trainLines = lines[:split]
    testLines = lines[split:]
    with open("./train.txt", "w") as TrainFile:
        for trainLine in trainLines:
            TrainFile.write(trainLine)
    with open("./test.txt", "w") as TestFile:
        for testLine in testLines:
            TestFile.write(testLine)
        
    
    print("aveUserFriend", sum(valList)/topNum)
    print("Num of User",len(topUserSet))
    print("Num of Business",len(topbusinessSet))
    return topUserSet
if __name__ == '__main__' :
    print("start")
    topUserSet = userBusinessRelation('./yelp_dataset/tip.json',"./userBusinessRelation.txt", "./topUserBusinessRelation.txt", 4000)
    print("SUCCESS")
