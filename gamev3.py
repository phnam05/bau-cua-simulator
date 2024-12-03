import random
import matplotlib.pyplot as plt
import numpy as np  # For calculating mean


class BauCuaGameSimulation:
    def __init__(self):
        # List of symbols representing the dice faces
        self.symbols = ["Cá", "Cua", "Gà", "Bầu", "Hươu", "Tôm"]
        self.balance = 1000  # Starting balance
        self.total_bets_placed = 0
        self.total_games_played = 1000  # Number of games to simulate
        self.total_won = 0
        self.total_lost = 0
        self.bet_amount = 1  # Fixed bet amount

    def simulate_game(self):
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

        return game_winnings

    def print_statistics(self):
        print(f"Total Bets Placed: {self.total_bets_placed}")
        print(f"Total Games Played: {self.total_games_played}")
        print(f"Total Money Won: {self.total_won}")
        print(f"Total Money Lost: {self.total_lost}")
        print(f"Ending Winnings: {self.total_won - self.total_lost}")


# Run the simulation 1000 times and record the winnings of each simulation
all_simulations_winnings = []

for i in range(1000):
    game_simulation = BauCuaGameSimulation()
    game_winnings = game_simulation.simulate_game()
    all_simulations_winnings.append(game_winnings)  # Store the winnings of each simulation

# Calculate the mean of the winnings
mean_winnings = np.mean(all_simulations_winnings)

# Plot the histogram of the winnings
plt.figure(figsize=(10, 6))
plt.hist(all_simulations_winnings, bins=30, color='skyblue', edgecolor='black')

# Add a vertical line at the mean
plt.axvline(mean_winnings, color='red', linestyle='dashed', linewidth=2)

# Display the mean value on the plot
plt.text(mean_winnings + 100, 50, f'Mean: {mean_winnings:.2f}', color='red', fontsize=12)

# Title and labels
plt.title("Histogram of Winnings from 1000 Simulations")
plt.xlabel("Winnings per Simulation")
plt.ylabel("Frequency")
plt.grid(True)

# Show the plot
plt.show()
