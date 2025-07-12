from flask import Flask, request, render_template, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

FLOWISE_API_URL = "https://limeutr-flowise.hf.space/api/v1/prediction/b53fd253-6e66-4b94-8b71-8792ee0337b7"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    # Enhance the user's question to get more focused responses
    if "city" in user_message.lower() or "cities" in user_message.lower():
        enhanced_message = f"{user_message} Please list only the names of the cities, separated by commas."
    elif "food" in user_message.lower() or "eat" in user_message.lower():
        enhanced_message = f"{user_message} Please list only the specific food names or dishes, separated by commas."
    elif "place" in user_message.lower() or "attraction" in user_message.lower():
        enhanced_message = f"{user_message} Please list only the names of the places or attractions, separated by commas."
    else:
        enhanced_message = f"{user_message} Please provide a brief, specific answer."
    
    # Call Flowise API
    try:
        response = requests.post(
            FLOWISE_API_URL,
            json={"question": enhanced_message}
        )
        response.raise_for_status()
        bot_response = response.json()
        
        # Extract and format the response text
        if isinstance(bot_response, dict):
            response_text = bot_response.get('text', '')
            if not response_text:
                response_text = str(bot_response)
        else:
            response_text = str(bot_response)
        
        # Clean up the response
        response_text = response_text.replace(" and ", ", ")  # Convert "and" to commas
        response_text = response_text.strip()  # Remove extra whitespace
        if response_text.endswith("."):  # Remove trailing period
            response_text = response_text[:-1]
        
        return jsonify({"response": response_text})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
