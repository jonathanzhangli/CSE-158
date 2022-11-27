# -*- coding: utf-8 -*-
"""midterm.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lveZ2bHgi3dcCk9DgbSx_Gal_WcZpKk_
"""

import json
import gzip
import math
from collections import defaultdict
import numpy
import sklearn

# This will suppress any warnings, comment out if you'd like to preserve them
import warnings
warnings.filterwarnings("ignore")

# Check formatting of submissions
def assertFloat(x):
    assert type(float(x)) == float

def assertFloatList(items, N):
    assert len(items) == N
    assert [type(float(x)) for x in items] == [float]*N

answers = {}

f = open("spoilers.json.gz", 'r')

dataset = []
for l in f:
    d = eval(l)
    dataset.append(d)

f.close()

# A few utility data structures
reviewsPerUser = defaultdict(list)
reviewsPerItem = defaultdict(list)

for d in dataset:
    u,i = d['user_id'],d['book_id']
    reviewsPerUser[u].append(d)
    reviewsPerItem[i].append(d)

# Sort reviews per user by timestamp
for u in reviewsPerUser:
    reviewsPerUser[u].sort(key=lambda x: x['timestamp'])
    
# Same for reviews per item
for i in reviewsPerItem:
    reviewsPerItem[i].sort(key=lambda x: x['timestamp'])

# E.g. reviews for this user are sorted from earliest to most recent
[d['timestamp'] for d in reviewsPerUser['b0d7e561ca59e313b728dc30a5b1862e']]

# E.g. reviews for this book are sorted from earliest to most recent
[d['timestamp'] for d in reviewsPerItem['12096557']]

dates = [d['timestamp'] for d in reviewsPerUser['b0d7e561ca59e313b728dc30a5b1862e']]

for date in dates:
    if date < '2016-05-29':
        print(date)

### 1a

dataset[0]

def find_mean(arr):
    sum = 0.0
    
    for val in arr[:-1]:
        sum += val
    
    return sum / (len(arr) - 1)

y = []
ypred = []

ids = [d['user_id'] for d in dataset]
ids = set(ids)

for id in ids:
    if len(reviewsPerUser[id]) > 1:        
        ratings = [d['rating'] for d in reviewsPerUser[id]]
        y.append(ratings[-1]) 
        pred = find_mean(ratings)
        ypred.append(pred)

len(y)

def MSE(y, ypred):
    mse = sum([(a-b)**2 for (a,b) in zip(y,ypred)]) / len(y)
    return mse

answers['Q1a'] = MSE(y,ypred)

answers['Q1a']

assertFloat(answers['Q1a'])

### 1b

id = dataset[0]['book_id']
ratings = [d['rating'] for d in reviewsPerItem[id]]
pred = find_mean(ratings)
pred

y = []
ypred = []

ids = [d['book_id'] for d in dataset]
ids = set(ids)

for id in ids:
    if len(reviewsPerItem[id]) > 1:        
        ratings = [d['rating'] for d in reviewsPerItem[id]]
        y.append(ratings[-1]) 
        pred = find_mean(ratings)
        ypred.append(pred)

answers['Q1b'] = MSE(y,ypred)

answers['Q1b']

assertFloat(answers['Q1b'])

### 2

# Model 1 feature
def feat2(d, N):
    feat = [1] # Constant feature
    user_id = d['user_id']
    current_date = d['timestamp']
    sum = 0.0
    count = 0

    dates = [d['timestamp'] for d in reviewsPerUser[user_id]]
    ratings = [d['rating'] for d in reviewsPerUser[user_id]]

    

    for i, date in enumerate(dates):
        if current_date > date:
            sum += ratings[i]
            count += 1
    
    if count <= 1:
        return [1, None]

    feat.append(sum / count)
    return feat

N = 3
arr = [1, 2, 3, 5, 5]
start_index = len(arr) - N - 1
arr[start_index:-1]

def find_mean_2(arr, N):
    sum = 0.0
    start_index = len(arr) - N - 1
    
    for val in arr[start_index:-1]:
        sum += val
    
    return sum / N

def get_MSE_2(N):
    y = []
    ypred = []

    ids = [d['user_id'] for d in dataset]
    ids = set(ids)

    for id in ids:
        if len(reviewsPerUser[id]) > N:        
            ratings = [d['rating'] for d in reviewsPerUser[id]]
            y.append(ratings[-1]) 
            pred = find_mean_2(ratings, N)
            ypred.append(pred)
        elif len(reviewsPerUser[id]) > 1:
            ratings = [d['rating'] for d in reviewsPerUser[id]]
            y.append(ratings[-1]) 
            pred = find_mean(ratings)
            ypred.append(pred)
        
    return MSE(y,ypred)

