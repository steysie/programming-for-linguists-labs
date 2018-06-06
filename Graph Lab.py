import random
import networkx as nx
import matplotlib.pyplot as plt

def generateMatrix(n):
    mat = []
    for i in range(n):
        row = []
        for j in range(i+1):            #we'll get what's below the diagonal

            if random.randint(0,5) < 4 or i == j:
                row.append(0)
            else:
                row.append(1)

        mat.append(row)
    print(mat)

    for row in mat:         #make it symmetrical
        for i in range(len(row)-1):
            mat[i].append(row[i])
    return mat

matrix = generateMatrix(10)
print(matrix)


# to be able to use NetworkX to build a graph, we need an info of nodes and edges
def getData(matrix):
    connect = {}
    #nodes = []
    edges = []
    for ind1, row in enumerate(matrix):
        list = []
        #if len(nodes) == 0:
            #nodes = [j for j in range(1, len(row) + 1)]
        for ind2, e in enumerate(row):
            if e == 1:
                list.append(ind2)
                if tuple((ind2, ind1)) not in edges:
                    edges.append(tuple((ind1, ind2)))
                else:
                    pass
        connect[ind1] = list
    kopi = connect.copy()

    for h in kopi.keys():
        kopi[h] = len(kopi[h])
    l = lambda x: x[1]
    kopi=sorted(kopi.items(), key=l, reverse=True)
    nodes_sorted=[]
    for i in kopi:
        nodes_sorted.append(i[0])

    return connect, nodes_sorted, edges

connect, nodes, edges = getData(matrix)
print(connect)
#print("these are nodes")
#print(nodes)
'''
def raskraska(dict1,upor):
    colored=[]
    g=[]
    used=[]
    hash=[]
    for h in upor:
        if upor.index(h)==0:
            hash.append(h)
            used.append(h)
            for j in dict1[h]:
                g.append(j)
        for i in upor:
            if i not in hash and i not in g and i not in used:
                hash.append(i)
                used.append(i)
                for j in dict1[i]:
                    g.append(j)
        colored.append(hash)
        hash=[]
        g=[]
    #print (colored)

    return colored

colored = raskraska(connect, nodes)
'''

# let's get it colored!
def graphColoring(matrix):
    colored = [[]]
    color = 0  # № цвета
    stack = []  # покрашенные узлы
    num2 = num1 = -1

    # можно ли покрасить в текущий цвет - есть ли edge меджу nodes
    def loop(num):
        for t in colored[color]:   # есть ли в группе данного цвета
            if matrix[t][num] == 1:
                return False
            else:
                return True

    for a in matrix:
        num1 += 1
        if num1 not in stack:  # просматриваем только те, которые еще не покрашены
            if not loop(num1):  # значит применяем новый цвет
                colored.append([])
                color += 1
                stack.append(num1)
                colored[color].append(num1)
            print(colored)
            num2 = num1
            for b in a[num1:]:
                if b == 0 and num2 not in stack and loop(num2):
                    stack.append(num2)
                    colored[color].append(num2)
                num2 += 1
    return colored

colored = graphColoring(matrix)
print(colored)

def showGraph():
    colored = []

nodes1 = [i for i in range(len(matrix))]

G = nx.Graph()
G.add_nodes_from(nodes1)
G.add_edges_from(edges)
pos = nx.spring_layout(G) # positions for all nodes

colors=['#660066', '#FFD700', '#00FFFF', '#FAFAD2', 'red', 'black', 'brown', 'blue', 'yellow', 'green', 'orange', 'beige', 'turquoise', 'pink']
s = -1
for c in colored:
    s += 1
    if len(c) != 0:
        nx.draw_networkx_nodes(G, pos, nodelist = c, node_color = colors[s], node_size = 300, alpha = 0.8)

nx.draw_networkx_edges(G, pos, width = 1.0, alpha = 0.5)
plt.draw()

#nx.draw(G, with_labels = True)
plt.show()