###############################################################################################
# Importing Libaries
###############################################################################################
import random
import pandas as pd
from tabulate import tabulate
import os
import time


def create_combinations(f_teams):
    """
    Create possible combinations of games for a given set of teams, excluding matchups
    where one team plays against itself.

    :param f_teams: List of teams available to create combinations.
    :return: List of possible game combinations.
    """
    f_game_combinations = []
    f_exclude_list = set()
    for f_home_team in f_teams:
        for f_away_team in f_teams:
            if f_away_team != f_home_team and (f_home_team, f_away_team) not in f_exclude_list:
                f_game_combinations.append([f_home_team, f_away_team])
                f_exclude_list.add((f_home_team, f_away_team))
                f_exclude_list.add((f_away_team, f_home_team))
    return f_game_combinations


def season_games(f_game_combinations, f_number_teams, f_tactics):
    """
    Create a full season schedule, avoiding repeating games and alternating home and away teams.
    Assign random tactics to each game and store the information in a DataFrame.

    :param f_game_combinations: List of possible game combinations.
    :param f_number_teams: Number of teams available.
    :param f_tactics: List of tactics available.
    :return: DataFrame containing the season schedule.
    """
    f_home_flag = True
    f_game_combinations_sec_round = f_game_combinations.copy()
    f_weeks_start = 1
    f_season_games = pd.DataFrame(columns=['week', 'HomeTeam', 'PlayerHome', 'HomeTactic', 'HomeScore', 'AwayScore',
                                           'AwayTeam', 'PlayerAway', 'AwayTactic', 'Status'])
    for f_rounds in range(2):
        for f_weeks in range(f_weeks_start, f_number_teams):
            f_exclude_list = set()
            for f_game in f_game_combinations.copy():
                if f_game[0] not in f_exclude_list and f_game[1] not in f_exclude_list:
                    f_exclude_list.update([f_game[0], f_game[1]])
                    if f_home_flag:
                        f_season_games.loc[len(f_season_games.index)] = [f_weeks, f_game[0], 'CPU',
                                                                         random.choice(f_tactics), 0, 0, f_game[1],
                                                                         'CPU', random.choice(f_tactics), "Pending"]
                    else:
                        f_season_games.loc[len(f_season_games.index)] = [f_weeks, f_game[1], 'CPU',
                                                                         random.choice(f_tactics), 0, 0, f_game[0],
                                                                         'CPU', random.choice(f_tactics), "Pending"]
                    f_game_combinations.remove(f_game)
            f_home_flag = not f_home_flag
            if not f_game_combinations:
                break
        f_game_combinations = f_game_combinations_sec_round
        f_weeks_start = f_number_teams + 2
        f_number_teams = f_weeks_start + f_number_teams + 1
    return f_season_games


def play_games(f_season_schedule_list, f_tactics):
    """
    Simulate games in the provided season schedule DataFrame.

    :param f_season_schedule_list: DataFrame with the season games.
    :param f_tactics: List of tactics available.
    :return: Updated season schedule DataFrame after simulating games.
    """
    f_copy_f_season_schedule_list = f_season_schedule_list.copy()
    f_first_pending_week = f_copy_f_season_schedule_list.loc[f_copy_f_season_schedule_list['Status'] == 'Pending',
    'week'].min()
    f_filtered_schedule = f_copy_f_season_schedule_list[f_season_schedule_list['week'] == f_first_pending_week]
    if f_filtered_schedule.empty:
        print("No more games available to play.")
        return f_season_schedule_list
    for f_time in range(0, 91, 5):
        time.sleep(1)
        if f_time == 0 or f_time == 45:
            # print("alterar tatica")
            pass
        else:
            os.system("cls")
            print(f"Time: {f_time}")
            f_tactics_choice = random.choice(f_tactics)
            print(f"tatica escolhida: {f_tactics_choice}")
            f_home_flag = random.randint(0, 1)
            print(f"home win: {f_home_flag}")
            for index, row in f_filtered_schedule.iterrows():
                if row['HomeTactic'] == f_tactics_choice and f_home_flag == 0:
                    f_filtered_schedule.at[index, 'HomeScore'] += 1
                if row['AwayTactic'] == f_tactics_choice and f_home_flag == 1:
                    f_filtered_schedule.at[index, 'AwayScore'] += 1
                if f_time == 90:
                    f_season_schedule_list.at[index, 'HomeScore'] = f_filtered_schedule.at[index, 'HomeScore']
                    f_season_schedule_list.at[index, 'AwayScore'] = f_filtered_schedule.at[index, 'AwayScore']
                    f_season_schedule_list.at[index, 'Status'] = 'Played'
        print(tabulate(f_filtered_schedule[['week', 'HomeTeam', 'HomeTactic', 'HomeScore', 'AwayScore', 'AwayTeam',
                                            'AwayTactic']], headers='keys', tablefmt='pretty', showindex='never'))
    f_season_schedule_list = f_season_schedule_list.reset_index(drop=True)
    f_season_schedule_list.index += 1
    print(tabulate(f_season_schedule_list[['week', 'HomeTeam', 'HomeScore', 'AwayScore', 'AwayTeam', 'Status']],
                   headers='keys', tablefmt='pretty', showindex='never'))
    return f_season_schedule_list


