from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    # Renders the index.html page
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # This is where you can handle the prediction logic.
        # For now, we'll just redirect to the result page as an example.
        
        # Example: You can process the form data here (if any) and then call your model for prediction
        
        return redirect(url_for('result'))

@app.route('/result')
def result():
    # Render a result page with a prediction message (modify this as per your need)
    prediction = "The predicted demand is 1500 units."  # Example result (replace with actual prediction logic)
    return render_template('result.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
