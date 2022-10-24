import tkinter as tk
import numpy as np
from tkinter import ttk


class Interface:

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Mechanisms v0.1")

        # Size of the window
        self.window_size = (768, 1024)
        self.root.geometry(str(self.window_size[1])+"x"+str(self.window_size[0]))

        # Frames
        self.f_canvas = tk.Frame(self.root, relief="sunken")
        self.f_controls = tk.LabelFrame(self.root, text="Controls")
        self.f_tree_bezier = tk.LabelFrame(self.root, text="Bezier Points")
        self.f_tree_all_points = tk.LabelFrame(self.root, text="Curve Points")

        self.f_canvas.grid(column=0, row=0, columnspan=3, sticky=tk.W+tk.E, padx=2, pady=2)
        self.f_controls.grid(column=0, row=1, sticky=tk.W+tk.E, padx=2, pady=2)
        self.f_tree_bezier.grid(column=1, row=1, sticky=tk.W+tk.E, padx=2, pady=2)
        self.f_tree_all_points.grid(column=2, row=1, sticky=tk.W+tk.E, padx=2, pady=2)

        # Variables
        self.entry_variables = []

        # Entries/Controls
        self.__input_entry(self.f_controls, "Test 1:", 0, 0)
        self.__input_entry(self.f_controls, "Test 2:", 2, 0)

        # Canvas
        self.__create_canvas(self.f_canvas)
        
        # Treeviews
        self.tv_bezier_points = ttk.Treeview(self.f_tree_bezier, columns=("X", "Y"))
        self.tv_bezier_points.grid(sticky=tk.W+tk.E, padx=2, pady=2)
        self.sc_bezier_points = ttk.Scrollbar(self.f_tree_bezier, orient="vertical", command=self.tv_bezier_points.yview)
        self.sc_bezier_points.grid(column=1, row=0, sticky=tk.N+tk.S)
        self.tv_bezier_points.heading("#0", text="Point")
        self.tv_bezier_points.column("#0", width=50)
        self.tv_bezier_points.heading("X", text="X")
        self.tv_bezier_points.column("X", width=50)
        self.tv_bezier_points.heading("Y", text="Y")
        self.tv_bezier_points.column("Y", width=50)

        # self.sc_bezier_points.configure(yscrollcommand=self.sc_bezier_points.set)

        self.tv_all_points = ttk.Treeview(self.f_tree_all_points, columns=("X", "Y"))
        self.tv_all_points.grid(sticky=tk.W+tk.E, padx=2, pady=2)
        self.sc_all_points = ttk.Scrollbar(self.f_tree_all_points, orient="vertical", command=self.tv_all_points.yview)
        self.sc_all_points.grid(column=1, row=0, sticky=tk.N+tk.S)
        self.tv_all_points.heading("#0", text="Point")
        self.tv_all_points.column("#0", width=50)
        self.tv_all_points.heading("X", text="X")
        self.tv_all_points.column("X", width=50)
        self.tv_all_points.heading("Y", text="Y")
        self.tv_all_points.column("Y", width=50)
        # Run the app
        self.root.mainloop()

    def __input_entry(self, root, name, x, y):
        this_variable = tk.IntVar(0)
        self.entry_variables.append(this_variable)
        tk.Label(root, text=name).grid(column=x, row=y)
        entry_control = tk.Entry(root, textvariable=this_variable)
        entry_control.grid(column=x+1, row=y, padx=2, pady=2)
        return entry_control

    def __create_canvas(self, root):
        self.work_area = self.WorkArea(root, (self.window_size[1]-10, 500))

    class WorkArea(tk.Canvas):
        def __init__(self, root, size) -> None:
            self.size = size
            self.root_canvas = root
            self.canvas = tk.Canvas(self.root_canvas, width=self.size[0], height=self.size[1], bg="white")
            self.canvas.grid(column=0, row=0, padx=2, pady=2)

            # Points
            self.control_points = []
            self.data_points = {"name":[], "id":[], "position":[]}

            # Update Line
            self.control_line = {"x": 0, "y": 0, "item": None}

            # Bezier
            self.bezier = 0
            self.points_bezier = []
            self.canvas.bind("<Button-1>", self.__add_point)
            self.canvas.bind("<Button-3>", self.__mod_point)

        def draw_bezier5(self):
            x_start = x_end = self.data_points["position"][0][0]
            y_start = y_end = self.data_points["position"][0][1]
            self.points_bezier.append([x_start, y_start])
            n = 1000
            p = self.data_points["position"]
            for i in range(n):
                t = i / n
            
                x = ((1-t)**5)*p[0][0] +(5*t*(1-t)**4)*p[1][0] + (10*(t**2))*((1-t)**3)*p[2][0] + (10*(t**3))*((1-t)**2)*p[3][0] + (5*(t**4))*((1-t))*p[4][0] + (t**5)*x_end
                y = ((1-t)**5)*p[0][1] +(5*t*(1-t)**4)*p[1][1] + (10*(t**2))*((1-t)**3)*p[2][1] + (10*(t**3))*((1-t)**2)*p[3][1] + (5*(t**4))*((1-t))*p[4][1] + (t**5)*y_end

                bc = self.canvas.create_line(x, y, x_start, y_start)
                self.points_bezier.append([x, y])
                # updates initial values
                x_start = x
                y_start = y
                self.bezier = bc

        def __add_point(self, event):
            
            point = x, y = (event.x, event.y)
            self.control_points.append(point)
            name = self.canvas.create_oval(x, y, x+5, y+5, fill="green", outline="green")
            # self.canvas.create_text(x-5, y-5, text=str(len(self.control_points)))
            self.data_points["name"].append("Point"+str(name))
            self.data_points["id"].append(name)
            self.data_points["position"].append([x, y])

            if len(self.control_points) == 5:
                self.draw_bezier5()
                self.canvas.unbind("<Button-1>")
            # print(self.data_points)
        
        def __mod_point(self, event):
            # Binds for the modification
            self.canvas.bind("<ButtonRelease-3>", self.__drag_stop)
            self.canvas.bind("<B3-Motion>", self.__drag)

            # Check if a point is close to the clicked area
            self.control_line["item"] = self.canvas.find_closest(event.x, event.y)[0]
            self.control_line["x"] = event.x
            self.control_line["y"] = event.y
                

        def __drag(self, event):

            delta_x = event.x - self.control_line["x"]
            delta_y = event.y - self.control_line["y"]

            self.canvas.move(self.control_line["item"], delta_x, delta_y)
            # record the new position
            self.control_line["x"] = event.x
            self.control_line["y"] = event.y
            

        def __drag_stop(self, event):
            # If released Button 3, update closes point in self.data_points
            # Update canvas with new points
            for line in range(1000):
                self.canvas.delete(self.bezier-999+line)
            self.data_points["position"][self.control_line["item"]-1]=[event.x, event.y]
            self.draw_bezier5()
            # print(self.points_bezier)
            self.control_line["item"] = None
            self.control_line["x"] = 0
            self.control_line["y"] = 0

        def get_bezier_points(self):
            return self.points_bezier

    
    
    class Synthesis():

        def __init__(self) -> None:
            pass

        class FourBar():

            def __init__(self, root) -> None:
                self.oA = []    # coordinates of fixed end-point of input link
                self.oB = []    # coordinates of fixed end-point of output link
Interface()