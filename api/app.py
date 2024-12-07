import joblib
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# Load the trained prediction model (ensure the model path is correct)
MODEL_PATH = "models/demand_prediction_model.pkl"
try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    raise FileNotFoundError(f"Model file not found at '{MODEL_PATH}'. Ensure the file exists.")

@app.route('/')
def index():
    """Home route to display the main form."""
    return render_template('index.html')

@app.route('/form')
def form():
    """Route to display a separate form page (if needed)."""
    return render_template('form.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle the prediction logic and display the results."""
    try:
        # Collect form data
        homepage = request.form.get('homepage')
        emailer = request.form.get('emailer')
        area = float(request.form.get('area', 0))
        cuisine = request.form.get('cuisine')
        city_code = int(request.form.get('city_code', 0))
        region_code = int(request.form.get('region_code', 0))
        category = request.form.get('category')

        # Map categorical values to numerical representations
        homepage_num = 1 if homepage == 'yes' else 0
        emailer_num = 1 if emailer == 'yes' else 0
        cuisine_map = {'Sri Lankan': 0, 'thai': 1, 'italian': 2, 'indian': 3, 'chinese': 4}
        cuisine_num = cuisine_map.get(cuisine, 0)
        category_map = {'beverages': 0, 'snacks': 1, 'main_dishes': 2, 'desserts': 3}
        category_num = category_map.get(category, 0)

        # Prepare input data as a DataFrame
        input_data = pd.DataFrame([[
            homepage_num, emailer_num, area, cuisine_num, city_code, region_code, category_num
        ]], columns=['homepage', 'emailer', 'area', 'cuisine', 'city_code', 'region_code', 'category'])

        # Make a prediction
        predicted_demand = model.predict(input_data)[0]

        # Render the result page with the prediction
        return render_template('result.html', prediction=predicted_demand)

    except Exception as e:
        # Handle errors and display a meaningful message
        return render_template('result.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
