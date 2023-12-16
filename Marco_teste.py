import pandas as pd
import time
import random
from tabulate import tabulate
import os
from Art import logo


def create_dataframes(data_cd, fields_cd):
    """
    Create a DataFrame from provided data and fields.

    :param data_cd: List of data to populate the DataFrame.
    :param fields_cd: List of column names for the DataFrame.
    :return: DataFrame
    """
    data_frame_cd = pd.DataFrame(data_cd, columns=fields_cd)
    data_frame_cd = data_frame_cd.reset_index(drop=True)
    data_frame_cd.index += 1
    return data_frame_cd


def create_game_combos(teams_df_cgc):
    """
    Create combinations of possible team combination to play game. Avoiding that one plays againt itself.

    :param teams_df_cgc: DataFrame containing team information.
    :return: DataFrame with combinations of teams for the game.
    """
    game_combos_cgc = []
    excluded_combos_cgc = set()
    for index, row in teams_df_cgc.iterrows():
        for inner_index, inner_row in teams_df_cgc.iterrows():
            if inner_row['Team'] != row['Team'] and (row['Team'], inner_row['Team']) not in excluded_combos_cgc:
                game_combos_cgc.append([row['Team'], inner_row['Team']])
                excluded_combos_cgc.add((row['Team'], inner_row['Team']))
                excluded_combos_cgc.add((inner_row['Team'], row['Team']))
    game_combos_fields_cgc = [['Home', 'Away']]
    game_combos_cgc = create_dataframes(game_combos_cgc, game_combos_fields_cgc)
    return game_combos_cgc


def season_games(game_combinations_sg, number_teams_sg, tactics_df_sg):
    """
    Create a DataFrame with information about the season games. Considerations:
     - 2 rounds of games
     - 1 team can't play 2 games in same week
     - alternates between home and away

    :param game_combinations_sg: DataFrame with combinations of teams for the game.
    :param number_teams_sg: Number of teams participating in the season.
    :param tactics_df_sg: DataFrame containing tactics information.
    :return: DataFrame with season games information.
    """
    weeks_sg = 1
    home_flag_sg = True
    season_games_list_sg = []
    for _ in range(1):
        while weeks_sg < number_teams_sg * 2 - 1:
            exclude_list_sg = set()
            for index, game in game_combinations_sg.iterrows():
                if game['Home'] not in exclude_list_sg and game['Away'] not in exclude_list_sg:
                    exclude_list_sg.update([game['Home'], game['Away']])
                    if home_flag_sg:
                        home_sg = game['Home']
                        away_sg = game['Away']
                    else:
                        home_sg = game['Away']
                        away_sg = game['Home']
                    tactic_sample_home_sg = tactics_df_sg['Tactic'].sample(n=1).iloc[0]
                    tactic_sample_away_sg = tactics_df_sg['Tactic'].sample(n=1).iloc[0]
                    season_games_list_sg.append([weeks_sg, home_sg, 'CPU', tactic_sample_home_sg, 0, 0, away_sg,
                                                 'CPU', tactic_sample_away_sg, "Pending"])
            home_flag_sg = not home_flag_sg

            weeks_sg += 1
    season_games_fields_sg = ['week', 'HomeTeam', 'PlayerHome', 'HomeTactic', 'HomeScore', 'AwayScore',
                              'AwayTeam', 'PlayerAway', 'AwayTactic', 'Status']
    season_games_df_sg = create_dataframes(season_games_list_sg, season_games_fields_sg)
    return season_games_df_sg


def create_scoreboard(teams_df_cs):
    """
    Create a DataFrame to track the scoreboard. Its created based on the teams available.

    :param teams_df_cs: DataFrame containing team information.
    :return: DataFrame to track the scoreboard.
    """
    score_list_cs = []
    for index, row in teams_df_cs.iterrows():
        score_list_cs.append([row['Team'], "CPU", 0, 0, 0, 0, 0, 0, 0, 0, random.randint(1, 99999), ""])
    score_fields_cs = ['Team', 'Player', 'GamesPlayed', 'Wins', 'Draws', 'Losses', 'GoalsFor',
                       'GoalsAgainst', 'GoalDiff', 'Points', 'CoinToss', 'Tactic']
    scoreboard_df_cs = create_dataframes(score_list_cs, score_fields_cs)
    return scoreboard_df_cs


