from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import traceback

# Load API key from environment
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

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
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({"response": reply})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"response": "⚠️ Hops hit a snag. Please try again later."}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)
