from flask import Flask, request, jsonify
import os

try:
    import openai
except ImportError:
    openai = None

app = Flask(__name__)

# Configure OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY", "your_openai_api_key_here")
if openai:
    openai.api_key = openai_api_key

@app.route('/generate_message', methods=['POST'])
def generate_message():
    if not openai:
        return jsonify({"error": "OpenAI library is not installed. Please install it using 'pip install openai'."}), 500
    
    try:
        # Get user input from the request
        user_data = request.json
        user_prompt = user_data.get('prompt', '')

        if not user_prompt:
            return jsonify({"error": "Missing prompt"}), 400

        # Call the OpenAI API to generate a response
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "אתה עוזר הומוריסטי ומחושב, שכותב הודעות חכמות, יצירתיות ומגניבות בעברית."},
                {"role": "user", "content": user_prompt}
            ]
        )

        # Extract the generated message
        generated_message = response['choices'][0]['message']['content']

        return jsonify({"message": generated_message}), 200

    except openai.error.OpenAIError as api_error:
        return jsonify({"error": f"OpenAI API error: {api_error}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500

if __name__ == '__main__':
    # Specify the host and port explicitly to avoid environment conflicts
    try:
        port = os.getenv("PORT", 5000)
        if not port or not port.isdigit():
            raise ValueError("PORT environment variable must be a valid integer.")

        port = int(port)
        app.run(host="0.0.0.0", port=port, debug=False)
    except ValueError as ve:
        print(f"Configuration error: {ve}")
    except Exception as e:
        print(f"Failed to start the server: {e}")
