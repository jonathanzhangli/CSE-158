# -*- coding: utf-8 -*-
"""Assignment1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xP2HkLArIuZrVp6POXTNz0Vzq5a_q0rz
"""

import gzip
from collections import defaultdict
import math
import scipy.optimize
from sklearn import svm
import numpy
import string
import random
import string
from sklearn import linear_model
import pandas as pd
from sklearn.preprocessing import StandardScaler

def readGz(path):
  for l in gzip.open(path, 'rt'):
    yield eval(l)

def readCSV(path):
  f = gzip.open(path, 'rt')
  f.readline()
  for l in f:
    yield l.strip().split(',')

# Real task 1

allRatings = []
for l in readCSV("train_Interactions.csv.gz"):
    allRatings.append(l)

# Create 2 data structures, one is all the book ids in the dataset, one is all the books each user has read

all_book_ids = [b for u, b, r in allRatings]
itemsPerUser = defaultdict(list)
for u,b,r in allRatings:
    itemsPerUser[u].append(b)

def Jaccard(s1, s2):
    numer = len(s1.intersection(s2))
    denom = len(s1.union(s2))
    if denom == 0:
        return 0
    return numer / denom

# Creating usersPerItem
usersPerItem = defaultdict(list)
for u,b,r in allRatings:
    usersPerItem[b].append(u)

def mostSimilar(i, b):
    
    users_same_book = set(usersPerItem[b])
    books_by_user = itemsPerUser[i]

    users_diff_book = find_users(books_by_user)

    return Jaccard(users_same_book, users_diff_book)

def find_users(books):
    users = set()
    for b in books:
        users_for_book = usersPerItem[b]
        users.update(users_for_book)
    return users

similarities = dict()
for u, b, r in allRatings:
    similarity_score = mostSimilar(u, b)
    similarities[(u, b)] = similarity_score

# thing = similarities[('u37758667', 'b99713185')]
get_similarity('u37758667', 'b99713185')

import statistics
similarity_mean = statistics.mean(similarities.values())

def get_similarity(u, b):
    if (u, b) in similarities:
        if b in return1 and similarities[(u, b)] > similarity_mean:
            return 1
        else:
            return 0

    for su, sb in similarities:
        if u == su:
            if b in return1 and similarities[(su, sb)] > similarity_mean:
                return 1
            else:
                return 0
    return 0

bookCount = defaultdict(int)
totalRead = 0

for user,book,_ in readCSV("train_Interactions.csv.gz"):
  bookCount[book] += 1
  totalRead += 1

mostPopular = [(bookCount[x], x) for x in bookCount]
mostPopular.sort()
mostPopular.reverse()

return1 = set()
count = 0
for ic, i in mostPopular:
  count += ic
  return1.add(i)
  if count > totalRead/2: break

predictions = open("predictions_Read.csv", 'w')
for l in open("pairs_Read.csv"):
    if l.startswith("userID"):
        #header
        predictions.write(l)
        continue
    u,b = l.strip().split(',')

    prediction = get_similarity(u, b)

    predictions.write(u + ',' + b + "," + str(prediction) + "\n")

    # if (u, b) in similarities:
    #     if b in return1 and similarities[(u, b)] > similarity_mean:
    #         predictions.write(u + ',' + b + ",1\n")
    #     else:
    #         predictions.write(u + ',' + b + ",0\n")
    # else:
    #     predictions.write(u + ',' + b + ",0\n")

predictions.close()

# Task 1

ratingsTrain = allRatings[:190000]
ratingsValid = allRatings[190000:]
ratingsPerUser = defaultdict(list)
ratingsPerItem = defaultdict(list)
for u,b,r in ratingsTrain:
    ratingsPerUser[u].append((b,r))
    ratingsPerItem[b].append((u,r))

# Finding Liked Books
bookCount = defaultdict(int)
totalRead = 0

for user,book,_ in readCSV("train_Interactions.csv.gz"):
    bookCount[book] += 1
    totalRead += 1

mostPopular = [(bookCount[x], x) for x in bookCount]
mostPopular.sort()
mostPopular.reverse()

return1 = set()
count = 0
for ic, i in mostPopular:
    count += ic
    return1.add(i)
    if count > totalRead/2: break

# Find users with similar taste
overlap_users = set()

for u,b,r in ratingsTrain:
    if u in overlap_users:
        continue

    if b in return1 and int(r) >= 4: 
        overlap_users.add(u)

# Find user infos with similar tastes
rec_lines = []

for u,b,r in ratingsTrain:
    if u in overlap_users:
        rec_lines.append([u, b, r])

