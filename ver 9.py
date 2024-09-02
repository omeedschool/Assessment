import tkinter as tk
from tkinter import ttk
import random

# Constants
RESOLUTION = 1000, 800  # Resolution of the game window
ANIMATION_DELAY = 40  # Delay in milliseconds for animation
LINE_STEP = 10  # Rate at which the road moves
CAR_MOVE_STEP = 5  # Step size for car movement
CAR_UP_TOTAL_MOVE, CAR_DOWN_TOTAL_MOVE = 50, 50
NORMAL_TEXT_FONT = ("Terminal", 18)  # Font for normal text
TITLE_TEXT_FONT = ("Terminal", 30)  # Font for title text
FINAL_SCORE = 12  # The score needed to win the game

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
            error_label = tk.Label(self.left_canvas, text="Invalid credentials, please try again.", font=NORMAL_TEXT_FONT, fg="red", bg="white")
            error_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    def show_difficulty_selection(self):
        """Show the difficulty selection menu."""
        # Clear previous widgets from left canvas
        self.clear_canvas_widgets()

        # Create difficulty selection frame on the left canvas
        difficulty_frame = tk.Frame(self.left_canvas, bg="white", padx=100)
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
        self.player1_score = 0
        self.player2_score = 0

        # Create game canvas
        self.create_game_canvas()

        self.generate_question()
        self.generate_question_2()

    def clear_canvas_widgets(self):
        """Remove all widgets from the left_canvas."""
        for widget in self.left_canvas.winfo_children():
            widget.destroy()

    def create_game_canvas(self):
        """Create the canvas and layout for the game."""
        self.bg_image_photo = tk.PhotoImage(file="cars/background.png")
        self.bg_image = self.left_canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image_photo)

        # PLAYER 1 SECTION
        # Set up player 1 frame
        self.player1_frame = tk.Canvas(self.left_canvas, relief="solid", borderwidth=5)
        self.player1_frame.place(x=300, y=250, anchor=tk.CENTER, width=500, height=300)

        # Question label for Player 1
        self.question_label = tk.Label(self.player1_frame, text="", font=NORMAL_TEXT_FONT)
        self.question_label.place(relx=0.5, rely=0.20, anchor=tk.CENTER)

        # Side car image for Player 1
        self.side_car1_photo = tk.PhotoImage(file="cars/carside1.png")
        self.bg_image = self.player1_frame.create_image(150, 150, anchor=tk.NW, image=self.side_car1_photo)

        # Answer labels for Player 1
        self.answer_labels = [
            tk.Label(self.player1_frame, text="", font=NORMAL_TEXT_FONT),
            tk.Label(self.player1_frame, text="", font=NORMAL_TEXT_FONT),
            tk.Label(self.player1_frame, text="", font=NORMAL_TEXT_FONT),
            tk.Label(self.player1_frame, text="", font=NORMAL_TEXT_FONT)
        ]
                
        # Place answer labels for Player 1
        for i, label in enumerate(self.answer_labels):
            label.place(relx=0.20*(i+1), rely=0.35, anchor=tk.CENTER)

        # Player 1 score label
        self.player1_score_label = tk.Label(self.player1_frame, text=f"Score: {self.player1_score}", font=NORMAL_TEXT_FONT)
        self.player1_score_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        # PLAYER 2 SECTION
        # Set up player 2 frame
        self.player2_frame = tk.Canvas(self.left_canvas, relief="solid", borderwidth=5)
        self.player2_frame.place(x=300, y=600, anchor=tk.CENTER, width=500, height=300)

        # Question label for Player 2
        self.question_label_2 = tk.Label(self.player2_frame, text="", font=NORMAL_TEXT_FONT)
        self.question_label_2.place(relx=0.5, rely=0.20, anchor=tk.CENTER)

        # Side car image for Player 2
        self.side_car2_photo = tk.PhotoImage(file="cars/carside2.png")
        self.bg_image = self.player2_frame.create_image(150, 150, anchor=tk.NW, image=self.side_car2_photo)

        # Answer labels for Player 2
        self.answer_labels_2 = [
            tk.Label(self.player2_frame, text="", font=NORMAL_TEXT_FONT),
            tk.Label(self.player2_frame, text="", font=NORMAL_TEXT_FONT),
            tk.Label(self.player2_frame, text="", font=NORMAL_TEXT_FONT),
            tk.Label(self.player2_frame, text="", font=NORMAL_TEXT_FONT)
        ]

        # Place answer labels for Player 2
        for i, label in enumerate(self.answer_labels_2):
            label.place(relx=0.20*(i+1), rely=0.35, anchor=tk.CENTER)

        # Player 2 score label
        self.player2_score_label = tk.Label(self.player2_frame, text=f"Score: {self.player2_score}", font=NORMAL_TEXT_FONT)
        self.player2_score_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        # BINDINGS
        # PLAYER 1
        # Bind keys to answer checking function for Player 1
        self.bind("<q>", lambda event: self.check_answer(0))
        self.bind("<w>", lambda event: self.check_answer(1))
        self.bind("<e>", lambda event: self.check_answer(2))
        self.bind("<r>", lambda event: self.check_answer(3))

        # PLAYER 2
        # Bind keys to answer checking function for Player 2
        self.bind("<u>", lambda event: self.check_answer_2(0))
        self.bind("<i>", lambda event: self.check_answer_2(1))
        self.bind("<o>", lambda event: self.check_answer_2(2))
        self.bind("<p>", lambda event: self.check_answer_2(3))

        # Generate the first question for both players
        self.generate_question()
        self.generate_question_2()

    def load_carscroll(self):
        """Load the scrolling background and cars."""
        # Create road and grass rectangles
        self.right_canvas.create_rectangle(100, 0, 300, 800, fill="grey")
        self.right_canvas.create_rectangle(0, 0, 100, 800, fill="green")
        self.right_canvas.create_rectangle(300, 0, 400, 800, fill="green")

        # Load and display the car images
        self.car_image = tk.PhotoImage(file="cars/car1.png")
        self.car2_image = tk.PhotoImage(file="cars/car2.png")

        # Create car images on the right_canvas
        self.car_id = self.right_canvas.create_image(125, 700, image=self.car_image)
        self.car_id2 = self.right_canvas.create_image(175, 700, image=self.car2_image)
        #self.right_canvas.create_image(225, 700, image=self.car_image)
        #self.right_canvas.create_image(275, 700, image=self.car2_image)

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

    def generate_question(self):
        """Generate a new math question and display it for Player 1."""
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        self.current_question = f"What is {num1} + {num2}?"  # Formulate the question
        self.correct_answer = num1 + num2  # Calculate the correct answer

        # Generate answer options
        answers = [self.correct_answer]
        while len(answers) < 4:
            wrong_answer = random.randint(1, 20)
            if wrong_answer not in answers:
                answers.append(wrong_answer)

        random.shuffle(answers)  # Shuffle the answers

        self.question_label.config(text=self.current_question)  # Display the question
        for i, label in enumerate(self.answer_labels):
            label.config(text=f"{['Q', 'W', 'E', 'R'][i]}: {answers[i]}")
            label.answer_value = answers[i]  # Assign answer values to labels

    def generate_question_2(self):
        """Generate a new math question and display it for Player 2."""
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        self.current_question_2 = f"What is {num1} + {num2}?"  # Formulate the question
        self.correct_answer_2 = num1 + num2  # Calculate the correct answer

        # Generate answer options
        answers = [self.correct_answer_2]
        while len(answers) < 4:
            wrong_answer = random.randint(1, 20)
            if wrong_answer not in answers:
                answers.append(wrong_answer)

        random.shuffle(answers)  # Shuffle the answers

        self.question_label_2.config(text=self.current_question_2)  # Display the question
        for i, label in enumerate(self.answer_labels_2):
            label.config(text=f"{['U', 'I', 'O', 'P'][i]}: {answers[i]}")
            label.answer_value = answers[i]  # Assign answer values to labels

    def check_answer(self, index):
        """Check if the selected answer is correct for Player 1."""
        if self.answer_labels[index].answer_value == self.correct_answer:
            self.player1_score += 1  # Increase score on correct answer
            if self.player1_score == FINAL_SCORE:
                self.winner = "PLAYER 1"
                self.end_game()
            else:
                self.animate_car_up(CAR_UP_TOTAL_MOVE // CAR_MOVE_STEP)  # Move the car up with animation
        elif self.player1_score > 0:
            self.animate_car_down(CAR_DOWN_TOTAL_MOVE // CAR_MOVE_STEP)  # Move the car down slowly
            self.player1_score -= 1  # Decrease score on incorrect answer

        self.player1_score_label.config(text=f"Score: {self.player1_score}")  # Update score label
        self.generate_question()  # Generate a new question

    def check_answer_2(self, index):
        """Check if the selected answer is correct for Player 2."""
        if self.answer_labels_2[index].answer_value == self.correct_answer_2:
            self.player2_score += 1  # Increase score on correct answer
            if self.player2_score == FINAL_SCORE:
                self.winner = "PLAYER 2"
                self.end_game()
            else:
                self.animate_car2_up(CAR_UP_TOTAL_MOVE // CAR_MOVE_STEP)  # Move the car up with animation
        elif self.player2_score > 0:
            self.animate_car2_down(CAR_DOWN_TOTAL_MOVE // CAR_MOVE_STEP)  # Move the car down slowly
            self.player2_score -= 1  # Decrease score on incorrect answer

        self.player2_score_label.config(text=f"Score: {self.player2_score}")  # Update score label
        self.generate_question_2()  # Generate a new question

    def animate_car_up(self, steps):
        """Animate the car moving up in steps."""
        if steps > 0:
            self.right_canvas.move(self.car_id, 0, -CAR_MOVE_STEP)  # Move the car up
            self.after(ANIMATION_DELAY, self.animate_car_up, steps - 1)  # Continue animation

    def animate_car_down(self, steps):
        """Animate the car moving down slowly until it reaches the starting point."""
        car_coords = self.right_canvas.coords(self.car_id)
        if car_coords[1] < 700 and steps > 0:  # Ensure car doesn't move down below starting point
            self.right_canvas.move(self.car_id, 0, CAR_MOVE_STEP)  # Move the car down
            self.after(200, self.animate_car_down, steps - 1)  # Continue animation

    def animate_car2_up(self, steps):
        """Animate the car moving up in steps for Player 2."""
        if steps > 0:
            self.right_canvas.move(self.car_id2, 0, -CAR_MOVE_STEP)  # Move the car up
            self.after(ANIMATION_DELAY, self.animate_car2_up, steps - 1)  # Continue animation

    def animate_car2_down(self, steps):
        """Animate the car moving down slowly until it reaches the starting point for Player 2."""
        car_coords = self.right_canvas.coords(self.car_id2)
        if car_coords[1] < 700 and steps > 0:  # Ensure car doesn't move down below starting point
            self.right_canvas.move(self.car_id2, 0, CAR_MOVE_STEP)  # Move the car down
            self.after(200, self.animate_car2_down, steps - 1)  # Continue animation

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

    def clear_canvas_widgets(self):
        """Remove all widgets from the left_canvas."""
        for widget in self.left_canvas.winfo_children():
            widget.destroy()

    def end_game(self):
        """Initiates the end sequence of the game."""
        self.game_won = True
        self.end_game_animation()

    def end_game_animation(self):
        """Initiates the end sequence animation of the game"""
        self.move_amount = 10

        self.right_canvas.move(self.car_id, 0, -self.move_amount)  # Move the car up
        self.right_canvas.move(self.car_id2, 0, -self.move_amount) # Move the car up

        x1, y1 = self.right_canvas.coords(self.car_id)
        x2, y2 = self.right_canvas.coords(self.car_id2)

        if y1 == -2000:
            self.right_canvas.coords(self.car_id, 125, 900)
        if y2 == -2000:
            self.right_canvas.coords(self.car_id2, 175, 900)

        for square_id in self.right_canvas.find_withtag("finish_line"):
            x1, y1, x2, y2 = self.right_canvas.coords(square_id)
            self.right_canvas.move(square_id, 0, LINE_STEP)

        self.after(ANIMATION_DELAY, self.end_game_animation) # Continue animation

game = Game()  # Create and start the game