from flask import Flask

app = Flask(__name__)

@app.route('/')  # Ye root route define karega
def home():
    return "Flask is working!"

if __name__ == '__main__':
    app.run(debug=True)
