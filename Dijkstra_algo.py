import tkinter as tk#used to create GUI window
from tkinter import messagebox#used to show popup results
import heapq
#graph data
#Dictionary storing coordinates of each node
POINTS = {
    'A': (120, 120),
    'B': (300, 90),
    'C': (520, 160),
    'D': (160, 320),
    'E': (360, 300),
    'F': (560, 340)
}
#Graph stored as adjacency list
NETWORK = {
    'A': {'B': 4, 'D': 2},
    'B': {'A': 4, 'C': 5, 'E': 10},
    'C': {'B': 5, 'F': 3},
    'D': {'A': 2, 'E': 6},
    'E': {'D': 6, 'B': 10, 'F': 2},
    'F': {'C': 3, 'E': 2}
}

SOURCE = 'A'
TARGET = 'F'
SPEED = 600#Controls how fast nodes highlight
#Defines a class to manage GUI + algorithm
class GraphVisualizer:
    def __init__(self, root):#constructor runs auto when object is created
        self.root = root#Stores window reference
        self.root.title("Dijkstra Shortest Path Visualizer")#Sets window title

        self.canvas = tk.Canvas(root, width=700, height=450, bg="#f5f5f5")
        self.canvas.pack(pady=10)

        tk.Button(root, text="Start Dijkstra", command=self.start_search).pack()

        self.nodes_drawn = {}#Dictionary to store node shapes (circles)
        self.draw_network()#Draw graph when program starts

    def draw_network(self):#Function to draw graph.
        self.canvas.delete("all")
        self.nodes_drawn.clear()

        drawn_edges = set()

        # Draw edges
        '''v = neighbor
w = weight'''
        for u in NETWORK:
            x1, y1 = POINTS[u]
            for v, w in NETWORK[u].items():
                if (v, u) in drawn_edges:
                    continue

                x2, y2 = POINTS[v]
                self.canvas.create_line(x1, y1, x2, y2, width=2, fill="gray")

                mx, my = (x1 + x2) // 2, (y1 + y2) // 2
                self.canvas.create_text(mx, my - 10, text=str(w), font=("Arial", 10, "bold"))

                drawn_edges.add((u, v))

        
        # Draw nodes
        for node, (x, y) in POINTS.items():
            if node == SOURCE:
                color = "cyan"
            elif node == TARGET:
                color = "orange"
            else:
                color = "#d3d3d3"

            circle = self.canvas.create_oval(x - 25, y - 25, x + 25, y + 25, fill=color)#Draw node as circle
            self.canvas.create_text(x, y, text=node, font=("Arial", 14, "bold"))#Write node name

            self.nodes_drawn[node] = circle#Save node reference

    def highlight_node(self, node, color):#Highlights node during traversal
        self.canvas.itemconfig(self.nodes_drawn[node], fill=color)#change color
        self.root.update()
        self.root.after(SPEED)

    # =========================
    # GET PATH
    # =========================
    def get_path(self, parent):#Builds final shortest path
        path = []
        curr = TARGET#Start from destination

        while curr in parent:#Move backwards
            path.append(curr)
            curr = parent[curr]#Follow parent links

        path.append(SOURCE)
        return path[::-1]#Reverse list to get correct order

  
    # DIJKSTRA ALGORITHM
   #Step 1: Initialize
    def start_search(self):
        pq = [(0, SOURCE)]
        distance = {SOURCE: 0}#Stores shortest distances
        parent = {}#Stores path
        visited = set()
#Step 2: Pick minimum node
        while pq:
            cost, current = heapq.heappop(pq)
#             Get node with minimum cost
# 👉 THIS is greedy step
#Skip if already visited
            if current in visited:
                continue
#Step 4: Mark visited
            visited.add(current)

            if current not in [SOURCE, TARGET]:
                self.highlight_node(current, "#a0e7e5")
#Step 5: Goal check
            # If target reached
            if current == TARGET:
                path = self.get_path(parent)#Get final path

                for node in path:
                    self.highlight_node(node, "#6a0dad")

                messagebox.showinfo(
                    "Result",
                    f"Path: {' -> '.join(path)}\nTotal Cost: {cost}"
                )
                return

            #step 6 Explore neighbors
            for neighbor, weight in NETWORK[current].items():
                new_cost = cost + weight#step 7Calculate new distance
#Step 8: Compare and update
                if neighbor not in distance or new_cost < distance[neighbor]:#Check if better path found
                    distance[neighbor] = new_cost# step 9 Update distance
                    parent[neighbor] = current
                    heapq.heappush(pq, (new_cost, neighbor))#Add to queue

        messagebox.showerror("Error", "No path available!")



# MAIN PROGRAM

if __name__ == "__main__":
    root = tk.Tk()#Create window
    app = GraphVisualizer(root)#Create object
    root.mainloop()

