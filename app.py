import joblib
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# Load the trained prediction model (ensure the model is located at the specified path)
model = joblib.load("models/demand_prediction_model.pkl")

@app.route('/')
def index():
    return render_template('index.html')

# Route for the form page
@app.route('/form')
def form():
    return render_template('result.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Collect form data
    homepage = request.form['homepage']
    emailer = request.form['emailer']
    area = float(request.form['area'])
    cuisine = request.form['cuisine']
    city_code = request.form['city_code']
    region_code = request.form['region_code']
    category = request.form['category']

    # Convert categorical features into numerical representations (you can use encoding techniques like one-hot encoding)
    homepage_num = 1 if homepage == 'yes' else 0
    emailer_num = 1 if emailer == 'yes' else 0
    cuisine_map = {'Sri Lankan': 0, 'thai': 1, 'italian': 2, 'indian': 3, 'chinese': 4}
    cuisine_num = cuisine_map.get(cuisine, 0)
    category_map = {'beverages': 0, 'snacks': 1, 'main_dishes': 2, 'desserts': 3}
    category_num = category_map.get(category, 0)

    # Prepare the input data as a DataFrame (assuming the model accepts this structure)
    input_data = pd.DataFrame([[
        homepage_num, emailer_num, area, cuisine_num, city_code, region_code, category_num
    ]], columns=['homepage', 'emailer', 'area', 'cuisine', 'city_code', 'region_code', 'category'])

    # Make a prediction
    predicted_demand = model.predict(input_data)[0]

    # Render the result page with the prediction
    return render_template('result.html', prediction=predicted_demand)

if __name__ == 'main':
    app.run(debug=True)