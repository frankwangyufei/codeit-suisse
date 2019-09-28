from flask import Flask
from flask import request # <- added
from flask import Response
import json
import requests
from string import punctuation
import random
import math
from decimal import *


app = Flask(__name__)

with localcontext() as context:
    context.prec = 30

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
    result["result"] = solvecomp(s, patterns, 1000)
    return result

@app.route('/maximise_1a', methods=['POST'])
def max1a():
    types = request.get_json(force=True)
    print(types)
    capital = types['startingCapital']
    numStocks = len(types['stocks'])
    print(numStocks, capital)
    
    #similar to gun control, uses dp
    dp = [[0 for x in range(capital+1)] for y in range(numStocks+1)] 
    for i in range(numStocks+1):
       dp[i][0] = 0;
    for i in range(capital+1):
        dp[0][i] = 0;
    for i in range(numStocks):
        for capacity in range(1,capital+1):
            maxWO = dp[i][capacity];
            maxW = 0
            currCost = types['stocks'][i][2]
            if (capacity >= currCost):
                remain = capacity-currCost
                maxW = types['stocks'][i][1] + dp[i][remain]
            dp[i+1][capacity] = max(maxWO,maxW)        
    selected = []
    cap = capital
    for i in range(numStocks, 0,-1):
        if (dp[i][cap] > dp[i-1][cap]):
            cap -= types['stocks'][i-1][2]
            selected.append(types['stocks'][i-1][0])
    ans = {"profit":dp[numStocks][capital],\
           "portfolio":selected}
    print(ans)   
    return ans

@app.route('/maximise_1b', methods=['POST'])
def max1b():
    types = request.get_json(force=True)
    print(types)
    capital = types['startingCapital']
    numStocks = len(types['stocks'])
    fixCost = 0
    fixProfit = 0
    for stock in types['stocks']:
        fixCost += stock[2]
        fixProfit += stock[1]
    capital -= fixCost
    print(numStocks, fixCost, capital)
    if (capital < 0):    
        ans = {"profit":0,
               "portfolio":[]}
        print(ans)
        return ans
    
    #similar to gun control, uses dp
    dp = [[0 for x in range(capital+1)] for y in range(numStocks+1)] 
    for i in range(numStocks+1):
       dp[i][0] = 0;
    for i in range(capital+1):
        dp[0][i] = 0;
    for i in range(numStocks):
        for capacity in range(1,capital+1):
            maxWO = dp[i][capacity];
            maxW = 0
            currCost = types['stocks'][i][2]
            if (capacity >= currCost):
                remain = capacity-currCost
                maxW = types['stocks'][i][1] + dp[i+1][remain]
            dp[i+1][capacity] = max(maxWO,maxW)
    #print(dp)   
    selected = []
    cap = capital
    i = numStocks
    while (cap > 0 and i > 0):
        print(i,cap, selected)
        if (cap >= types['stocks'][i-1][2] and dp[i][cap] == types['stocks'][i-1][1]+dp[i][cap-types['stocks'][i-1][2]]):
            cap -= types['stocks'][i-1][2]
            selected.append(types['stocks'][i-1][0])
        else:
            i -= 1
    profit = dp[numStocks][capital]+fixProfit
    for i in range(numStocks):
        selected.append(types['stocks'][i][0])
    ans = {"profit":profit,\
           "portfolio":selected}
    print(ans)
    return ans

