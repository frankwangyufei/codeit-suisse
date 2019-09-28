from flask import Flask
from flask import request # <- added


app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route('/chessgame', methods=['POST'])
def chessgame():
    data = request.get_json(force=True)
    a = []
    size = 0
    kI = 1000
    kJ = 1000
    for char in range(len(data)):
        if (data[char] == '['):
            quoteCount = 0
            l = []
        if (data[char] == '\"' or data[char] == '\'' ):
            if (quoteCount%2 == 0):
                if (data[char+1] == 'K'):
                    kJ = quoteCount//2+1
                l.append(data[char+1])
            quoteCount = quoteCount+1
        if (data[char] == ']' and len(l) > 0):
            if (kJ != 1000 and kI == 1000):
                kI = size
            size = size+1
            a.append(l)  
            l = []
    kJ = kJ-1
    count = 0;
    s = [True,True,True,True,True,True,True,True]
    for x in range(1,size):
        #up
        if (s[0] and kI-x >= 0):
            if (a[kI-x][kJ] == 'X'):
                s[0] = False;
            else:
                count = count+1
        #down
        if (s[1] and kI+x < size):
            if (a[kI+x][kJ] == 'X'):
                s[1] = False;
            else:
                count = count+1
        #left
        if (s[2] and kJ-x >= 0):
            if (a[kI][kJ-x] == 'X'):
                s[2] = False;
            else:
                count = count+1
        #right
        if (s[3] and kJ+x < size):
            if (a[kI][kJ+x] == 'X'):
                s[3] = False;
            else:
                count = count+1
        #top-left
        if (s[4] and kI-x >= 0 and kJ-x >= 0):
            if (a[kI-x][kJ-x] == 'X'):
                s[4] = False;
            else:
                count = count+1
        #top-right
        if (s[5] and kI-x >= 0 and kJ+x < size):
            if (a[kI-x][kJ+x] == 'X'):
                s[5] = False;
            else:
                count = count+1
        #bottom-left
        if (s[6] and kI+x < size and kJ-x >= 0):
            if (a[kI+x][kJ-x] == 'X'):
                s[6] = False;
            else:
                count = count+1
        #top-right
        if (s[7] and kI+x < size and kJ+x < size):
            if (a[kI+x][kJ+x] == 'X'):
                s[7] = False;
            else:
                count = count+1
    return str(count)