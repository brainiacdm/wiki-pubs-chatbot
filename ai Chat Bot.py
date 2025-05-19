# File: C:/Users/David/OneDrive/Desktop/ai Chat Bot.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import traceback

# Set OpenAI API key directly (temporary fix)
openai.api_key = os.environ.get("OPENAI_API_KEY")
print("API Key Loaded:", openai.api_key[:8] + "...")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)  # Fully enable CORS

SYSTEM_PROMPT = """
You are 'Hops the WikiPubs Road Trip Bot' – an Aussie pub-loving chatbot helping travellers discover outback pubs, vanlife tips, and pub road trips.
Be casual, helpful, and on-brand with the WikiPubs vibe.
"""

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({"response": reply})
    except Exception as e:
        traceback.print_exc()  # Show full error in terminal
        return jsonify({"response": "⚠️ Hops hit a snag. Please try again or check the server log."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

