import tkinter as tk

# Constants
RESOLUTION = 1000, 800
LINE_SPEED = 10
LINE_INTERVAL = 2000  # Interval in milliseconds (1 second)

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
        self.resizable(False, False)

        # Create a Canvas widget
        self.canvas = tk.Canvas(self, width=RESOLUTION[0], height=RESOLUTION[1])
        self.canvas.pack()

        self.line_ids = []

        self.load_carscroll()
        self.create_moving_lines()

        self.mainloop()
    
    def load_carscroll(self):
        self.canvas.create_rectangle(600, 0, 800, 800, fill="grey")

        # Load and display the car image
        self.car_image = tk.PhotoImage(file="cars/car1.png")
        self.car2_image = tk.PhotoImage(file="cars/car2.png")

        self.canvas.create_image(625, 700, image=self.car_image)
        self.canvas.create_image(675, 700, image=self.car2_image)
        self.canvas.create_image(725, 700, image=self.car_image)
        self.canvas.create_image(775, 700, image=self.car2_image)

    def create_moving_lines(self):
        # Create the first line
        self.line_ids.append(self.canvas.create_line(650, 50, 650, 100, fill="white"))
        self.line_ids.append(self.canvas.create_line(650, 150, 650, 200, fill="white"))
        self.line_ids.append(self.canvas.create_line(650, 250, 650, 300, fill="white"))
        self.line_ids.append(self.canvas.create_line(650, 350, 650, 400, fill="white"))
        self.line_ids.append(self.canvas.create_line(650, 450, 650, 500, fill="white"))
        self.line_ids.append(self.canvas.create_line(650, 550, 650, 600, fill="white"))
        self.line_ids.append(self.canvas.create_line(650, 650, 650, 700, fill="white"))
        self.line_ids.append(self.canvas.create_line(650, 750, 650, 800, fill="white"))

        self.line_ids.append(self.canvas.create_line(700, 50, 700, 100, fill="white"))
        self.line_ids.append(self.canvas.create_line(700, 150, 700, 200, fill="white"))
        self.line_ids.append(self.canvas.create_line(700, 250, 700, 300, fill="white"))
        self.line_ids.append(self.canvas.create_line(700, 350, 700, 400, fill="white"))
        self.line_ids.append(self.canvas.create_line(700, 450, 700, 500, fill="white"))
        self.line_ids.append(self.canvas.create_line(700, 550, 700, 600, fill="white"))
        self.line_ids.append(self.canvas.create_line(700, 650, 700, 700, fill="white"))
        self.line_ids.append(self.canvas.create_line(700, 750, 700, 800, fill="white"))

        self.line_ids.append(self.canvas.create_line(750, 50, 750, 100, fill="white"))
        self.line_ids.append(self.canvas.create_line(750, 150, 750, 200, fill="white"))
        self.line_ids.append(self.canvas.create_line(750, 250, 750, 300, fill="white"))
        self.line_ids.append(self.canvas.create_line(750, 350, 750, 400, fill="white"))
        self.line_ids.append(self.canvas.create_line(750, 450, 750, 500, fill="white"))
        self.line_ids.append(self.canvas.create_line(750, 550, 750, 600, fill="white"))
        self.line_ids.append(self.canvas.create_line(750, 650, 750, 700, fill="white"))
        self.line_ids.append(self.canvas.create_line(750, 750, 750, 800, fill="white"))

        # Start the movement of the lines
        self.move_lines()

    def move_lines(self):
        for line_id in self.line_ids:
            x1, y1, x2, y2 = self.canvas.coords(line_id)
            if y1 < RESOLUTION[1]:
                self.canvas.move(line_id, 0, LINE_SPEED)
            else:
                # Reset the line's position to the top
                self.canvas.coords(line_id, x1, 0, x2, 50)
        # Continue moving lines
        self.after(50, self.move_lines)  # Update every 50ms

game = Game()