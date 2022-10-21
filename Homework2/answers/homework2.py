# -*- coding: utf-8 -*-
"""Homework2_stub.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Dmjbt-miJUTinLQBpjh_98YOK5g25ihU
"""

import numpy
import urllib
import scipy.optimize
import random
import sklearn
from sklearn import linear_model
import gzip
from collections import defaultdict

def assertFloat(x):
    assert type(float(x)) == float

def assertFloatList(items, N):
    assert len(items) == N
    assert [type(float(x)) for x in items] == [float]*N

f = open("5year.arff", 'r')

# Read and parse the data
while not '@data' in f.readline():
    pass

dataset = []
for l in f:
    if '?' in l: # Missing entry
        continue
    l = l.split(',')
    values = [1] + [float(x) for x in l]
    values[-1] = values[-1] > 0 # Convert to bool
    dataset.append(values)

X = [d[:-1] for d in dataset]
y = [d[-1] for d in dataset]

answers = {} # Your answers

def accuracy(predictions, y):
    correct = predictions == y
    return sum(correct) / len(correct)

def BER(predictions, y):
    TP = sum([(p and l) for (p,l) in zip(predictions, y)])
    FP = sum([(p and not l) for (p,l) in zip(predictions, y)])
    TN = sum([(not p and not l) for (p,l) in zip(predictions, y)])
    FN = sum([(not p and l) for (p,l) in zip(predictions, y)])

    TPR = TP / (TP + FN)
    TNR = TN / (TN + FP)

    BER = 1 - 1/2 * (TPR + TNR)

    return BER

### Question 1

mod = linear_model.LogisticRegression(C=1)
mod.fit(X,y)

pred = mod.predict(X)

acc1 = accuracy(pred, y)
ber1 = BER(pred, y)
acc1, ber1

answers['Q1'] = [acc1, ber1] # Accuracy and balanced error rate

assertFloatList(answers['Q1'], 2)

### Question 2

mod = linear_model.LogisticRegression(C=1, class_weight='balanced')
mod.fit(X,y)

pred = mod.predict(X)

acc2 = accuracy(pred, y)
ber2 = BER(pred, y)
acc2, ber2

answers['Q2'] = [acc2, ber2]

assertFloatList(answers['Q2'], 2)

### Question 3

random.seed(3)
random.shuffle(dataset)

X = [d[:-1] for d in dataset]
y = [d[-1] for d in dataset]

