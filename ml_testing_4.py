# -*- coding: utf-8 -*-
"""ml_testing_4

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VhaIiWd4u79SJY4jPw-UU9KJG3HMyL6T

# Лабораторная работа 4. ОБУЧЕНИЕ С УЧИТЕЛЕМ. ЗАДАЧА КЛАССИФИКАЦИИ.

# Задание 1

Какова вероятность отправиться на прогулку если идёт дождь, при наличии следующих наблюдений?
```
data = [
        ('солнечно', True),
        ('снег', False),
        ('облачно', False),
        ('дождь', False),
        ('солнечно', True),
        ('снег', False),
        ('облачно', True),
        ('снег', False),
        ('солнечно', False),
        ('облачно', True),
        ('снег', True),
        ('солнечно', True),
        ('дождь', False),
        ('дождь', True),
        ('облачно', True),
]
```

Для начала нужно представить данные в удобном для работы виде. Погодные условия будут представлены в виде чисел индексов от 0 до 4, а булевы значения 1 и 0 соотвественно. Далее происходит распределение на обучающую и тестовую выборки и обучение модели по обучающей выборке. И наконец вычисляем вероятность отправится на прогулку во время дождя.
"""

from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


# Исходные данные
data = [
        ('солнечно', True),
        ('снег', False),
        ('облачно', False),
        ('дождь', False),
        ('солнечно', True),
        ('снег', False),
        ('облачно', True),
        ('снег', False),
        ('солнечно', False),
        ('облачно', True),
        ('снег', True),
        ('солнечно', True),
        ('дождь', False),
        ('дождь', True),
        ('облачно', True),
]


# 1. Преобразуем текстовые данные в числовые
le = LabelEncoder()
X = le.fit_transform([weather for weather, _ in data]).reshape(-1, 1)
y = [int(go_out) for _, go_out in data]

# 2. Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Обучение модели логистической регрессии
clf = LogisticRegression(random_state=0)
clf.fit(X_train, y_train)

# 4. Оценка вероятности отправиться на прогулку при дожде
prob_rain = clf.predict_proba([[le.transform(['дождь'])[0]]])[0][1]

prob_rain

"""Ответ: **42,36%**

# Задание 2

Для начала выведем датасет и выполним полную обработку.
"""

import pandas as pd

# Загрузка данных
data = pd.read_csv("airlines_task.csv")

# Просмотр первых строк датасета
data.head()

#main info bout dataset
data.info()

#number of missed values
data.isna().sum()

#cleaning missed values
columns_to_median = ['Length']

for row in columns_to_median:
  data[row]=data[row].fillna(data[row].median())

data.dropna(subset=['DayOfWeek', 'AirportTo', 'Airline', 'Delay', 'Length'],inplace=True)

data.isna().sum()

"""На этом стартовая предобработка завершена, теперь можно приступить к выделению целевой переменной и предикторов."""

data.head()

y = data["Delay"]
X = data.drop(["Delay", "id", 'Flight'], axis=1)


airline_codes = X['Airline'].unique()
airline_to_number = {code: i for i, code in enumerate(airline_codes)}

# Преобразовываем столбцы авиакомпаний в числовые индикаторы
X['Airline'] = X['Airline'].map(airline_to_number)

all_airports = pd.concat([X['AirportFrom'], X['AirportTo']]).unique()

airport_to_number = {airport: i for i, airport in enumerate(all_airports)}

X['AirportFrom'] = X['AirportFrom'].map(airport_to_number)
X['AirportTo'] = X['AirportTo'].map(airport_to_number)

X.head(10)

y

"""Теперь выделим тестовые и обучающие выборки."""

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создайте уменьшенные обучающую и тестовую выборки
desired_train_size = 1000  # Задайте желаемый размер обучающей выборки
desired_test_size = 500  # Задайте желаемый размер тестовой выборки

X_train = X_train[:desired_train_size]
y_train = y_train[:desired_train_size]
X_test = X_test[:desired_test_size]
y_test = y_test[:desired_test_size]

"""**Масштабирование числовых признаков**"""

from sklearn.preprocessing import StandardScaler

num_features = ['DayOfWeek', 'Time', 'Length', 'Airline', 'AirportFrom', 'AirportTo']

scaler = StandardScaler()
X_train[num_features] = scaler.fit_transform(X_train[num_features])
X_test[num_features] = scaler.transform(X_test[num_features])

