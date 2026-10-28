import os
import pickle
import warnings
 
import pandas as pd
from flask import Flask, render_template_string, request
 
warnings.filterwarnings("ignore")
 
app = Flask(__name__)
 
# --------------------------------------------------------------------------
# Load model
# --------------------------------------------------------------------------
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "svc.pkl")
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)
 
FEATURES = list(model.feature_names_in_)   # exact column order the model expects
 
# --------------------------------------------------------------------------
# What each predicted class means (alphabetical label-encoding assumed:
# 0 = Diabetes, 1 = Normal, 2 = Prediabetes). EDIT here if your labels differ.
# --------------------------------------------------------------------------
CLASS_INFO = {
    0: {"label": "Diabetes", "icon": "🩸", "bg": "#ffd1dc", "edge": "#f4a3b8",
        "msg": "The model places this profile in the diabetes group. Please confirm with a lab test and a doctor."},
    1: {"label": "Normal", "icon": "🌿", "bg": "#c9f2dd", "edge": "#8fdcb4",
        "msg": "The model places this profile in the normal group. Keep up the healthy habits."},
    2: {"label": "Prediabetes", "icon": "🌤️", "bg": "#ffe8b8", "edge": "#f6cf7f",
        "msg": "The model places this profile in the prediabetes group. Early lifestyle changes can make a big difference."},
}
METER_ORDER = [1, 2, 0]   # Normal -> Prediabetes -> Diabetes
 
# --------------------------------------------------------------------------
# Label-encoded categories. Position in each list = number sent to the model.
# The pickle stores numbers only, so rename these to match YOUR encoders.
# --------------------------------------------------------------------------
GENDER   = ["Female", "Male", "Other"]
YES_NO   = ["No", "Yes"]
ACTIVITY = ["High", "Low", "Moderate"]
SMOKING  = ["Current", "Former", "Never"]
INCOME   = ["High", "Low", "Medium"]
CITY     = [f"City #{i}" for i in range(18)]
DIET     = [f"Diet type #{i}" for i in range(4)]
ALCOHOL  = [f"Alcohol level #{i}" for i in range(3)]
 
 
def opts(lst):
    return list(enumerate(lst))
 
 
# --------------------------------------------------------------------------
# Form definition
# --------------------------------------------------------------------------
SECTIONS = [
    {"title": "🧑 Personal Details", "fields": [
        {"name": "age", "label": "Age", "kind": "range", "min": 18, "max": 80, "step": 1, "default": 45},
        {"name": "gender", "label": "Gender", "kind": "select", "options": opts(GENDER), "default": 0},
        {"name": "city", "label": "City", "kind": "select", "options": opts(CITY), "default": 0},
        {"name": "income_bracket", "label": "Income Bracket", "kind": "select", "options": opts(INCOME), "default": 2},
        {"name": "family_history_diabetes", "label": "Family History of Diabetes", "kind": "select",
         "options": opts(YES_NO), "default": 0},
    ]},
    {"title": "🥗 Lifestyle", "fields": [
        {"name": "physical_activity_level", "label": "Physical Activity", "kind": "select",
         "options": opts(ACTIVITY), "default": 2},
        {"name": "diet_type", "label": "Diet Type", "kind": "select", "options": opts(DIET), "default": 0},
        {"name": "smoking_status", "label": "Smoking", "kind": "select", "options": opts(SMOKING), "default": 2},
        {"name": "alcohol_consumption", "label": "Alcohol Consumption", "kind": "select",
         "options": opts(ALCOHOL), "default": 0},
        {"name": "hours_sleep_per_night", "label": "Sleep (hours / night)", "kind": "range",
         "min": 3, "max": 12, "step": 0.5, "default": 7},
        {"name": "stress_level", "label": "Stress Level (1-10)", "kind": "range",
         "min": 1, "max": 10, "step": 1, "default": 5},
    ]},
    {"title": "🩺 Body & Blood Tests", "fields": [
        {"name": "bmi", "label": "BMI", "kind": "range", "min": 15, "max": 45, "step": 0.1, "default": 24},
        {"name": "waist_circumference_cm", "label": "Waist Circumference (cm)", "kind": "range",
         "min": 60, "max": 150, "step": 0.5, "default": 90},
        {"name": "fasting_blood_sugar", "label": "Fasting Blood Sugar (mg/dL)", "kind": "range",
         "min": 60, "max": 300, "step": 1, "default": 95},
        {"name": "hba1c_level", "label": "HbA1c (%)", "kind": "range",
         "min": 4, "max": 12, "step": 0.1, "default": 5.3},
        {"name": "blood_pressure_systolic", "label": "Blood Pressure - Systolic", "kind": "range",
         "min": 90, "max": 200, "step": 1, "default": 120},
        {"name": "blood_pressure_diastolic", "label": "Blood Pressure - Diastolic", "kind": "range",
         "min": 50, "max": 120, "step": 1, "default": 80},
    ]},
]
 
 
# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def reference_chips(v: dict) -> list:
    """General clinical reference ranges (independent of the model)."""
    g, a = v["fasting_blood_sugar"], v["hba1c_level"]
    bmi, sbp, dbp = v["bmi"], v["blood_pressure_systolic"], v["blood_pressure_diastolic"]
 
    def level(val, mid, high):
        return 0 if val < mid else (1 if val < high else 2)
 
    tone = [("Normal", "#c9f2dd"), ("Elevated", "#ffe8b8"), ("High", "#ffd1dc")]
    g_l, a_l = level(g, 100, 126), level(a, 5.7, 6.5)
    bmi_l = 0 if bmi < 25 else (1 if bmi < 30 else 2)
    bp_l = 0 if (sbp < 130 and dbp < 85) else (1 if (sbp < 140 and dbp < 90) else 2)
    return [
        {"name": "Fasting glucose", "val": f"{g:g} mg/dL", "text": tone[g_l][0], "bg": tone[g_l][1]},
        {"name": "HbA1c", "val": f"{a:g}%", "text": tone[a_l][0], "bg": tone[a_l][1]},
        {"name": "BMI", "val": f"{bmi:g}", "text": tone[bmi_l][0], "bg": tone[bmi_l][1]},
        {"name": "Blood pressure", "val": f"{sbp:g}/{dbp:g}", "text": tone[bp_l][0], "bg": tone[bp_l][1]},
    ]
 
 
