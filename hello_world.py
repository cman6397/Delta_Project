from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/test')
def hello_test():
    return 'Hello test!'

if __name__ == '__main__':
    app.run()