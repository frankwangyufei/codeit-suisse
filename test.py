from flask import Flask
from flask import request # <- added
from flask import Response
import json
import requests
from string import punctuation
import random


app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route('/chessgame', methods=['POST'])
def chessgame():
    data = request.get_json(force=True)
    data = format(data)
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






    

def dep_resolve(node, resolved, unresolved):
   unresolved.append(node)
   for edge in node.edges:
      if edge not in resolved:
         if edge in unresolved:
            return
         dep_resolve(edge, resolved, unresolved)
   resolved.append(node)
   unresolved.remove(node)

class Node:
  def __init__(self, name):
    self.name = name
    self.edges = [] 

  def addEdge(self, node):
        self.edges.append(node)


def dfs(graph, start, end):
    fringe = [(start, [])]
    while fringe:
        state, path = fringe.pop()
        if path and state == end:
            yield path
            continue
        for next_state in graph[state]:
            if next_state in path:
                continue
            fringe.append((next_state, path+[next_state]))

def remove_node(node):
  if node.name in nodes:
    del nodes[node.name]
  for (key, item) in nodes.items():
    try:
      item.edges.remove(node)
    except ValueError:
      pass

nodes = {}  

@app.route('/generateSequence', methods=['POST'])
def gs():
    global nodes
    nodes = {}
    input = request.get_json(force=True)
    print(input)

    for module in input['modules']:
      nodes[module] = Node(module)
    extra = []
    remove = []
    for pair in input['dependencyPairs']:
      if pair['dependentOn'] == pair['dependee']:
        continue
      if pair['dependee'] not in nodes:
        nodes[pair['dependee']] = Node(pair['dependee']) 
        extra.append(pair['dependee'])
      if pair['dependentOn'] not in nodes:
        nodes[pair['dependentOn']] = Node(pair['dependentOn']) 
        extra.append(pair['dependentOn'])
      nodes[pair['dependee']].addEdge(nodes[pair['dependentOn']])
      # if pair['dependee'] == pair['dependentOn']:
      #   remove.append(nodes[pair['dependee']])
    for item in remove:
        remove_node(item)
    graph = {}

    for node in nodes.values():
      graph[node] = node.edges
    cycles = [[node]+ path for node in graph for path in dfs(graph, node, node)]

    for cycle in cycles:
      for node in cycle:
        remove_node(node)


    resolved = []
    unresolved = []
    for node in nodes.values():
      if node not in resolved:
        dep_resolve(node, resolved, unresolved)
    resolved = [item.name for item in resolved]
    for item in extra:
        try:
            resolved.remove(item)
        except ValueError:
            pass
    return format(resolved)



def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)

@app.route('/sentiment-analysis', methods=['POST'])
def sa():

    input = request.get_json(force=True)
    headers = {
        'api-key': 'f96743df-2e48-4e7b-9532-b20b1242dece',
    }
    result = {}
    result['response'] = []
    for review in input['reviews']:
      review = strip_punctuation(review[:500])
      review = review + '.'
      print(review)
      files = {
         'text': (None, review),
      }
      response = requests.post('https://api.deepai.org/api/sentiment-analysis', headers=headers, files=files)
      json = response.json()['output']

      if json[0] == "Verypositive" or json[0] == "Positive" or json[0] == "Neutral":
        result['response'].append("positive")
      else:
        result['response'].append("negative")
    return result


