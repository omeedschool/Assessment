import tkinter as tk
from tkinter import ttk
import random
from threading import Timer

# Constants
RESOLUTION = 1000, 800  # Resolution of the game window
ANIMATION_DELAY = 40  # Delay in milliseconds for animation
LINE_STEP = 10  # Rate at which the road moves
CAR_MOVE_STEP = 5  # Step size for car movement
CAR_UP_TOTAL_MOVE, CAR_DOWN_TOTAL_MOVE = 50, 50
NORMAL_TEXT_FONT = ("Terminal", 18)  # Font for normal text
TITLE_TEXT_FONT = ("Terminal", 20)  # Font for title text
FINAL_SCORE = 2  # The score needed to win the game

class Player:
    """Class to represent a player in the game."""
    def __init__(self, game, car_image_file, car_side_image_file, car_start_x, car_start_y, keys,  name):
        self.game = game
        self.car_image = tk.PhotoImage(file=car_image_file)
        self.car_side_image = tk.PhotoImage(file=car_side_image_file)
        self.player_car = self.game.right_canvas.create_image(car_start_x, car_start_y, image=self.car_image, tag="car")
        self.score = 0
        self.score_label = None
        self.question_label = None
        self.answer_labels = []
        self.correct_answer = None
        self.keys = keys
        self.name = name

        # bind keys
        for index, key in enumerate(keys):
            self.game.bind(f"<{keys[index]}>", lambda event, idx=index: self.check_answer(idx))

    def create_player_frame(self, frame_x, frame_y):
        """Creates a frame for the player with questions and answers."""
        player_frame = tk.Canvas(self.game.left_canvas, relief="solid", borderwidth=5)
        player_frame.place(x=frame_x, y=frame_y, anchor=tk.CENTER, width=500, height=300)

        self.question_label = tk.Label(player_frame, text="", font=NORMAL_TEXT_FONT)
        self.question_label.place(relx=0.5, rely=0.20, anchor=tk.CENTER)

        # Side car image for Player
        player_frame.create_image(150, 150, anchor=tk.NW, image=self.car_side_image)

        # Answer labels for Player
        self.answer_labels = [
            tk.Label(player_frame, text="", font=NORMAL_TEXT_FONT),
            tk.Label(player_frame, text="", font=NORMAL_TEXT_FONT),
            tk.Label(player_frame, text="", font=NORMAL_TEXT_FONT),
            tk.Label(player_frame, text="", font=NORMAL_TEXT_FONT)
        ]

        # Place answer labels
        for i, label in enumerate(self.answer_labels):
            label.place(relx=0.20*(i+1), rely=0.35, anchor=tk.CENTER)

        # Player score label
        self.score_label = tk.Label(player_frame, text=f"Score: {self.score}", font=NORMAL_TEXT_FONT)
        self.score_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    def generate_question(self, difficulty):
        """Generate a new math question and display it for the player."""
        self.difficulty = difficulty

        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)

        if difficulty == "easy":
            self.correct_answer = num1 + num2
            current_question = f"What is {num1} + {num2}?"

        elif difficulty == "medium":
            chosen_operation = random.choice(("+", "-"))
            if chosen_operation == "+":
                self.correct_answer = num1 + num2
            elif chosen_operation == "-":
                self.correct_answer = num1 - num2
            current_question = f"What is {num1} {chosen_operation} {num2}?"
        
        elif difficulty == "hard":
            chosen_operation = random.choice(("+", "-", "*"))
            if chosen_operation == "+":
                self.correct_answer = num1 + num2
            elif chosen_operation == "-":
                self.correct_answer = num1 - num2
            elif chosen_operation == "*":
                self.correct_answer = num1 * num2
            elif chosen_operation == "/":
                self.correct_answer = num1 / num2
            current_question = f"What is {num1} {chosen_operation} {num2}?"

        # Generate answer options
        answers = [self.correct_answer]
        while len(answers) < 4:
            wrong_answer = random.randint(-20, 20)
            if wrong_answer not in answers:
                answers.append(wrong_answer)

        random.shuffle(answers)

        # Update the question and answers on the GUI
        self.question_label.config(text=current_question)
        for i, label in enumerate(self.answer_labels):
            label.config(text=f"{self.keys[i]}: {answers[i]}")
            label.answer_value = answers[i]

    def check_answer(self, index):
        """Check if the selected answer is correct."""
        if self.answer_labels[index].answer_value == self.correct_answer:
            self.score += 1  # Increase score on correct answer
            if self.score == FINAL_SCORE:
                self.game.winner = self.name
                self.game.end_game()
            else:
                self.animate_car_up(CAR_UP_TOTAL_MOVE // CAR_MOVE_STEP)  # Move the car up with animation
        elif self.score > 0:
            self.animate_car_down(CAR_DOWN_TOTAL_MOVE // CAR_MOVE_STEP)  # Move the car down slowly
            self.score -= 1  # Decrease score on incorrect answer

        self.score_label.config(text=f"Score: {self.score}")  # Update score label
        self.generate_question(self.difficulty)  # Generate a new question

    def animate_car_up(self, steps):
        """Animate the car moving up in steps."""
        if steps > 0:
            self.game.right_canvas.move(self.player_car, 0, -CAR_MOVE_STEP)  # Move the car up
            self.game.after(ANIMATION_DELAY, self.animate_car_up, steps - 1)  # Continue animation

    def animate_car_down(self, steps):
        """Animate the car moving down slowly until it reaches the starting point."""
        car_coords = self.game.right_canvas.coords(self.player_car)
        if car_coords[1] < 700 and steps > 0:  # Ensure car doesn't move down below starting point
            self.game.right_canvas.move(self.player_car, 0, CAR_MOVE_STEP)  # Move the car down
            self.game.after(200, self.animate_car_down, steps - 1)  # Continue animation

class Game(tk.Tk):
    """Main game application class."""
    
    def __init__(self):
        super().__init__()
        self.title("Trivia Turbo")

        # Center the game window on the screen
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        position_right = (screen_width - RESOLUTION[0]) // 2
        position_down = (screen_height - RESOLUTION[1]) // 2
        self.geometry(f"{RESOLUTION[0]}x{RESOLUTION[1]}+{position_right}+{position_down}")
        self.resizable(False, False)
        
        # Create the left canvas
        self.left_canvas = tk.Canvas(self, width=600, height=800)
        self.left_canvas.place(x=0, y=0)
        self.bg_image_photo = tk.PhotoImage(file="cars/background.png")
        self.bg_image = self.left_canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image_photo)

        # Create the right canvas
        self.right_canvas = tk.Canvas(self, width=400, height=800)
        self.right_canvas.place(x=600, y=0)

        # Title Label
        self.title_label = tk.Label(self.left_canvas, text="Trivia Turbo", font=TITLE_TEXT_FONT, background="#ef476f", borderwidth=3, relief="solid", padx=50, pady=5)
        self.title_label.place(x=300, y=50, anchor=tk.CENTER)
        
        # Initialize login screen
        self.show_login_screen()
        
        self.load_carscroll()  # Load the cars and scrolling background
        self.create_moving_lines()  # Create the moving lines

        self.mainloop()

    def show_login_screen(self):
        """Display the login screen."""
        self.geometry("1000x800")
        self.resizable(False, False)

        # Clear previous widgets from left canvas
        self.clear_canvas_widgets()

        # Create a login frame on the left canvas
        login_frame = tk.Frame(self.left_canvas, bg="white", padx=100)
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Username label and entry
        username_label = tk.Label(login_frame, text="Username:", font=NORMAL_TEXT_FONT, bg="white")
        username_label.pack(pady=10)
        self.username_entry = tk.Entry(login_frame, font=NORMAL_TEXT_FONT)
        self.username_entry.pack(pady=10)

        # Password label and entry
        password_label = tk.Label(login_frame, text="Password:", font=NORMAL_TEXT_FONT, bg="white")
        password_label.pack(pady=10)
        self.password_entry = tk.Entry(login_frame, show="*", font=NORMAL_TEXT_FONT)
        self.password_entry.pack(pady=10)

        # Login button
        login_button = tk.Button(login_frame, text="Login", font=NORMAL_TEXT_FONT, command=self.check_login)
        login_button.pack(pady=20)

    def check_login(self):
        """Check the user's login credentials."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if the credentials are correct (you can replace this with a more secure check)
        if username == "" and password == "":
            self.show_difficulty_selection()
        else:
            error_label = tk.Label(self.left_canvas, text="Invalid, please try again.", font=NORMAL_TEXT_FONT, fg="red", bg="white")
            error_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    def show_difficulty_selection(self):
        """Show the difficulty selection menu."""
        # Clear previous widgets from left canvas
        self.clear_canvas_widgets()

        # Create difficulty selection frame on the left canvas
        difficulty_frame = tk.Frame(self.left_canvas, bg="white", padx=50)
        difficulty_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Difficulty selection label
        difficulty_label = tk.Label(difficulty_frame, text="Select Difficulty", font=TITLE_TEXT_FONT, bg="white")
        difficulty_label.pack(pady=20)

        # Buttons for selecting difficulty
        easy_button = tk.Button(difficulty_frame, text="Easy", font=NORMAL_TEXT_FONT, command=lambda: self.start_game("easy"))
        medium_button = tk.Button(difficulty_frame, text="Medium", font=NORMAL_TEXT_FONT, command=lambda: self.start_game("medium"))
        hard_button = tk.Button(difficulty_frame, text="Hard", font=NORMAL_TEXT_FONT, command=lambda: self.start_game("hard"))

        easy_button.pack(pady=10)
        medium_button.pack(pady=10)
        hard_button.pack(pady=10)

    def start_game(self, difficulty):
        """Start the game by removing the difficulty selection screen and displaying the game screen."""
        self.difficulty = difficulty  # Store selected difficulty

        self.clear_canvas_widgets()  # Remove all widgets from the left canvas

        # Initialize game elements
        self.winner = None

        self.player1 = Player(self, "cars\car1.png", "cars\carside1.png", 175, 1000, ("q", "w", "e", "r"), "Player 1")
        self.player1.create_player_frame(300, 250)
        self.player1.generate_question(self.difficulty)

        self.player2 = Player(self, "cars\car2.png", "cars\carside2.png", 225, 1000, ("u", "i", "o", "p"), "Player 2")
        self.player2.create_player_frame(300, 600)
        self.player2.generate_question(self.difficulty)

        #(125, 700), (175, 700), (225, 700), (275, 700)

        self.start_animation()

    def start_animation(self):
        for car in self.right_canvas.find_withtag("car"):
            x1, y1 = self.right_canvas.coords(car)
            self.right_canvas.move(car, 0, -10)  # Move the car up
        
        if y1 > 700:
            self.after(ANIMATION_DELAY, self.start_animation)

    def clear_canvas_widgets(self):
        """Remove all widgets from the left_canvas."""
        for widget in self.left_canvas.winfo_children():
            widget.destroy()

    def load_carscroll(self):
        """Load the scrolling background and cars."""
        # Create road and grass rectangles
        self.right_canvas.create_rectangle(100, 0, 300, 800, fill="grey")
        self.right_canvas.create_rectangle(0, 0, 100, 800, fill="green")
        self.right_canvas.create_rectangle(300, 0, 400, 800, fill="green")

        # Closing rectangles
        self.left_closing_bar = self.right_canvas.create_rectangle(0, 0, 0, 800, fill="black", tags="closing_bar")
        self.right_closing_bar = self.right_canvas.create_rectangle(400, 0, 400, 800, fill="black", tags="closing_bar")

        # Create finish line and place off screen
        for i in range (0, 20):
            x = i * 10
            y = -100 # offset the finish line by 100
            if i % 2:
                self.right_canvas.create_rectangle(100 + x, 0 + y, 110 + x, 10 + y, fill="white", tags="finish_line")
                self.right_canvas.create_rectangle(100 + x, 10 + y, 110 + x, 20 + y, fill="black", tags="finish_line")
            if i % 2 == 0:
                self.right_canvas.create_rectangle(100 + x, 0 + y, 110 + x, 10 + y, fill="black", tags="finish_line")
                self.right_canvas.create_rectangle(100 + x, 10 + y, 110 + x, 20 + y, fill="white", tags="finish_line")

    def create_moving_lines(self):
        """Create the moving lines on the road."""
        # Create lines with tags
        for x in [150, 200, 250]:
            for y in range(50, RESOLUTION[1] + 50, 100):
                line_id = self.right_canvas.create_line(x, y, x, y + 50, fill="white", tags="moving_lines")

        # Start the movement of the lines
        self.move_lines()

    def move_lines(self):
        """Move all lines with the tag 'moving_lines'."""
        for line_id in self.right_canvas.find_withtag("moving_lines"):
            x1, y1, x2, y2 = self.right_canvas.coords(line_id)
            if y1 < RESOLUTION[1]:
                self.right_canvas.move(line_id, 0, LINE_STEP)  # Move the line down
            else:
                # Reset the line's position to the top
                self.right_canvas.coords(line_id, x1, 0, x2, 50)
        # Continue moving lines
        self.after(ANIMATION_DELAY, self.move_lines)  # Update

    def end_game(self):
        """Initiates the end sequence of the game."""
        self.end_game_animation()
        self.game_winner = self.winner
        print(self.game_winner)

    def end_game_animation(self):
        """Initiates the end sequence animation of the game"""
        self.move_amount = 10

        for car in self.right_canvas.find_withtag("car"):
            self.right_canvas.move(car, 0, -self.move_amount)  # Move the car up
            x1, y1 = self.right_canvas.coords(car)
            if y1 == -2000:
                self.right_canvas.coords(car, x1, 900)

        for square_id in self.right_canvas.find_withtag("finish_line"):
            x1, y1, x2, y2 = self.right_canvas.coords(square_id)
            self.right_canvas.move(square_id, 0, LINE_STEP)

        self.after(ANIMATION_DELAY, self.end_game_animation) # Continue animation

game = Game()  # Create and start the game