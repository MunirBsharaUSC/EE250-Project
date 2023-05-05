from flask import Flask, request, jsonify
import grovepi

from grove_rgb_lcd import *

grovepi.set_bus("RPI_1")

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'message': 'Welcome'})

@app.route('/display',methods=['POST'])
def done():
    #x = request.get_data()
    fig = request.json

    # THESE ARE FOR TESTING FIX LATER.
    #print(x +"\n")
    print(fig+"\n")
    
    fig2 = fig.split(",")
    note = fig2[-1]
    freq = fig2[0]
    
    
    txt = "{:>7}HZ\n{:>4}"
    #TESTER
    #setText_norefresh(txt.format(343,"C"))

    setText_norefresh(txt.format(freq,note))    

    #print(fig) 
    return fig
    
    #return fig
if __name__ == "__main__":
    setText("")             # clears lcd
    app.run(host="0.0.0.0")