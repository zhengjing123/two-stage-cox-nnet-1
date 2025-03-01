from cox_nnet import *

import numpy

import sklearn
x = numpy.loadtxt(fname="coxnet_x.csv",delimiter=",",skiprows=0)

ytime = numpy.loadtxt(fname="y_days.csv",delimiter=",",skiprows=0)

ystatus = numpy.loadtxt(fname="event.csv",delimiter=",",skiprows=0)

x_train, x_test, ytime_train, ytime_test, ystatus_train, ystatus_test = sklearn.cross_validation.train_test_split(x, ytime, ystatus, test_size = 0.2, random_state = 11)

model_params = dict(node_map = None, input_split = None)

search_params = dict(method = "nesterov", learning_rate=0.005, momentum=0.9,

max_iter=2000, stop_threshold=0.995, patience=1000, patience_incr=2, rand_seed = 100,

eval_step=23, lr_decay = 0.9, lr_growth = 1.0)

cv_params = dict(cv_seed=1, n_folds=5, cv_metric = "loglikelihood", L2_range = numpy.arange(-4,3,0.5))

cv_likelihoods, L2_reg_params, mean_cvpl = L2CVProfile(x,ytime,ystatus,

model_params,search_params,cv_params, verbose=False)
L2_reg = L2_reg_params[numpy.argmax(mean_cvpl)]

model_params = dict(node_map = None, input_split = None, L2_reg=numpy.exp(L2_reg))

model, cost_iter = trainCoxMlp(x_train, ytime_train, ystatus_train, model_params, search_params, verbose=True)

featureScore = varImportance(model, x_train, ytime_train, ystatus_train)

numpy.savetxt('feature_importance.csv', featureScore, delimiter=",")

saveModel(model,'hidden_layer.csv')