Xtrain, Xvalid, Xtest = X[:len(X)//2], X[len(X)//2:(3*len(X))//4], X[(3*len(X))//4:]
ytrain, yvalid, ytest = y[:len(X)//2], y[len(X)//2:(3*len(X))//4], y[(3*len(X))//4:]

len(Xtrain), len(Xvalid), len(Xtest)

mod = linear_model.LogisticRegression(C=1, class_weight='balanced')
mod.fit(Xtrain,ytrain)

predTrain = mod.predict(Xtrain)
predValid = mod.predict(Xvalid)
predTest = mod.predict(Xtest)

berTrain = BER(predTrain, ytrain)
berValid = BER(predValid, yvalid)
berTest = BER(predTest, ytest)

berTrain, berValid, berTest

answers['Q3'] = [berTrain, berValid, berTest]

assertFloatList(answers['Q3'], 3)

### Question 4

X = [d[:-1] for d in dataset]
y = [d[-1] for d in dataset]

Xtrain, Xvalid, Xtest = X[:len(X)//2], X[len(X)//2:(3*len(X))//4], X[(3*len(X))//4:]
ytrain, yvalid, ytest = y[:len(X)//2], y[len(X)//2:(3*len(X))//4], y[(3*len(X))//4:]

C = [.0001, .001, .01, .1, 1, 10, 100, 1000, 10000]
berList = []
for c in C:
    model = linear_model.LogisticRegression(C=c, class_weight='balanced')
    model.fit(Xtrain, ytrain)
    predictValid = model.predict(Xvalid)

    berValid = BER(predictValid, yvalid)
    berList.append(berValid)
    print("l = " + str(c) + ", validation BER = " + str(berValid))

answers['Q4'] = berList

assertFloatList(answers['Q4'], 9)

### Question 5

bestModel = None
bestVal = None
bestC = None

C = [.0001, .001, .01, .1, 1, 10, 100, 1000, 10000]
berList = []
for c in C:
    model = linear_model.LogisticRegression(C=c, class_weight='balanced')
    model.fit(Xtrain, ytrain)
    predictValid = model.predict(Xvalid)

    berValid = BER(predictValid, yvalid)
    berList.append(berValid)
    # print("l = " + str(c) + ", validation BER = " + str(berValid))

    # Updating best values
    if bestVal == None or berValid < bestVal:
        bestVal = berValid
        bestModel = model
        bestC = c
ber5 = bestVal

answers['Q5'] = [bestC, ber5]

assertFloatList(answers['Q5'], 2)

### Question 6

f = gzip.open("young_adult_10000.json.gz")
dataset = []
for l in f:
    dataset.append(eval(l))

dataTrain = dataset[:9000]
dataTest = dataset[9000:]

# Some data structures you might want

usersPerItem = defaultdict(set) # Maps an item to the users who rated it
itemsPerUser = defaultdict(set) # Maps a user to the items that they rated
reviewsPerUser = defaultdict(list)
reviewsPerItem = defaultdict(list)
ratingDict = {} # To retrieve a rating for a specific user/item pair

for d in dataTrain:

    user,item = d['user_id'], d['book_id']
    usersPerItem[item].add(user)
    itemsPerUser[user].add(item)
    reviewsPerUser[user].append(d)
    reviewsPerItem[item].append(d)
    ratingDict[(user,item)] = d['rating']

def Jaccard(s1, s2):
    numer = len(s1.intersection(s2))
    denom = len(s1.union(s2))
    if denom == 0:
        return 0
    return numer / denom

def mostSimilar(i, N):
    similarities = []
    users = usersPerItem[i]
    for i2 in usersPerItem:
        if i2 == i: continue
        sim = Jaccard(users, usersPerItem[i2])
        #sim = Pearson(i, i2) # Could use alternate similarity metrics straightforwardly
        similarities.append((sim,i2))
    similarities.sort(reverse=True)
    return similarities[:10]

mostSimilar('2767052', 10)

answers['Q6'] = mostSimilar('2767052', 10)

assert len(answers['Q6']) == 10
assertFloatList([x[0] for x in answers['Q6']], 10)

### Question 7

userAverages = {}
itemAverages = {}

for u in itemsPerUser:
    rs = [ratingDict[(u,i)] for i in itemsPerUser[u]]
    userAverages[u] = sum(rs) / len(rs)
    
for i in usersPerItem:
    rs = [ratingDict[(u,i)] for u in usersPerItem[i]]
    itemAverages[i] = sum(rs) / len(rs)

reviewsPerUser = defaultdict(list)
reviewsPerItem = defaultdict(list)

for d in dataTrain:
    user,item = d['user_id'], d['book_id']
    reviewsPerUser[user].append(d)
    reviewsPerItem[item].append(d)

ratingMean = sum([d['rating'] for d in dataTrain]) / len(dataTrain)
ratingMean

def predictRating(user,item):
    ratings = []
    similarities = []
    for d in reviewsPerUser[user]:
        i2 = d['book_id']
        if i2 == item: continue
        ratings.append(d['rating'] - itemAverages[i2])
        similarities.append(Jaccard(usersPerItem[item],usersPerItem[i2]))
    if (sum(similarities) > 0):
        weightedRatings = [(x*y) for x,y in zip(ratings,similarities)]
        return itemAverages[item] + sum(weightedRatings) / sum(similarities)
    else:
        # User hasn't rated any similar items
        return ratingMean

def MSE(predictions, labels):
    differences = [(x-y)**2 for x,y in zip(predictions,labels)]
    return sum(differences) / len(differences)

simPredictions = [predictRating(d['user_id'], d['book_id']) for d in dataTest]
labels = [d['rating'] for d in dataTest]
mse7 = MSE(simPredictions, labels)
mse7

answers['Q7'] = mse7

assertFloat(answers['Q7'])

### Question 8

simPredictions = [predictRating(d['book_id'], d['user_id']) for d in dataTest]
labels = [d['rating'] for d in dataTest]
mse8 = MSE(simPredictions, labels)
mse8

answers['Q8'] = mse8

assertFloat(answers['Q8'])

f = open("answers_hw2.txt", 'w')
f.write(str(answers) + '\n')
f.close()

f

