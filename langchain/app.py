from flask import Flask, render_template, request, jsonify
from new import main  # Import RUBY's logic

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask_ruby', methods=['POST'])
def ask_ruby():
    user_query = request.json.get('query')
    bot_response = main(user_query)  # Fetch RUBY's response
    return jsonify({"answer": bot_response["answer"]})

if __name__ == '__main__':
    app.run(debug=True)
