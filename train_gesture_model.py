import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Load collected data
df = pd.read_csv("gesture_data.csv", header=None)
X = df.iloc[:, :-1].values  # All landmark coords
y = df.iloc[:, -1].values   # Gesture labels

# Split into train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train classifier
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "gesture_model.pkl")
print("Saved model as gesture_model.pkl")
