from flask import Flask
from flask import request # <- added


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
    input = request.get_json(force=True)
    print(input)

    for module in input['modules']:
      nodes[module] = Node(module)
    extra = []
    for pair in input['dependencyPairs']:
      if pair['dependee'] not in nodes:
        nodes[pair['dependee']] = Node(pair['dependee']) 
        extra.append(pair['dependee'])
      if pair['dependentOn'] not in nodes:
        nodes[pair['dependentOn']] = Node(pair['dependentOn']) 
        extra.append(pair['dependentOn'])
      nodes[pair['dependee']].addEdge(nodes[pair['dependentOn']])

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