def create_scoreboard(f_teams):
    """
      Generate a scoreboard based on the available teams.

      :param teams: List of teams to create the scoreboard.
      :return: DataFrame containing the scoreboard. The index starts at 1, and a random coin toss value
               (between 1 and 99999) is assigned when multiple teams have the same points.
      """
    f_score = []
    for f_team in f_teams:
        f_score.append([f_team, "CPU", 0, 0, 0, 0, 0, 0, 0, 0, random.randint(1, 99999), ""])
    f_season_score = pd.DataFrame(f_score, columns=['Team', 'Player', 'GamesPlayed',
                                                    'Wins', 'Draws', 'Losses', 'GoalsFor', 'GoalsAgainst', 'GoalDiff',
                                                    'Points', 'CoinToss', 'Tactic'])
    f_season_score = f_season_score.reset_index(drop=True)
    f_season_score.index += 1
    return f_season_score


def calculate_scoreboard(f_scoreboard, f_season_schedule_list):
    """
    Update and calculate scores for the provided scoreboard based on the completed games in the season schedule.

    :param scoreboard: DataFrame containing team scores and statistics.
    :param season_schedule_list: DataFrame with a list of all games, including played and pending ones.
    :return: Updated scoreboard DataFrame sorted by points, goals scored, goal difference, and coin toss.
             The function iterates through played games, updates team statistics, and assigns points accordingly.
             The final scoreboard includes columns such as 'GamesPlayed', 'Wins', 'Draws', 'Losses', 'GoalsFor',
             'GoalsAgainst', 'GoalDiff', 'Points', 'CoinToss', and 'Tactic'.
             The DataFrame is sorted in descending order based on points, goals scored, goal difference,
             and coin toss, and a new index starting from 1 is assigned.
    """
    # Filter rows with "Status" different from "Pending"
    f_filtered_schedule = f_season_schedule_list[f_season_schedule_list['Status'] != 'Pending']
    # Update scoreboard based on match results
    for index, row in f_filtered_schedule.iterrows():
        f_home_team = row['HomeTeam']
        f_away_team = row['AwayTeam']
        f_home_score = row['HomeScore']
        f_away_score = row['AwayScore']
        f_scoreboard.loc[f_scoreboard['Team'] == f_home_team, 'GamesPlayed'] += 1
        f_scoreboard.loc[f_scoreboard['Team'] == f_away_team, 'GamesPlayed'] += 1
        if f_home_score > f_away_score:
            f_scoreboard.loc[f_scoreboard['Team'] == f_home_team, 'Wins'] += 1
            f_scoreboard.loc[f_scoreboard['Team'] == f_away_team, 'Losses'] += 1
        elif f_home_score < f_away_score:
            f_scoreboard.loc[f_scoreboard['Team'] == f_home_team, 'Losses'] += 1
            f_scoreboard.loc[f_scoreboard['Team'] == f_away_team, 'Wins'] += 1
        else:
            f_scoreboard.loc[f_scoreboard['Team'] == f_home_team, 'Draws'] += 1
            f_scoreboard.loc[f_scoreboard['Team'] == f_away_team, 'Draws'] += 1
        f_scoreboard.loc[f_scoreboard['Team'] == f_home_team, 'GoalsFor'] += f_home_score
        f_scoreboard.loc[f_scoreboard['Team'] == f_away_team, 'GoalsFor'] += f_away_score
        f_scoreboard.loc[f_scoreboard['Team'] == f_home_team, 'GoalsAgainst'] += f_away_score
        f_scoreboard.loc[f_scoreboard['Team'] == f_away_team, 'GoalsAgainst'] += f_home_score
    f_scoreboard['GoalDiff'] = f_scoreboard['GoalsFor'] - f_scoreboard['GoalsAgainst']
    f_scoreboard['Points'] = f_scoreboard['Wins'] * 3 + f_scoreboard['Draws']
    f_scoreboard = f_scoreboard.sort_values(by=['Points', 'GoalsFor', 'GoalDiff', 'CoinToss'], ascending=False)
    f_scoreboard = f_scoreboard.reset_index(drop=True)
    f_scoreboard.index += 1
    return f_scoreboard