def update_scoreboard(scoreboard_us, season_games_df_us):
    """
    Calculate and update the scoreboard based on played games.

    :param scoreboard_us: DataFrame tracking the scoreboard.
    :param season_games_df_us: DataFrame containing information about season games.
    :return: Updated scoreboard DataFrame.
    """
    filtered_schedule_us = season_games_df_us[season_games_df_us['Status'] != 'Pending']
    for index, row in filtered_schedule_us.iterrows():
        home_team_us = row['HomeTeam']
        away_team_us = row['AwayTeam']
        home_score_us = row['HomeScore']
        away_score_us = row['AwayScore']
        scoreboard_us.loc[scoreboard_us['Team'] == home_team_us, 'GamesPlayed'] += 1
        scoreboard_us.loc[scoreboard_us['Team'] == away_team_us, 'GamesPlayed'] += 1
        if home_score_us > away_score_us:
            scoreboard_us.loc[scoreboard_us['Team'] == home_team_us, 'Wins'] += 1
            scoreboard_us.loc[scoreboard_us['Team'] == away_team_us, 'Losses'] += 1
        elif home_score_us < away_score_us:
            scoreboard_us.loc[scoreboard_us['Team'] == home_team_us, 'Losses'] += 1
            scoreboard_us.loc[scoreboard_us['Team'] == away_team_us, 'Wins'] += 1
        else:
            scoreboard_us.loc[scoreboard_us['Team'] == home_team_us, 'Draws'] += 1
            scoreboard_us.loc[scoreboard_us['Team'] == away_team_us, 'Draws'] += 1
        scoreboard_us.loc[scoreboard_us['Team'] == home_team_us, 'GoalsFor'] += home_score_us
        scoreboard_us.loc[scoreboard_us['Team'] == away_team_us, 'GoalsFor'] += away_score_us
        scoreboard_us.loc[scoreboard_us['Team'] == home_team_us, 'GoalsAgainst'] += away_score_us
        scoreboard_us.loc[scoreboard_us['Team'] == away_team_us, 'GoalsAgainst'] += home_score_us
    scoreboard_us['GoalDiff'] = scoreboard_us['GoalsFor'] - scoreboard_us['GoalsAgainst']
    scoreboard_us['Points'] = scoreboard_us['Wins'] * 3 + scoreboard_us['Draws']
    scoreboard_us = scoreboard_us.sort_values(by=['Points', 'GoalsFor', 'GoalDiff', 'CoinToss'], ascending=False)
    scoreboard_us = scoreboard_us.reset_index(drop=True)
    scoreboard_us.index += 1
    return scoreboard_us


def change_tactics(filtered_schedule_df_ct, tactics_df_ct):
    """
    Allow players to change tactics for a given match.

    :param filtered_schedule_df_ct: DataFrame containing filtered schedule information.
    :param tactics_df_ct: DataFrame containing tactics information.
    :return: None
    """
    os.system("cls")
    print("Alterar tatica:")
    for index, row in filtered_schedule_df_ct.iterrows():
        if row['PlayerHome'] != 'CPU':
            os.system("cls")
            #####################################################################################
            # Imprimir filtered schedule
            #####################################################################################
            print(tabulate(filtered_schedule_df_ct[['week', 'HomeTeam', 'HomeTactic', 'PlayerHome', 'HomeScore',
                                                    'AwayScore', 'AwayTeam', 'PlayerAway', 'AwayTactic']],
                           headers='keys', tablefmt='pretty', showindex='never'))
            print(tabulate(tactics_df_ct, headers='keys'))
            print(f"{row['HomeTeam']} ({row['PlayerHome']}) - Tatica atual: {row['HomeTactic']}")
            new_tactic_home_ct = input("Nova tatica (ou pressione Enter para manter a mesma): ")
            #####################################################################################
            # Validar Input numerico e no range da dataframe --> Marco
            while True:
                new_tactic_home_ct = input("Nova tática (ou pressione Enter para manter a mesma): ")
                if not new_tactic_home_ct:
                    break  # Mantenha a tática atual se Enter for pressionado
                # Validar Input numérico e dentro do intervalo da DataFrame
                if new_tactic_home_ct.isnumeric() and int(new_tactic_home_ct) in tactics_df_ct.index:
                    filtered_schedule_df_ct.at[index, 'HomeTactic'] = tactics_df_ct.at[
                        int(new_tactic_home_ct), 'Tactic']
                    break
                else:
                    print("Por favor, insira um número válido.")

            #####################################################################################
            if new_tactic_home_ct:
                filtered_schedule_df_ct.at[index, 'HomeTactic'] = tactics_df_ct.at[int(new_tactic_home_ct), 'Tactic']
        if row['PlayerAway'] != 'CPU':
            os.system("cls")
            #####################################################################################
            # Imprimir filtered schedule
            #####################################################################################
            print(tabulate(filtered_schedule_df_ct[['week', 'HomeTeam', 'HomeTactic', 'PlayerHome', 'HomeScore',
                                                    'AwayScore', 'AwayTeam', 'PlayerAway', 'AwayTactic']],
                           headers='keys', tablefmt='pretty', showindex='never'))
            print(tabulate(tactics_df_ct, headers='keys'))
            print(f"{row['AwayTeam']} ({row['PlayerAway']}) - Tatica atual: {row['AwayTactic']}")
            new_tactic_away_ct = input("Nova tatica (ou pressione Enter para manter a mesma): ")
            #############################################################################
            # Validar Input numerico e no range da dataframe
            while True:
                new_tactic_away_ct = input("Nova tática (ou pressione Enter para manter a mesma): ")
                if not new_tactic_away_ct:
                    break  # Mantenha a tática atual se Enter for pressionado
                # Validar Input numérico e dentro do intervalo da DataFrame
                if new_tactic_away_ct.isnumeric() and int(new_tactic_away_ct) in tactics_df_ct.index:
                    filtered_schedule_df_ct.at[index, 'AwayTactic'] = tactics_df_ct.at[
                        int(new_tactic_away_ct), 'Tactic']
                    break
                else:
                    print("Por favor, insira um número válido.")
            #############################################################################
            if new_tactic_away_ct:
                filtered_schedule_df_ct.at[index, 'AwayTactic'] = tactics_df_ct.at[int(new_tactic_away_ct), 'Tactic']