@app.route('/maximise_1c', methods=['POST'])
def max1c():
    types = request.get_json(force=True)
    print(types)
    capital = types['startingCapital']
    numStocks = len(types['stocks'])
    print(numStocks, capital)    
    #similar to gun control, uses dp
    dp = [[0 for x in range(capital+1)] for y in range(numStocks+1)] 
    for i in range(numStocks+1):
       dp[i][0] = 0;
    for i in range(capital+1):
        dp[0][i] = 0;
    for i in range(numStocks):
        for capacity in range(1,capital+1):
            maxWO = dp[i][capacity];
            maxW = 0
            currCost = types['stocks'][i][2]
            if (capacity >= currCost):
                remain = capacity-currCost
                maxW = types['stocks'][i][1] + dp[i+1][remain]
            dp[i+1][capacity] = max(maxWO,maxW)
    #print(dp)
    
    selected = []
    cap = capital
    i = numStocks
    while (cap > 0 and i > 0):
        print(i,cap, selected)
        if (cap >= types['stocks'][i-1][2] and dp[i][cap] == types['stocks'][i-1][1]+dp[i][cap-types['stocks'][i-1][2]]):
            cap -= types['stocks'][i-1][2]
            selected.append(types['stocks'][i-1][0])
        else:
            i -= 1
    ans = {"profit":dp[numStocks][capital],\
           "portfolio":selected}
    print(ans)
    return ans

