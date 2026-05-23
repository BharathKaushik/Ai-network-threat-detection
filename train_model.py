import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib

# Load dataset
print("Loading dataset...")

df = pd.read_csv("../dataset/network_dataset.csv")

print(df.head())

# Encode protocol column
protocol_encoder = LabelEncoder()
df['protocol'] = protocol_encoder.fit_transform(df['protocol'])

# Encode labels
label_encoder = LabelEncoder()
df['label'] = label_encoder.fit_transform(df['label'])

# Features
X = df[[
    'packet_size',
    'protocol',
    'connection_rate'
]]

# Target
y = df['label']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train model
print("Training model...")
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Accuracy report
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, 'model.pkl')
joblib.dump(protocol_encoder, 'protocol_encoder.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')

print("Model saved successfully!")