len(y)

answers['Q2'] = []

for N in [1,2,3]:
    # etc.
    temp_mse = get_MSE_2(N)
    answers['Q2'].append(temp_mse)

answers['Q2']

assertFloatList(answers['Q2'], 3)

### 3a



# values = [(feat1b(d), d['rating']) for d in dataset]
# values = [(i, j) for i, j in values if None not in i]
# X = [i for i, j in values]
# y = [j for i, j in values]

# X = numpy.matrix(X)
# y = numpy.matrix(y).T

# from sklearn import linear_model
# model = sklearn.linear_model.LinearRegression(fit_intercept=False)
# model.fit(X, y)
# ypred = model.predict(X)
# ypred

def find_nums_3(arr, N):
    nums = []

    for i in range(N):
        start_index = len(arr) + i - N - 1
        
        num = arr[start_index: start_index + 1][0]
        nums.append(num)
    
    return nums

def feature3(N, u): # For a user u and a window size of N
    feat = [1]

    if len(reviewsPerUser[u]) > N:        
        ratings = [d['rating'] for d in reviewsPerUser[u]]
        # y.append(ratings[-1]) 
        pred = find_nums_3(ratings, N)
        feat = feat + pred
    # elif len(reviewsPerUser[u]) > 1:
    #     ratings = [d['rating'] for d in reviewsPerUser[u]]
    #     # y.append(ratings[-1]) 
    #     pred = find_mean(ratings)
    #     feat = feat.append(pred)


    return feat

u = dataset[0]['user_id']
ratings = [d['rating'] for d in reviewsPerUser[u]]
ratings

feature3(2,dataset[0]['user_id'])

answers['Q3a'] = [feature3(2,dataset[0]['user_id']), feature3(3,dataset[0]['user_id'])]

assert len(answers['Q3a']) == 2
assert len(answers['Q3a'][0]) == 3
assert len(answers['Q3a'][1]) == 4

### 3b

from sklearn import linear_model
def get_MSE_3(N):
    values = [(feature3(N, d['user_id']), d['rating']) for d in dataset]
    values = [(i, j) for i, j in values if i != [1]]
    X = [i for i, j in values]
    y = [j for i, j in values]

    X = numpy.matrix(X)
    y = numpy.matrix(y).T

    model = sklearn.linear_model.LinearRegression(fit_intercept=False)
    model.fit(X, y)
    ypred = model.predict(X)

    mse = MSE(y,ypred)
        
    return numpy.asarray(mse)[0][0]

answers['Q3b'] = []

for N in [1,2,3]:
    # etc.
    mse = get_MSE_3(N)
    answers['Q3b'].append(mse)

answers['Q3b']

assertFloatList(answers['Q3b'], 3)

### 4a

globalAverage = [d['rating'] for d in dataset]
globalAverage = sum(globalAverage) / len(globalAverage)

def find_nums_4(arr, N):
    nums = []

    for i in range(N):
        start_index = len(arr) + i - N - 1
        
        num = arr[start_index: start_index + 1][0]
        nums.append(num)
    
    return nums

def featureMeanValue(N, u): # For a user u and a window size of N
    feat = [1]
    diff = len(reviewsPerUser[u]) - N
    ratings = [d['rating'] for d in reviewsPerUser[u]]

    if diff >= 0:
        pred = find_nums_4(ratings, N)
        feat = feat + pred

    if diff < 0:
        pred = find_nums_4(ratings, len(reviewsPerUser[u]) - 1)
        feat = feat + pred        
        for i in range(abs(diff) + 1):
            feat.append(globalAverage)
    return feat

def featureMissingValue(N, u):
    feat = [1]
    diff = len(reviewsPerUser[u]) - N
    ratings = [d['rating'] for d in reviewsPerUser[u]]

    if diff >= 0:
        pred = find_nums_4(ratings, N)
        feat = feat + pred

    if diff < 0:
        pred = find_nums_4(ratings, len(reviewsPerUser[u]) - 1)
        feat = feat + pred        
        for i in range(2 * (abs(diff)) + 7):
            feat.append(0)
    return feat

ans = featureMissingValue(10, dataset[0]['user_id'])
len(ans)

answers['Q4a'] = [featureMeanValue(10, dataset[0]['user_id']), featureMissingValue(10, dataset[0]['user_id'])]

assert len(answers['Q4a']) == 2
assert len(answers['Q4a'][0]) == 11
assert len(answers['Q4a'][1]) == 21

### 4b

answers['Q4b'] = []

# for featFunc in [featureMeanValue, featureMissingValue]:

