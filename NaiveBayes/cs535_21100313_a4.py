# -*- coding: utf-8 -*-
"""CS535_21100313_A4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BcCDka4rhXzIf-TKex4pvYCvEzxIxjD8
"""

# -*- coding: utf-8 -*-
"""CS535_21100313_A4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BcCDka4rhXzIf-TKex4pvYCvEzxIxjD8
"""

import os
import math
import numpy as np
import glob
import re
import pickle
#change  datasetpath to where dataset is stored or create a Dataset folder in directory you run this file
dataset_path  = os.getcwd() + "/Dataset"
train_logs_path = os.getcwd()+ "/train_logs.data"
train_raw_pos_reviews_path = os.getcwd() + "/train_raw_pos_reviews.data"
train_raw_neg_reviews_path = os.getcwd() + "/train_raw_neg_reviews.data"
train_pos_reviews_path = os.getcwd() + "/train_pos_reviews.data"
train_neg_reviews_path = os.getcwd() + "/train_neg_reviews.data"
test_pos_reviews_path = os.getcwd() + "/test_pos_reviews.data"
test_neg_reviews_path = os.getcwd() + "/test_neg_reviews.data"
train_bigdoc_path = os.getcwd() + "/train_bigdoc.data"
test_bigdoc_path = os.getcwd() + "/test_bigdoc.data"
train_pos_reviews_words_path = os.getcwd() + "/train_pos_reviews_words.data"
train_neg_reviews_words_path = os.getcwd() + "/train_neg_reviews_words.data"
test_pos_reviews_words_path = os.getcwd() + "/test_pos_reviews_words.data"
test_neg_reviews_words_path = os.getcwd() + "/test_neg_reviews_words.data"
training_vocab_path = os.getcwd() + "/training_vocab.data"
testing_vocab_path = os.getcwd() + "/testing_vocab.data"
training_vocab_dict_path = os.getcwd() + "/training_vocab_dict.data"
training_vocab_index_dict_path = os.getcwd() + "/training_vocab_index_dict.data"
training_document_path = os.getcwd() + "/training_document.data"
index_dict_path = os.getcwd() + "/index_dict.data"
bow_path = os.getcwd() + "/bow.data"
stopwords_path = dataset_path + "/stop_words.txt"
pos_words_path = dataset_path + "/positive_words.txt"
neg_words_path = dataset_path + "/negative_words.txt"
train_path = dataset_path + "/train"
pos_train_path = train_path + "/pos"
neg_train_path = train_path + "/neg"
test_path = dataset_path + "/test"
pos_test_path = test_path + "/pos"
neg_test_path = test_path + "/neg"

def read_file(filepath):
    if '.txt' in filepath:
        with open(filepath,'r',encoding='utf-8') as f:
            file_content = f.read()
    return file_content
def read_words(filepath):
    if '.txt' in filepath:
        with open(filepath,'r') as f:
            file_content = f.readlines()
    return file_content
def load_words(word_filepath):
    word_list = read_words(word_filepath)
    words = []
    for line in word_list:
        words.append(line.strip())
    return words
def read_reviews(path):
    new_path = path + "/*.*"
    filenames = glob.glob(new_path)
    reviews = []
    i = 0 
    for filename in filenames:
        review  = read_file(filename)
        reviews.append(review)
        i = i + 1
    return reviews
def remove_stopwords_from_reviews_words(reviews_words,stopwords):
  stopless_review_words = []
  stopwords_dict = dict.fromkeys(stopwords)
  for word in reviews_words:
    index = stopwords_dict.get(word,-1)
    if index == -1:
      stopless_review_words.append(word)
  return stopless_review_words
def remove_stopwords_from_reviews(reviews,stopwords):
    stopless_review_list = []
    for review in reviews:
        split_review = [word.lower() for word in re.split("\W+",review) if word.lower() not in stopwords]
        empty_char = ' '
        stopless_review = empty_char.join(split_review)
        stopless_review_list.append(stopless_review)
    return stopless_review_list
def preprocess_reviews(pos_path,neg_path):
    pos_reviews = read_reviews(pos_path)
    neg_reviews = read_reviews(neg_path)
    stopwords = load_words(stopwords_path)
    stopless_pos_reviews = remove_stopwords_from_reviews(pos_reviews,stopwords)
    stopless_neg_reviews = remove_stopwords_from_reviews(neg_reviews,stopwords)
    return [stopless_neg_reviews,stopless_pos_reviews]
def load_test_reviews():
    import datetime
    start_time = datetime.datetime.now()
    print("starting preprocessing of test reviews")
    processed_reviews = preprocess_reviews(pos_test_path,neg_test_path)
    finish_time = datetime.datetime.now() - start_time

    print("finished preprocessing of test reviews in",finish_time)
    neg_reviews = processed_reviews[0]
    pos_reviews = processed_reviews[1]
    return [neg_reviews,pos_reviews]
