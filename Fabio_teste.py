import os
import random

import pandas as pd
from tabulate import tabulate

import Decorations as Dec


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


def color_players_season_games(row_cpsg):
    player_home_cpsg, player_away_cpsg, status_cpsg = row_cpsg['PlayerHome'], row_cpsg['PlayerAway'], row_cpsg['Status']
    if player_home_cpsg != 'CPU' or player_away_cpsg != 'CPU' and status_cpsg == 'Pending':
        return [f'\033[96m{val}\033[0m' for val in
                row_cpsg.values]
    else:
        return list(row_cpsg)


def color_players_scoreboard(row_cps):
    player_cps = row_cps['Player']
    if player_cps != 'CPU':
        return [f'\033[96m{val}\033[0m' for val in row_cps.values]
    else:
        return list(row_cps)


def color_game_status(row_cgs):
    home_score_cgs, home_player_cgs, away_score_cgs, away_player_cgs, status_cgs = (
        row_cgs['HomeScore'], row_cgs['PlayerHome'], row_cgs['AwayScore'], row_cgs['PlayerAway'], row_cgs['Status'])
    if status_cgs != 'Pending':
        if home_score_cgs > away_score_cgs:
            return f'\033[92m{row_cgs["HomeTeam"]}({row_cgs["PlayerHome"]})\033[0m'
        elif home_score_cgs < away_score_cgs:
            return f'\033[92m{row_cgs["AwayTeam"]}({row_cgs["PlayerAway"]})\033[0m'
        else:
            return f'\033[93mEmpate\033[0m'
    else:
        return status_cgs


def print_season_games(season_games_df_psg):
    season_games_df_psg = pd.DataFrame(season_games_df_psg.apply(color_players_season_games, axis=1).tolist(),
                                       columns=season_games_df_psg.columns)
    print(tabulate(season_games_df_psg[['week', 'HomeTeam', 'PlayerHome', 'HomeScore',
                                        'AwayScore', 'AwayTeam', 'PlayerAway', 'Status']],
                   headers='keys', tablefmt='fancy_grid', showindex=False,
                   numalign="right", stralign="right", colalign=("center", "left", "left", "center",
                                                                 "center", "left", "left", "center")))


def print_tactics(tactics_df_pt):
    print(tabulate(tactics_df_pt[['Tactic']], headers=['ID', 'Tactic'], tablefmt='fancy_grid', showindex=True,
                   numalign="right", stralign="right"))


def print_teams_list(teams_df_ptl):
    print(tabulate(teams_df_ptl[['Team']], headers=['ID', 'Team'], tablefmt='fancy_grid', showindex=True,
                   numalign="right", stralign="right"))


def print_scoreboard(scoreboard_df_ps):
    scoreboard_df_ps[['Points', 'GoalsFor', 'GoalDiff', 'CoinToss']] = scoreboard_df_ps[
        ['Points', 'GoalsFor', 'GoalDiff', 'CoinToss']].astype(int)
    scoreboard_df_ps = scoreboard_df_ps.sort_values(by=['Points', 'GoalsFor', 'GoalDiff', 'CoinToss'], ascending=[
        False, False, False, True])
    scoreboard_df_ps = scoreboard_df_ps.reset_index(drop=True)
    scoreboard_df_ps_print = pd.DataFrame(scoreboard_df_ps.apply(color_players_scoreboard, axis=1).tolist(),
                                          columns=scoreboard_df_ps.columns)
    print(tabulate(scoreboard_df_ps_print[
                       ['Team', 'Player', 'GamesPlayed', 'Wins', 'Draws', 'Losses', 'GoalsFor', 'GoalsAgainst',
                        'Points']], headers='keys', tablefmt='fancy_grid', showindex=False, numalign="right",
                   stralign="right"))
    return scoreboard_df_ps


