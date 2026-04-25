# Source: https://course.fast.ai/Lessons/lesson5.html
# Author: fast.ai
# Author Slug: fast-ai
# Downloaded: 2026-04-06
# Words: 116
5: From-scratch model
Today we look at how to create a neural network from scratch using Python and PyTorch, and how to implement a training loop for optimising the weights of a model. We build up from a single layer regression model up to a neural net with one hidden layer, and then to a deep learning model. Along the way we’ll also look at how we can use a special function called sigmoid to make binary classification models easier to train, and we’ll also learn about metrics.
Video
This lesson is based partly on [chapter 4](https://github.com/fastai/fastbook/blob/master/04_mnist_basics.ipynb) and [chapter 9](https://github.com/fastai/fastbook/blob/master/09_tabular.ipynb) of the [book](https://www.amazon.com/Deep-Learning-Coders-fastai-PyTorch/dp/1492045527).
Lesson notebooks
Links from the lesson
[OneR paper](https://link.springer.com/article/10.1023/A:1022631118932)- Some great Titanic notebooks:
[1](https://www.kaggle.com/code/mrisdal/exploring-survival-on-the-titanic);[2](https://www.kaggle.com/code/cdeotte/titanic-wcg-xgboost-0-84688/notebook);[3](https://www.kaggle.com/code/pliptor/divide-and-conquer-0-82296);[4](https://www.kaggle.com/code/cdeotte/titanic-using-name-only-0-81818/notebook)