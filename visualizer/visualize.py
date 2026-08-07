import sys
import tkinter as tk
from tkinter import scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict

class ClusterVisualizer:
    def __init__(self, rawData):
        self.data = rawData
        # Dictionary to group coordinates by their cluster ID
        self.clusters = defaultdict(list)
        self.clusterIds = self._determineClusters()
        self.load_data()
        self.setup_gui()

    def load_data(self):
        """converts the raw data into a dictionary of clusters with their respective coordinates."""
        for row in self.data:
            clusterId = row[0]
            x = row[1]
            y = row[2]
            self.clusters[clusterId].append((x, y))

    def setup_gui(self):
        """Builds the main window with a plot on the left and text on the right."""
        self.root = tk.Tk()
        self.root.title("K-Means Clustering Results")
        self.root.geometry("1000x600")

        # Intercept the 'X' button close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create two main frames: Left for Plot, Right for Text
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_frame = tk.Frame(self.root, width=300)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.draw_plot()
        self.draw_text_list()

    def draw_plot(self):
        """Renders the scatter plot using matplotlib."""
        fig, ax = plt.subplots(figsize=(6, 5), dpi=100)
        
        # Define a list of colors (matplotlib handles recycling if needed)
        colors = plt.colormaps['tab10']

        for idx, (cluster_id, points) in enumerate(self.clusters.items()):
            # Unzip the list of (x,y) tuples into separate X and Y lists
            xs, ys = zip(*points)
            # Plot this specific cluster
            print(f'Cluster {cluster_id}')
            ax.scatter(xs, ys, color=colors(idx % 10), label=f'Cluster {cluster_id}', alpha=0.7)

        ax.set_title("K-Means Cluster Map")
        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Y Coordinate")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.5)

        # Embed the matplotlib figure into the Tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=self.left_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def draw_text_list(self):
        """Populates the scrollable text box with cluster coordinates."""
        # Add a label above the text box
        lbl = tk.Label(self.right_frame, text="Coordinates by Cluster", font=("Arial", 12, "bold"))
        lbl.pack(anchor=tk.W, pady=(0, 5))

        # Create a scrollable text widget
        text_area = scrolledtext.ScrolledText(self.right_frame, wrap=tk.WORD, width=35, height=30)
        text_area.pack(fill=tk.Y, expand=True)

        # Build the text content
        display_text = ""
        for cluster_id in sorted(self.clusters.keys()):
            display_text += f"--- Cluster {cluster_id} ---\n"
            for x, y in self.clusters[cluster_id]:
                display_text += f"  ({x}, {y})\n"
            display_text += "\n"

        # Insert text and disable editing
        text_area.insert(tk.INSERT, display_text)
        text_area.configure(state='disabled')

    def show(self):
        """Starts the GUI event loop."""
        self.root.mainloop()
    def on_closing(self):
        """Forces the entire Python script to terminate when the window closes."""
        self.root.quit()     # Stops the Tkinter mainloop
        self.root.destroy()  # Destroys the UI components safely
        sys.exit(0)          # Kills the Python process
    def _determineClusters(self):
        """Identifies the clusterIds & returns them."""
        clusterIds = []
        for row in self.data:
            clusterId = row[0]
            if clusterId not in clusterIds:
                clusterIds.append(clusterId)
        return clusterIds