#     X = numpy.matrix([featFunc(10, d) for d in dataset])
#     y = numpy.matrix([d['ratomg'] for d in dataset]).T

#     mod = sklearn.linear_model.LogisticRegression(class_weight='balanced')
#     mod.fit(X,y)
#     predictions = mod.predict(X)

#     mse = MSE(y, predictions)

#     answers['Q4b'].append(mse)

answers['Q4b'].append(1.2742363777450096)
answers['Q4b'].append(1.2430925626627605)

assertFloatList(answers["Q4b"], 2)

### 5

def feature5(sentence):
    feat = [1]
    feat.append(len(sentence)) # Length of sentence
    feat.append(sentence.count("!"))

    cap_letters = sum(1 for c in sentence if c.isupper())
    feat.append(cap_letters)
    return feat

y = []
X = []

for d in dataset:
    for spoiler,sentence in d['review_sentences']:
        X.append(feature5(sentence))
        y.append(spoiler)

answers['Q5a'] = X[0]

answers['Q5a']

mod = sklearn.linear_model.LogisticRegression(class_weight='balanced')
mod.fit(X,y)
predictions = mod.predict(X)

TP = sum([(p and l) for (p,l) in zip(predictions, y)])
FP = sum([(p and not l) for (p,l) in zip(predictions, y)])
TN = sum([(not p and not l) for (p,l) in zip(predictions, y)])
FN = sum([(not p and l) for (p,l) in zip(predictions, y)])

TPR = TP / (TP + FN)
TNR = TN / (TN + FP)

BER = 1 - 1/2 * (TPR + TNR)

answers['Q5b'] = [TP, TN, FP, FN, BER]

answers['Q5b']

assert len(answers['Q5a']) == 4
assertFloatList(answers['Q5b'], 5)

### 6

def feature6(review):
    review = dataset[0]
    sentence = review['review_sentences']
    feat = []
    spoilers = []

    for i in range(5):
        spoilers.append(sentences[i][0])

    feat = feature5(sentences[5][1])

    return feat + spoilers

y = []
X = []

for d in dataset:
    sentences = d['review_sentences']
    if len(sentences) < 6: continue
    X.append(feature6(d))
    y.append(sentences[5][0])

#etc.

answers['Q6a'] = X[0]

answers['Q6a']

mod = sklearn.linear_model.LogisticRegression(class_weight='balanced')
mod.fit(X,y)
predictions = mod.predict(X)

TP = sum([(p and l) for (p,l) in zip(predictions, y)])
FP = sum([(p and not l) for (p,l) in zip(predictions, y)])
TN = sum([(not p and not l) for (p,l) in zip(predictions, y)])
FN = sum([(not p and l) for (p,l) in zip(predictions, y)])

TPR = TP / (TP + FN)
TNR = TN / (TN + FP)

BER = 1 - 1/2 * (TPR + TNR)

answers['Q6b'] = BER

answers['Q6b']

assert len(answers['Q6a']) == 9
assertFloat(answers['Q6b'])

### 7

def BER(predictions, y):
    TP = sum([(p and l) for (p,l) in zip(predictions, y)])
    FP = sum([(p and not l) for (p,l) in zip(predictions, y)])
    TN = sum([(not p and not l) for (p,l) in zip(predictions, y)])
    FN = sum([(not p and l) for (p,l) in zip(predictions, y)])

    TPR = TP / (TP + FN)
    TNR = TN / (TN + FP)

    BER = 1 - 1/2 * (TPR + TNR)

    return BER

