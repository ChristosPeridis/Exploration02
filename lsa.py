# -*- coding: utf-8 -*-
"""LSA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BXr4DuL-uKdQeTHUI_jVfhyuAykrair8

# **Python Latent Semantic Analysis (LSA) Tutorial**

Import dependencies:
"""
#%%
from sklearn.decomposition import TruncatedSVD
from scipy.sparse import rand
from sklearn.metrics.pairwise import cosine_similarity
from numpy import argsort
import numpy as np

"""In this tutorial we assume that rows represent samples and columns are features according to sklearn.

Generate a random binary 150x100 matrix (150 samples, 100 features):




"""
#%%
B = rand(150, 100, density=0.3, format='csr')
B.data[:] = 1
print("B shape: " + str(B.shape))
print(B)

"""Generate a random binary query (1x100 vector):"""
#%%
query = rand(1, 100, density=0.3, format='csr')
query.data[:] = 1
print("Query shape: " + str(query.shape))
print(query)

"""Generate the k-truncated B matrix using SVD decomposition:


*   trunc_SVD_model is a TruncatedSVD object;
*   fit_transform is a method of TruncatedSVD which computes the rank k SVD decomposition of B and the approximated B matrix;
*   the SVD decomposition is saved into the trunc_SVD_model state.

In this case k=5:
"""
#%%
trunc_SVD_model = TruncatedSVD(n_components=5)
approx_B = trunc_SVD_model.fit_transform(B)
print("Approximated B shape: " + str(approx_B.shape))

"""Transform the query for the new B using the transform method of trunc_SVD_model:


"""
#%%
transformed_query = trunc_SVD_model.transform(query)
print("Transformed query: " + str(transformed_query))
print("Query shape: " + str(transformed_query.shape))
print(transformed_query)

"""Compute cosine similarities between the transformed query and the column vectors of B:"""
#%%
similarities = cosine_similarity(approx_B, transformed_query)
print("Similarities shape: " + str(similarities.shape))
print(similarities)

"""Let's take the indexes of the n most similarity documents:"""
#%%
n=3
indexes = np.argsort(similarities.flat)[-n:]
print("Top n documents: " + str(indexes))
print("Top n similarities: " + str(similarities.flat[indexes]))

"""How to convert corpus to TFIDF:"""
#%%
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

corpus = ['this is the first document',
          'this document is the second document',
          'and this is the third one',
          'is this the first document']
vocabulary = ['this', 'document', 'first', 'is', 'second', 'the',
               'and', 'one']

# use countVectorizer to compute word occurrence
vectorizer = CountVectorizer(vocabulary=vocabulary)

# transform the count matrix to a normalized tf-idf representation
# Normalization is "c" (cosine) when ``norm='l2'``, "n" (none) when ``norm=None``
transformer = TfidfTransformer(norm='l2')
TFIDF = transformer.fit_transform(vectorizer.fit_transform(corpus))

print(TFIDF.shape)
print(TFIDF.toarray())