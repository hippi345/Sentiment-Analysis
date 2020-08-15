# import the Flask class from the flask module
from flask import Flask, render_template, request
import sentimental_script
import matplotlib.pyplot as plt
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


# create the application object
app = Flask(__name__)


def makePlot(w):
    fig, ax1 = plt.subplots()
    ax1.bar(w.keys(), w.values())
    fig.autofmt_xdate()
    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)

    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String


# use decorators to link the function to a url
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        text = request.form['text']
        print(text)
        w = sentimental_script.run_script(text)
        sentiment = w[1]
        emotionCounts = w[0]
        return render_template("image.html", vibe=sentiment, counts=emotionCounts)

    elif request.method == "GET":
        print("this is a get method")
        return render_template('index.html')  # render home template


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