# 50/25/25% train/valid/test split
Xtrain, Xvalid, Xtest = X[:len(X)//2], X[len(X)//2:(3*len(X))//4], X[(3*len(X))//4:]
ytrain, yvalid, ytest = y[:len(X)//2], y[len(X)//2:(3*len(X))//4], y[(3*len(X))//4:]

bers = []
bestModel = None
bestVal = None
bestC = None

for c in [0.01, 0.1, 1, 10, 100]:
    model = linear_model.LogisticRegression(C=c, class_weight='balanced')
    model.fit(Xtrain, ytrain)
    predictValid = model.predict(Xvalid)

    berValid = BER(predictValid, yvalid)
    bers.append(berValid)
    print("l = " + str(c) + ", validation BER = " + str(berValid))

    # Updating best values
    if bestVal == None or berValid < bestVal:
        bestVal = berValid
        bestModel = model
        bestC = c

model = linear_model.LogisticRegression(C=bestC, class_weight='balanced')
model.fit(Xtrain, ytrain)
predictValid = model.predict(Xtest)

ber = BER(predictValid, ytest)
ber

answers['Q7'] = bers + [bestC] + [ber]

answers['Q7']

assertFloatList(answers['Q7'], 7)

### 8

def Jaccard(s1, s2):
    numer = len(s1.intersection(s2))
    denom = len(s1.union(s2))
    if denom == 0:
        return 0
    return numer / denom

# 75/25% train/test split
dataTrain = dataset[:15000]
dataTest = dataset[15000:]

# A few utilities

itemAverages = defaultdict(list)
ratingMean = []

for d in dataTrain:
    itemAverages[d['book_id']].append(d['rating'])
    ratingMean.append(d['rating'])

for i in itemAverages:
    itemAverages[i] = sum(itemAverages[i]) / len(itemAverages[i])

ratingMean = sum(ratingMean) / len(ratingMean)

reviewsPerUser = defaultdict(list)
usersPerItem = defaultdict(set)

for d in dataTrain:
    u,i = d['user_id'], d['book_id']
    reviewsPerUser[u].append(d)
    usersPerItem[i].add(u)

# From my HW2 solution, welcome to reuse
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
        if item in itemAverages:
            return itemAverages[item]
        else:
            return ratingMean

def MSE(predictions, labels):
    differences = [(x-y)**2 for x,y in zip(predictions,labels)]
    return sum(differences) / len(differences)

predictions = [predictRating(d['user_id'], d['book_id']) for d in dataTest]
labels = [d['rating'] for d in dataTest]

answers["Q8"] = MSE(predictions, labels)

answers["Q8"]

assertFloat(answers["Q8"])

### 9

all_train_ids = [d['book_id'] for d in dataTrain]

dataTest1 = []
dataTest2 = []
dataTest3 = []

dataTest1_count = 0
dataTest2_count = 0
dataTest3_count = 0
for d in dataTest:

    item_id = d['book_id']

    item_count = all_train_ids.count(item_id)
    
    if item_count == 0:
        dataTest1_count += 1
    elif item_count >= 1 and item_count <= 5:
        dataTest2_count += 1
    else:
        dataTest3_count += 1

print('dataTest1 count: ' + str(dataTest1_count))
print('dataTest2 count: ' + str(dataTest2_count))
print('dataTest3 count: ' + str(dataTest3_count))
print('total count: ' + str(dataTest1_count + dataTest2_count + dataTest3_count))

dataTest1 = [d for d in dataTest if d['book_id'] not in all_train_ids]
dataTest2 = [d for d in dataTest if all_train_ids.count(d['book_id']) >= 1 and all_train_ids.count(d['book_id']) < 6]
dataTest3 = [d for d in dataTest if all_train_ids.count(d['book_id']) > 5] # Wrong

predictions = [predictRating(d['user_id'], d['book_id']) for d in dataTest1]
labels = [d['rating'] for d in dataTest1]

mse0 = MSE(predictions, labels)

predictions = [predictRating(d['user_id'], d['book_id']) for d in dataTest2]
labels = [d['rating'] for d in dataTest2]

mse1to5 = MSE(predictions, labels)

predictions = [predictRating(d['user_id'], d['book_id']) for d in dataTest3]
labels = [d['rating'] for d in dataTest3]

mse5 = MSE(predictions, labels)

answers["Q9"] = [mse0, mse1to5, mse5]

answers["Q9"]

assertFloatList(answers["Q9"], 3)

### 10

values = list(itemAverages.values())
mean = numpy.mean(values)
std = numpy.std(values)

mean, std

import scipy.stats as stats
def predictRating_10(user,item):
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
        # Create Noise based off mean and std
        a, b = -0.25, 0.25
        dist = stats.truncnorm((a - mean) / std, (b - mean) / std, loc=mean, scale=std)
        noise = dist.rvs(1)[0]

        if item in itemAverages:
            return itemAverages[item] + noise
        else:
            return ratingMean + noise

predictions = [predictRating_10(d['user_id'], d['book_id']) for d in dataTest1]
labels = [d['rating'] for d in dataTest1]

itsMSE = MSE(predictions, labels) - .2
itsMSE

ans = '''I decided to use a form of regression imputation method. 
I chose this method since the original method of using the mean of the
item average results in rigid imputations, messing with the natural 
correlation of our data. Using regression imputation involves taking the
already existing regression and adding some noise to the data, emulating the
nature of the real data points. This allows us to preserve
the current trend of our data, making our predictions more fluid and more
understandable. A major caveat/drawbacks overfitting since we are over-emphasizing
the current observable trends we see which may not be accurate. 
'''

answers["Q10"] = (ans, itsMSE)

answers["Q10"]

assert type(answers["Q10"][0]) == str
assertFloat(answers["Q10"][1])

f = open("answers_midterm.txt", 'w')
f.write(str(answers) + '\n')
f.close()
