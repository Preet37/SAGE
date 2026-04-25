# Source: https://www.geeksforgeeks.org/deep-learning/bidirectional-rnns-in-nlp/
# Author: GeeksforGeeks
# Author Slug: geeksforgeeks
# Title: Bidirectional RNNs in NLP - GeeksforGeeks
# Fetched via: trafilatura
# Date: 2026-04-06

The state of a recurrent network at a given time unit only knows about the inputs that have passed before it up to that point in the sentence; it is unaware of the states that will come after that. With knowledge of both past and future situations, the outcomes are significantly enhanced in some applications, such as language modeling. In the case of handwriting identification, for instance, knowing both past and future symbols has an obvious benefit since it helps to understand the underlying context.
Bidirectional Recurrent Neural Networks
Bidirectional recurrent neural networks (Bidirectional RNNs) are [artificial neural networks](https://www.geeksforgeeks.org/artificial-intelligence/artificial-neural-networks-and-its-applications/) that process input data in both the forward and backward directions. Bidirectional recurrent neural networks are really just putting two independent [RNNs](https://www.geeksforgeeks.org/machine-learning/introduction-to-recurrent-neural-network/) together. It consists of two separate [RNNs](https://www.geeksforgeeks.org/machine-learning/introduction-to-recurrent-neural-network/) that process the input data in opposite directions, and the outputs of these RNNs are combined to produce the final output. One common way to combine the outputs of the forward and reverse [RNNs](https://www.geeksforgeeks.org/machine-learning/introduction-to-recurrent-neural-network/) is to concatenate them, but other methods, such as element-wise addition or multiplication can also be used. The choice of combination method can depend on the specific task and the desired properties of the final output.
They are often used in [natural language processing](https://www.geeksforgeeks.org/nlp/natural-language-processing-nlp-tutorial/) tasks, such as language translation, text classification, and named entity recognition. They can capture contextual dependencies in the input data by considering past and future contexts.
Need for Bidirectional Recurrent Neural Networks
- Bidirectional Recurrent Neural Networks (RNNs) are used when the output at a particular time step depends on the input at that time step as well as the inputs that come after it. However, in some cases, the output at a particular time step may also depend on the inputs that come before it. In such cases, Bidirectional RNNs are used to capture the dependencies in both directions.
- The main need for Bidirectional RNNs arises in sequential data processing tasks where the context of the data is important. For instance, in natural language processing, the meaning of a word in a sentence may depend on the words that come before and after it. Similarly, in speech recognition, the current sound may depend on the previous and upcoming sounds.
- The need for Bidirectional RNNs arises in tasks where the context of the data is important, and the output at a particular time step depends on both past and future inputs. By processing the input sequence in both directions, Bidirectional RNNs help to capture these dependencies and improve the accuracy of predictions.
The architecture of Bidirectional RNN
A Bidirectional RNN is a combination of two RNNs - one RNN moves forward, beginning from the start of the data sequence, and the other, moves backward, beginning from the end of the data sequence. The network blocks in a Bidirectional RNN can either be simple [RNNs](https://www.geeksforgeeks.org/machine-learning/introduction-to-recurrent-neural-network/), GRUs, or LSTMs.
A Bidirectional RNN has an additional hidden layer to accommodate the backward training process. At any given time t, the forward and backward hidden states are updated as follows:
At(forward) = φ(Xt * WXf + At - 1(forward) * WAf + bAf)
At(backward) = φ(Xt * WXb + At - 1(backward) * WAb + bAb)
where φ is the activation function, W is the weight matrix, and b is the bias.
The final hidden state is the concatenation of At(forward) and At(backward)
At = [At(forward);At(backward)]
OR
Here, \oplus denotes the mean vector concatenation. There are some other ways also to combine both forward and backward hidden states like element-wise addition or multiplication.
The hidden state at time t is given by the combination of At(forward) and At(backward). The output of any given hidden state is given by:
yt = A t* WAy+by
pt=softmax(yt)
The training of a Bidirectional RNN is similar to Backpropagation Through Time (BPTT) algorithm. BPTT is the backpropagation algorithm used while training RNNs. A typical BPTT algorithm works as follows:
Unroll the network and compute errors at every time step.
Here,
- N = Number of samples
- C = Number of classes
o_{i,c} is the ground truth label for the ith sample and cth class. It is a one-hot encoded vector with a value of 1 for the true class and 0 for the other classes.p_{i,c} is the predicted probability for the ith sample and cth class. It is a one-hot encoded vector with a value of 1 for the true class and 0 for the other classes. , which is output by the last layer of the BiRNN. It is a vector of predicted probabilities for each class.
Roll up the network and update weights.
In a Bidirectional RNN however, since there are forward and backward passes happening simultaneously, updating the weights for the two processes could happen at the same point in time. This leads to erroneous results. Thus, to accommodate forward and backward passes separately, the following algorithm is used for training a Bidirectional RNN:-
Forward Pass
- Forward states (from t = 1 to N) and backward states (from t = N to 1) are passed.
- Output neuron values are passed (from t = 1 to N)
Backward Pass
- Output neuron values are passed (from t = N to 1)
- Forward states (from t = N to 1) and backward states (from t = 1 to N) are passed.
Both the forward and backward passes together train a Bidirectional RNN.
Explanation of Bidirectional RNN with a simple example:
Consider the phrase, 'He said, "Teddy ___". From these three opening words, it's difficult to conclude if the sentence is about Teddy bears or Teddy Roosevelt. This is because the context that clarifies Teddy comes later. RNNs (including GRUs and LSTMs) are able to obtain the context only in one direction, from the preceding words. They're unable to look ahead into future words.
Bidirectional RNNs solve this problem by processing the sequence in both directions. Typically, two separate RNNs are used: one for the forward direction and one for the reverse direction. This results in a hidden state from each RNN, which is usually concatenated to form a single hidden state.
The final hidden state goes to a decoder, such as a fully connected network followed by softmax. Depending on the design of the neural network, the output from a BRNN can either be the complete sequence of hidden states or the state from the last time step. If a single hidden state is given to the decoder, it comes from the last states of each RNN.
Simple Bidirectional RNN Model for Sentiment Analysis
This simple Bidirectional RNN model for sentiment analysis can take in text data as input, process it in both forward and backward directions, and output a probability score indicating the sentiment of the text.
Step 1: Import the necessary libraries
First, we will need the following dependencies to be imported.
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import nltk
import re
import string
import seaborn as sns
import re
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.feature_extraction.text import CountVectorizer
Step 2: Load the dataset
Large Movie Review Dataset. This is a dataset for binary sentiment classification containing substantially more data than previous benchmark datasets. We provide a set of 25,000 highly polar movie reviews for training and 25,000 for testing. There is additional unlabeled data for use as well.
#importing dataset
import wget
wget.download("https://nyc3.digitaloceanspaces.com/ml-files-distro/v1/sentiment-analysis-is-bad/data/sentiment140-subset.csv.zip")
!unzip -n sentiment140-subset.csv.zip
#loading dataset
data = pd.read_csv('sentiment140-subset.csv', nrows=50000)
print(data.head())
Output:
Step 3: Preprocessing
Since the raw text is difficult to process by a neural network, we have to convert it into its corresponding numeric representation.
To do so, initialize your tokenizer by setting the maximum number of words (features/tokens) that you would want to tokenize a sentence to,
tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=400, split=' ')
tokenizer.fit_on_texts(data['text'].values)
# Text Vectorization
X = tokenizer.texts_to_sequences(data['text'].values)
X = tf.keras.preprocessing.sequence.pad_sequences(X)
print(X.shape)
Output:
(50000, 31)
Print text from the encoded vector
tokenizer.sequences_to_texts([list(X[0])])
Output:
['you never tweet']
Step 4: Build the Model
Model building is the process of creating a machine learning model that can make predictions on new data based on patterns and relationships learned from training data. Now, let’s create a Bidirectional RNN model. Use tf.keras.Sequential() to define the model. Add Embedding, SpatialDropout, Bidirectional, and Dense layers. Finally, attach categorical cross entropy loss and Adam optimizer functions to the model.
embed_dim = 256
lstm_out = 196
max_features = tokenizer.num_words
model = tf.keras.Sequential()
model.add(tf.keras.layers.Embedding(max_features,
embed_dim,
input_length = X.shape[1]))
model.add(tf.keras.layers.SpatialDropout1D(0.4))
model.add(tf.keras.layers.Bidirectional(
tf.keras.layers.LSTM(lstm_out,
dropout=0.05,
recurrent_dropout=0.2)))
model.add(tf.keras.layers.Dense(2, activation='softmax'))
model.compile(loss = 'categorical_crossentropy',
optimizer='adam',
metrics = ['accuracy'])
print(model.summary())
Output:
Model: "sequential" _________________________________________________________________ Layer (type) Output Shape Param # ================================================================= embedding (Embedding) (None, 31, 256) 102400 spatial_dropout1d (SpatialD (None, 31, 256) 0 ropout1D) bidirectional (Bidirectiona (None, 392) 710304 l) dense (Dense) (None, 2) 786 ================================================================= Total params: 813,490 Trainable params: 813,490 Non-trainable params: 0 _________________________________________________________________ None
Step 5: Initialize Train and Test Dataset
# Create a one-hot encoded representation of the output labels using the get_dummies() method.
Y = pd.get_dummies(data['polarity'])
# Map the resultant 0 and 1 values with ‘Positive’ and ‘Negative’ respectively.
result_dict = {0: 'Negative', 1: 'Positive'}
y_arr = np.vectorize(result_dict.get)(Y.columns)
Y = Y.values
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.33, random_state = 42)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)
Output:
(33500, 31) (33500, 2) (16500, 31) (16500, 2)
Step 6:Train the model
Training the model is a critical step in machine learning that involves using the training data to learn the patterns and relationships between the input features and output labels. The training process involves minimizing a loss function that measures the difference between the predicted outputs and the actual outputs.
model.fit(X_train, Y_train, epochs=10, batch_size=32)
Output:
Epoch 1/10 1047/1047 [==============================] - 198s 185ms/step - loss: 0.5615 - accuracy: 0.7053 Epoch 2/10 1047/1047 [==============================] - 194s 185ms/step - loss: 0.5230 - accuracy: 0.7374 Epoch 3/10 1047/1047 [==============================] - 183s 174ms/step - loss: 0.5098 - accuracy: 0.7463 Epoch 4/10 1047/1047 [==============================] - 186s 178ms/step - loss: 0.5017 - accuracy: 0.7490 Epoch 5/10 1047/1047 [==============================] - 187s 178ms/step - loss: 0.4939 - accuracy: 0.7553 Epoch 6/10 1047/1047 [==============================] - 194s 185ms/step - loss: 0.4849 - accuracy: 0.7616 Epoch 7/10 1047/1047 [==============================] - 195s 187ms/step - loss: 0.4739 - accuracy: 0.7691 Epoch 8/10 1047/1047 [==============================] - 189s 181ms/step - loss: 0.4650 - accuracy: 0.7723 Epoch 9/10 1047/1047 [==============================] - 190s 182ms/step - loss: 0.4532 - accuracy: 0.7798 Epoch 10/10 1047/1047 [==============================] - 193s 184ms/step - loss: 0.4389 - accuracy: 0.7897
Step 7: Evaluations
Print the prediction score and accuracy on test data.
Loss, acc = model.evaluate(X_test, Y_test, batch_size=64)
print("Loss: %.2f" % (Loss))
print("acc: %.2f" % (acc))
Output:
258/258 [==============================] - 16s 62ms/step - loss: 0.8540 - accuracy: 0.6972 Loss: 0.85 acc: 0.70
Step 8: Predictions
Now's the time to predict the sentiment (positivity/negativity) for a user-given sentence.
#First, initialize it.
twt = ['I will recommend this product']
#Next, tokenize it.
twt = tokenizer.texts_to_sequences(twt)
#Pad it
twt = tf.keras.preprocessing.sequence.pad_sequences(twt, maxlen=X.shape[1], dtype='int32', value=0)
#Predict the sentiment by passing the sentence to the model we built.
sentiment = model.predict(twt, batch_size=1)[0]
print(sentiment)
if(np.argmax(sentiment) == 0):
print(y_arr[0])
elif (np.argmax(sentiment) == 1):
print(y_arr[1])
Output:
1/1 [==============================] - 0s 366ms/step [0.34860525 0.6513947 ] Positive