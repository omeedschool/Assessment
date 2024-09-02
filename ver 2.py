import tkinter as tk

# Constants
RESOLUTION = 1000, 800
LINE_SPEED = 10
LINE_INTERVAL = 2000  # Interval in milliseconds (2 seconds)

class Game(tk.Tk):
    """Main game application class."""
    
    def __init__(self):
        super().__init__()
        self.title("Title")

        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calculate position x, y to center the window
        position_right = int(screen_width / 2 - RESOLUTION[0] / 2)
        position_down = int(screen_height / 2 - RESOLUTION[1] / 2)
        
        # Set the geometry of the window to center it on the screen
        self.geometry(f"{RESOLUTION[0]}x{RESOLUTION[1]}+{position_right}+{position_down}")
        #self.resizable(False, False)

        # Create a Canvas widget
        self.canvas = tk.Canvas(self, width=400, height=800)
        self.canvas.pack(side=tk.RIGHT)

        self.frame = tk.Frame(self, width=600, height=800)
        self.frame.pack(side=tk.LEFT)

        self.line_ids = []

        self.load_carscroll()
        self.create_moving_lines()

        self.mainloop()
    
    def load_carscroll(self):
        self.canvas.create_rectangle(100, 0, 300, 800, fill="grey")
        self.canvas.create_rectangle(0, 0, 100, 800, fill="green")
        self.canvas.create_rectangle(300, 0, 400, 800, fill="green")

        # Load and display the car image
        self.car_image = tk.PhotoImage(file="cars/car1.png")
        self.car2_image = tk.PhotoImage(file="cars/car2.png")

        self.canvas.create_image(125, 700, image=self.car_image)
        self.canvas.create_image(175, 700, image=self.car2_image)
        self.canvas.create_image(225, 700, image=self.car_image)
        self.canvas.create_image(275, 700, image=self.car2_image)

    def create_moving_lines(self):
        # Create lines with tags
        for x in [150, 200, 250]:
            for y in range(50, RESOLUTION[1] + 50, 100):
                line_id = self.canvas.create_line(x, y, x, y + 50, fill="white", tags="moving_lines")

        # Start the movement of the lines
        self.move_lines()

    def move_lines(self):
        # Move all lines with the tag "moving_lines"
        for line_id in self.canvas.find_withtag("moving_lines"):
            x1, y1, x2, y2 = self.canvas.coords(line_id)
            if y1 < RESOLUTION[1]:
                self.canvas.move(line_id, 0, LINE_SPEED)
            else:
                # Reset the line's position to the top
                self.canvas.coords(line_id, x1, 0, x2, 50)
        # Continue moving lines
        self.after(50, self.move_lines)  # Update every 50ms

game = Game()