def build_tips(v: dict) -> list:
    tips = []
    if v["bmi"] >= 25:
        tips.append("⚖️ A BMI above 25 raises risk, so gradual weight management can help.")
    if ACTIVITY[int(v["physical_activity_level"])] == "Low":
        tips.append("🚶 Aim for about 150 minutes of moderate activity each week.")
    if v["hours_sleep_per_night"] < 6:
        tips.append("😴 Short sleep affects blood sugar, so aim for 7 to 8 hours.")
    if v["stress_level"] >= 7:
        tips.append("🧘 High stress can raise glucose; try relaxation, walks or breathing exercises.")
    if int(v["family_history_diabetes"]) == 1:
        tips.append("🧬 With a family history, regular screening is especially worthwhile.")
    if v["blood_pressure_systolic"] >= 140 or v["blood_pressure_diastolic"] >= 90:
        tips.append("❤️ Blood pressure is high, so it is worth discussing with a doctor.")
    if SMOKING[int(v["smoking_status"])] == "Current":
        tips.append("🚭 Quitting smoking lowers diabetes and heart risk.")
    if not tips:
        tips.append("✅ Your inputs look healthy. Keep up regular check-ups.")
    return tips[:4]
 
 
# --------------------------------------------------------------------------
# HTML template (pastel theme)
# --------------------------------------------------------------------------
TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Diabetes Risk Predictor</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
  :root{
    --lav:#d9ccff; --pink:#ffd1dc; --mint:#c9f2dd; --sky:#c6e4ff; --peach:#ffe3c6; --butter:#fff1b8;
    --ink:#3b3355; --muted:#7a7396; --card:rgba(255,255,255,.72); --line:rgba(120,100,170,.18);
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{
    font-family:'Nunito',system-ui,sans-serif;color:var(--ink);min-height:100vh;padding:34px 16px 60px;
    background:
      radial-gradient(700px 420px at 0% 0%, var(--pink), transparent 65%),
      radial-gradient(700px 460px at 100% 0%, var(--sky), transparent 65%),
      radial-gradient(800px 520px at 50% 110%, var(--mint), transparent 65%),
      linear-gradient(160deg,#fbf7ff,#f1f7ff);
    background-attachment:fixed;
  }
  .wrap{max-width:1100px;margin:0 auto}
  header{text-align:center;margin-bottom:30px}
  .badge{display:inline-block;padding:6px 16px;border-radius:999px;font-size:12px;font-weight:800;
    letter-spacing:.08em;text-transform:uppercase;color:#6b4fb3;background:var(--lav);
    border:1px solid rgba(107,79,179,.2)}
  h1{font-size:clamp(28px,5vw,44px);font-weight:800;margin:14px 0 8px;color:var(--ink)}
  h1 span{background:linear-gradient(90deg,#b39cf5,#f49ac1);-webkit-background-clip:text;
    background-clip:text;color:transparent}
  header p{color:var(--muted);max-width:580px;margin:0 auto;font-size:15px}
 
  /* result */
  .result{margin-bottom:28px;padding:30px;border-radius:26px;background:var(--rbg);
    border:2px solid var(--redge);box-shadow:0 18px 50px rgba(120,100,170,.18);animation:pop .5s ease}
  @keyframes pop{from{opacity:0;transform:translateY(14px) scale(.98)}to{opacity:1;transform:none}}
  .top{display:flex;gap:22px;align-items:center;flex-wrap:wrap;justify-content:center;text-align:left}
  .big-icon{font-size:64px;width:110px;height:110px;border-radius:50%;display:flex;align-items:center;
    justify-content:center;background:rgba(255,255,255,.7);box-shadow:0 8px 24px rgba(120,100,170,.18)}
  .top .txt{max-width:480px}
  .top .small{font-size:12px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
  .top h2{font-size:34px;font-weight:800;margin:2px 0 6px}
  .top p{font-size:14px;color:#4d4568}
 
  .meter{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;max-width:520px;margin:24px auto 0}
  .seg{padding:10px 6px;border-radius:14px;text-align:center;font-size:13px;font-weight:700;
    background:rgba(255,255,255,.55);color:var(--muted);border:2px solid transparent;transition:.3s}
  .seg.on{background:#fff;color:var(--ink);border-color:var(--ink);transform:translateY(-3px);
    box-shadow:0 8px 18px rgba(59,51,85,.18)}
 
  .sub{font-size:13px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);
    margin:26px 0 10px}
  .chips{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px}
  .chip{padding:12px 14px;border-radius:16px;border:1px solid var(--line)}
  .chip .cn{font-size:12px;color:#5d5578;font-weight:600}
  .chip .cv{font-size:18px;font-weight:800;margin:2px 0}
  .chip .ct{font-size:12px;font-weight:700;color:#4d4568}
  .note{font-size:12px;color:var(--muted);margin-top:8px}
  .tips{list-style:none;display:grid;gap:8px}
  .tips li{font-size:13.5px;padding:10px 14px;border-radius:14px;background:rgba(255,255,255,.7);
    border:1px solid var(--line)}
 
  .error{background:#ffd9d9;border:1px solid #f3a6a6;padding:14px 18px;border-radius:14px;margin-bottom:20px}
 
  /* form */
  form{display:grid;gap:20px}
  .grid3{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:20px}
  .card{background:var(--card);border:1px solid var(--line);border-radius:22px;padding:22px;
    box-shadow:0 10px 30px rgba(120,100,170,.10);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px)}
  .card:nth-child(1){border-top:6px solid var(--lav)}
  .card:nth-child(2){border-top:6px solid var(--mint)}
  .card:nth-child(3){border-top:6px solid var(--pink)}
  .card h2{font-size:17px;margin-bottom:16px;padding-bottom:10px;border-bottom:1px solid var(--line)}
  .field{margin-bottom:16px}.field:last-child{margin-bottom:0}
  label{display:flex;justify-content:space-between;font-size:13px;font-weight:700;color:var(--muted);margin-bottom:7px}
  label output{color:#7a5fc4;font-weight:800;background:var(--lav);padding:0 9px;border-radius:99px}
  select{width:100%;padding:11px 12px;border-radius:12px;font:inherit;color:var(--ink);font-weight:600;
    background:#fff;border:1px solid #d9d2ee;outline:none;transition:.2s}
  select:focus{border-color:#b39cf5;box-shadow:0 0 0 4px rgba(179,156,245,.3)}
  input[type=range]{width:100%;-webkit-appearance:none;height:8px;border-radius:99px;outline:none;
    background:linear-gradient(90deg,var(--lav),var(--pink))}
  input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:22px;height:22px;border-radius:50%;
    background:#fff;border:4px solid #b39cf5;cursor:pointer;box-shadow:0 3px 8px rgba(120,100,170,.35)}
  input[type=range]::-moz-range-thumb{width:16px;height:16px;border-radius:50%;background:#fff;
    border:4px solid #b39cf5;cursor:pointer}
 
  .actions{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:6px}
  button,.reset{padding:15px 38px;border-radius:16px;border:0;font:inherit;font-weight:800;font-size:16px;
    cursor:pointer;transition:.2s;text-decoration:none;display:inline-block}
  button{color:var(--ink);background:linear-gradient(90deg,#c9b8ff,#ffc1d6);
    box-shadow:0 10px 26px rgba(179,156,245,.45)}
  button:hover{transform:translateY(-2px);box-shadow:0 14px 32px rgba(244,154,193,.5)}
  .reset{color:var(--ink);background:#fff;border:1px solid #d9d2ee}
  .reset:hover{background:var(--butter)}
  footer{text-align:center;color:var(--muted);font-size:12px;margin:34px auto 0;max-width:640px}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <span class="badge">Support Vector Machine · Health AI</span>
    <h1>Diabetes <span>Risk Predictor</span></h1>
    <p>Enter lifestyle details and health measurements to see which group the model places you in.</p>
  </header>
 
  {% if error %}<div class="error">⚠️ {{ error }}</div>{% endif %}
 
  {% if result %}
  <div class="result" style="--rbg: {{ result.bg }}; --redge: {{ result.edge }}">
    <div class="top">
      <div class="big-icon">{{ result.icon }}</div>
      <div class="txt">
        <div class="small">Model prediction</div>
        <h2>{{ result.label }}</h2>
        <p>{{ result.msg }}</p>
      </div>
    </div>
 
    <div class="meter">
      {% for m in result.meter %}<div class="seg {{ 'on' if m.on }}">{{ m.label }}</div>{% endfor %}
    </div>
 
    <div class="sub">Standard clinical reference</div>
    <div class="chips">
      {% for c in result.chips %}
      <div class="chip" style="background:{{ c.bg }}">
        <div class="cn">{{ c.name }}</div><div class="cv">{{ c.val }}</div><div class="ct">{{ c.text }}</div>
      </div>
      {% endfor %}
    </div>
    <p class="note">These ranges are general guidelines and are independent of the model's prediction.</p>
 
    <div class="sub">Helpful pointers</div>
    <ul class="tips">{% for t in result.tips %}<li>{{ t }}</li>{% endfor %}</ul>
  </div>
  {% endif %}
 
  <form method="POST" action="/">
    <div class="grid3">
    {% for s in sections %}
      <div class="card">
        <h2>{{ s.title }}</h2>
        {% for f in s.fields %}
        <div class="field">
          {% set val = values.get(f.name, f.default) %}
          {% if f.kind == 'select' %}
            <label for="{{ f.name }}">{{ f.label }}</label>
            <select id="{{ f.name }}" name="{{ f.name }}">
              {% for code, text in f.options %}
              <option value="{{ code }}" {{ 'selected' if code|string == val|string }}>{{ text }}</option>
              {% endfor %}
            </select>
          {% else %}
            <label for="{{ f.name }}">{{ f.label }}<output id="o_{{ f.name }}">{{ val }}</output></label>
            <input type="range" id="{{ f.name }}" name="{{ f.name }}" min="{{ f.min }}" max="{{ f.max }}"
                   step="{{ f.step }}" value="{{ val }}"
                   oninput="document.getElementById('o_{{ f.name }}').textContent=this.value">
          {% endif %}
        </div>
        {% endfor %}
      </div>
    {% endfor %}
    </div>
    <div class="actions">
      <button type="submit">✨ Predict My Risk</button>
      <a class="reset" href="/">↺ Reset</a>
    </div>
  </form>
  <footer>Built with Flask &amp; scikit-learn. This tool is for learning and awareness only and is not
    medical advice. Please consult a qualified doctor for diagnosis.</footer>
</div>
</body>
</html>
"""
 
 
# --------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    result, error, values = None, None, {}
 
    if request.method == "POST":
        values = request.form.to_dict()
        try:
            v = {name: float(values[name]) for name in FEATURES}
            X = pd.DataFrame([v])[FEATURES]
 
            pred = int(model.predict(X)[0])
            info = CLASS_INFO.get(pred, {"label": f"Class {pred}", "icon": "🔮", "bg": "#e6defa",
                                         "edge": "#c9b8ff", "msg": ""})
            result = {
                **info,
                "meter": [{"label": CLASS_INFO[c]["label"], "on": c == pred} for c in METER_ORDER],
                "chips": reference_chips(v),
                "tips": build_tips(v),
            }
        except (KeyError, ValueError) as e:
            error = f"Please fill every field with valid values ({e})."
        except Exception as e:  # noqa: BLE001
            error = f"Prediction failed: {e}"
 
    return render_template_string(
        TEMPLATE, sections=SECTIONS, values=values, result=result, error=error
    )
 
 
if __name__ == "__main__":
    app.run(debug=True)