def select_team(f_scoreboard, f_tactics, f_season_schedule_list):
    """
     Allows users to select teams, player names, and tactics for the upcoming season.

     :param scoreboard: DataFrame containing team scores and player information.
     :param tactics: List of available tactics for selection.
     :param season_schedule_list: DataFrame with a list of all games, including played and pending ones.
     :return: Updated scoreboard DataFrame with selected player names and tactics for chosen teams.
             The function prompts users to input the number of players, their names, team selections, and tactics.
             User input is validated to ensure correctness, and the selected information is updated in the scoreboard.
             The function returns the modified scoreboard.
     """
    f_played_games = f_season_schedule_list[f_season_schedule_list['PlayerHome'] != 'CPU']
    if len(f_played_games) > 0:
        os.system("cls")
        print("Ja foram seleccionadas equipas e não podem ser alteradas.")
        return f_scoreboard
    f_valid_users = True
    while f_valid_users:
        os.system("cls")
        f_num_players = input("Introduza o numero de jogadores: ")
        if f_num_players.isnumeric() and len(f_scoreboard.index) >= int(f_num_players):
            for n in range(int(f_num_players)):
                f_player_name = ""
                while f_player_name == "":
                    os.system("cls")
                    f_player_name = input(f"Introduza o nome do {n + 1} jogador:")
                f_team_select = ""
                while f_team_select == "":
                    f_available_teams = f_scoreboard[f_scoreboard['Player'] == "CPU"]
                    os.system("cls")
                    print(f_available_teams[['Team', 'Player']])
                    f_team_select = input(f"{f_player_name} introduza o numero da equipa pretendida: ")
                    if not (f_team_select.isnumeric() and int(f_team_select) in f_available_teams.index):
                        os.system("cls")
                        print(f"O valor introduzido não e valido ou o numero não corresponde a uma equipa.")
                        f_team_select = ""
                f_tactics_select = ""
                while f_tactics_select == "":
                    os.system("cls")
                    print_tactics(f_tactics)
                    f_tactics_select = input(f"{f_player_name} escolha uma tatica: ")
                    if not (f_tactics_select.isnumeric() and int(f_tactics_select) <= len(f_tactics)):
                        os.system("cls")
                        print(f"O valor introduzido não e valido ou o numero não corresponde a uma tatica.")
                        f_tactics_select = ""
                f_scoreboard.loc[int(f_team_select), 'Player'] = f_player_name
                f_scoreboard.loc[int(f_team_select), 'Tactic'] = f_tactics[int(f_tactics_select) - 1]
            return f_scoreboard
        else:
            print(f"O valor introduzido não e valido ou é superior ao numero de equipas disponiveis."
                  f" Apenas existem {len(f_scoreboard.index)} equipas.")


def print_tactics(f_tactics):
    """
    Prints a numbered list of available tactics.

    :param tactics: List of tactics to be displayed.
    :return: None
    """
    for counter in range(len(f_tactics)):
        print(f"{counter + 1} - {f_tactics[counter]}")


def update_player_season(f_season_schedule_list, f_scoreboard):
    """
    Update the player and tactic information in the season schedule list based on the scoreboard.

    :param season_schedule_list: DataFrame containing the schedule of the season.
    :param scoreboard: DataFrame containing the scores and player information.
    :return: Updated season schedule list.
    """
    for index, row in f_scoreboard.iterrows():
        f_team = row['Team']
        f_matching_rows_home = f_season_schedule_list[f_season_schedule_list['HomeTeam'] == f_team]
        if not f_matching_rows_home.empty:
            f_season_schedule_list.loc[f_matching_rows_home.index, 'PlayerHome'] = row['Player']
            if row['Tactic']:
                f_season_schedule_list.loc[f_matching_rows_home.index, 'HomeTactic'] = row['Tactic']
        f_matching_rows_away = f_season_schedule_list[f_season_schedule_list['AwayTeam'] == f_team]
        if not f_matching_rows_away.empty:
            f_season_schedule_list.loc[f_matching_rows_away.index, 'PlayerAway'] = row['Player']
            if row['Tactic']:
                f_season_schedule_list.loc[f_matching_rows_away.index, 'AwayTactic'] = row['Tactic']
    return f_season_schedule_list