def play_games(season_games_df_pg, tactics_df_pg):
    """
    Simulate football matches for the season.

    :param season_games_df_pg: DataFrame containing information about season games.
    :param tactics_df_pg: DataFrame containing tactics information.
    :return: Updated season games DataFrame.
    """
    copy_season_games_df_pg = season_games_df_pg.copy()
    first_pending_week_pg = copy_season_games_df_pg.loc[copy_season_games_df_pg['Status'] == 'Pending', 'week'].min()
    filtered_schedule_df_pg = copy_season_games_df_pg[season_games_df_pg['week'] == first_pending_week_pg]
    if filtered_schedule_df_pg.empty:
        os.system("cls")
        print("Não existem mais jogos disponiveis.")
        input("Pressione 'Enter' para continuar")
        return season_games_df_pg
    clock_pg = 0
    while clock_pg < 91:
        time.sleep(1)
        if clock_pg == 0 or clock_pg == 45:
            change_tactics(filtered_schedule_df_pg, tactics_df_pg)
        else:
            os.system("cls")
            print(f"Time: {clock_pg}")
            tactics_choice_pg = tactics_df_pg['Tactic'].sample(n=1).iloc[0]
            print(f"Tatica sorteada: {tactics_choice_pg}")
            home_flag_pg = random.randint(0, 1)
            print(f"Quem marca: {home_flag_pg}")
            for index, row in filtered_schedule_df_pg.iterrows():
                if row['HomeTactic'] == tactics_choice_pg and home_flag_pg == 0:
                    filtered_schedule_df_pg.at[index, 'HomeScore'] += 1
                if row['AwayTactic'] == tactics_choice_pg and home_flag_pg == 1:
                    filtered_schedule_df_pg.at[index, 'AwayScore'] += 1
                if clock_pg == 90:
                    season_games_df_pg.at[index, 'HomeScore'] = filtered_schedule_df_pg.at[index, 'HomeScore']
                    season_games_df_pg.at[index, 'AwayScore'] = filtered_schedule_df_pg.at[index, 'AwayScore']
                    season_games_df_pg.at[index, 'Status'] = 'Played'
        print(tabulate(filtered_schedule_df_pg[['week', 'HomeTeam', 'HomeTactic', 'PlayerHome', 'HomeScore',
                                                'AwayScore', 'AwayTeam', 'PlayerAway', 'AwayTactic']],
                       headers='keys', tablefmt='pretty', showindex='never'))
        clock_pg += 5
    season_games_df_pg = season_games_df_pg.reset_index(drop=True)
    season_games_df_pg.index += 1
    print(tabulate(filtered_schedule_df_pg[['week', 'HomeTeam', 'HomeTactic', 'PlayerHome', 'HomeScore',
                                            'AwayScore', 'AwayTeam', 'PlayerAway', 'AwayTactic']],
                   headers='keys', tablefmt='pretty', showindex='never'))
    return season_games_df_pg


