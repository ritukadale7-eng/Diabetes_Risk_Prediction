import pickle
from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

# Load your trained SVC model
with open('svc.pkl', 'rb') as f:
  model = pickle.load(f)


@app.route('/')
def home():
  return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
  try:
    form_data = request.form

    # Extract features corresponding to your model's 17 training inputs
    age = float(form_data.get('age', 0))
    gender = 1 if form_data.get('gender') == 'Male' else 0
    city = float(form_data.get('city', 0))
    bmi = float(form_data.get('bmi', 0))
    family_history_diabetes = (
        1 if form_data.get('family_history_diabetes') == 'Yes' else 0
    )
    physical_activity_level = float(
        form_data.get('physical_activity_level', 0)
    )
    diet_type = float(form_data.get('diet_type', 0))
    smoking_status = float(form_data.get('smoking_status', 0))
    alcohol_consumption = float(form_data.get('alcohol_consumption', 0))
    hours_sleep_per_night = float(form_data.get('hours_sleep_per_night', 0))
    stress_level = float(form_data.get('stress_level', 0))
    fasting_blood_sugar = float(form_data.get('fasting_blood_sugar', 0))
    hba1c_level = float(form_data.get('hba1c_level', 0))
    blood_pressure_systolic = float(form_data.get('blood_pressure_systolic', 0))
    blood_pressure_diastolic = float(
        form_data.get('blood_pressure_diastolic', 0)
    )
    waist_circumference_cm = float(
        form_data.get('waist_circumference_cm', 0)
    )
    income_bracket = float(form_data.get('income_bracket', 0))

    # Assemble feature array for prediction
    features = np.array([[
        age,
        gender,
        city,
        bmi,
        family_history_diabetes,
        physical_activity_level,
        diet_type,
        smoking_status,
        alcohol_consumption,
        hours_sleep_per_night,
        stress_level,
        fasting_blood_sugar,
        hba1c_level,
        blood_pressure_systolic,
        blood_pressure_diastolic,
        waist_circumference_cm,
        income_bracket,
    ]])

    # Make prediction using your SVC model
    prediction = model.predict(features)[0]
    result_text = f'Prediction Result: Class {prediction}'

    return render_template('index.html', prediction_text=result_text)

  except Exception as e:
    return render_template(
        'index.html', prediction_text=f'Error in processing: {str(e)}'
    )


if __name__ == '__main__':
  app.run(debug=True)
