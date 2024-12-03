import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk


class BauCuaGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Bầu Cua Game")

        # List of symbols representing the dice faces
        self.symbols = ["Cá", "Cua", "Gà", "Bầu", "Hươu", "Tôm"]
        self.image_paths = {
            "Cá": "fish.png",  # Replace with actual image paths
            "Cua": "crab.png",  # Replace with actual image paths
            "Gà": "chicken.png",  # Replace with actual image paths
            "Bầu": "gourd.png",  # Replace with actual image paths
            "Hươu": "deer.png",  # Replace with actual image paths
            "Tôm": "lobster.png"  # Replace with actual image paths
        }

        # Load images
        self.images = {symbol: Image.open(path) for symbol, path in self.image_paths.items()}
        self.images = {symbol: ImageTk.PhotoImage(img.resize((200, 200))) for symbol, img in self.images.items()}

        # User's current bet and balance
        self.amount_spent = 0
        self.current_bet = None
        self.balance = 100000  # Starting balance

        # Game statistics tracking
        self.total_bets_placed = 0
        self.total_games_played = 0
        self.total_won = 0
        self.total_lost = 0

        # Create the GUI components
        self.balance_label = tk.Label(root, text=f"Balance: {self.balance}", font=("Arial", 14))
        self.balance_label.grid(row=0, column=0, pady=10, padx=10)

        self.result_label = tk.Label(root, text="Make your bet and roll!", font=("Arial", 16))
        self.result_label.grid(row=1, column=0, columnspan=3, pady=10)

        # Frame for the symbol buttons (to organize them in rows)
        self.symbol_frame = tk.Frame(root)
        self.symbol_frame.grid(row=2, column=0, columnspan=3, pady=20)

        # Buttons for each symbol, placed in two rows
        self.symbol_buttons = {}
        # First row (Hươu, Bầu, Gà)
        self.symbol_buttons["Hươu"] = tk.Button(self.symbol_frame, text="Hươu", font=("Arial", 14),
                                                 command=lambda s="Hươu": self.set_bet(s), image=self.images["Hươu"],
                                                 compound=tk.TOP)
        self.symbol_buttons["Hươu"].grid(row=0, column=0, padx=5)

        self.symbol_buttons["Bầu"] = tk.Button(self.symbol_frame, text="Bầu", font=("Arial", 14),
                                                command=lambda s="Bầu": self.set_bet(s), image=self.images["Bầu"],
                                                compound=tk.TOP)
        self.symbol_buttons["Bầu"].grid(row=0, column=1, padx=5)

        self.symbol_buttons["Gà"] = tk.Button(self.symbol_frame, text="Gà", font=("Arial", 14),
                                               command=lambda s="Gà": self.set_bet(s), image=self.images["Gà"],
                                               compound=tk.TOP)
        self.symbol_buttons["Gà"].grid(row=0, column=2, padx=5)

        # Second row (Cá, Cua, Tôm)
        self.symbol_buttons["Cá"] = tk.Button(self.symbol_frame, text="Cá", font=("Arial", 14),
                                               command=lambda s="Cá": self.set_bet(s), image=self.images["Cá"],
                                               compound=tk.TOP)
        self.symbol_buttons["Cá"].grid(row=1, column=0, padx=5)

        self.symbol_buttons["Cua"] = tk.Button(self.symbol_frame, text="Cua", font=("Arial", 14),
                                                command=lambda s="Cua": self.set_bet(s), image=self.images["Cua"],
                                                compound=tk.TOP)
        self.symbol_buttons["Cua"].grid(row=1, column=1, padx=5)

        self.symbol_buttons["Tôm"] = tk.Button(self.symbol_frame, text="Tôm", font=("Arial", 14),
                                                command=lambda s="Tôm": self.set_bet(s), image=self.images["Tôm"],
                                                compound=tk.TOP)
        self.symbol_buttons["Tôm"].grid(row=1, column=2, padx=5)

        # Entry for customizable bet amount
        self.bet_label = tk.Label(root, text="Enter your bet amount:", font=("Arial", 12))
        self.bet_label.grid(row=3, column=0, pady=10, padx=10)

        self.bet_entry = tk.Entry(root, font=("Arial", 14))
        self.bet_entry.grid(row=3, column=1, pady=10)

        # Roll button
        self.roll_button = tk.Button(root, text="Roll Dice", font=("Arial", 14), command=self.roll_dice)
        self.roll_button.grid(row=4, column=0, columnspan=3, pady=20)

        # Labels for dice roll result images
        self.dice_labels = [tk.Label(root) for _ in range(3)]
        for i, label in enumerate(self.dice_labels):
            label.grid(row=2, column=i + 3, padx=10)

    def set_bet(self, symbol):
        """Set the player's current bet."""
        self.current_bet = symbol
        self.result_label.config(text=f"You've bet on {symbol}. Enter your bet amount and click 'Roll Dice' to play!")

    def roll_dice(self):
        """Simulate the rolling of the dice and update balance."""
        if self.current_bet is None:
            self.result_label.config(text="Please place your bet before rolling!")
            return

        # Get the custom bet amount
        bet_amount_str = self.bet_entry.get()
        if not bet_amount_str.isdigit():
            self.result_label.config(text="Please enter a valid bet amount!")
            return

        bet_amount = int(bet_amount_str)

        if bet_amount <= 0 or bet_amount > self.balance:
            self.result_label.config(text="Bet amount must be a positive number and cannot exceed your balance!")
            return

        # Track total bets placed and total games played
        self.total_bets_placed += bet_amount
        self.total_games_played += 1

        # Randomly select 3 outcomes from the symbols
        roll_results = random.choices(self.symbols, k=3)

        # Update the dice labels with the rolled images
        for i, result in enumerate(roll_results):
            self.dice_labels[i].config(image=self.images[result])

        # Count how many times the player's bet appears
        occurrence_count = roll_results.count(self.current_bet)

        # Update balance based on win/loss
        if occurrence_count == 0:
            self.balance -= bet_amount  # Player loses the bet
            self.total_lost += bet_amount  # Add to total money lost
            result_message = f"Sorry! You lose. Dice rolled: {', '.join(roll_results)}"
        else:
            win_amount = occurrence_count * bet_amount
            self.balance += win_amount  # Player wins
            self.total_won += win_amount  # Add to total money won
            result_message = f"Congratulations! You win {win_amount} units. Dice rolled: {', '.join(roll_results)}"

        # Update the result label and the balance
        self.result_label.config(text=result_message)
        self.balance_label.config(text=f"Balance: {self.balance}")

        # Check for balance warning (if player runs out of money)
        if self.balance <= 0:
            messagebox.showinfo("Game Over", "You have run out of money! Game Over.")
            self.root.quit()

        # Print the statistics (for debugging or tracking purposes)
        print(f"Total Bets Placed: {self.total_bets_placed}")
        print(f"Total Games Played: {self.total_games_played}")
        print(f"Total Money Won: {self.total_won}")
        print(f"Total Money Lost: {self.total_lost}")


# Create the Tkinter window
root = tk.Tk()
game = BauCuaGame(root)
root.mainloop()
