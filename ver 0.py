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

game = Game()