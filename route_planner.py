import tkinter as tk
from tkinter import messagebox, ttk
import random

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Route Planner - Dijkstra Algorithm")
        
        # Canvas for displaying graph
        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack()
        
        # Define graph nodes with positions
        self.nodes = {
            "A": (100, 200), "B": (200, 100), "C": (300, 200), "D": (400, 100), "E": (500, 200)
        }
        
        # Define edges with weights
        self.edges = [("A", "B", 5), ("B", "C", 3), ("C", "D", 4), ("A", "D", 10), ("B", "E", 7), ("D", "E", 2)]
        
        # Create adjacency list for Dijkstra's algorithm
        self.adj_list = {city: [] for city in self.nodes}
        self.colors = ["red", "blue", "green", "orange", "purple", "brown"]
        
        for city1, city2, weight in self.edges:
            self.adj_list[city1].append((city2, weight))
            self.adj_list[city2].append((city1, weight))
        
        self.draw_graph()
        
        # UI for user input (source and destination selection)
        self.info_frame = tk.Frame(root)
        self.info_frame.pack()
        
        tk.Label(self.info_frame, text="Select Source:").grid(row=0, column=0)
        self.source_var = tk.StringVar()
        self.source_dropdown = ttk.Combobox(self.info_frame, textvariable=self.source_var, values=list(self.nodes.keys()))
        self.source_dropdown.grid(row=0, column=1)
        
        tk.Label(self.info_frame, text="Select Destination:").grid(row=0, column=2)
        self.dest_var = tk.StringVar()
        self.dest_dropdown = ttk.Combobox(self.info_frame, textvariable=self.dest_var, values=list(self.nodes.keys()))
        self.dest_dropdown.grid(row=0, column=3)
        
        tk.Button(self.info_frame, text="Find Shortest Path", command=self.find_shortest_path).grid(row=0, column=4)
        
    def draw_graph(self):
        """Draw nodes and edges on the canvas."""
        for city, (x, y) in self.nodes.items():
            self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="blue", outline="black", tags=city)
            self.canvas.create_text(x, y-15, text=city, font=("Arial", 10))
        
        for city1, city2, weight in self.edges:
            x1, y1 = self.nodes[city1]
            x2, y2 = self.nodes[city2]
            color = random.choice(self.colors)
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
            mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
            self.canvas.create_text(mid_x, mid_y, text=str(weight), font=("Arial", 10), fill="black")
    
    def dijkstra(self, src, dest):
        """Implement Dijkstra's algorithm to find the shortest path."""
        import heapq
        queue = [(0, src)]
        distances = {city: float('inf') for city in self.nodes}
        distances[src] = 0
        previous = {}
        
        while queue:
            cost, node = heapq.heappop(queue)
            if node == dest:
                path = []
                while node in previous:
                    path.insert(0, node)
                    node = previous[node]
                path.insert(0, src)
                return path, distances[dest]
            
            for neighbor, weight in self.adj_list[node]:
                new_cost = cost + weight
                if new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    previous[neighbor] = node
                    heapq.heappush(queue, (new_cost, neighbor))
        return None, None
    
    def find_shortest_path(self):
        """Handle user input and find the shortest path."""
        src = self.source_var.get()
        dest = self.dest_var.get()
        
        if src and dest and src in self.nodes and dest in self.nodes:
            path, cost = self.dijkstra(src, dest)
            if path:
                self.highlight_path(path)
                messagebox.showinfo("Shortest Path", f"Path: {' -> '.join(path)}\nCost: {cost}")
            else:
                messagebox.showerror("Error", "No path found")
        else:
            messagebox.showerror("Error", "Invalid source or destination")
    
    def highlight_path(self, path):
        """Highlight the shortest path in red."""
        for i in range(len(path) - 1):
            x1, y1 = self.nodes[path[i]]
            x2, y2 = self.nodes[path[i+1]]
            self.canvas.create_line(x1, y1, x2, y2, fill="red", width=3)

# Run the Tkinter application
root = tk.Tk()
app = GraphApp(root)
root.mainloop()