def season_games(teams_sg, tactics_df_sg):
    num_teams_sg = len(teams_sg)
    num_rounds_sg = num_teams_sg - 1
    season_games_list_sg = []
    total_week_count_sg = 1
    played_home_last_week = False
    for hands_sg in range(1, 3):
        for week_num_sg in range(1, num_rounds_sg + 1):
            for i_sg in range(num_teams_sg // 2):
                team1_sg, team2_sg = teams_sg[i_sg], teams_sg[num_teams_sg - 1 - i_sg]
                if played_home_last_week:
                    home_team_sg, away_team_sg = team2_sg, team1_sg
                else:
                    home_team_sg, away_team_sg = team1_sg, team2_sg
                tactic_sample_home_sg = tactics_df_sg['Tactic'].sample(n=1).iloc[0]
                tactic_sample_away_sg = tactics_df_sg['Tactic'].sample(n=1).iloc[0]
                season_games_list_sg.append([total_week_count_sg, home_team_sg, 'CPU', tactic_sample_home_sg, 0, 0,
                                             away_team_sg, 'CPU', tactic_sample_away_sg, 'Pending'])
            total_week_count_sg += 1
            played_home_last_week = not played_home_last_week
            teams_sg.insert(1, teams_sg.pop())
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
    print("Alterar tatica:")
    for index, row in filtered_schedule_df_ct.iterrows():
        if row['PlayerHome'] != 'CPU':
            print_season_games(filtered_schedule_df_ct)
            print_tactics(tactics_df_ct)
            print(f"{row['HomeTeam']} ({row['PlayerHome']}) - Tatica atual: {row['HomeTactic']}")
            while True:
                new_tactic_home_ct = input("Nova tática (ou pressione Enter para manter a mesma): ")
                os.system("cls")
                if not new_tactic_home_ct:
                    break
                if new_tactic_home_ct.isnumeric() and int(new_tactic_home_ct) in tactics_df_ct.index:
                    filtered_schedule_df_ct.at[index, 'HomeTactic'] = tactics_df_ct.at[
                        int(new_tactic_home_ct), 'Tactic']
                    break
                else:
                    print("Por favor, insira um número válido.")
            if new_tactic_home_ct:
                filtered_schedule_df_ct.at[index, 'HomeTactic'] = tactics_df_ct.at[int(new_tactic_home_ct), 'Tactic']
        if row['PlayerAway'] != 'CPU':
            print_season_games(filtered_schedule_df_ct)
            print_tactics(tactics_df_ct)
            print(f"{row['AwayTeam']} ({row['PlayerAway']}) - Tatica atual: {row['AwayTactic']}")
            while True:
                new_tactic_away_ct = input("Nova tática (ou pressione Enter para manter a mesma): ")
                os.system("cls")
                if not new_tactic_away_ct:
                    break
                if new_tactic_away_ct.isnumeric() and int(new_tactic_away_ct) in tactics_df_ct.index:
                    filtered_schedule_df_ct.at[index, 'AwayTactic'] = tactics_df_ct.at[
                        int(new_tactic_away_ct), 'Tactic']
                    break
                else:
                    print("Por favor, insira um número válido.")
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
        # time.sleep(1)
        if clock_pg == 0 or clock_pg == 45:
            os.system("cls")
            change_tactics(filtered_schedule_df_pg, tactics_df_pg)
        else:
            os.system("cls")
            print(f"Time: {clock_pg}")
            tactics_choice_pg = tactics_df_pg['Tactic'].sample(n=1).iloc[0]
            print(f"Tatica sorteada: {tactics_choice_pg}")
            home_flag_pg = random.randint(0, 1)
            print(f"Quem marca: {home_flag_pg}")
            print_season_games(filtered_schedule_df_pg)
            for index, row in filtered_schedule_df_pg.iterrows():
                if row['HomeTactic'] == tactics_choice_pg and home_flag_pg == 0:
                    filtered_schedule_df_pg.at[index, 'HomeScore'] += 1
                if row['AwayTactic'] == tactics_choice_pg and home_flag_pg == 1:
                    filtered_schedule_df_pg.at[index, 'AwayScore'] += 1
                if clock_pg == 90:
                    season_games_df_pg.at[index, 'HomeScore'] = filtered_schedule_df_pg.at[index, 'HomeScore']
                    season_games_df_pg.at[index, 'AwayScore'] = filtered_schedule_df_pg.at[index, 'AwayScore']
                    season_games_df_pg.at[index, 'Status'] = 'Played'

        clock_pg += 5
    season_games_df_pg = season_games_df_pg.reset_index(drop=True)
    season_games_df_pg.index += 1
    input("O jogo terminou. Prima 'Enter' para continuar...")
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
        print_teams_list(teams_df_ct)
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
                    print_teams_list(available_teams_st)
                    team_select_st = input(f"{player_name_st} introduza o numero da equipa pretendida: ")
                    if not (team_select_st.isnumeric() and int(team_select_st) in available_teams_st.index):
                        os.system("cls")
                        print(f"O valor introduzido não e valido ou o numero não corresponde a uma equipa.")
                        team_select_st = ""
                tactics_select_st = ""
                while tactics_select_st == "":
                    os.system("cls")
                    print_tactics(tactics_df_st)
                    tactics_select_st = input(f"{player_name_st} escolha uma tatica: ")
                    if not (tactics_select_st.isnumeric() and int(tactics_select_st) <= len(tactics_df_st)):
                        os.system("cls")
                        print(f"O valor introduzido não e valido ou o numero não corresponde a uma tatica.")
                        tactics_select_st = ""
                scoreboard_df_st.loc[int(team_select_st), 'Player'] = player_name_st
                scoreboard_df_st.loc[int(team_select_st), 'Tactic'] = tactics_df_st.at[int(tactics_select_st), 'Tactic']
            return scoreboard_df_st
        else:
            print(f"O valor introduzido não e valido ou é superior ao numero de equipas disponiveis."
                  f" Apenas existem {len(scoreboard_df_st.index)} equipas.")


teams_list = ['FC Porto', 'SL Benfica', 'Sporting CP', 'SC Braga']
# , 'Vitória SC', 'Rio Ave', 'FC Famalicão','Moreirense FC']
teams_fields = ['Team']
tactics_list = ["4-4-2", "4-3-3", "5-4-1", "5-3-2", "3-4-3", "4-1-2-2-1"]
tactics_fields = ['Tactic']
num_teams = len(teams_list)
teams_df = create_dataframes(teams_list, teams_fields)
tactics_df = create_dataframes(tactics_list, tactics_fields)
season_games_df = season_games(teams_list, tactics_df)
scoreboard_df = create_scoreboard(teams_df)

menu = ()
while menu != "7":
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Dec.logo)
    menu = (input(Dec.options))
    os.system('cls' if os.name == 'nt' else 'clear')
    if menu == "1":
        play_games(season_games_df, tactics_df)
        pending_games = season_games_df.loc[season_games_df['Status'] == 'Pending']
    elif menu == "2":
        scoreboard_df[
            ['GamesPlayed', 'Wins', 'Draws', 'Losses', 'GoalsFor', 'GoalsAgainst', 'GoalDiff', 'Points']] = 0
        update_scoreboard(scoreboard_df, season_games_df)
        if season_games_df['Status'].iloc[-1] != 'Played':
            scoreboard_df = print_scoreboard(scoreboard_df)
            input("Prima 'Enter' para continuar...")
        else:
            scoreboard_df = print_scoreboard(scoreboard_df)
            print(
                f"O CAMPEAO DO CAMPEONATE É: \033[94m{scoreboard_df['Team'].iloc[0]}\033[0m com "
                f"\033[94m'{scoreboard_df['Points'].iloc[0]} pontos\033[0m")
            input("Prima 'Enter' para continuar...")
    elif menu == "3":
        season_games_df['Status'] = season_games_df.apply(color_game_status, axis=1)
        print_season_games(season_games_df)
        input("Prima 'Enter' para continuar...")
    elif menu == "4":
        scoreboard_df = select_team(scoreboard_df, tactics_df, season_games_df)
        season_games_df = update_player_season(season_games_df, scoreboard_df)
    elif menu == "5":
        teams_df = create_dataframes(teams_list, teams_fields)
        tactics_df = create_dataframes(tactics_list, tactics_fields)
        season_games_df = season_games(teams_list, tactics_df)
        scoreboard_df = create_scoreboard(teams_df)
    elif menu == "6":
        teams_df = change_teams(teams_df, season_games_df)
        teams_list = teams_df.values.flatten().tolist()
        season_games_df = season_games(teams_list, tactics_df)
        scoreboard_df = create_scoreboard(teams_df)
    elif menu == "7":
        print("Bye")
        break
    elif menu >= "8" or menu <= "0" or float(menu):
        print("Opção invalida")