X_train.head()

"""**Проверяем распределение классов в обучающей выборке**"""

class_distribution = y_train.value_counts(normalize=True)
class_distribution

"""Распределение классов в обучающей выборке следующее:

    Класс 0 (без задержки): 74.8%
    Класс 1 (с задержкой): 25.2%

Действительно, у нас есть дисбаланс классов, но он не слишком сильный.
Произведем балансировку.
"""

from imblearn.over_sampling import SMOTE

# Проведение балансировки (SMOTE)
smote = SMOTE(sampling_strategy='auto', random_state=42)
X_train, y_train = smote.fit_resample(X_train, y_train)

class_distribution = y_train_resampled.value_counts(normalize=True)
class_distribution

"""Теперь проведем обучение модели

Для начала подберем гиперпараметры для каждой модели обучения.
"""

from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

# Создайте списки параметров для каждой модели
param_grid_knn = {
    'n_neighbors': [3, 5, 7],
    'weights': ['uniform', 'distance']
}

param_grid_nb = {
    # Наивный Байес не имеет гиперпараметров для настройки
}

param_grid_lr = {
    'C': [0.1, 1, 10],
    'penalty': ['l1', 'l2']
}

param_grid_svm = {
    'C': [0.1, 1, 10],
    'kernel': ['linear', 'rbf']
}

# Создайте экземпляры моделей
knn = KNeighborsClassifier()
nb = GaussianNB()
lr = LogisticRegression(max_iter=10000, multi_class='ovr', solver='liblinear')
svm = SVC()

# Создайте объекты GridSearchCV для каждой модели
grid_search_knn = GridSearchCV(knn, param_grid_knn, scoring='accuracy')
grid_search_nb = GridSearchCV(nb, param_grid_nb, scoring='accuracy')
grid_search_lr = GridSearchCV(lr, param_grid_lr, scoring='accuracy')
grid_search_svm = GridSearchCV(svm, param_grid_svm, scoring='accuracy')

# Выполните поиск по сетке для каждой модели
grid_search_knn.fit(X_train, y_train)
grid_search_nb.fit(X_train, y_train)
grid_search_lr.fit(X_train, y_train)
grid_search_svm.fit(X_train, y_train)

# Выведите лучшие параметры для каждой модели
best_params_knn = grid_search_knn.best_params_
best_params_nb = grid_search_nb.best_params_
best_params_lr = grid_search_lr.best_params_
best_params_svm = grid_search_svm.best_params_

print("Лучшие параметры для k-NN:", best_params_knn)
print("Лучшие параметры для Naive Bayes:", best_params_nb)
print("Лучшие параметры для Logistic Regression:", best_params_lr)
print("Лучшие параметры для SVM:", best_params_svm)

from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression

# Обучение моделей
knn = KNeighborsClassifier(**best_params_knn)
naive_bayes = GaussianNB()
logistic_regression = LogisticRegression(**best_params_lr)
svm = SVC(**best_params_svm)

knn.fit(X_train_resampled, y_train_resampled)
naive_bayes.fit(X_train_resampled, y_train_resampled)
logistic_regression.fit(X_train_resampled, y_train_resampled)
svm.fit(X_train_resampled, y_train_resampled)

# Предсказание на тестовой выборке
y_pred_knn = knn.predict(X_test)
y_pred_naive_bayes = naive_bayes.predict(X_test)
y_pred_logistic_regression = logistic_regression.predict(X_test)
y_pred_svm = svm.predict(X_test)

"""Предсказание выполнено, время вычислить точность прогнозов с помошью различных метрик."""

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt


y_true = y_test

#preparing predict results for counting metrics
y_knn = [y_pred_knn]
y_knn.append("KNN Results:")

y_naive = [y_pred_naive_bayes]
y_naive.append("Naive bayes Results:")

y_logistic = [y_pred_logistic_regression]
y_logistic.append("Logistic regression Results:")

y_svm = [y_pred_svm]
y_svm.append("SVM Results:")


# Вычисление метрик
def get_metrics(y_pred_model):
  accuracy_model1 = accuracy_score(y_true, y_pred_model[0])
  precision_model1 = precision_score(y_true, y_pred_model[0])
  recall_model1 = recall_score(y_true, y_pred_model[0])
  f1_model1 = f1_score(y_true, y_pred_model[0])
  roc_auc_model1 = roc_auc_score(y_true, y_pred_model[0])

  print(f"Model ---> {y_pred_model[1]}\nAccuracy: {accuracy_model1}\nPrecision: {precision_model1}\nRecall: {recall_model1}\nF1: {f1_model1}\nROC AUC: {roc_auc_model1}\n\n")


