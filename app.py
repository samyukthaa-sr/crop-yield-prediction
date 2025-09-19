from flask import Flask, request, render_template
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

# Initialize Flask app
app = Flask(__name__)

# Dataset
data = {
    'Crop': ['Wheat', 'Rice', 'Maize', 'Barley', 'Rice', 'Wheat', 'Soybean', 'Maize', 'Wheat', 'Rice',
             'Maize', 'Soybean', 'Barley', 'Wheat', 'Rice', 'Maize', 'Soybean', 'Rice', 'Barley', 'Wheat',
             'Soybean', 'Maize', 'Wheat', 'Rice', 'Soybean', 'Wheat', 'Maize', 'Rice', 'Barley', 'Wheat',
             'Rice', 'Soybean'],
    'Temperature': [16, 30, 26, 14, 29, 16, 25, 27, 15, 31, 26, 24, 13, 17, 32, 26, 24, 29, 12, 18,
                    28, 29, 16, 30, 26, 18, 27, 25, 32, 17, 22, 30],
    'Rainfall': [50, 300, 120, 45, 310, 55, 110, 125, 60, 320, 130, 100, 40, 65, 330, 140, 105, 315, 35, 70,
                 160, 200, 55, 330, 135, 75, 210, 110, 340, 90, 120, 215],
    'Soil_pH': [6.5, 5.5, 6.0, 6.8, 5.4, 6.4, 6.2, 6.1, 6.5, 5.3, 6.0, 6.3, 6.7, 6.6, 5.2, 6.0, 6.3, 5.5, 6.9, 6.5,
                6.2, 5.7, 6.0, 5.8, 6.3, 6.5, 6.1, 5.9, 6.7, 6.0, 6.3, 6.8],
    'Humidity': [70, 85, 80, 65, 88, 72, 78, 82, 74, 90, 81, 77, 63, 75, 92, 83, 79, 89, 60, 76,
                 70, 85, 78, 81, 79, 74, 76, 83, 91, 85, 79, 88],
    'Fertilizer': [50, 70, 60, 45, 75, 55, 65, 68, 52, 80, 70, 64, 40, 53, 85, 66, 63, 78, 38, 57,
                   55, 70, 60, 62, 68, 74, 72, 65, 78, 67, 64, 73],
    'Yield': ['High', 'Medium', 'High', 'Low', 'Medium', 'High', 'Medium', 'High', 'High', 'Medium',
              'High', 'Medium', 'Low', 'High', 'Medium', 'High', 'Medium', 'Medium', 'Low', 'High',
              'Medium', 'High', 'High', 'Medium', 'Medium', 'High', 'Medium', 'Low', 'High', 'Medium',
              'High', 'Medium']
}

df = pd.DataFrame(data)

# Encode categorical variables
le_crop = LabelEncoder()
le_yield = LabelEncoder()

df['Crop'] = le_crop.fit_transform(df['Crop'])
df['Yield'] = le_yield.fit_transform(df['Yield'])

# Features & target
X = df[['Crop', 'Temperature', 'Rainfall', 'Soil_pH', 'Humidity', 'Fertilizer']]
y = df['Yield']

# Train Decision Tree model
model = DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=42)
model.fit(X, y)

@app.route('/')
def home():
    crops = le_crop.classes_
    return render_template('index.html', crops=crops)

@app.route('/predict', methods=['POST'])
def predict():
    crop_name = request.form['crop']
    temperature = float(request.form['temperature'])
    rainfall = float(request.form['rainfall'])
    soil_ph = float(request.form['soil_ph'])
    humidity = float(request.form['humidity'])
    fertilizer = float(request.form['fertilizer'])

    # Encode crop name
    crop_encoded = le_crop.transform([crop_name])[0]

    # Prepare input data
    input_data = [[crop_encoded, temperature, rainfall, soil_ph, humidity, fertilizer]]

    # Predict yield
    prediction = model.predict(input_data)
    yield_category = le_yield.inverse_transform(prediction)[0]

    return render_template('index.html', crops=le_crop.classes_,
                           prediction=True, crop=crop_name, yield_category=yield_category)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