# Convert to Pandas Dataframe
recs = pd.DataFrame(rec_lines, columns=['user_id', 'book_id', 'rating'])
recs['book_id'] = recs['book_id'].astype(str)
print('Number of books read amongst similar users: ' + str(len(recs)))

# Get the top 10 recommended books
top_recs = recs['book_id'].value_counts().head(10)
top_recs = top_recs.index.values
top_recs

# Create df with the sum of ratings
book_rating__sum_df = pd.DataFrame(ratingsTrain, columns=['user_id', 'book_id', 'rating'])
book_rating__sum_df['rating'] = book_rating__sum_df['rating'].astype(int)
book_rating__sum_df = book_rating__sum_df.groupby('book_id').sum().reset_index()
book_rating__sum_df = book_rating__sum_df.rename(columns={"rating": "ratings"})
book_rating__sum_df = book_rating__sum_df.sort_values('ratings', ascending=False)

book_rating__sum_df

# Get all recommendations
all_recs = recs['book_id'].value_counts()
all_recs = all_recs.to_frame().reset_index()
all_recs.columns = ['book_id', 'book_count']

# Get all recommendations with ratings that aren't 0
all_recs = all_recs.merge(book_rating__sum_df, how='inner', on='book_id')
all_recs['ratings'] = all_recs['ratings'].astype(int)
all_recs = all_recs[all_recs.ratings != 0]

all_recs['score'] = all_recs['book_count'] * (all_recs['book_count'] / all_recs['ratings'])

# all_recs['standarized_score'] = (all_recs['score'] - all_recs['score'].mean()) / all_recs['score'].std()

all_recs['standarized_score'] = StandardScaler().fit_transform(all_recs[['score']])

popular_recs = all_recs[all_recs['standarized_score'] > .5].sort_values('standarized_score', ascending=False)

popular_recs

popular_recs = popular_recs['book_id']

### Would-read baseline: just rank which books are popular and which are not, and return '1' if a book is among the top-ranked

bookCount = defaultdict(int)
totalRead = 0

for user,book,_ in readCSV("train_Interactions.csv.gz"):
  bookCount[book] += 1
  totalRead += 1

mostPopular = [(bookCount[x], x) for x in bookCount]
mostPopular.sort()
mostPopular.reverse()

return1 = set()
count = 0
for ic, i in mostPopular:
  count += ic
  return1.add(i)
  if count > totalRead/2: break

predictions = open("predictions_Read.csv", 'w')
for l in open("pairs_Read.csv"):
  if l.startswith("userID"):
    #header
    predictions.write(l)
    continue
  u,b = l.strip().split(',')
  if b in return1:
    predictions.write(u + ',' + b + ",1\n")
  else:
    predictions.write(u + ',' + b + ",0\n")

predictions.close()

# Task 2

data = []

for d in readGz("train_Category.json.gz"):
    data.append(d)

wordCount = defaultdict(int)
punctuation = set(string.punctuation)
for d in data:
    r = ''.join([c for c in d['review_text'].lower() if not c in punctuation])
    for w in r.split():
        wordCount[w] += 1

len(wordCount)

counts = [(wordCount[w], w) for w in wordCount]
counts.sort()
counts.reverse()

words = [x[1] for x in counts[:10000]]

wordId = dict(zip(words, range(len(words))))
wordSet = set(words)

def feature(datum):
    feat = [0]*len(words)
    r = ''.join([c for c in datum['review_text'].lower() if not c in punctuation])
    for w in r.split():
        if w in words:
            feat[wordId[w]] += 1
    feat.append(1) # offset
    return feat

Xtrain = [feature(d) for d in data]
ytrain = [d['genre'] for d in data]

import sklearn
mod = sklearn.linear_model.LogisticRegression(fit_intercept=False)
mod.fit(Xtrain,ytrain)

practice = 'mystery_thriller_crime\n'
practice.strip().split(',')[0]

catDict = {
  "children": 0,
  "comics_graphic": 1,
  "fantasy_paranormal": 2,
  "mystery_thriller_crime": 3,
  "young_adult": 4
}

predictions = open("predictions_Category.csv", 'w')
predictions.write("userID,reviewID,prediction\n")
for l in readGz("test_Category.json.gz"):
    data = feature(l)
    prediction = mod.predict([data])[0].strip().split(',')[0]
    prediction = catDict[prediction]
    predictions.write(l['user_id'] + ',' + l['review_id'] + "," + str(prediction) + "\n")

predictions.close()

from psutil import virtual_memory
ram_gb = virtual_memory().total / 1e9
print('Your runtime has {:.1f} gigabytes of available RAM\n'.format(ram_gb))

if ram_gb < 20:
  print('Not using a high-RAM runtime')
else:
  print('You are using a high-RAM runtime!')