def change_teams(f_teams, f_season_schedule_list):
    os.system("cls")
    f_played_games = f_season_schedule_list[f_season_schedule_list['PlayerHome'] != 'CPU']
    if len(f_played_games) > 0:
        print("Ja foram seleccionadas equipas e os nomes não podem ser alterados.")
        return f_teams

    f_select_team = ""
    while f_select_team == "":
        for i in range(len(f_teams)):
            print(f"{i + 1} - {f_teams[i]}")
        f_select_team = input("Qual a equipa que deseja editar o nome: ")
        if f_select_team.isnumeric() and int(f_select_team) - 1 < len(f_teams) and int(f_select_team) > 0:
            f_team_name = input("Introduza o novo nome: ")
            f_teams[int(f_select_team) - 1] = f_team_name
        else:
            os.system("cls")
            print(f"O valor introduzido não e valido ou o numero não corresponde a uma equipa.")
            input("Pressione 'Enter' para continuar...")
            f_select_team = ""
    return f_teams


#################################################################################################
# GAME
#################################################################################################
teams = ["a - Equipa 1", "b - Equipa 2", "c - Equipa 3", "d - Equipa 4"]
tactics = ["4-4-2", "4-3-3", "5-4-1", "5-3-2", "3-4-3", "4-1-2-2-1"]
number_teams = len(teams) + 1
# criar combinações de jogos possiveis
game_combinations = create_combinations(teams)
# criar calendario de jogos para 2 rondas
season_schedule_list = season_games(game_combinations, number_teams, tactics)
# criar scoreboard
scoreboard = create_scoreboard(teams)


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


end_game = True
while end_game:
    os.system("cls")
    menu = input('''
        {}[1] - Jogar Campeonato
        {}[2] - Tabela Classificativa
        {}[3] - Calendario de jogos
        {}[4] - Escolher equipas
        {}[5] - Restart
        {}[6] - Alterar nomes de equipas
        {}[7] - Sair\n
    Escolha uma opção: {}
    '''.format(bcolors.OKBLUE, bcolors.OKGREEN, bcolors.HEADER, bcolors.FAIL, bcolors.OKCYAN, bcolors.OKGREEN,
               bcolors.HEADER, bcolors.ENDC))

    if menu == "1":
        os.system("cls")
        play_games(season_schedule_list, tactics)
        input("Pressione 'Enter' para continuar...")
    elif menu == "2":
        os.system("cls")
        scoreboard = calculate_scoreboard(scoreboard, season_schedule_list)
        print(tabulate(scoreboard[['Team', 'Player', 'GamesPlayed', 'Wins', 'Draws', 'Losses',
                                   'GoalsFor', 'GoalsAgainst', 'GoalDiff', 'Points']], headers='keys',
                       tablefmt='pretty',
                       showindex='never'))
        input("Pressione 'Enter' para continuar...")
    elif menu == "3":
        os.system("cls")
        print(tabulate(season_schedule_list[['week', 'HomeTeam', 'HomeScore', 'AwayScore', 'AwayTeam', 'Status']],
                       headers='keys', tablefmt='pretty', showindex='never'))
        input("Pressione 'Enter' para continuar...")
    elif menu == "4":
        os.system("cls")
        scoreboard = select_team(scoreboard, tactics, season_schedule_list)
        season_schedule_list = update_player_season(season_schedule_list, scoreboard)
        input("Pressione 'Enter' para continuar...")
    elif menu == "5":
        # criar combinações de jogos possiveis
        game_combinations = create_combinations(teams)
        # criar calendario de jogos para 2 rondas
        season_schedule_list = season_games(game_combinations, number_teams, tactics)
        # criar scoreboard
        scoreboard = create_scoreboard(teams)
    elif menu == "6":
        teams = change_teams(teams, season_schedule_list)
        # criar combinações de jogos possiveis
        game_combinations = create_combinations(teams)
        # criar calendario de jogos para 2 rondas
        season_schedule_list = season_games(game_combinations, number_teams, tactics)
        # criar scoreboard
        scoreboard = create_scoreboard(teams)
    else:
        end_game = False
