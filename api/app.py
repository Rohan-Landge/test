from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(_name_)

# Configure Gemini API
GENAI_API_KEY = "curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=GEMINI_API_KEY" \
-H 'Content-Type: application/json' \
-X POST \
-d '{
  "contents": [{
    "parts":[{"text": "Explain how AI works"}]
    }] # type: ignore  }'"

genai.configure(api_key=GENAI_API_KEY)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    query = req.get("queryResult", {}).get("queryText", "")

    if not query:
        return jsonify({"fulfillmentText": "I didn't understand the question."})

    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(query)
        answer = response.text if response.text else "I couldn't find an answer."

        return jsonify({"fulfillmentText": answer})

    except Exception as e:
        return jsonify({"fulfillmentText": "Sorry, an error occurred while fetching the response."})

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=8080)