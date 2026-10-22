import os
import pickle
import traceback
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

# Load the trained SVC model
MODEL_PATH = 'svc.pkl'
model = None
expected_features = None

try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    
    # Check how many features the model was trained on (supported in scikit-learn >= 0.24)
    if hasattr(model, 'n_features_in_'):
        expected_features = model.n_features_in_
        print(f"Model loaded successfully! It expects {expected_features} features.")
    else:
        print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")

@app.route('/')
def home():
    return render_template('index.html', prediction_text=None, expected_features=expected_features)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if model is None:
            return render_template('index.html', prediction_text="Error: Model 'svc.pkl' could not be loaded.", expected_features=expected_features)

        # Helper to safely grab form inputs
        def get_float(field_name, default=0.0):
            val = request.form.get(field_name, '').strip()
            return float(val) if val else default

        # Collect features from the form
        # NOTE: Adjust this list to match the exact features your model was trained on!
        features_list = [
            get_float('age'),
            1 if request.form.get('gender', '').lower() == 'male' else 0,
            get_float('city'),
            get_float('bmi'),
            1 if request.form.get('family_history_diabetes', '').lower() == 'yes' else 0,
            get_float('physical_activity_level'),
            get_float('diet_type'),
            get_float('smoking_status'),
            get_float('alcohol_consumption'),
            get_float('hours_sleep_per_night'),
            get_float('stress_level'),
            get_float('fasting_blood_sugar'),
            get_float('hba1c_level'),
            get_float('blood_pressure_systolic'),
            get_float('blood_pressure_diastolic'),
            get_float('waist_circumference_cm'),
            get_float('income_bracket')
        ]

        # If we know how many features the model expects, slice or pad the list to match
        if expected_features is not None:
            if len(features_list) != expected_features:
                return render_template(
                    'index.html', 
                    prediction_text=f"Shape Error: Your model expects {expected_features} features, but your form sent {len(features_list)} features. Update your form fields in app.py to match your training data.",
                    expected_features=expected_features
                )

        features = np.array([features_list])

        # Run prediction
        prediction = model.predict(features)
        result = "Positive / High Risk" if int(prediction[0]) == 1 else "Negative / Low Risk"

        return render_template('index.html', prediction_text=f'Prediction Result: {result}', expected_features=expected_features)
    
    except Exception as e:
        error_msg = traceback.format_exc()
        print(error_msg) # Prints details to your terminal
        return render_template('index.html', prediction_text=f"Runtime Error: {str(e)}", expected_features=expected_features)

if __name__ == '__main__':
    app.run(debug=True)