def load_train_reviews():
    import datetime
    start_time = datetime.datetime.now()
    print("starting preprocessing of train reviews")
    processed_reviews = preprocess_reviews(pos_train_path,neg_train_path)
    finish_time = datetime.datetime.now() - start_time

    print("finished preprocessing of train reviews in",finish_time)
    neg_reviews = processed_reviews[0]
    pos_reviews = processed_reviews[1]
    return [neg_reviews,pos_reviews]
#creates a long string of all reviews
def create_corpus_from_reviews(reviews):
    corpus = ''
    for review in reviews:
        corpus = corpus + ' '+review.lower() + ' '
    return corpus
def remove_empty_words_from_vocab(unique_words):
    new_unique_words = []
    for word in unique_words:
        if len(word)!= 0 and word != ' ' :
            new_unique_words.append(word)
    return new_unique_words
#this function takes train reviews and computes all the unique words in train reviews 
def create_vocabulary(neg_reviews,pos_reviews):
    neg_corpus = create_corpus_from_reviews(neg_reviews)
    pos_corpus = create_corpus_from_reviews(pos_reviews)
    corpus = neg_corpus + pos_corpus
    unique_words = list (set (re.split("\W+",corpus)))
    return unique_words 
def create_training_vocabulary_from_documents(documents):
    corpus = create_corpus_from_reviews(document)
    unique_words = list (set (re.split("\W+",corpus)))
    return unique_words
def convert_vocab_into_dict(unique_words):
    unique_words_dict = {}
    for word in unique_words:
        unique_words_dict[word] = 0
    return unique_words_dict
def word2index(word,unique_words_dict):
    index = 0 
    for key in unique_words_dict:
        if key == word:
            break
        index = index + 1
    if index == len(unique_words_dict):
        index = -1
    return index
def save_pickled_data(data,path):
    with open(path,'wb' ,) as f:
        pickle.dump(data,f)
    print("pickled data saved as pickle dump at",path)
def load_pickled_data(path):
    with open(path,'rb' ,) as f:
        data = pickle.load(f)
    print("pickled data loaded as pickle dump from",path)
    return data
def split_review_into_list_of_words(review):
    words = review.split()
    return words

#conveerts [['hey],'['bye']] to ['hey','bye']   
def create_words_from_reviews(reviews):
  reviews_words =  []
  for i in range(len(reviews)):
    words = split_review_into_list_of_words(reviews[i])
    for word in words:
      reviews_words.append(word)
  return reviews_words

def count(w,big_doc,c):
  
  count = big_doc[c][w]
  return count
  

def train_naive_bayes_classifier(D,C):
  from collections import Counter
  V = load_pickled_data(training_vocab_path)
  train_pos_reviews_words = load_pickled_data(train_pos_reviews_words_path)
  train_neg_reviews_words = load_pickled_data(train_neg_reviews_words_path)
  nd = len(D)
  nc = 12500
  log_likelihood =[{},{}]
  bigdoc = [[''],['']]
  log_prior = [0,0]
  for c in C:
    log_prior[c]  = np.log(nc/nd)
    if c == 0:
      bigdoc[c] = Counter(train_neg_reviews_words)
    else:
      bigdoc[c] = Counter(train_pos_reviews_words)
    for word in V:
      count_w_c = count(word,bigdoc,c)
      count_of_all_words = sum(bigdoc[c].values())
      log_likelihood_w_c = np.log( (count_w_c + 1)/ (count_of_all_words + len(V)))
      log_likelihood[c][word] = log_likelihood_w_c 
  return [log_prior,log_likelihood]

def compute_accuracy(predictions,ground_truth):
  total = len(predictions) 
  l = len(predictions)
  match = 0
  for i in range(l):
    if predictions[i] == ground_truth[i]:
      match = match + 1
  accuracy = match / total
  return accuracy

def test_naive_bayes_classifier(test_doc,log_prior,log_likelihood,C,V):
  sum = [0,0]
  vocab_dict = convert_vocab_into_dict(V)
  for c in C:
    sum[c] = log_prior[c]
    for i in range(len(test_doc)):
      word = test_doc[i]
      index = vocab_dict.get(word,-1)
      if index != -1:
        sum[c] = sum[c] + log_likelihood[c][word]
  sum = np.array(sum)
  return np.argmax(sum)


