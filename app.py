import os
import pickle
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

# Load the trained SVC model
MODEL_PATH = 'svc.pkl'
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract features based on your model's training attributes
        age = float(request.form['age'])
        gender = 1 if request.form['gender'].lower() == 'male' else 0
        city = float(request.form['city'])
        bmi = float(request.form['bmi'])
        family_history_diabetes = 1 if request.form['family_history_diabetes'].lower() == 'yes' else 0
        physical_activity_level = float(request.form['physical_activity_level'])
        diet_type = float(request.form['diet_type'])
        smoking_status = float(request.form['smoking_status'])
        alcohol_consumption = float(request.form['alcohol_consumption'])
        hours_sleep_per_night = float(request.form['hours_sleep_per_night'])
        stress_level = float(request.form['stress_level'])
        fasting_blood_sugar = float(request.form['fasting_blood_sugar'])
        hba1c_level = float(request.form['hba1c_level'])
        blood_pressure_systolic = float(request.form['blood_pressure_systolic'])
        blood_pressure_diastolic = float(request.form['blood_pressure_diastolic'])
        waist_circumference_cm = float(request.form['waist_circumference_cm'])
        income_bracket = float(request.form['income_bracket'])

        # Arrange features into an array for the classifier
        features = np.array([[
            age, gender, city, bmi, family_history_diabetes,
            physical_activity_level, diet_type, smoking_status, alcohol_consumption,
            hours_sleep_per_night, stress_level, fasting_blood_sugar, hba1c_level,
            blood_pressure_systolic, blood_pressure_diastolic, waist_circumference_cm,
            income_bracket
        ]])

        prediction = model.predict(features)
        result = "Positive / High Risk" if int(prediction[0]) == 1 else "Negative / Low Risk"

        return render_template('index.html', prediction_text=f'Prediction Result: {result}')
    
    except Exception as e:
        return render_template('index.html', prediction_text=f'Error in processing: {str(e)}')

if __name__ == '__main__':
    app.run(debug=True)
