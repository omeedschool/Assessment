import tkinter as tk
import random
import json
import os

# Account Data
account_data_file = "account_data.json"

# Load existing account data if it exists, otherwise create an empty dictionary
if os.path.exists(account_data_file):
    with open(account_data_file, "r") as file:
        accounts = json.load(file)
else:
    accounts = {}

# Constants
RESOLUTION = 1000, 800  # Resolution of the game window.
ANIMATION_DELAY = 40  # Delay in milliseconds for animation.
LINE_STEP = 10  # Rate at which the road moves.
CAR_MOVE_STEP = 5  # Step size for car movement.
CAR_UP_TOTAL_MOVE, CAR_DOWN_TOTAL_MOVE = 50, 50
SMALL_TEXT_FONT = ("Terminal", 12)  # Font for small text.
NORMAL_TEXT_FONT = ("Terminal", 18)  # Font for normal text.
TITLE_TEXT_FONT = ("Terminal", 20)  # Font for title text.
FINAL_SCORE = 12  # The score needed to win the game.

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

    def game_won(self):
        if self.game.winner:
            return True
        else:
            return False

    def create_player_frame(self, frame_x, frame_y):
        """Creates a frame for the player with questions and answers."""
        self.frame_x, self.frame_y = frame_x, frame_y

        self.player_frame = tk.Canvas(self.game.left_canvas, relief="solid", borderwidth=5)
        self.player_frame.place(x=frame_x, y=frame_y, anchor=tk.CENTER, width=500, height=300)

        self.question_label = tk.Label(self.player_frame, text="", font=NORMAL_TEXT_FONT)
        self.question_label.place(relx=0.5, rely=0.20, anchor=tk.CENTER)

        # Side car image for Player
        self.player_frame.create_image(150, 150, anchor=tk.NW, image=self.car_side_image)

        # Answer labels for Player
        self.answer_labels = [
            tk.Label(self.player_frame, text="", font=NORMAL_TEXT_FONT),
            tk.Label(self.player_frame, text="", font=NORMAL_TEXT_FONT),
            tk.Label(self.player_frame, text="", font=NORMAL_TEXT_FONT),
            tk.Label(self.player_frame, text="", font=NORMAL_TEXT_FONT)
        ]

        # Place answer labels
        for i, label in enumerate(self.answer_labels):
            label.place(relx=0.20*(i+1), rely=0.35, anchor=tk.CENTER)

        # Player score label
        self.score_label = tk.Label(self.player_frame, text=f"Score: {self.score}", font=NORMAL_TEXT_FONT)
        self.score_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    def generate_question(self, difficulty):
        """Generate a new math question and display it for the player."""
        if self.game_won():
            return

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
        if self.game_won():
            return

        if self.answer_labels[index].answer_value == self.correct_answer:
            self.score += 1  # Increase score on correct answer
            if self.score == FINAL_SCORE:
                self.game.winner = self.name
                self.animate_car_up(CAR_UP_TOTAL_MOVE // CAR_MOVE_STEP)  # Move the car up with animation
                self.game.end_game()
            else:
                self.animate_car_up(CAR_UP_TOTAL_MOVE // CAR_MOVE_STEP)  # Move the car up with animation
        elif self.score > 0:
            self.animate_car_down(CAR_DOWN_TOTAL_MOVE // CAR_MOVE_STEP)  # Move the car down slowly
            self.score -= 1  # Decrease score on incorrect answer

        # Check if the score_label exists before updating
        if self.score_label.winfo_exists():
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

    def hide_frame(self):
        """Hide the player's frame."""
        if self.player_frame:
            self.player_frame.place_forget()

    def show_frame(self):
        """Show the player's frame."""
        if self.player_frame:
            self.player_frame.place(x=self.frame_x, y=self.frame_y, anchor=tk.CENTER, width=500, height=300)

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
        
        # Initialize variables to hold references to the labels
        self.error_label = None
        self.success_label = None
        
        self.load_carscroll()  # Load the cars and scrolling background
        self.create_moving_lines()  # Create the moving lines

        self.npc_movement()

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
        login_button.pack(pady=(10, 0))

        signup_button = tk.Button(login_frame, text="Sign Up", font=NORMAL_TEXT_FONT, command=self.create_login)
        signup_button.pack(pady=10)

    def remove_existing_labels(self):
        """Remove existing error or success labels if they exist."""
        if self.error_label:
            self.error_label.destroy()
            self.error_label = None
        if self.success_label:
            self.success_label.destroy()
            self.success_label = None

    def check_login(self):
        """Check the user's login credentials."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Remove any existing labels before showing a new one
        self.remove_existing_labels()

        # Check if the credentials are correct
        if username in accounts and accounts[username] == password:
            self.show_difficulty_selection()
        else:
            self.error_label = tk.Label(self.left_canvas, text="Invalid username or password, please try again.", font=SMALL_TEXT_FONT, fg="red", bg="white")
            self.error_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    def create_login(self):
        """Create a new account."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Remove any existing labels before showing a new one
        self.remove_existing_labels()

        if username in accounts:
            self.error_label = tk.Label(self.left_canvas, text="Username already exists, please choose another.", font=SMALL_TEXT_FONT, fg="red", bg="white")

        if not username.isalpha():
            self.error_label = tk.Label(self.left_canvas, text="Username may only contain letters", font=SMALL_TEXT_FONT, fg="red", bg="white")

        if len(username) < 3:
            self.error_label = tk.Label(self.left_canvas, text="Username must at least 3 characters.", font=SMALL_TEXT_FONT, fg="red", bg="white")

        if not password or not username:
            self.error_label = tk.Label(self.left_canvas, text="Please enter a username and password", font=SMALL_TEXT_FONT, fg="red", bg="white")


        if self.error_label:
            self.error_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
        else:
            accounts[username] = password
            with open(account_data_file, "w") as file:
                json.dump(accounts, file)
            self.success_label = tk.Label(self.left_canvas, text="Account created successfully!", font=SMALL_TEXT_FONT, fg="green", bg="white")
            self.success_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    def show_difficulty_selection(self):
        """Show the difficulty selection menu."""
        self.game_running = True
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

    def countdown(self, seconds):
        """Countdown from a given number of seconds."""
        if seconds > 0:
            self.countdown_label.config(text=str(seconds))
            self.after(1000, self.countdown, seconds - 1)  # Schedule next countdown tick using after
        else:
            # After countdown, show frames and generate questions
            self.countdown_frame.destroy()

            self.player1.show_frame()
            self.player2.show_frame()

            self.player1.generate_question(self.difficulty)
            self.player2.generate_question(self.difficulty)

    def start_game(self, difficulty):
        """Start the game by removing the difficulty selection screen and displaying the game screen."""
        self.difficulty = difficulty  # Store selected difficulty

        self.clear_canvas_widgets()  # Remove all widgets from the left canvas

        # Initialize game elements
        self.winner = None

        self.player1 = Player(self, "cars/car1.png", "cars/carside1.png", 175, 1000, ("q", "w", "e", "r"), "Player 1")
        self.player1.create_player_frame(300, 250)

        self.player2 = Player(self, "cars/car2.png", "cars/carside2.png", 225, 1000, ("u", "i", "o", "p"), "Player 2")
        self.player2.create_player_frame(300, 600)

        #(125, 700), (175, 700), (225, 700), (275, 700)
        
        self.start_animation()

        # Hide player frames initially
        self.player1.hide_frame()
        self.player2.hide_frame()

        self.countdown_frame = tk.Canvas(self.left_canvas, relief="solid", borderwidth=5)
        self.countdown_frame.place(x=300, y=400, anchor=tk.CENTER, width=500, height=700)

        self.countdown_label = tk.Label(self.countdown_frame, text="3", font=("Terminal", 200), foreground="Red")
        self.countdown_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.countdown(3)

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
        self.game_running = False

        for car in self.right_canvas.find_withtag("car"):
            self.right_canvas.addtag_withtag("npc", car)
            self.right_canvas.dtag(car, "car")

        self.end_game_animation()

        # Clear previous widgets
        self.clear_canvas_widgets()

        # Create the end game frame
        self.end_frame = tk.Canvas(self.left_canvas, relief="solid", borderwidth=5)
        self.end_frame.place(x=300, y=400, anchor=tk.CENTER, width=500, height=600)

        # Display the winner's name
        self.winner_label = tk.Label(self.end_frame, text=f"{self.winner} Won!", font=NORMAL_TEXT_FONT)
        self.winner_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        # Load and display the winner's side car image
        if self.winner == "Player 1":
            winner_car_image_file = "cars/carside1.png"
            score = self.player1.score
        elif self.winner == "Player 2":
            winner_car_image_file = "cars/carside2.png"
            score = self.player2.score

        self.score_label = tk.Label(self.end_frame, text=f"Score: {score}", font=NORMAL_TEXT_FONT)
        self.score_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        winner_car_image = tk.PhotoImage(file=winner_car_image_file)
        self.end_frame.create_image(150, 200, anchor=tk.NW, image=winner_car_image)

        # Keep a reference to prevent garbage collection
        self.end_frame.image = winner_car_image

        self.play_again_label = tk.Label(self.end_frame, text=f"Play Again?", font=NORMAL_TEXT_FONT)
        self.play_again_label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.yes_button = tk.Button(self.end_frame, text="Yes", font=NORMAL_TEXT_FONT, command=lambda: self.show_difficulty_selection())
        self.yes_button.place(relx=0.4, rely=0.7, anchor=tk.CENTER)

        self.no_button = tk.Button(self.end_frame, text="No", font=NORMAL_TEXT_FONT, command=lambda: self.destroy())
        self.no_button.place(relx=0.6, rely=0.7, anchor=tk.CENTER)

    def end_game_animation(self):
        """Initiates the end sequence animation of the game."""
        # Ensure we don't create multiple animations
        self.right_canvas.delete("finish_line")

        # Recreate finish line for animation
        for i in range(0, 20):
            x = i * 10
            y = -100  # offset the finish line by 100
            if i % 2:
                self.right_canvas.create_rectangle(100 + x, 0 + y, 110 + x, 10 + y, fill="white", tags="finish_line")
                self.right_canvas.create_rectangle(100 + x, 10 + y, 110 + x, 20 + y, fill="black", tags="finish_line")
            if i % 2 == 0:
                self.right_canvas.create_rectangle(100 + x, 0 + y, 110 + x, 10 + y, fill="black", tags="finish_line")
                self.right_canvas.create_rectangle(100 + x, 10 + y, 110 + x, 20 + y, fill="white", tags="finish_line")

        self.move_amount = 10
        self.animate_finish_line()

    def animate_finish_line(self):
        """Animate the finish line moving up."""
        for square_id in self.right_canvas.find_withtag("finish_line"):
            x1, y1, x2, y2 = self.right_canvas.coords(square_id)
            if y1 < RESOLUTION[1]:  # Continue animation if not reached end
                self.right_canvas.move(square_id, 0, LINE_STEP)
            else:
                self.right_canvas.delete(square_id)  # Remove the finish line if it reaches the end

        if self.right_canvas.find_withtag("finish_line"):
            self.after(ANIMATION_DELAY, self.animate_finish_line)  # Continue animation if finish lines remain
    
    def npc_movement(self):
        for val, car in enumerate(self.right_canvas.find_withtag("npc")):
            self.right_canvas.move(car, 0, -10)  # Move the car up
            x1, y1 = self.right_canvas.coords(car)
            if y1 == -2000:
                self.right_canvas.coords(car, random.choice([125, 275]), 900)

        self.after(ANIMATION_DELAY, self.npc_movement)  # Continue animation

game = Game()  # Create and start the game