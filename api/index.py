from flask import Flask, jsonify, request

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the Flask app deployed on Vercel!",
        "status": "success"
    })

# Example route
@app.route('/api/greet', methods=['GET'])
def greet():
    name = request.args.get('name', 'Guest')  # Get the 'name' query parameter
    return jsonify({
        "message": f"Hello, {name}!",
        "status": "success"
    })

# Health check route
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy"
    })

# Run locally for debugging
if __name__ == "__main__":
    app.run(debug=True)
