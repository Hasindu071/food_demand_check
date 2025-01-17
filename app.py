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
    return render_template('form.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Collect form data
    week = request.form['week']
    city_code = request.form['city_code']
    region_code = request.form['region_code']
    area = float(request.form['area'])
    category = request.form['category']
    checkout_price = request.form['checkout_price']
    base_price = request.form['base_price']
    emailer = request.form['emailer']
    homepage = request.form['homepage']
    center = float(request.form['center'])
    cuisine = request.form['cuisine']

    price_diference  = (checkout_price - base_price)

    # Convert categorical features into numerical representations (you can use encoding techniques like one-hot encoding)
    homepage_num = 1 if homepage == 'yes' else 0
    emailer_num = 1 if emailer == 'yes' else 0

    # get the cuisine type
    Thai = 0
    Italian = 0
    Indian = 0
    Continental = 0

    if cuisine == 'Thai':
        Thai = 1
    elif cuisine == 'Italian':
        Italian = 1
    elif cuisine == 'Indian':
        Indian = 1
    elif cuisine == 'Continental':
        Continental = 1

    # get the center type
    type_A = 0
    type_B = 0
    type_C = 0

    if center == 'TYPE_A':
        type_A = 1
    elif center == 'TYPE_B':
        type_B = 1
    elif center == 'TYPE_C':
        type_C = 1

    # Prepare the input data as a DataFrame (assuming the model accepts this structure)
    input_data = pd.DataFrame([[
        week, city_code,region_code, area,checkout_price,base_price, emailer_num,homepage_num,
        type_A,type_B,type_C ,Continental, Indian, Italian , Thai , price_diference
    ]],
    columns=['week', 'city_code', 'region_code', 'op_area', 'category_0', 'category_1',
    'category_2', 'category_3', 'checkout_price', 'base_price', 'emailer_for_promotion',
    'homepage_featured', 'center_type_TYPE_A', 'center_type_TYPE_B', 'center_type_TYPE_C',
    'cuisine_Continental', 'cuisine_Indian', 'cuisine_Italian', 'cuisine_Thai', 'price_difference']
    )

    # Make a prediction
    predicted_demand = model.predict(input_data)[0]

    # Render the result page with the prediction
    return render_template('form.html', prediction=predicted_demand)

if __name__ == 'main':
    app.run(debug=True)