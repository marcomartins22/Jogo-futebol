###############################################################################################
# Importing Libraries
###############################################################################################
import os
import time
import random
import pandas as pd
from tabulate import tabulate
#import Marco_teste


# import time


def create_combinations(f_teams):
    """
    :param f_teams: It's necessary to pass to the function the teams available to create the combinations
    :return: This function will create the possible combinations of games excluding the combination 1 team playing
     against itself.
    """
    f_game_combinations = []
    f_exclude_list = []
    for f_home in f_teams:
        for f_away in f_teams:
            if f_away != f_home and (f_home + "_" + f_away) not in f_exclude_list:
                f_game_combinations.append([f_home, f_away])
                f_exclude_list.append(f_home + "_" + f_away)
                f_exclude_list.append(f_away + "_" + f_home)
    return f_game_combinations


def season_games(f_game_combinations, f_number_teams, f_tactics):
    """:param f_game_combinations: variable with the possible combinations of games
    :param f_number_teams: numer of teams available
    :param f_tactics: list of tactics available
    :return: This function will create a full season schedule by week without repeating games, controlling who is
     playing at home or way to give same advantages, calculates the random tactics for each game and store the information
     in a dataframe"""
    f_home_flag = True
    f_game_combinations_sec_round = f_game_combinations.copy()
    f_weeks_start = 1
    f_season_games = pd.DataFrame(columns=['week', 'HomeTeam', 'PlayerHome', 'HomeTatic', 'HomeScore', 'AwayScore',
                                           'AwayTeam', 'PlayerAway', 'AwayTatic', 'Status'])
    for f_rounds in range(1, 3):
        for f_weeks in range(f_weeks_start, f_number_teams):
            f_exclude_list = []
            for f_game in f_game_combinations.copy():
                if f_game[0] not in f_exclude_list and f_game[1] not in f_exclude_list:
                    f_exclude_list.append(f_game[0])
                    f_exclude_list.append(f_game[1])
                    if f_home_flag:
                        f_season_games.loc[len(f_season_games.index)] = [f_weeks, f_game[0], 'CPU',
                                                                         random.choice(f_tactics), 0, 0, f_game[1],
                                                                         'CPU', random.choice(f_tactics), "Pending"]
                    else:
                        f_season_games.loc[len(f_season_games.index)] = [f_weeks, f_game[1], 'CPU',
                                                                         random.choice(f_tactics), 0, 0, f_game[0],
                                                                         'CPU', random.choice(f_tactics), "Pending"]
                    f_game_combinations.remove(f_game)
            f_home_flag = not f_home_flag  # Toggle the home flag
            if not f_game_combinations:
                break
        f_game_combinations = f_game_combinations_sec_round
        f_weeks_start = f_number_teams + 2
        f_number_teams = f_weeks_start + f_number_teams + 1
    return f_season_games


def play_games(f_season_schedule_list, f_tactics):
    """ :param f_season_schedule_list: the dataframe with the season games
    :param f_tactics: the list of tactics
    :return:this function will search for the first week with pending games in the season and simulate the game.
    every 5m a random choice of tactics will be generated and a goal scored it will generate also a random to score
    home or away.
    At the beginning and middle its possible for the users to change tactics.
    CAso não existam jogos pendente inform o utilizador
    """
    f_copy_f_season_schedule_list = f_season_schedule_list.copy()
    f_first_pending_week = f_copy_f_season_schedule_list.loc[f_copy_f_season_schedule_list['Status'] == 'Pending',
    'week'].min()
    f_filtered_schedule = f_copy_f_season_schedule_list[f_copy_f_season_schedule_list['week'] == f_first_pending_week]
    if f_filtered_schedule.empty:
        print("No more games available to play.")
        return f_season_schedule_list
    for f_time in range(0, 91, 5):
        if f_time == 0 or f_time == 45:
            # print("alterar tatica")
            pass
        else:
            # print(f"Time: {f_time}")
            f_tactics_choice = random.choice(f_tactics)
            f_home_flag = random.randint(0, 1)
            # print(f"home win: {f_home_flag}")
            for index, row in f_filtered_schedule.iterrows():
                # Check if HomeTatic matches tactics_choice
                if row['HomeTatic'] == f_tactics_choice and f_home_flag == 0:
                    f_filtered_schedule.at[index, 'HomeScore'] += 1
                # Check if AwayTatic matches tactics_choice
                if row['AwayTatic'] == f_tactics_choice and f_home_flag == 1:
                    f_filtered_schedule.at[index, 'AwayScore'] += 1
                if f_time == 90:
                    f_season_schedule_list.at[index, 'HomeScore'] = f_filtered_schedule.at[index, 'HomeScore']
                    f_season_schedule_list.at[index, 'AwayScore'] = f_filtered_schedule.at[index, 'AwayScore']
                    f_season_schedule_list.at[index, 'Status'] = 'Played'

    #print scoreboard após cada jogo
    print("\nLive Scoreboard:")
    print(tabulate(calculate_scoreboard(create_scoreboard(teams), f_season_schedule_list), headers='keys',
                                 tablefmt='psql'))
    
    # print(f"tatica escolhida: {f_tactics_choice}")
        # print(f_filtered_schedule[['week', 'HomeTeam', 'HomeTatic', 'HomeScore', 'AwayScore', 'AwayTeam', 'AwayTatic']])
    # print(tabulate(f_season_schedule_list[['week', 'HomeTeam', 'HomeTatic', 'HomeScore', 'AwayScore', 'AwayTeam',
    #                                       'AwayTatic', 'Status']], headers='keys', tablefmt='psql'))
    return f_season_schedule_list


