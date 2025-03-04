from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)  # ✅ Fixed the __name__ issue

# ✅ Correctly Assign the API Key
GENAI_API_KEY = "AIzaSyAnMEX2nSILcMLIbUG1LjKSrfsUFYcXDNQ"  # Replace with your actual API key

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

        # ✅ Handle response correctly
        if response and response.candidates:
            answer = response.candidates[0].content.parts[0].text
        else:
            answer = "I couldn't find an answer."

        return jsonify({"fulfillmentText": answer})

    except Exception as e:
        return jsonify({"fulfillmentText": f"Sorry, an error occurred: {str(e)}"})

# ✅ Fixed __name__ issue
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