@app.route('/gun-control', methods=['POST'])
def gunControl():
    types = request.get_json(force=True)
    print(types)
    print(types['fuel'])
    y = len(types['grid'])
    x = len(types['grid'][0])
    print(x,y)
    gun = []
    gas = []
    sol = []
    curr = 0;
    visited = [0]*(x*y);
    queue = []
    queue.append(curr)
    visited[curr] = 1;
    while queue:
        curr = queue.pop(0)
        dead = True
        #print("curr",curr, curr//x, curr%x)
        #up
        if (curr-x >= 0 and visited[curr-x] == False and \
            types['grid'][curr//x-1][curr%x] == 'O'):
            queue.append(curr-x);
            visited[curr-x] = visited[curr]+1
            dead = False
            #print("u",types['grid'][curr//x-1][curr%x])
        #down
        if (curr+x < x*y and visited[curr+x] == False and \
            types['grid'][curr//x+1][curr%x] == 'O'):
            queue.append(curr+x);
            visited[curr+x] = visited[curr]+1
            dead = False
            #print("d",types['grid'][curr//x+1][curr%x])
        #left
        if (curr%x > 0 and visited[curr-1] == False and \
            types['grid'][curr//x][curr%x-1] == 'O'):
            queue.append(curr-1);
            visited[curr-1] = visited[curr]+1
            dead = False
            #print("l",types['grid'][curr//x][curr%x-1])
        #right
        if (curr%x < x-1 and visited[curr+1] == False and \
            types['grid'][curr//x][curr%x+1] == 'O'):
            queue.append(curr+1);
            visited[curr+1] = visited[curr]+1
            dead = False
            #print("r",types['grid'][curr//x][curr%x+1])
        if dead:
            gun.append(curr)
            gas.append(visited[curr])
            sol.append(False)
    #print(visited)
    print(gun)
    print(gas)
    #print(len(gun))
    
    #https://medium.com/@fabianterh/how-to-solve-the-knapsack-problem-with-dynamic-programming-eb88c706d3cf
    dp = [[0 for x in range(types['fuel']+1)] for y in range(len(gun)+1)] 
    for i in range(len(gun)+1):
       dp[i][0] = 0;
    for i in range(types['fuel']+1):
        dp[0][i] = 0;
    for i in range(len(gun)):
        for capacity in range(1,types['fuel']+1):
            maxWO = dp[i][capacity];
            maxW = 0
            currFuel = gas[i]
            if (capacity >= currFuel):
                remain = capacity-currFuel
                maxW = currFuel + dp[i][remain]
            dp[i+1][capacity] = max(maxWO,maxW)
    print("sol",dp[len(gun)][types['fuel']])
    cap = types['fuel']
    for i in range(len(gun), 0,-1):
        if (dp[i][cap] > dp[i-1][cap]):
            cap -= gas[i-1]
            sol[i-1] = True
    print(sol)
    count = sol.count(True)
    print(count)
    
    ans = ""
    ans += '{'
    ans += '\"hits\": ['
    for i in range(len(sol)):
        if (sol[i] == True):
            count -= 1
            ans += '{'
            ans += '\"cell\":{'
            ans += '\"x\": '+str(gun[i]%x+1)+','
            ans += '\"y\": '+str(gun[i]//x+1)
            ans += '},'
            ans += '\"guns\": '+str(visited[gun[i]])
            ans += '}'
            if (count > 0):
                ans += ','
    ans += ']'
    ans += '}'
    print(ans)
    return json.loads(ans)
@app.route('/lottery', methods=['GET'])
def lottery():
    dict1 = []
    for i in range(10):
        dict1.append(random.randint(1,100))
    return Response(json.dumps(dict1), mimetype='application/json')


def solvep1(n, t):
  if t > 2*n:

    if solvep1(n-2, t-2*n-1) == -1:
      return -1
    else:
      return solvep1(n-2, t-2*n-1) + 2
  if t%n == 1:
    return -1
  else:
    return 3

@app.route('/readyplayerone', methods=['POST'])
def p1():
    input = request.get_json(force=True)
    n = int(input["maxChoosableInteger"])
    t = int(input["desiredTotal"])

    print(n, t)

    output = {}

    if (n*(n+1))/2 < t:
      output["res"] = -1
      print(output)
      
    else:
      
      output["res"] = solvep1(n, t)
      print(output["res"])
    return output


def solvecomp(s, patterns, min):

  lastmin = min
  if (min < 0):
    return min
  for pattern in patterns:
    rep = s.count(pattern)
    if rep == 0:
      continue
    for char in pattern:
      new_s = s
      rep = len(new_s)
      while (len(new_s) != len(new_s.replace(pattern, char))):
        new_s = new_s.replace(pattern, char)

      rep -= len(new_s)
      new_s.replace(pattern, char)
      ret = solvecomp(new_s, patterns, min - rep)
      if ret + rep < min:
        min = ret + rep
  if min == lastmin:
    return 0
  return min
@app.route('/composition', methods=['POST'])
def comp():
    input = request.get_json(force=True)

    result = {}
    result["testId"] = input["setId"]
    s = input["composition"]

    print(s)
    patterns = input["patterns"]

    print(patterns)
    result["result"] = solvecomp(s, patterns, 5000)
    return result