def print_scoreboard(teams, season_schedule_list):
    scoreboard = calculate_scoreboard(create_scoreboard(teams), season_schedule_list)
    print(tabulate(scoreboard, headers='keys', tablefmt='psql'))


def create_scoreboard(f_teams):
    score = []
    for f_team in f_teams:
        score.append([f_team, "CPU", 0, 0, 0, 0, 0, 0, 0, 0, random.randint(1, 99999)])
    season_score = pd.DataFrame(score, columns=['Team', 'Player', 'GamesPlayed',
                                                'Wins', 'Draws', 'Losses', 'GoalsFor', 'GoalsAgainst', 'GoalDiff',
                                                'Points', 'CoinToss'])
    return season_score


def calculate_scoreboard(f_scoreboard, f_season_schedule_list):
    # Filter rows with "Status" different from "Pending"
    f_filtered_schedule = f_season_schedule_list[f_season_schedule_list['Status'] != 'Pending']
    # Update scoreboard based on match results
    for index, row in f_filtered_schedule.iterrows():
        f_home_team = row['HomeTeam']
        f_away_team = row['AwayTeam']
        f_home_score = row['HomeScore']
        f_away_score = row['AwayScore']

        # Update GamesPlayed
        f_scoreboard.loc[f_scoreboard['Team'] == f_home_team, 'GamesPlayed'] += 1
        f_scoreboard.loc[f_scoreboard['Team'] == f_away_team, 'GamesPlayed'] += 1

        # Update Wins, Draws, Losses, GoalsFor, GoalsAgainst
        if f_home_score > f_away_score:
            f_scoreboard.loc[f_scoreboard['Team'] == f_home_team, 'Wins'] += 1
            f_scoreboard.loc[f_scoreboard['Team'] == f_away_team, 'Losses'] += 1
        elif f_home_score < f_away_score:
            f_scoreboard.loc[f_scoreboard['Team'] == f_home_team, 'Losses'] += 1
            f_scoreboard.loc[f_scoreboard['Team'] == f_away_team, 'Wins'] += 1
        else:
            f_scoreboard.loc[f_scoreboard['Team'] == f_home_team, 'Draws'] += 1
            f_scoreboard.loc[f_scoreboard['Team'] == f_away_team, 'Draws'] += 1

        # Update GoalsFor and GoalsAgainst
        f_scoreboard.loc[f_scoreboard['Team'] == f_home_team, 'GoalsFor'] += f_home_score
        f_scoreboard.loc[f_scoreboard['Team'] == f_away_team, 'GoalsFor'] += f_away_score
        f_scoreboard.loc[f_scoreboard['Team'] == f_home_team, 'GoalsAgainst'] += f_away_score
        f_scoreboard.loc[f_scoreboard['Team'] == f_away_team, 'GoalsAgainst'] += f_home_score

    # Calculate GoalDiff and Points
    f_scoreboard['GoalDiff'] = f_scoreboard['GoalsFor'] - f_scoreboard['GoalsAgainst']
    f_scoreboard['Points'] = f_scoreboard['Wins'] * 3 + f_scoreboard['Draws']
    f_scoreboard = f_scoreboard.sort_values(by=['Points', 'GoalsFor', 'GoalDiff', 'CoinToss'], ascending=False)

    return f_scoreboard


def criar_lista_equipes(equipas):
    teams = []
    for i in range(1, equipas + 1):
        team_name = input(f"Digite o nome da equipa {i}: ")
        team = f"{team_name}"
        teams.append(team)

    print("Lista de equipas:")
    for team in teams:
        print(team)
    time.sleep(5)

    return teams

def print_teams(f_teams):
    for counter, team in enumerate(f_teams, start=1):
        print(f"{counter} - {team}")

def select_team():
    print("Escolha a sua equipa:")
    print_teams(teams)
    choice = int(input("Escolha a sua equipa: "))
    return teams[choice - 1]

