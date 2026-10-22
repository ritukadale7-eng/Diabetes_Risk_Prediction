import os
import pickle
import traceback
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

# Load the trained SVC model
MODEL_PATH = 'svc.pkl'
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.route('/')
def home():
    return render_template('index.html', prediction_text=None)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if model is None:
            return render_template('index.html', prediction_text="Error: Model 'svc.pkl' could not be loaded on the server.")

        # Helper function to safely convert form inputs to float
        def get_float(field_name, default=0.0):
            val = request.form.get(field_name, '').strip()
            return float(val) if val else default

        # Extract features based on your model's training attributes
        age = get_float('age')
        gender = 1 if request.form.get('gender', '').lower() == 'male' else 0
        city = get_float('city')
        bmi = get_float('bmi')
        family_history_diabetes = 1 if request.form.get('family_history_diabetes', '').lower() == 'yes' else 0
        physical_activity_level = get_float('physical_activity_level')
        diet_type = get_float('diet_type')
        smoking_status = get_float('smoking_status')
        alcohol_consumption = get_float('alcohol_consumption')
        hours_sleep_per_night = get_float('hours_sleep_per_night')
        stress_level = get_float('stress_level')
        fasting_blood_sugar = get_float('fasting_blood_sugar')
        hba1c_level = get_float('hba1c_level')
        blood_pressure_systolic = get_float('blood_pressure_systolic')
        blood_pressure_diastolic = get_float('blood_pressure_diastolic')
        waist_circumference_cm = get_float('waist_circumference_cm')
        income_bracket = get_float('income_bracket')

        # Arrange features into an array for the classifier
        features = np.array([[
            age, gender, city, bmi, family_history_diabetes,
            physical_activity_level, diet_type, smoking_status, alcohol_consumption,
            hours_sleep_per_night, stress_level, fasting_blood_sugar, hba1c_level,
            blood_pressure_systolic, blood_pressure_diastolic, waist_circumference_cm,
            income_bracket
        ]])

        # Run prediction
        prediction = model.predict(features)
        result = "Positive / High Risk" if int(prediction[0]) == 1 else "Negative / Low Risk"

        return render_template('index.html', prediction_text=f'Prediction Result: {result}')
    
    except Exception as e:
        # Capture the full error stack trace for easy debugging
        error_details = traceback.format_exc()
        print(error_details)  # Prints to your terminal
        return render_template('index.html', prediction_text=f"Processing Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
