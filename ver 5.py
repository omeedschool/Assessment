import tkinter as tk
from tkinter import ttk
import random

# Constants
RESOLUTION = 1000, 800
LINE_SPEED = 10
LINE_INTERVAL = 2000  # Interval in milliseconds (2 seconds)
CAR_MOVE_STEP = 5  # Step size for car movement
CAR_ANIMATION_DELAY = 50  # Delay in milliseconds for animation
CAR_UP_TOTAL_MOVE = 50  # Total pixels to move up
CAR_DOWN_TOTAL_MOVE = 50 # Total pixels to move down

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

        # Styles
        style = ttk.Style(self)
        style.theme_use('clam')

        # Create a Canvas widget
        self.canvas = tk.Canvas(self, width=400, height=800)
        self.canvas.pack(side=tk.RIGHT)

        self.frame = tk.Frame(self, width=600, height=800)
        self.frame.pack(side=tk.LEFT)

        self.line_ids = []

        self.load_carscroll()
        self.create_moving_lines()

        # Set up question and answer display for Player 1
        self.question_label = tk.Label(self.frame, text="", font=("Helvetica", 16))
        self.question_label.place(relx=0.5, rely=0.20, anchor=tk.CENTER)

        # Set up question and answer display for Player 2
        self.question_label_2 = tk.Label(self.frame, text="", font=("Helvetica", 16))
        self.question_label_2.place(relx=0.5, rely=0.70, anchor=tk.CENTER)
        
        self.answer_labels = [
            tk.Label(self.frame, text="", font=("Helvetica", 16)),
            tk.Label(self.frame, text="", font=("Helvetica", 16)),
            tk.Label(self.frame, text="", font=("Helvetica", 16)),
            tk.Label(self.frame, text="", font=("Helvetica", 16))
        ]

        self.answer_labels_2 = [
            tk.Label(self.frame, text="", font=("Helvetica", 16)),
            tk.Label(self.frame, text="", font=("Helvetica", 16)),
            tk.Label(self.frame, text="", font=("Helvetica", 16)),
            tk.Label(self.frame, text="", font=("Helvetica", 16))
        ]
        
        for i, label in enumerate(self.answer_labels):
            label.place(relx=0.20*(i+1), rely=0.25, anchor=tk.CENTER)

        for i, label in enumerate(self.answer_labels_2):
            label.place(relx=0.20*(i+1), rely=0.75, anchor=tk.CENTER)

        self.current_question = None
        self.correct_answer = None

        self.current_question_2 = None
        self.correct_answer_2 = None
        
        # PLAYER 1
        # Bind keys to answer checking function
        self.bind("<q>", lambda event: self.check_answer(0))
        self.bind("<w>", lambda event: self.check_answer(1))
        self.bind("<e>", lambda event: self.check_answer(2))
        self.bind("<r>", lambda event: self.check_answer(3))

        # PLAYER 2
        # Bind keys to answer checking function
        self.bind("<u>", lambda event: self.check_answer_2(0))
        self.bind("<i>", lambda event: self.check_answer_2(1))
        self.bind("<o>", lambda event: self.check_answer_2(2))
        self.bind("<p>", lambda event: self.check_answer_2(3))

        # Generate the first question
        self.generate_question()
        self.generate_question_2()

        self.mainloop()

    def load_carscroll(self):
        self.canvas.create_rectangle(100, 0, 300, 800, fill="grey")
        self.canvas.create_rectangle(0, 0, 100, 800, fill="green")
        self.canvas.create_rectangle(300, 0, 400, 800, fill="green")

        # Load and display the car image
        self.car_image = tk.PhotoImage(file="cars/car1.png")
        self.car2_image = tk.PhotoImage(file="cars/car2.png")

        self.car_id = self.canvas.create_image(125, 700, image=self.car_image)
        self.car_id2 = self.canvas.create_image(175, 700, image=self.car2_image)
        self.canvas.create_image(225, 700, image=self.car_image)
        self.canvas.create_image(275, 700, image=self.car2_image) 

    def generate_question(self):
        """Generate a new math question and display it."""
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        self.current_question = f"What is {num1} + {num2}?"
        self.correct_answer = num1 + num2

        answers = [self.correct_answer]
        while len(answers) < 4:
            wrong_answer = random.randint(1, 20)
            if wrong_answer not in answers:
                answers.append(wrong_answer)

        random.shuffle(answers)

        self.question_label.config(text=self.current_question)
        for i, label in enumerate(self.answer_labels):
            label.config(text=f"{['Q', 'W', 'E', 'R'][i]}: {answers[i]}")
            label.answer_value = answers[i]

    def generate_question_2(self):
        """Generate a new math question and display it."""
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        self.current_question_2 = f"What is {num1} + {num2}?"
        self.correct_answer_2 = num1 + num2

        answers = [self.correct_answer_2]
        while len(answers) < 4:
            wrong_answer = random.randint(1, 20)
            if wrong_answer not in answers:
                answers.append(wrong_answer)

        random.shuffle(answers)

        self.question_label_2.config(text=self.current_question_2)
        for i, label in enumerate(self.answer_labels_2):
            label.config(text=f"{['U', 'I', 'O', 'P'][i]}: {answers[i]}")
            label.answer_value = answers[i]

    def check_answer(self, index):
        """Check if the selected answer is correct."""
        if self.answer_labels[index].answer_value == self.correct_answer:
            self.animate_car_up(CAR_UP_TOTAL_MOVE // CAR_MOVE_STEP)  # Move the car up with animation
        else:
            self.animate_car_down(CAR_DOWN_TOTAL_MOVE // CAR_MOVE_STEP)  # Move the car down slowly

        self.generate_question()

    def check_answer_2(self, index):
        """Check if the selected answer is correct."""
        if self.answer_labels_2[index].answer_value == self.correct_answer_2:
            self.animate_car2_up(CAR_UP_TOTAL_MOVE // CAR_MOVE_STEP)  # Move the car up with animation
        else:
            self.animate_car2_down(CAR_DOWN_TOTAL_MOVE // CAR_MOVE_STEP)  # Move the car down slowly

        self.generate_question_2()

    def animate_car_up(self, steps):
        """Animate the car moving up in steps."""
        if steps > 0:
            self.canvas.move(self.car_id, 0, -CAR_MOVE_STEP)
            self.after(CAR_ANIMATION_DELAY, self.animate_car_up, steps - 1)

    def animate_car_down(self, steps):
        """Animate the car moving down slowly until it reaches the starting point."""
        car_coords = self.canvas.coords(self.car_id)
        if car_coords[1] < 700 and steps > 0:  # Ensure car doesn't move down below starting point
            self.canvas.move(self.car_id, 0, CAR_MOVE_STEP)
            self.after(200, self.animate_car_down, steps - 1)

    def animate_car2_up(self, steps):
        """Animate the car moving up in steps."""
        if steps > 0:
            self.canvas.move(self.car_id2, 0, -CAR_MOVE_STEP)
            self.after(CAR_ANIMATION_DELAY, self.animate_car2_up, steps - 1)

    def animate_car2_down(self, steps):
        """Animate the car moving down slowly until it reaches the starting point."""
        car_coords = self.canvas.coords(self.car_id2)
        if car_coords[1] < 700 and steps > 0:  # Ensure car doesn't move down below starting point
            self.canvas.move(self.car_id2, 0, CAR_MOVE_STEP)
            self.after(200, self.animate_car2_down, steps - 1)

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