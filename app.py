import joblib
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# Load the trained prediction model (ensure the model path is correct)
model = joblib.load("models/demand_prediction_model.pkl")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Collect form data
        week = int(request.form['week'])
        city_code = int(request.form['city_code'])
        region_code = int(request.form['region_code'])
        area = float(request.form['area'])
        category = request.form['category']
        checkout_price = float(request.form['checkout_price'])
        base_price = float(request.form['base_price'])
        emailer = request.form['emailer']
        homepage = request.form['homepage']
        center = request.form['center']
        cuisine = request.form['cuisine']

        # Calculate price difference
        price_difference = checkout_price - base_price

        # Convert categorical features into numerical representations
        homepage_num = 1 if homepage.lower() == 'yes' else 0
        emailer_num = 1 if emailer.lower() == 'yes' else 0

        # Map the category to binary code
        category_mapping = {
            "beverages": "0001",
            "rice bowl": "0010",
            "starters": "0011",
            "pasta": "0100",
            "sandwich": "0101",
            "biryani": "0110",
            "extras": "0111",
            "pizza": "1000",
            "seafood": "1001",
            "other snacks": "1010",
            "desert": "1011",
            "salad": "1100",
            "fish": "1101",
            "soup": "1110"
        }

        # Get the binary code for the selected category
        binary_code = category_mapping.get(category.lower(), "0000")  # Default to "0000" if not found

        # Decode the binary code into category columns
        category_0 = int(binary_code[0])
        category_1 = int(binary_code[1])
        category_2 = int(binary_code[2])
        category_3 = int(binary_code[3])

        # Get the cuisine type
        Thai = 1 if cuisine.lower() == 'thai' else 0
        Italian = 1 if cuisine.lower() == 'italian' else 0
        Indian = 1 if cuisine.lower() == 'indian' else 0
        Continental = 1 if cuisine.lower() == 'continental' else 0

        # Get the center type
        type_A = 1 if center == 'TYPE_A' else 0
        type_B = 1 if center == 'TYPE_B' else 0
        type_C = 1 if center == 'TYPE_C' else 0

        # Prepare the input data as a DataFrame
        input_data = pd.DataFrame([[
            week, city_code, region_code, area, category_0, category_1, category_2, category_3,
            checkout_price, base_price, emailer_num, homepage_num,
            type_A, type_B, type_C, Continental, Indian, Italian, Thai, price_difference
        ]],
            columns=[
                'week', 'city_code', 'region_code', 'op_area', 'category_0', 'category_1',
                'category_2', 'category_3', 'checkout_price', 'base_price', 'emailer_for_promotion',
                'homepage_featured', 'center_type_TYPE_A', 'center_type_TYPE_B', 'center_type_TYPE_C',
                'cuisine_Continental', 'cuisine_Indian', 'cuisine_Italian', 'cuisine_Thai', 'price_difference'
            ])

        # Output the DataFrame (for debugging purposes)
        print(input_data)

        # Make a prediction
        predicted_demand = model.predict(input_data)[0]

        # Render the result page with the prediction
        return render_template('form.html', prediction=predicted_demand)

    except Exception as e:
        return f"An error occurred: {str(e)}"

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