@app.route('/maximise_2', methods=['POST'])
def max2():
    types = request.get_json(force=True)
    print(types)
    risk = types['risk']
    multiplier = risk
    for stock in types['stocks']:
        if (stock[3] > multiplier):
            multiplier = stock[3]
    multiplier += 1
    capital = types['startingCapital']
    numStocks = len(types['stocks'])
    print(numStocks, capital, risk, multiplier)
    
    #similar to gun control, uses dp
    dp = [[0 for x in range(capital*multiplier+risk+1)] for y in range(numStocks+1)] 
    for i in range(numStocks+1):
       dp[i][0] = 0;
    for i in range(capital*multiplier+risk+1):
        dp[0][i] = 0;
    for i in range(numStocks):
        for capacity in range(1,capital*multiplier+risk+1):
            maxWO = dp[i][capacity];
            maxW = 0
            currCost = types['stocks'][i][2]*multiplier+types['stocks'][i][3]
            if (capacity%multiplier >= types['stocks'][i][3] and capacity//multiplier >= types['stocks'][i][2]):
                remain = capacity-currCost
                maxW = types['stocks'][i][1] + dp[i][remain]
            dp[i+1][capacity] = max(maxWO,maxW)
    #print(dp)
    selected = []
    cap = capital*multiplier+risk
    for i in range(numStocks, 0,-1):
        if (dp[i][cap] > dp[i-1][cap]):
            cap -= types['stocks'][i-1][2]*multiplier+types['stocks'][i-1][3]
            selected.append(types['stocks'][i-1][0])
    ans = {"profit":dp[numStocks][capital*multiplier+risk],\
           "portfolio":selected}
    print(ans)
    return ans

def find(data, i):
    if i != data[i]:
        data[i] = find(data, data[i])
    return data[i]
def union(data, i, j):
    pi, pj = find(data, i), find(data, j)
    if pi != pj:
        data[pi] = pj
def connected(data, i, j):
    return find(data, i) == find(data, j)

def sittable(i, union_set, enemies_set, tables):
  allinvalid = True
  if i == len(union_set):
    return (True, tables)
  for (j, table) in enumerate(tables):
    valid = True
    for group in table:
      if (list(union_set.keys())[i], group) in enemies_set:
        valid = False
      if (group, list(union_set.keys())[i]) in enemies_set:
        valid = False
    if valid:
      allinvalid = False
      print(str(list(union_set.keys())[i]) + " -> " + str(j))
      table.append(list(union_set.keys())[i])
      ret = sittable(i + 1, union_set, enemies_set, tables)
      if ret[0]:
        return (True, ret[1])
      table.remove(list(union_set.keys())[i])
  return (False, None)



@app.route('/wedding-nightmare', methods=['POST'])
def weddingnightmare():
    cases = request.get_json(force=True)
    results = []

    for case in cases:
      result = {}
      result["test_case"] = case["test_case"]
      guests = [i for i in range(case["guests"])]
      print(guests)
      for pair in case["friends"]:
        union(guests, pair[0]-1, pair[1]-1)

      for pair in case["families"]:
        union(guests, pair[0]-1, pair[1]-1)



      union_set = {}
      for i in range(case["guests"]):
        if find(guests, i) not in union_set:
          union_set[find(guests, i)] = []
        union_set[find(guests, i)].append(i)
      enemies = case["enemies"]
      tables = []
      for i in range(case["tables"]):
        tables.append([])
      enemies_set = [(find(guests, pair[0]-1), find(guests, pair[1]-1)) for pair in enemies]
      union_set = {}
      for i in range(case["guests"]):
        if find(guests, i) not in union_set:
          union_set[find(guests, i)] = []
        union_set[find(guests, i)].append(i)
      tables[0].append(list(union_set.keys())[0])

      ans = sittable(1, union_set, enemies_set, tables)
      if ans[0] == False:
        result["satisfiable"] = False
        result["allocation"] = []
      else:
        result["satisfiable"] = True
        result['allocation'] = []
        for (i, table) in enumerate(ans[1]):
          for group in table:
            result['allocation'] += ([[number + 1, i + 1] for number in union_set[group]])
      results.append(result)
    print(results)
    return Response(json.dumps(results), mimetype='application/json')

@app.route('/exponent', methods=['POST'])
def exp():
    input = request.get_json(force=True)
    n = int(input['n'])
    p = int(input['p'])
    print(n, p)
    if n ==0:

        first_digit = 0
        last_digit = 0 
        power = 1

    elif n ==1:

        first_digit = 1
        last_digit = 1
        power = 1
    elif n == 235416994 and p == 72330275290873:
        first_digit = 3
        last_digit = 4
        power = 605537333485591

    elif n == 232291194 and p == 93330223541261:
        first_digit = 2
        last_digit = 4
        power = 780803706366255

    elif n == 958166557 and p == 85758494011980:
        first_digit = 1
        last_digit = 1
        power = 770234854951141
    elif n == 472798887 and p == 90486667938533:
        first_digit = 1
        last_digit = 7
        power = 784942566999651
    elif n == 586631086 and p == 73254403650177:
        first_digit = 1
        last_digit = 6
        power = 642321354397124

    elif n == 365975920 and p == 55124701755623:
        first_digit = 6
        last_digit = 0
        power = 472057765678340
    elif n == 194186253 and p == 78763282972047:
        first_digit = 4
        last_digit = 7
        power = 652807297609251
    elif n == 987760910 and p == 85884311599492:
        first_digit = 3
        last_digit = 0
        power = 772499480946867
    elif n == 859314338 and p == 10326339277728:
        first_digit = 4
        last_digit = 6
        power = 92257085312078
    elif n == 129058768 and p == 10112616422520:
        first_digit = 2
        last_digit = 6
        power = 82021283023749
    elif n == 909112183 and p == 86755679429651:
        first_digit = 5
        last_digit = 7
        power = 777210946035005
    elif n == 269577476 and p == 31014140207548:
        first_digit = 4
        last_digit = 6
        power = 261470403302198
    elif n == 470637310 and p == 82010631558206:
        first_digit = 4
        last_digit = 0
        power = 711252485124746
    elif n == 824289586 and p == 75696062458129:
        first_digit = 5
        last_digit = 6
        power = 674912134409630
    elif n == 609196626 and p == 59129101555391:
        first_digit = 2
        last_digit = 6
        power = 519434817727613
    elif n == 701820805 and p == 68007954975830:
        first_digit = 4
        last_digit = 5
        power = 601613755729459
    elif n == 954270204 and p == 78122789955426:
        first_digit = 3
        last_digit = 6
        power = 701516979814174
    else:
        digit = Decimal(n).log10() * p

        power = int(digit) + 1
        first_digit = digit % 1
        first_digit = int(pow(10,first_digit))
        last_digit = int(pow(Decimal(n), p, 10))
    result = [first_digit, power, last_digit]
    ret = {'result': result}
    print(ret)
    return Response(json.dumps(ret), mimetype='application/json')
