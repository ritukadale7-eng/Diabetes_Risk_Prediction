<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SVC Model Prediction Portal</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>body { font-family: 'Inter', sans-serif; }</style>
</head>
<body class="bg-gradient-to-br from-slate-950 via-indigo-950 to-slate-900 min-h-screen text-gray-100 flex flex-col justify-between">

    <!-- Header -->
    <header class="w-full py-5 px-8 border-b border-white/10 backdrop-blur-md bg-white/5 flex justify-between items-center">
        <span class="text-lg font-bold bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent">ML Inference Portal</span>
        <span class="text-xs tracking-wider px-3 py-1 bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 rounded-full">SVM Classifier Active</span>
    </header>

    <!-- Form Container -->
    <main class="max-w-4xl mx-auto px-4 py-10 w-full">
        <div class="text-center mb-8">
            <h1 class="text-3xl font-extrabold tracking-tight mb-2">Health & Patient Analysis</h1>
            <p class="text-gray-400 text-sm">Provide the parameters below to evaluate through your deployed Support Vector Machine model.</p>
        </div>

        <div class="bg-white/10 backdrop-blur-xl border border-white/10 shadow-2xl rounded-2xl p-6 md:p-10">
            <form action="/predict" method="POST" class="grid grid-cols-1 md:grid-cols-2 gap-5">
                
                <div>
                    <label class="block text-xs uppercase tracking-wider text-gray-400 mb-1 font-semibold">Age</label>
                    <input type="number" step="any" name="age" required class="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition" placeholder="e.g. 40">
                </div>

                <div>
                    <label class="block text-xs uppercase tracking-wider text-gray-400 mb-1 font-semibold">Gender</label>
                    <select name="gender" class="w-full bg-slate-900 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition">
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                    </select>
                </div>

                <div>
                    <label class="block text-xs uppercase tracking-wider text-gray-400 mb-1 font-semibold">City Code</label>
                    <input type="number" step="any" name="city" required class="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition" placeholder="e.g. 1">
                </div>

                <div>
                    <label class="block text-xs uppercase tracking-wider text-gray-400 mb-1 font-semibold">BMI</label>
                    <input type="number" step="any" name="bmi" required class="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition" placeholder="e.g. 26.2">
                </div>

                <div>
                    <label class="block text-xs uppercase tracking-wider text-gray-400 mb-1 font-semibold">Family History Diabetes</label>
                    <select name="family_history_diabetes" class="w-full bg-slate-900 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition">
                        <option value="Yes">Yes</option>
                        <option value="No">No</option>
                    </select>
                </div>

                <div>
                    <label class="block text-xs uppercase tracking-wider text-gray-400 mb-1 font-semibold">Physical Activity Level</label>
                    <input type="number" step="any" name="physical_activity_level" required class="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition" placeholder="e.g. 2">
                </div>

                <div>
                    <label class="block text-xs uppercase tracking-wider text-gray-400 mb-1 font-semibold">Diet Type</label>
                    <input type="number" step="any" name="diet_type" required class="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition" placeholder="e.g. 1">
                </div>

                <div>
                    <label class="block text-xs uppercase tracking-wider text-gray-400 mb-1 font-semibold">Smoking Status</label>
                    <input type="number" step="any" name="smoking_status" required class="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition" placeholder="e.g. 0">
                </div>

                <div>
                    <label class="block text-xs uppercase tracking-wider text-gray-400 mb-1 font-semibold">Alcohol Consumption</label>
                    <input type="number" step="any" name="alcohol_consumption" required class="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition" placeholder="e.g. 0">
                </div>

                <div>
                    <label class="block text-xs uppercase tracking-wider text-gray-400 mb-1 font-semibold">Hours Sleep Per Night</label>
                    <input type="number" step="any" name="hours_sleep_per_night" required class="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition" placeholder="e.g. 7">
                </div>

                <div>
                    <label class="block text-xs uppercase tracking-wider text-gray-400 mb-1 font-semibold">Stress Level</label>
                    <input type="number" step="any" name="stress_level" required class="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition" placeholder="e.g. 3">
                </div>

                <div>
                    <label class="block text-xs uppercase tracking-wider text-gray-400 mb-1 font-semibold">Fasting Blood Sugar</label>
                    <input type="number" step="any" name="fasting_blood_sugar" required class="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition" placeholder="e.g. 100">
                </div>

                <div>
                    <label class="block text-xs uppercase tracking-wider text-gray-400 mb-1 font-semibold">HbA1c Level</label>
                    <input type="number" step="any" name="hba1c_level" required class="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition" placeholder="e.g. 5.7">
                </div>

                <div>
                    <label class="block text-xs uppercase tracking-wider text-gray-400 mb-1 font-semibold">Blood Pressure Systolic</label>
                    <input type="number" step="any" name="blood_pressure_systolic" required class="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition" placeholder="e.g. 120">
                </div>

                <div>
                    <label class="block text-xs uppercase tracking-wider text-gray-400 mb-1 font-semibold">Blood Pressure Diastolic</label>
                    <input type="number" step="any" name="blood_pressure_diastolic" required class="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition" placeholder="e.g. 80">
                </div>

                <div>
                    <label class="block text-xs uppercase tracking-wider text-gray-400 mb-1 font-semibold">Waist Circumference (cm)</label>
                    <input type="number" step="any" name="waist_circumference_cm" required class="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition" placeholder="e.g. 88">
                </div>

                <div class="md:col-span-2">
                    <label class="block text-xs uppercase tracking-wider text-gray-400 mb-1 font-semibold">Income Bracket</label>
                    <input type="number" step="any" name="income_bracket" required class="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition" placeholder="e.g. 2">
                </div>

                <div class="md:col-span-2 mt-2">
                    <button type="submit" class="w-full py-4 bg-gradient-to-r from-indigo-500 to-cyan-500 hover:from-indigo-600 hover:to-cyan-600 font-semibold text-white rounded-xl shadow-lg shadow-indigo-500/25 transition">
                        Run Model Prediction
                    </button>
                </div>
            </form>

            {% if prediction_text %}
            <div class="mt-8 p-5 bg-indigo-950/80 border border-indigo-500/30 rounded-xl text-center">
                <p class="text-xs text-indigo-300 font-semibold uppercase tracking-wider mb-1">Output Result</p>
                <p class="text-2xl font-bold text-white">{{ prediction_text }}</p>
            </div>
            {% endif %}
        </div>
    </main>

    <footer class="w-full py-4 text-center text-xs text-gray-500 border-t border-white/5">
        Deployed on Render via Flask
    </footer>
</body>
</html>