get_metrics(y_knn)
get_metrics(y_naive)
get_metrics(y_logistic)
get_metrics(y_svm)

"""Accuracy количество правильных предсказаний самое лучшее у **KNN модели**.
Precision практически одинаоковое у всех моделей.
Recall лучший показатель у **Naive Bayes** количество положительных предсказаний предсказаных моделью.
Последний показатель ROC AUC показывает производительность модели пока что она около отметки **0.5** .

Последний этап построение итоговой модели классификаторов.
"""

import numpy as np
from sklearn.metrics import classification_report



best_knn_params = {'n_neighbors': 7, 'weights': 'distance'}
best_lr_params = {'C': 0.1, 'penalty': 'l2'}
best_svm_params = {'C': 0.1, 'kernel': 'linear'}

# Создаем словарь с моделями и их лучшими параметрами
classifiers = {
    'k-NN': KNeighborsClassifier(**best_knn_params),
    'Naive Bayes': GaussianNB(),
    'Logistic Regression': LogisticRegression(**best_lr_params),
    'SVM': SVC(**best_svm_params)
}

n_classifiers = len(classifiers)

for name, classifier in classifiers.items():
    classifier.fit(X_train, np.ravel(y_train))

    y_pred = classifier.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy (test) for {name}: {accuracy * 100:.1f}%")
    print(classification_report(y_test, y_pred))
    print("---------------------------------------------")

"""k-NN:
        Accuracy (точность) составляет 72.4%, что означает, что модель правильно классифицировала 72.4% тестовых данных.
    Naive Bayes:
        Accuracy повысилась до 74.4%, и для класса 0 (отрицательный класс) метрики Precision, Recall и F1-score высоки.
    Logistic Regression и SVM:
        Оба метода показывают одинаковую точность в 74.6%, но, как и в случае с Naive Bayes, метрики для класса 1 (положительный класс) низки.

# Задание 3

Давайте начнем с реализации метрик Accuracy, Precision, Recall и F1.
"""

def accuracy(y_true, y_pred):
    correct_predictions = np.sum(y_true == y_pred)
    total_samples = len(y_true)
    return correct_predictions / total_samples

def precision(y_true, y_pred):
    true_positives = np.sum((y_true == 1) & (y_pred == 1))
    false_positives = np.sum((y_true == 0) & (y_pred == 1))
    return true_positives / (true_positives + false_positives + 1e-10)

def recall(y_true, y_pred):
    true_positives = np.sum((y_true == 1) & (y_pred == 1))
    false_negatives = np.sum((y_true == 1) & (y_pred == 0))
    return true_positives / (true_positives + false_negatives + 1e-10)

def f1_score(y_true, y_pred):
    precision_value = precision(y_true, y_pred)
    recall_value = recall(y_true, y_pred)
    return 2 * (precision_value * recall_value) / (precision_value + recall_value + 1e-10)

#проверка работоспособности
print(accuracy(y_true, y_pred_knn))
print(precision(y_true, y_pred_knn))
print(recall(y_true, y_pred_knn))
print(f1_score(y_true, y_pred_knn))

"""`Вычисление метрик корректно!`

Теперь перейдем к реализации k-NN.
"""

class KNNClassifier:
    def __init__(self, k=3):
        self.k = k

    def fit(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train

    def predict(self, X_test):
        predictions = []
        for i, row in X_test.iterrows():
            x = row.values
            distances = np.linalg.norm(self.X_train.iloc[1:] - x, axis=1)
            indices = np.argsort(distances)[:self.k]
            neighbors_labels = self.y_train.iloc[indices]
            unique_labels, counts = np.unique(neighbors_labels, return_counts=True)
            predicted_label = unique_labels[np.argmax(counts)]
            predictions.append(predicted_label)
        return np.array(predictions)

#testing our self made class
knn = KNNClassifier()

knn.fit(X_train_resampled, y_train_resampled)
y_pred_knn = knn.predict(X_test)
y_pred_model = [y_pred_knn]
y_pred_model.append("KNN Results:")

get_metrics(y_pred_model)

"""`Класс реализован и проверен!`"""