def update_player_season(season_games_df_ps, scoreboard_ps):
    """
     Update the player information for the season.

     :param season_games_df_ps: DataFrame containing information about season games.
     :param scoreboard_ps: DataFrame tracking the scoreboard.
     :return: Updated season games DataFrame.
     """
    for index, row in scoreboard_ps.iterrows():
        team_ps = row['Team']
        matching_rows_home_ps = season_games_df_ps[season_games_df_ps['HomeTeam'] == team_ps]
        if not matching_rows_home_ps.empty:
            season_games_df_ps.loc[matching_rows_home_ps.index, 'PlayerHome'] = row['Player']
            if row['Tactic']:
                season_games_df_ps.loc[matching_rows_home_ps.index, 'HomeTactic'] = row['Tactic']
        matching_rows_away_ps = season_games_df_ps[season_games_df_ps['AwayTeam'] == team_ps]
        if not matching_rows_away_ps.empty:
            season_games_df_ps.loc[matching_rows_away_ps.index, 'PlayerAway'] = row['Player']
            if row['Tactic']:
                season_games_df_ps.loc[matching_rows_away_ps.index, 'AwayTactic'] = row['Tactic']
    return season_games_df_ps


def change_teams(teams_df_ct, season_games_df_ct):
    """
    Allow users to change team names.

    :param teams_df_ct: DataFrame containing team information.
    :param season_games_df_ct: DataFrame containing information about season games.
    :return: Updated teams DataFrame.
    """
    played_games_ct = season_games_df_ct[
        (season_games_df_ct['PlayerHome'] != 'CPU') |
        (season_games_df_ct['HomeScore'] > 0) |
        (season_games_df_ct['AwayScore'] > 0)]
    if not played_games_ct.empty:
        os.system("cls")
        print("Ja foram seleccionadas equipas e os nomes não podem ser alterados.")
        input("Prima 'Enter' para continuar...")
        return teams_df_ct
    select_team_ct = ""
    while select_team_ct == "":
        os.system("cls")
        print(teams_df_ct)
        select_team_ct = input("Qual numero da equipa que deseja editar o nome: ")
        if select_team_ct.isnumeric() and 1 <= int(select_team_ct) <= len(teams_df_ct):
            team_name_ct = input("Introduza o novo nome: ")
            teams_df_ct.at[int(select_team_ct), 'Team'] = team_name_ct
            return teams_df_ct
        else:
            os.system("cls")
            print(f"O valor introduzido:'{select_team_ct}'; não é valido ou o número não corresponde a uma equipa.")
            input("Prima 'Enter' para continuar...")
            select_team_ct = ""


def select_team(scoreboard_df_st, tactics_df_st, season_games_df_st):
    """
    Allow users to select teams and players for the season.

    :param scoreboard_df_st: DataFrame tracking the scoreboard.
    :param tactics_df_st: DataFrame containing tactics information.
    :param season_games_df_st: DataFrame containing information about season games.
    :return: Updated scoreboard DataFrame.
    """
    played_games_st = season_games_df_st[(season_games_df_st['PlayerHome'] != 'CPU') | (
            season_games_df_st['HomeScore'] > 0) | (season_games_df_st['AwayScore'] > 0)]
    if not played_games_st.empty:
        os.system("cls")
        print("Ja foram seleccionadas equipas e os nomes não podem ser alterados.")
        input("Prima 'Enter' para continuar...")
        return scoreboard_df_st
    valid_users_st = True
    while valid_users_st:
        os.system("cls")
        num_players_st = input("Introduza o numero de jogadores: ")
        if num_players_st.isnumeric() and len(scoreboard_df_st.index) >= int(num_players_st):
            for n in range(int(num_players_st)):
                player_name_st = ""
                while player_name_st == "":
                    os.system("cls")
                    player_name_st = input(f"Introduza o nome do {n + 1} jogador:")
                team_select_st = ""
                while team_select_st == "":
                    available_teams_st = scoreboard_df_st[scoreboard_df_st['Player'] == "CPU"]
                    os.system("cls")
                    print(available_teams_st[['Team']])
                    team_select_st = input(f"{player_name_st} introduza o numero da equipa pretendida: ")
                    if not (team_select_st.isnumeric() and int(team_select_st) in available_teams_st.index):
                        os.system("cls")
                        print(f"O valor introduzido não e valido ou o numero não corresponde a uma equipa.")
                        team_select_st = ""
                tactics_select_st = ""
                while tactics_select_st == "":
                    os.system("cls")
                    print(tactics_df_st)
                    tactics_select_st = input(f"{player_name_st} escolha uma tatica: ")
                    if not (tactics_select_st.isnumeric() and int(tactics_select_st) <= len(tactics_df_st)):
                        os.system("cls")
                        print(f"O valor introduzido não e valido ou o numero não corresponde a uma tatica.")
                        tactics_select_st = ""
                scoreboard_df_st.loc[int(team_select_st), 'Player'] = player_name_st
                scoreboard_df_st.loc[int(team_select_st), 'Tactic'] = tactics_df_st.at[int(tactics_select_st), 'Tactic']
            return scoreboard_df_st
        else:
            print("Por favor, insira um número válido.")


