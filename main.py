import pandas as pd
s2017_df = pd.read_csv('2017_season_data.csv')
players_df = pd.read_csv('player_data.csv')

s2017_df.head()
players_df.head()

# Data Wrangling

## Merge s2017_df and players_df with a left join.
df = s2017_df.merge(players_df, how='left', left_on='Player', right_on="Name")

## Are there misses (mismatches) in the resulting dataframe?
df['name'].isna().any()
                    
## How many rows could not be matched?
df['name'].isna().sum()

## Extract the names of the player that could not be matched.
player_misses = list(df.loc[df['name'].isna(), 'Player'].values())
player_misses

## Modify players_df with the correct names to re-try a successful merge.
players_df.head()

# players_df.      #season 2017
names_mapping = {
    "Luc Mbah a Moute" : "Luc Mbah",
    "Sheldan Mac"      : "Sheldon McClellan",
    "James Michael McAdoo" : "James Michael",
    "Metta World Peace": "Metta World"
}
#players_df.loc[players_df['name'] == "Luc Mbah a Moute", 'name'] = 'Luc Mbah'

for new_name, name_2017 in names_mapping.items():
    players_df.loc[players_df['name'] == new_name, 'name'] = name_2017

## Perform the merge between s2017_df and players_df again, this time, without misses
df = s2017_df.merge(players_df, how='left', left_on='Player', right_on="Name")
df['name'].isna() # No misses!

## Remove unnecessary columns.
columns_to_drop = [
    "Year",
    "PER",
    "TS%",
    "3PAr"
]
df.drop(columns=columns_to_drop, inplace=True)

## Rename teams to their full name.
team_mapping = {
    "OKC": "Oklahoma City Thunder",
    "DAL": "Dallas Mavericks",
    "BRK": "Brooklyn Nets",
    "SAC": "Sacramento Kings",
    "NOP": "New Orleans Pelicans",
    "MIN": "Minnesota Timberwolves",
    "SAS": "San Antonio Spurs",
    "IND": "Indiana Pacers",
    "MEM": "Memphis Grizzlies",
    "POR": "Portland Trail Blazers",
    "CLE": "Cleveland Cavaliers",
    "LAC": "Los Angeles Clippers",
    "PHI": "Philadelphia 76ers",
    "HOU": "Houston Rockets",
    "MIL": "Milwaukee Bucks",
    "NYK": "New York Knicks",
    "DEN": "Denver Nuggets",
    "ORL": "Orlando Magic",
    "MIA": "Miami Heat",
    "PHO": "Phoenix Suns",
    "GSW": "Golden State Warriors",
    "CHO": "Charlotte Hornets",
    "DET": "Detroit Pistons",
    "ATL": "Atlanta Hawks",
    "WAS": "Washington Wizards",
    "LAL": "Los Angeles Lakers",
    "UTA": "Utah Jazz",
    "BOS": "Boston Celtics",
    "CHI": "Chicago Bulls",
    "TOR": "Toronto Raptors"
}

df['Team'] = df['Tm'].replace(team_mapping)

## Convert birthday to a datetime object.
df.head()
df['birth_date'] = pd.to_datetime(df['birth_date'])

## Delete all players from the TOT team
#df_copy = df.copy()

df = df.loc[df['Tm'] != 'TOT']


# Analysis!

## What is the team with the most players in the league?
df['Team'].value_counts().head()

## What is the team with the lowest FG?
df.groupby('Team')['FG'].sum().sort_values().head()

## What is the team with the best FG%?
fg_per_team = df.groupby('Team')[]'FG', 'FGA']].sum()
fg_per_team.head()

fg_per_team['FG%'] = fg_per_team['FG'] / fg_per_team['FGA']
fg_per_team.sort_values(by='FG%', ascending=False).head()

## What is the difference between the best and worst 3P shooters (by position)?
pos_3p_acc = df.groupby('Pos')[['3P', '3PA']].sum()
pos_3p_acc['3P%'] = pos_3p_acc['3P'] / pos_3p_acc['3PA']
pos_3p_acc['3P%'].max() - pos_3p_acc['3P%'].min()

## Find the best scorers in each team
#TEAM = 'BOS'
#max_points_in_team = df.loc[df['Tm'] == TEAM, 'PTS'].max()
#df.loc[(df['Tm'] == TEAM) & (df['PTS'] == max_points_in_team)]

#df['Best Score per Team'] = df.groupby('Team')['PTS'].transform('max')
#df.loc[df['Tm'] == 'OKC', ['Player', 'Tm', 'PTS', 'Best Score per Term']].sort_values(by='PTS', ascending=False)
#df.loc[df['Tm'] == 'BOS', ['Player', 'Tm', 'PTS', 'Best Score per Term']].sort_values(by='PTS', ascending=False)
#df.loc[df['Tm'] == 'CHI', ['Player', 'Tm', 'PTS', 'Best Score per Term']].sort_values(by='PTS', ascending=False)

best_scorers_per_team = df.loc[
                            df['PTS'] == df['Best Score per Team'], ['Player', 'Tm', 'PTS']
                            ].sort_values(by='PTS', ascending=False)

best_scorers_per_team

## Which team has the 'youngest squad', by average player age?
df.groupby('Team')['birth_date'].mean().sort_values()
