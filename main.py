# -- INTERNO --
from future_population import estimate, gen_chart
# -- EXTERNO --
from flask import Flask, render_template, request, send_file

app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def index() -> str:
    year = 2030

    if request.method == 'POST':
        year = int(request.form['year'])
        
    img_url = f'/plot?year={year}'

    return render_template('index.html', year = year, img_url = img_url)


@app.route('/plot')
def plot():
    year = request.args.get('year', default = 2030, type = int)
    img = gen_chart(year)
    
    return send_file(img, mimetype='image/png')