teams_list = ["Sporting CP", "FC Porto", "SL Benfica", "SC Braga"]
teams_fields = ['Team']
tactics_list = ["4-4-2", "4-3-3", "5-4-1", "5-3-2", "3-4-3", "4-1-2-2-1"]
tactics_fields = ['Tactic']
num_teams = len(teams_list)
teams_df = create_dataframes(teams_list, teams_fields)
tactics_df = create_dataframes(tactics_list, tactics_fields)
game_combos_df = create_game_combos(teams_df)
season_games_df = season_games(game_combos_df, num_teams, tactics_df)
scoreboard_df = create_scoreboard(teams_df)


class Bcolors:
    header = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


menu = ()
while menu != "7":
    os.system("cls")

    print(logo)
    menu = (input('''
        {}[1] - Jogar Campeonato
        {}[2] - Tabela Classificativa
        {}[3] - Calendario de jogos
        {}[4] - Escolher equipas
        {}[5] - Restart
        {}[6] - Alterar nomes de equipas
        {}[7] - Sair\n
    Escolha uma opção: {}
    '''.format(Bcolors.OKBLUE, Bcolors.OKGREEN, Bcolors.header, Bcolors.FAIL, Bcolors.OKCYAN, Bcolors.OKGREEN,
               Bcolors.header, Bcolors.ENDC)))

    if menu == "1":
        play_games(season_games_df, tactics_df)
        scoreboard_df = update_scoreboard(scoreboard_df, season_games_df)
    elif menu == "2":
        os.system("cls")
        if season_games_df['Status'].iloc[-1] != 'Played':
            print(tabulate(scoreboard_df, headers='keys'))
            input("Prima 'Enter' para continuar...")

        #####################################################################################
        #  # Verficar se ja não ha jogos pendentes e apresentar menssengem campeonato teminou vencedor: ---> David
        #####################################################################################

        else:
            season_games_df['Status'].iloc[-1] == 'Played'
            print(tabulate(scoreboard_df, headers='keys'))
            print(
                f"O CAMPEAO DO CAMPEONATE É: {Bcolors.OKBLUE}{scoreboard_df['Team'].iloc[0]}{Bcolors.ENDC} com {Bcolors.OKBLUE}{scoreboard_df['Points'].iloc[0]} pontos{Bcolors.ENDC}")
            input("Prima 'Enter' para continuar...")



    elif menu == "3":
        os.system("cls")
        print(tabulate(season_games_df, headers='keys'))
        input("Prima 'Enter' para continuar...")

    elif menu == "4":
        scoreboard_df = select_team(scoreboard_df, tactics_df, season_games_df)
        season_games_df = update_player_season(season_games_df, scoreboard_df)

    elif menu == "5":
        teams_df = create_dataframes(teams_list, teams_fields)
        tactics_df = create_dataframes(tactics_list, tactics_fields)
        game_combos_df = create_game_combos(teams_df)
        season_games_df = season_games(game_combos_df, num_teams, tactics_df)
        scoreboard_df = create_scoreboard(teams_df)

    elif menu == "6":
        teams_df = change_teams(teams_df, season_games_df)
        game_combos_df = create_game_combos(teams_df)
        season_games_df = season_games(game_combos_df, num_teams, tactics_df)
        scoreboard_df = create_scoreboard(teams_df)
    elif menu == "7":
        print("Bye")
        time.sleep(2)
        break
    elif menu >= "8" or menu <= "0" or float(menu):
        print("Opção invalida")
        time.sleep(2)
