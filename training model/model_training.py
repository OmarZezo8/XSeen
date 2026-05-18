import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# preparing dataset
file_path = "exoplanets.csv"
df = pd.read_csv(file_path)
df = df.drop_duplicates()
df = df.dropna()

X = df.drop(columns=["koi_disposition"])
y=df['koi_disposition'].map({"FALSE POSITIVE":0, "CANDIDATE":1, "CONFIRMED":2})

# splitting data and getting model ready
X_train, X_test, y_train, y_test=train_test_split(X, y, test_size=0.1, stratify=y, random_state=42)
clf = RandomForestClassifier(n_estimators=3000, max_depth=450, class_weight="balanced", random_state=42)

# training and predicting
clf.fit(X_train, y_train)
y_pred=clf.predict(X_test)

# evaluating the model
print(classification_report(y_test, y_pred))

# saving the model
joblib.dump(clf, 'model.pkl')



