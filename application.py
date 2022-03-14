from flask import Flask 

app = Flask(__name__)
app.secret_key = 'replace later'

@app.route( "/", method=['GET' , 'POST'])
def index(): 

    return 'I am here'

if __name__ == "__main__": 

    app.run(debug=True)  