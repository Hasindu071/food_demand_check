from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    # Render the index.html page
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Here you can add your prediction logic.
        # For example, let's assume you're running a machine learning model to predict demand.
        
        # Dummy prediction logic (replace with your model's prediction):
        predicted_demand = 1500  # Replace this with your actual prediction logic

        # Pass the prediction to the result page
        return render_template('result.html', prediction=predicted_demand)

@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
