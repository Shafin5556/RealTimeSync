import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import LabelEncoder
import pickle

# Load the data
data = pd.read_csv('V3_crop_environment_data_with_lih_and_advice_with_error.csv')

# Define the features and the target
X = data[['Temperature', 'Humidity', 'Soil Moisture', 'Light Intensity', 'Crop Name']]
y = data['Advice']  # Assuming we're predicting the 'Advice' column

# Encode the crop names
label_encoder = LabelEncoder()
X['Crop Name'] = label_encoder.fit_transform(X['Crop Name'])

# Handle class imbalance with SMOTE
smote = SMOTE()
X_resampled, y_resampled = smote.fit_resample(X, y)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Create and train the RandomForest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'Model accuracy: {accuracy * 100:.2f}%')

# Save the model if accuracy is above 90%
if accuracy >= 0.90:
    with open('crop_prediction_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("Model saved successfully.")
