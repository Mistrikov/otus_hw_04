from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aboutus/')
def aboutus():
    return render_template('about.html')

@app.route('/post/<int:id>/')
def post_by_id(id):
    '''message = {
        'id': id,
        'title': 'Треугольник',
        'text': 'Треугольник - это геометрическая фигура у которой три стороны и три угла'
    }'''
    return render_template(f'post{id}.html')

if __name__ == '__main__':
    app.run(host='10.8.0.9', port=5000)