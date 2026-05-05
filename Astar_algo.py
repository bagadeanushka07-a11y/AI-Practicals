import tkinter as tk#GUI window, grid drawing
from tkinter import messagebox#popup messages
import heapq#priority queue
import random#generate obstacles
'''Grid = 20 × 20
Each cell size = 30 pixels
Speed controls animation delay'''
ROWS = 20
COLS = 20
SIZE = 30
SPEED = 20

START_NODE = (0, 0)#top left
END_NODE = (ROWS - 1, COLS - 1)#bottom-right

# Create grid (0 = free, 1 = obstacle) 2D matrix
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Generate random obstacles
def generate_grid():
    global grid
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for i in range(ROWS):
        for j in range(COLS):
            if random.random() < 0.28:#28% cells become obstacles
                grid[i][j] = 1


    # Ensure start and end are free
    grid[START_NODE[0]][START_NODE[1]] = 0
    grid[END_NODE[0]][END_NODE[1]] = 0

'''Only horizontal + vertical moves no diagonal distance
Perfect for grid'''
# Heuristic (Manhattan Distance)
def calc_h(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])#h(n)

# Get valid neighbors
def neighbors(cell):
    x, y = cell
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
#Up, Down, Left, Right
    result = []
    for dx, dy in moves:
        '''Conditions:

Inside grid
Not obstacle'''
        nx, ny = x + dx, y + dy
        if 0 <= nx < ROWS and 0 <= ny < COLS and grid[nx][ny] == 0:
            result.append((nx, ny))
    return result
#main class
class AStarApp:
#controls the GUI + algorithm
    def __init__(self, root):
        self.root = root
        self.root.title("A* Pathfinding Visualizer")
#Creates drawing area
        self.canvas = tk.Canvas(
            root,
            width=COLS * SIZE,
            height=ROWS * SIZE,
            bg="#f0f0f0"
        )
        self.canvas.pack()

        btn_frame = tk.Frame(root)
        btn_frame.pack()

        tk.Button(btn_frame, text="Start Search", command=self.run_astar).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Generate Maze", command=self.reset_grid).grid(row=0, column=1, padx=5)

        self.cells = {}
        self.draw_grid()

    def draw_grid(self):#draw each cell
        self.canvas.delete("all")
        self.cells.clear()

        for i in range(ROWS):
            for j in range(COLS):
                x1 = j * SIZE
                y1 = i * SIZE
                x2 = x1 + SIZE
                y2 = y1 + SIZE

                color = "#444444" if grid[i][j] == 1 else "#f0f0f0"

                if (i, j) == START_NODE:
                    color = "cyan"
                elif (i, j) == END_NODE:
                    color = "orange"

                rect = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline="gray"
                )

                self.cells[(i, j)] = rect

    def paint(self, cell, color):#Updates cell color during algorithm
        if cell not in [START_NODE, END_NODE]:
            self.canvas.itemconfig(self.cells[cell], fill=color)
            self.root.update()
            self.root.after(SPEED)#Shows animation step-by-step

    def build_path(self, parent, current):#Reconstructs path
        path = []
        while current in parent:#Goes backward from goal → start
            path.append(current)
            current = parent[current]
        path.reverse()
        return path

    def run_astar(self):#A* ALGORITHM
        open_list = []#Priority queue → stores nodes to explore
        heapq.heappush(open_list, (0, START_NODE))

        parent = {}
        g_cost = {START_NODE: 0}
        f_cost = {START_NODE: calc_h(START_NODE, END_NODE)}

        visited = set()#To avoid revisiting
        '''Runs until:

Path found OR
No nodes left'''
        while open_list:
            _, current = heapq.heappop(open_list)#Gets node with lowest f(n)

            if current in visited:#skip visited
                continue

            visited.add(current)

            if current == END_NODE:#goal check
                path = self.build_path(parent, current)#Reconstruct and paint path
                for step in path:
                    self.paint(step, "#800080")  # purple path

                messagebox.showinfo("Done", "Goal reached using A*!")
                return

            if current != START_NODE:
                self.paint(current, "#cba6f7")  # visited nodes

            for nb in neighbors(current):#explore neighbor
                temp_g = g_cost[current] + 1#Cost increases by 1 per step g(n)

                if nb not in g_cost or temp_g < g_cost[nb]:
                    parent[nb] = current
                    g_cost[nb] = temp_g
                    f_cost[nb] = temp_g + calc_h(nb, END_NODE)#Core A* formula

                    heapq.heappush(open_list, (f_cost[nb], nb))#Add to priority queue

                    if nb != END_NODE:
                        self.paint(nb, "#ffb3c6")  # open nodes

        messagebox.showerror("Oops", "No possible path found!")

    def reset_grid(self):#Generates new maze
        generate_grid()
        self.draw_grid()


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    generate_grid()
    root = tk.Tk()
    app = AStarApp(root)
    root.mainloop()
