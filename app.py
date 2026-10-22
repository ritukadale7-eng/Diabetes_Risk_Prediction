import pickle
import numpy as np
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Load the trained SVM model
with open('SVM.pkl', 'rb') as f:
    model = pickle.load(f)

# HTML template with modern Tailwind CSS styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Health Risk Prediction Portal</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-br from-slate-50 to-blue-50 min-h-screen py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto bg-white rounded-2xl shadow-xl overflow-hidden border border-slate-100">
        <!-- Header -->
        <div class="bg-gradient-to-r from-blue-600 to-indigo-700 py-6 px-8 text-white">
            <h1 class="text-3xl font-extrabold tracking-tight">Health Risk Assessment</h1>
            <p class="mt-2 text-blue-100 text-sm">Enter your biometric and lifestyle details below to get an instant SVM prediction.</p>
        </div>

        <!-- Form Body -->
        <form method="POST" class="p-8 space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                
                <!-- Age -->
                <div>
                    <label class="block text-sm font-semibold text-slate-700 mb-1">Age</label>
                    <input type="number" name="age" required class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none" placeholder="e.g., 45">
                </div>

                <!-- Gender -->
                <div>
                    <label class="block text-sm font-semibold text-slate-700 mb-1">Gender</label>
                    <select name="gender" class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none">
                        <option value="0">Female</option>
                        <option value="1">Male</option>
                    </select>
                </div>

                <!-- City (Encoded or numeric representation) -->
                <div>
                    <label class="block text-sm font-semibold text-slate-700 mb-1">City Code</label>
                    <input type="number" name="city" required class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none" placeholder="e.g., 1">
                </div>

                <!-- BMI -->
                <div>
                    <label class="block text-sm font-semibold text-slate-700 mb-1">BMI</label>
                    <input type="step" step="0.1" name="bmi" required class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none" placeholder="e.g., 24.5">
                </div>

                <!-- Family History Diabetes -->
                <div>
                    <label class="block text-sm font-semibold text-slate-700 mb-1">Family History of Diabetes</label>
                    <select name="family_history_diabetes" class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none">
                        <option value="0">No</option>
                        <option value="1">Yes</option>
                    </select>
                </div>

                <!-- Physical Activity Level -->
                <div>
                    <label class="block text-sm font-semibold text-slate-700 mb-1">Physical Activity Level</label>
                    <input type="number" name="physical_activity_level" required class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none" placeholder="e.g., 2">
                </div>

                <!-- Diet Type -->
                <div>
                    <label class="block text-sm font-semibold text-slate-700 mb-1">Diet Type Code</label>
                    <input type="number" name="diet_type" required class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none" placeholder="e.g., 1">
                </div>

                <!-- Smoking Status -->
                <div>
                    <label class="block text-sm font-semibold text-slate-700 mb-1">Smoking Status Code</label>
                    <input type="number" name="smoking_status" required class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none" placeholder="e.g., 0">
                </div>

                <!-- Alcohol Consumption -->
                <div>
                    <label class="block text-sm font-semibold text-slate-700 mb-1">Alcohol Consumption Code</label>
                    <input type="number" name="alcohol_consumption" required class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none" placeholder="e.g., 0">
                </div>

                <!-- Hours Sleep Per Night -->
                <div>
                    <label class="block text-sm font-semibold text-slate-700 mb-1">Hours Sleep Per Night</label>
                    <input type="step" step="0.1" name="hours_sleep_per_night" required class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none" placeholder="e.g., 7.5">
                </div>

                <!-- Stress Level -->
                <div>
                    <label class="block text-sm font-semibold text-slate-700 mb-1">Stress Level (1-10)</label>
                    <input type="number" name="stress_level" required class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none" placeholder="e.g., 4">
                </div>

                <!-- Fasting Blood Sugar -->
                <div>
                    <label class="block text-sm font-semibold text-slate-700 mb-1">Fasting Blood Sugar</label>
                    <input type="step" step="0.1" name="fasting_blood_sugar" required class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none" placeholder="e.g., 95">
                </div>

                <!-- HbA1c Level -->
                <div>
                    <label class="block text-sm font-semibold text-slate-700 mb-1">HbA1c Level</label>
                    <input type="step" step="0.1" name="hba1c_level" required class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none" placeholder="e.g., 5.6">
                </div>

                <!-- Blood Pressure Systolic -->
                <div>
                    <label class="block text-sm font-semibold text-slate-700 mb-1">BP Systolic</label>
                    <input type="number" name="blood_pressure_systolic" required class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none" placeholder="e.g., 120">
                </div>

                <!-- Blood Pressure Diastolic -->
                <div>
                    <label class="block text-sm font-semibold text-slate-700 mb-1">BP Diastolic</label>
                    <input type="number" name="blood_pressure_diastolic" required class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none" placeholder="e.g., 80">
                </div>

                <!-- Waist Circumference CM -->
                <div>
                    <label class="block text-sm font-semibold text-slate-700 mb-1">Waist Circumference (cm)</label>
                    <input type="step" step="0.1" name="waist_circumference_cm" required class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none" placeholder="e.g., 85">
                </div>

                <!-- Income Bracket -->
                <div>
                    <label class="block text-sm font-semibold text-slate-700 mb-1">Income Bracket Code</label>
                    <input type="number" name="income_bracket" required class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none" placeholder="e.g., 2">
                </div>

            </div>

            <!-- Submit Button -->
            <div class="pt-4">
                <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-lg transition duration-200 shadow-md">
                    Predict Result
                </button>
            </div>
        </form>

        <!-- Prediction Result Section -->
        {% if prediction_text is not none %}
        <div class="bg-slate-50 border-t border-slate-200 p-6 text-center">
            <h2 class="text-lg font-medium text-slate-600">Prediction Output:</h2>
            <div class="mt-2 inline-block px-6 py-3 rounded-xl text-xl font-bold {{ 'bg-red-100 text-red-700' if prediction_text == 1 else 'bg-green-100 text-green-700' }}">
                {{ "High Risk / Positive" if prediction_text == 1 else "Low Risk / Negative" }} (Class: {{ prediction_text }})
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction_text = None
    if request.method == 'POST':
        try:
            # Extract inputs in the exact order matching your model's n_features_in_
            features = [
                float(request.form['age']),
                float(request.form['gender']),
                float(request.form['city']),
                float(request.form['bmi']),
                float(request.form['family_history_diabetes']),
                float(request.form['physical_activity_level']),
                float(request.form['diet_type']),
                float(request.form['smoking_status']),
                float(request.form['alcohol_consumption']),
                float(request.form['hours_sleep_per_night']),
                float(request.form['stress_level']),
                float(request.form['fasting_blood_sugar']),
                float(request.form['hba1c_level']),
                float(request.form['blood_pressure_systolic']),
                float(request.form['blood_pressure_diastolic']),
                float(request.form['waist_circumference_cm']),
                float(request.form['income_bracket'])
            ]
            
            final_features = np.array([features])
            prediction = model.predict(final_features)
            prediction_text = int(prediction[0])
        except Exception as e:
            prediction_text = f"Error processing input: {str(e)}"

    return render_template_string(HTML_TEMPLATE, prediction_text=prediction_text)

if __name__ == '__main__':
    app.run(debug=True)
