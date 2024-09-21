#-------------------------------------------------------------------------
# AUTHOR: Nathaniel Dale
# FILENAME: indexing.py
# SPECIFICATION: A program finding tf-idf matrix 
# FOR: CS 4250- Assignment #1
# TIME SPENT: 3 hours
#-----------------------------------------------------------*/

# omporting required Python libraries
import csv
import math

# reading data in a csv file
documents = []
with open('collection.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        if i > 0:  # skipping the header
            documents.append(row[0].lower())  # lowercase conversion

# stopword removal
stopWords = {"i", "she", "her", "and", "they", "their"}
documents = [" ".join([word for word in doc.split() if word not in stopWords]) for doc in documents]

# outline words for stemming
stemming = {
  "cats": "cat",
  "cat" : "cat",
  "dogs": "dog",
  "dog" : "dog",
  "loves": "love",
  "love" : "love"
}

# stemming loop
for i, doc in enumerate(documents):
    new_doc = []
    for word in doc.split():
        for stem, variations in stemming.items():
            if word in variations:
              new_doc.append(stem)
              break
        else:
            new_doc.append(word)
    documents[i] = " ".join(new_doc)

# find index terms (unique terms)
terms = []
for doc in documents:
    for word in doc.split():
        if word not in terms:
            terms.append(word)

# helper functions for calculations
def tf(word, doc):
  return doc.count(word) / len(doc)

def df(word):
  return sum(1 for doc in documents if word in doc)

def idf(word):
  return math.log(len(documents) / df(word), 10)

def tf_idf(word, doc):
  return tf(word, doc) * idf(word)

# construct document-term matrix
docTermMatrix = []

for doc in documents:
  docWords = doc.split()
  current_doc = [round(tf_idf(term, docWords), 4) for term in terms]
  docTermMatrix.append(current_doc)

# print the actual document-term matrix
print(f"{'docs':<10} {' '.join([f'|| {term:<6}' for term in terms])}")
print("______________________________________________")

for i, doc in enumerate(docTermMatrix):
  row = f"d{i+1:<7}" + " ".join([f" || {val:<6}" for val in doc])
  print(row)