def player_selection(f_tactics):
    print(print_tatics(f_tactics))


def print_tatics(f_tactics):
    for counter in range(len(f_tactics)):
        print(f"{counter + 1} - {f_tactics[counter]}")

def select_tactic(f_tactics):
    print("Choose your tactic:")
    print_tatics(f_tactics)
    choice = int(input("Enter the number of the tactic you want to use: "))
    return f_tactics[choice - 1]


#################################################################################################
# GAME
#################################################################################################
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print(f"{bcolors.WARNING}Soccer Play Isla Championship \n{bcolors.ENDC}")

num_equipas = 1
while num_equipas == 1 or num_equipas >= 9:
    num_equipas = int(input((f"{bcolors.HEADER}Please enter a number of manual players between 2 and 8 or 0 for auto-complete:{bcolors.ENDC}")))
    teams = criar_lista_equipes(num_equipas)
    os.system('cls')  # Clearing the screen
    
    if num_equipas == 0:
        teams = ["a - Equipa 1", "b - Equipa 2", "c - Equipa 3", "d - Equipa 4"] #penso que pode ser apagado uma vez que já está acima
    elif num_equipas >= 9:
        print("Please enter a number of manual players between 2 and 8")



tactics = ["4-4-2", "4-3-3", "5-4-1", "5-3-2", "3-4-3", "4-1-2-2-1"]
number_teams = len(teams) + 1
weeks_start = 1
# criar combinações de jogos possiveis
game_combinations = create_combinations(teams)
# criar calendario de jogos para 2 rondas
season_schedule_list = season_games(game_combinations, number_teams, tactics)
# criar scoreboard
scoreboard = create_scoreboard(teams)
#seleção de equipa
# player_team = select_team()
# print(f"Escolheu a equipa {player_team}!")

# Seleção da tática
# player_tactic = select_tactic(tactics)
# print(f"Escolheu a táctica {player_tactic}!")

#################################################################################################
# MENU
#################################################################################################

end_game = False
while end_game == False:

    choice = input("\nEscolha o menu: \n"
                +(f"{bcolors.OKBLUE}[1] - Escolher Equipas\n{bcolors.ENDC}")
                +(f"{bcolors.OKGREEN}[2] - Escolher Tacticas\n{bcolors.ENDC}")
                +(f"{bcolors.HEADER}[3] - Correr Campeonato \n{bcolors.ENDC}")
                +(f"{bcolors.FAIL}[4] - Calendario de jogos \n{bcolors.ENDC}") 
                +(f"{bcolors.OKCYAN}[5] - Tabela Classificativa Final \n{bcolors.ENDC}") ##Ao correr o campeonato no fim, desaparce os menus anteriores apenas mostra opcao 4 e 5
                +(f"{bcolors.OKGREEN}[6] - Sair \n{bcolors.ENDC}")
                +(f"{bcolors.HEADER}[7] - Reiniciar \n\n{bcolors.ENDC}"
    "Escolha: "))

    if (choice == "1"):
        player_team = select_team()
        print(f" Escolheu a equipa {player_team}!")
    elif(choice == "2"):
        player_tactic = select_tactic(tactics)
        print(f"Escolheu a táctica {player_tactic}!")
    elif(choice == "3"):
        play_games(season_schedule_list, tactics)
    elif(choice == "4"):
        print(tabulate(season_schedule_list, headers='keys', tablefmt='psql'))
    elif(choice == "5"):
        os.system('cls')
        print_scoreboard(teams, season_schedule_list)
    elif(choice == "6"):
        print("bye!!!")
        time.sleep(1)
        os.system('cls')
        break
    elif(choice =="7"):
        print('Restarting...')
        os.system('Marco_teste.py')
os.system('cls')


# end_game = False
# while end_game == False:
#     menu = input('''

#     1 - jogar jogo
#     2 - classificação
#     3 - Calendario
#     4 - Escolher equipas
#     5 - Sair 
    

#     Escolha uma opção: 
#     ''')
#     if menu == "1":
#         play_games(season_schedule_list, tactics)
#     elif menu == "2":
#         scoreboard = calculate_scoreboard(scoreboard, season_schedule_list)
#         print("Scoreboard:")
#         print(tabulate(scoreboard, headers='keys', tablefmt='psql'))
#     elif menu == "3":
#         print(tabulate(season_schedule_list, headers='keys', tablefmt='psql'))
#     elif menu == "4":
#         player_team = select_team()
#         print(f" Escolheu a equipa {player_team}!")
#     else:
#         end_game = True


# #    1 - jogar jogo
# #    2 - classificação
# #    3 - Calendario
# #    4 - Escolher equipas
# #    5 - Sair 