def execute_part1():
    files_pickled = True # set to False , if you want to run from scratch or true if you want cached version e.g variables/files like vocab/preprocessing data are already processed as pickle files so it runs faster
    print("executing part 1 -----------------------------------------")
    import datetime
    start_time = datetime.datetime.now()
    if not files_pickled:
        train_reviews = load_train_reviews()
        train_neg_reviews = train_reviews[0] # processed data
        train_pos_reviews = train_reviews[1]
        train_pos_reviews_words =  create_words_from_reviews(train_pos_reviews)
        train_neg_reviews_words =  create_words_from_reviews(train_neg_reviews)
        save_pickled_data(train_pos_reviews_words,train_pos_reviews_words_path)
        save_pickled_data(train_neg_reviews_words,train_neg_reviews_words_path)
        documents = train_neg_reviews + train_pos_reviews
        save_pickled_data(documents,training_document_path)
        print("generating training vocab")
        training_vocab = create_vocabulary(train_neg_reviews,train_pos_reviews)
        training_vocab = remove_empty_words_from_vocab(training_vocab)
        print("train_vocab generated of",len(training_vocab),"words")
        save_pickled_data(training_vocab,training_vocab_path)
        classes = [0,1]
        print("starting training of naive_bayes_classifier")
        logs = train_naive_bayes_classifier(documents,classes)
        log_prior = logs[0]
        log_likelihood = logs[1]
        print("completed training of naive_bayes_classifier")
        print("starting testing phase")
        test_reviews = load_test_reviews()
        test_neg_reviews = test_reviews[0]
        test_pos_reviews = test_reviews[1]
        test_reviews = test_neg_reviews + test_pos_reviews
        pred_labels = []
        pos_labels =[ 1 for i in range(12500)]
        neg_labels = [0 for i in range(12500)]
        true_labels= neg_labels + pos_labels
        C = [0,1]
        for test_doc in test_reviews:
          label = test_naive_bayes_classifier(test_doc.split(),log_prior,log_likelihodd,C,training_vocab)
          pred_labels.append(label)
        acc = compute_accuracy(pred_labels,true_labels)
        print("the accuracy is:", acc)
        print("finished testing phase")

    else:
        print("starting training phase")
        train_neg_reviews = load_pickled_data(train_neg_reviews_path) # processed data
        train_pos_reviews = load_pickled_data(train_pos_reviews_path)
        documents = train_neg_reviews + train_pos_reviews
        classes = [0,1]
        print("generating training vocab")
        training_vocab = load_pickled_data(training_vocab_path)
        train_pos_reviews_words = load_pickled_data(train_pos_reviews_words_path) # each review is a list of words rather than string
        train_neg_reviews_words = load_pickled_data(train_neg_reviews_words_path)
        train_D = train_neg_reviews_words + train_pos_reviews_words
        print("train_vocab generated of",len(training_vocab),"words")
        print("starting training of naive_bayes_classifier")
        logs = train_naive_bayes_classifier(train_D,classes)
        log_prior = logs[0]
        log_likelihood = logs[1]
        print("completed training of naive_bayes_classifier")
        print("finished traininig phase")
        print("starting testing phase")
        test_neg_reviews = load_pickled_data(test_neg_reviews_path)
        test_pos_reviews = load_pickled_data(test_pos_reviews_path)
        test_reviews = test_neg_reviews + test_pos_reviews
        pred_labels = []
        pos_labels =[ 1 for i in range(12500)]
        neg_labels = [0 for i in range(12500)]
        true_labels= neg_labels + pos_labels
        C = [0,1]
        for test_doc in test_reviews:
          label = test_naive_bayes_classifier(test_doc.split(),log_prior,log_likelihood,C,training_vocab)
          pred_labels.append(label)
        acc = compute_accuracy(pred_labels,true_labels)
        print("the accuracy is:", acc)
        print("finished testing phase")
    finish_time = datetime.datetime.now() - start_time
    print("executed part 1 in",finish_time ,"-----------------------------------------") # just so you know how much time you should expect my program to run

execute_part1()

def execute_part2():
    print("executing part 2 -----------------------------------------")
    import datetime
    start_time = datetime.datetime.now()
    train_neg_reviews = load_pickled_data(train_neg_reviews_path) # processed data
    train_pos_reviews = load_pickled_data(train_pos_reviews_path)
    train_reviews = train_neg_reviews + train_pos_reviews
    from sklearn.feature_extraction.text import CountVectorizer
    cv = CountVectorizer()
    X_train = cv.fit_transform(train_reviews)
    pos_labels =[ 1 for i in range(12500)]
    neg_labels = [0 for i in range(12500)]
    Y_train= neg_labels + pos_labels
    from sklearn.naive_bayes import MultinomialNB
    clf = MultinomialNB()
    clf.fit(X_train,Y_train)
    test_neg_reviews = load_pickled_data(test_neg_reviews_path)
    test_pos_reviews = load_pickled_data(test_pos_reviews_path)
    test_reviews = test_neg_reviews + test_pos_reviews
    X_test = cv.transform(test_reviews)
    Y_test= neg_labels + pos_labels
    pred_Y = clf.predict(X_test)
    from sklearn.metrics import accuracy_score
    from sklearn.metrics import confusion_matrix
    print("testing acc is",accuracy_score(pred_Y,Y_test))
    print("confusion matrix is\n",confusion_matrix(pred_Y,Y_test))
    finish_time = datetime.datetime.now() - start_time
    print("executed part 2 in",finish_time ,"-----------------------------------------")



execute_part2()