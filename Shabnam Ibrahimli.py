import pandas as pd
import matplotlib.pyplot as plt

filename = 'dart_hits.csv'
try:
    df = pd.read_csv(filename, header = None, names = ['player', 'x', 'y'])
except FileNotFoundError:
    print('File', filename, 'not found.')
    exit()

def main_menu():
    while True:
        print('Choose an option:')
        print('1. Plots')
        print('2. Analyse Data')
        print('3. Exit')
        user_input = input('Enter your choice: ')
        if user_input == '1':
            second_menu()
        elif user_input == '2':
            data_analysis()
        elif user_input == '3':
            print('Exiting...')
            break
        else:
            print('Invalid choice. Please try again.')

def second_menu():
    while True:
        print('Choose an option:')
        print('1. Scatter plot for Player 1')
        print('2. Scatter plot for Player 2')
        print('3. Scatter plot for Player 3')
        print('4. Scatter plot for all three players')
        print('5. Stacked bar chart showing score distribution for each player')
        print('6. Go back')
        user_input = input('Enter your choice: ')
        if user_input == '6':
            break
        else:
            function_menu(user_input)

def function_menu(user_input):
    if user_input == '1':
        scatter_plot(1)
    elif user_input == '2':
        scatter_plot(2)
    elif user_input == '3':
        scatter_plot(3)
    elif user_input == '4':
        all_scatter_plot()
    elif user_input == '5':
        bar_chart()
    else:
        print('ERROR in input. Please try again.')

def scatter_plot(player):
    data_player = df[df['player'] == player]
    plt.scatter(data_player['x'], data_player['y'], label = f'Player {player}', color = 'black', marker = '+')
    plt.xlim(-4, 4)
    plt.ylim(-4, 4)
    plt.gca().spines['bottom'].set_position('zero')
    plt.gca().spines['left'].set_position('zero')
    plt.gca().spines['bottom'].set_color('blue')
    plt.gca().spines['left'].set_color('blue')
    plt.gca().spines['right'].set_color('none') 
    plt.gca().spines['top'].set_color('none') 
    plt.title(f'Dart Hits for Player {player}', color='red')
    plt.text(3.9, -0.7, 'x', color='blue') 
    plt.text(-0.5, 3.9, 'y', color='blue')  
    plt.show()

def all_scatter_plot():
    plt.figure(figsize = (10, 6))
    for player in df['player'].unique():
        data_player = df[df['player'] == player]
        if player == 1:
            plt.scatter(data_player['x'], data_player['y'], label = f'Player {player}', color = 'black', marker = '+')
        elif player == 2:
            plt.scatter(data_player['x'], data_player['y'], label = f'Player {player}', color = 'green', marker = 'x')
        elif player == 3:
            plt.scatter(data_player['x'], data_player['y'], label = f'Player {player}', color = 'blue', marker = 'o')
    plt.xlim(-4, 4)
    plt.ylim(-4, 4)
    plt.gca().spines['bottom'].set_position('zero')
    plt.gca().spines['left'].set_position('zero')
    plt.gca().spines['bottom'].set_color('blue')
    plt.gca().spines['left'].set_color('blue')
    plt.gca().spines['right'].set_color('none') 
    plt.gca().spines['top'].set_color('none') 
    plt.title('Dart Hits for All Players', color='red')
    plt.text(3.9, -0.7, 'x', color='blue') 
    plt.text(-0.5, 3.9, 'y', color='blue')  
    plt.show()

def calculate_scores(df):
    scores = {1: [0, 0, 0, 0], 2: [0, 0, 0, 0], 3: [0, 0, 0, 0]}
    for index, row in df.iterrows():
        player = row['player']
        distance = (row['x'] ** 2 + row['y'] ** 2) ** 0.5
        if distance <= 1:
            scores[player][0] += 1
        elif distance <= 2:
            scores[player][1] += 1
        elif distance <= 3:
            scores[player][2] += 1
        else:
            scores[player][3] += 1
    return scores

def bar_chart():
    scores = calculate_scores(df)
    players = list(scores.keys())
    point_10 = [scores[player][0] for player in players]
    point_5 = [scores[player][1] for player in players]
    point_1 = [scores[player][2] for player in players]
    point_0 = [scores[player][3] for player in players]

    width_bar = 0.7
    plt.bar(players, point_10, color = 'red', label = '10 Points', width = width_bar)
    plt.bar(players, point_5, bottom = point_10, color = 'blue', label = '5 Points', width = width_bar)
    plt.bar(players, point_1, bottom = [i + j for i,j in zip(point_10, point_5)], color = 'green', label = '1 Point', width = width_bar)
    plt.bar(players, point_0, bottom = [i + j + k for i,j,k in zip(point_10, point_5, point_1)], color = 'purple', label = '0 Points', width = width_bar)
    plt.ylabel('Frequency')
    plt.title('Frequency of Hits')
    plt.xticks(players, ['Player 1', 'Player 2', 'Player 3'])
    plt.legend()
    plt.show()
    
def data_analysis():
    scores = calculate_scores(df)
    total_scores = {player: sum([10 * scores[player][0], 5 * scores[player][1], scores[player][2]]) for player in scores}
    avg_displacement = {player: (df[df['player'] == player]['x'].mean(), df[df['player'] == player]['y'].mean()) for player in scores}
    
    print('Data Analysis Results:')
    for player in scores:
        print('Player', player, ':')
        print('Total Score: ', total_scores[player])
        print('Average Displacement: ', avg_displacement[player])
    winner = max(total_scores, key = total_scores.get)
    print('\nWinner: Player', winner, 'with a score of', total_scores[winner], '\n')
    
main_menu()
