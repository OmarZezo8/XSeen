import os
import joblib
import numpy as np
from flask import Flask, render_template, jsonify, request
from groq import Client

app = Flask(__name__)

# Initialize Groq Client
# WARNING: Hardcoding API keys is a security risk. It is recommended to use environment variables instead.
try:
    api_key = 'API_KEY'
    client = Client(api_key=api_key)
except Exception as e:
    print(f"Failed to initialize Groq client: {e}")
    client = None

# Load ML Model
model = None
try:
    model = joblib.load('model.pkl')
    print("Model loaded successfully!")
    print(f"Model type: {type(model)}")
except Exception as e:
    print(f"Failed to load model: {e}")
    import traceback
    traceback.print_exc()

@app.route('/')
def index():
    return render_template('app.html')

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

@app.route('/classification')
def classification():
    return render_template('classification.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/xeno', methods=['POST'])
def handle_xeno():
    if not client:
        return jsonify({"error": "Groq client not initialized. Check API key."}), 500

    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        print(f"Sending message to Groq: {user_message}")
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are Xseen-net, an exoplanet AI assistant. Provide helpful, accurate information about exoplanets, detection methods, planetary characteristics, space missions, and astronomical discoveries. Be informative, engaging, and scientifically accurate. Format your responses using markdown, including headers, bold text, and lists where appropriate. Keep responses concise and clear."
                },
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
            model="meta-llama/llama-4-maverick-17b-128e-instruct"
        )
        response_text = chat_completion.choices[0].message.content
        print(f"Received response: {response_text}")
        return jsonify({"response": response_text})

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error calling Groq API: {e}")
        print(f"Full traceback: {error_details}")
        return jsonify({"error": f"Failed to get response from AI model: {str(e)}"}), 500

@app.route('/classify', methods=['POST'])
def classify():
    if not model:
        return jsonify({"error": "Model not loaded. Please restart the server and check logs."}), 500

    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data received. Please fill in all fields."}), 400
        
        # Extract features from the form
        try:
            features = [
                float(data.get('orbitalPeriod', 0)),
                float(data.get('impactParameter', 0)),
                float(data.get('transitDuration', 0)),
                float(data.get('transitDepth', 0)),
                float(data.get('planetRadius', 0)),
                float(data.get('signalToNoise', 0))
            ]
        except (ValueError, TypeError) as e:
            return jsonify({"error": f"Invalid input values. Please enter valid numbers. Error: {str(e)}"}), 400
        
        print(f"Classifying with features: {features}")
        print(f"Feature names: ['orbitalPeriod', 'planetRadius', 'impactParameter', 'transitDuration', 'transitDepth', 'signalToNoise']")
        
        # Make prediction
        features_array = np.array([features])
        print(f"Feature array shape: {features_array.shape}")
        prediction = model.predict(features_array)[0]
        print(f"Raw prediction: {prediction}")
        print(f"Prediction type: {type(prediction)}")
        
        # Check if model has predict_proba to see probabilities
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(features_array)[0]
            print(f"Prediction probabilities: {proba}")
        
        # Earth reference values for comparison
        earth_values = {
            'orbitalPeriod': 365.25,      # days
            'impactParameter': 0.0,        # central transit
            'transitDuration': 13.0,       # hours
            'transitDepth': 0.0084,        # percentage
            'planetRadius': 1.0,           # Earth radii
            'signalToNoise': 100.0         # typical good detection
        }
        
        # Calculate similarity to Earth for each property
        def calculate_similarity(value, earth_value):
            if earth_value == 0:
                return 100 if value == 0 else 0
            # Calculate percentage difference and convert to similarity
            diff_ratio = abs(value - earth_value) / earth_value
            # Cap the difference at 100% and convert to similarity percentage
            similarity = max(0, 100 - (diff_ratio * 100))
            return round(similarity, 1)
        
        earth_comparison = {
            'orbitalPeriod': {
                'value': float(data.get('orbitalPeriod', 0)),
                'earthValue': earth_values['orbitalPeriod'],
                'similarity': calculate_similarity(float(data.get('orbitalPeriod', 0)), earth_values['orbitalPeriod'])
            },
            'impactParameter': {
                'value': float(data.get('impactParameter', 0)),
                'earthValue': earth_values['impactParameter'],
                'similarity': calculate_similarity(float(data.get('impactParameter', 0)), earth_values['impactParameter']) if float(data.get('impactParameter', 0)) <= 1 else 0
            },
            'transitDuration': {
                'value': float(data.get('transitDuration', 0)),
                'earthValue': earth_values['transitDuration'],
                'similarity': calculate_similarity(float(data.get('transitDuration', 0)), earth_values['transitDuration'])
            },
            'transitDepth': {
                'value': float(data.get('transitDepth', 0)),
                'earthValue': earth_values['transitDepth'],
                'similarity': calculate_similarity(float(data.get('transitDepth', 0)), earth_values['transitDepth'])
            },
            'planetRadius': {
                'value': float(data.get('planetRadius', 0)),
                'earthValue': earth_values['planetRadius'],
                'similarity': calculate_similarity(float(data.get('planetRadius', 0)), earth_values['planetRadius'])
            },
            'signalToNoise': {
                'value': float(data.get('signalToNoise', 0)),
                'earthValue': earth_values['signalToNoise'],
                'similarity': calculate_similarity(float(data.get('signalToNoise', 0)), earth_values['signalToNoise'])
            }
        }
        
        # Interpret the prediction
        # 0 = Not an exoplanet, 1 = Candidate, 2 = Confirmed exoplanet
        if prediction == 0:
            result_type = "Not an Exoplanet"
            description = "The data suggests this is not an exoplanet."
        elif prediction == 1:
            result_type = "Exoplanet Candidate"
            description = "This object shows characteristics of a potential exoplanet and requires further observation."
        else:  # prediction == 2
            result_type = "Confirmed Exoplanet"
            description = "The data strongly indicates this is a confirmed exoplanet."
        
        response = {
            "prediction": int(prediction),
            "result_type": result_type,
            "description": description,
            "earth_comparison": earth_comparison
        }
        
        print(f"Classification result: {response}")
        return jsonify(response)
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in classification: {e}")
        print(f"Full traceback: {error_details}")
        return jsonify({"error": f"Classification failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
