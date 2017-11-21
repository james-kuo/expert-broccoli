import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
# from sklearn.preprocessing import label_binarize
from xgboost import XGBClassifier
# from keras.models import load_model
import pandas as pd
import joblib
from joblib import Parallel, delayed


names = ["Nearest Neighbors", "SVM", "Decision Tree", "Random Forest", "Neural Net", "AdaBoost", "Naive Bayes", "LDA", "XGBoost"]

filenames = ["nearestneighbors", "svm", "decisiontree", "randomforest", "neuralnet", "adaboost", "naivebayes", "lda", "xgb"]
inception_filenames = ["inception_epoch-02", "inception_epoch-05", "inception_epoch-08", "inception_epoch-final"]

# inception_model_path = '/path'
classifiers = [
    KNeighborsClassifier(3),
    SVC(kernel="linear", C=0.025),
    DecisionTreeClassifier(max_depth=5),
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    MLPClassifier(alpha=1),
    AdaBoostClassifier(),
    GaussianNB(),
    QuadraticDiscriminantAnalysis(),
    XGBClassifier()
    ]

# inception_models = [
#     load_model(inception_model_path + 'finetuned_model_epoch-02.hdf5'),
#     load_model(inception_model_path + 'finetuned_model_epoch-05.hdf5'),
#     load_model(inception_model_path + 'finetuned_model_epoch-08.hdf5'),
#     load_model(inception_model_path + 'finetuned_model_epoch-final.hdf5')
#     ]



X, labels = joblib.load("representations.joblib")

y = np.array(labels)
X = np.array(X)

#X = joblib.load("./pca_representations.joblib")

print(X.shape)
print(y.shape)
# y_array = np.array(label_binarize(y, range(len(set(y)))))
y_array = np.array(pd.get_dummies(y).as_matrix())

X_train, X_test, y_train, y_test =  train_test_split(X, y, random_state=42)
X_train, X_test, y_train_array, y_test_array =  train_test_split(X, y_array, random_state=42)

joblib.dump((X_train, X_test, y_train_array, y_test_array), "testdata.joblib")
print(np.array(y_test).shape)
print(np.array(y_test_array).shape)

def train_save(model, filename):
    try:
        model.fit(X_train, y_train)
    except ValueError:
        model.fit(X_train, y_train_array)
    joblib.dump(model, "{}.joblib".format(filename))
    try:
        print("{0}: {1} acc".format(filename, model.score(X_test, y_test)))
    except ValueError:
        print("{0}: {1} acc".format(filename, model.score(X_test, y_test_array)))

Parallel(n_jobs=-1)(delayed(train_save)(m, f) for (m,f) in zip(classifiers, filenames))

# preprocessed image data for keras model
X , labels = joblib.load("preprocessed_imgs.joblib")
X_train, X_test, y_train, y_test =  train_test_split(X, y, random_state=42)
joblib.dump((X_train, X_test, y_train, y_test), "imgs_testdata.joblib")

#for model, filename in zip(classifiers, filenames):
#    model.fit(X_train, y_train)
#    joblib.dump(model, "{}.joblib".format(filename))

