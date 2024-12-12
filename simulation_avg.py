import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np  # For calculating mean


class BauCuaGameSimulation:
    def __init__(self):
        # List of symbols representing the dice faces
        self.symbols = ["Cá", "Cua", "Gà", "Bầu", "Hươu", "Tôm"]
        self.balance = 1000  # Starting balance
        self.total_bets_placed = 0
        # self.total_games_played = 10000  # Number of games to simulate
        self.total_won = 0
        self.total_lost = 0
        self.bet_amount = 1  # Fixed bet amount

    def simulate_game(self, total_games_played):
        self.total_games_played = total_games_played
        # Store the winnings for each game played
        game_winnings = 0

        for _ in range(self.total_games_played):
            # Randomly select a symbol to bet on
            current_bet = random.choice(self.symbols)

            # Update total bets placed
            self.total_bets_placed += self.bet_amount

            # Randomly select 3 outcomes from the symbols to simulate the dice roll
            roll_results = random.choices(self.symbols, k=3)

            # Count how many times the player's bet appears in the roll results
            occurrence_count = roll_results.count(current_bet)

            # Update balance based on win/loss
            if occurrence_count == 0:
                self.balance -= self.bet_amount  # Player loses the bet
                self.total_lost += self.bet_amount  # Add to total money lost
                game_winnings -= self.bet_amount  # Record the loss
            else:
                win_amount = occurrence_count * self.bet_amount
                self.balance += win_amount  # Player wins
                self.total_won += win_amount  # Add to total money won
                game_winnings += win_amount  # Record the win

        return game_winnings/total_games_played

    def print_statistics(self):
        print(f"Total Bets Placed: {self.total_bets_placed}")
        print(f"Total Games Played: {self.total_games_played}")
        print(f"Total Money Won: {self.total_won}")
        print(f"Total Money Lost: {self.total_lost}")
        print(f"Ending Winnings: {self.total_won - self.total_lost}")
        print(f"Average Winning per Game:{(self.total_won - self.total_lost)/self.total_games_played}")
        print("-"*50)

def draw_ev():
    # Run the simulation 1000 times and record the winnings of each simulation
    all_simulations_winnings = []
    max_nummber_bets = 10000 

    for i in range(1, max_nummber_bets):
        game_simulation = BauCuaGameSimulation()
        game_winnings = game_simulation.simulate_game(i)
        all_simulations_winnings.append(game_winnings)  # Store the winnings of each simulation
        # game_simulation.print_statistics()

    # Calculate the mean of the winnings
    # mean_winnings = np.mean(all_simulations_winnings)

    moving_data = pd.Series(all_simulations_winnings).rolling(window=10).mean()
    # Plot the histogram of the winnings
    plt.figure(figsize=(10, 6))
    plt.plot(moving_data)
    
    ev_value = -17/216
    plt.axhline(ev_value, color='red', linestyle='dashed', linewidth=2)
    
    # Display the mean value on the plot
    plt.text(max_nummber_bets - 2000, -0.06, f'EV: {ev_value:.4f}', color='red', fontsize=12)

    # Title and labels
    plt.xlabel("Number of bets")
    plt.ylabel("Average winnings per bet")
    plt.grid(True)

    # Show the plot
    plt.show()

draw_ev()