# NBA 2017 Data Analysis Project

This project involves analyzing NBA 2017 season data to uncover various insights about team performances, player statistics, and more.

## Dataset

The datasets used in this analysis are:
- `2017_season_data.csv`: Contains information about the 2017 NBA season.
- `player_data.csv`: Contains detailed player information.

## Setup

1. Install necessary packages:
    ```sh
    pip install pandas
    ```
2. Load the datasets:
    ```python
    import pandas as pd
    s2017_df = pd.read_csv('2017_season_data.csv')
    players_df = pd.read_csv('player_data.csv')
    s2017_df.head()
    players_df.head()
    ```

## Data Wrangling

### 1. Merge Datasets
Merge `s2017_df` and `players_df` using a left join:
```python
df = s2017_df.merge(players_df, how='left', left_on='Player', right_on='Name')
```

### 2. Identify Mismatches
Check for mismatches in the resulting dataframe:
```python
df['name'].isna().any()  # Are there misses?
df['name'].isna().sum()  # How many rows could not be matched?
player_misses = list(df.loc[df['name'].isna(), 'Player'].values())
print(player_misses)     # Names of players that could not be matched
```

### 3. Correct Names and Retry Merge
Modify `players_df` with the correct names:
```python
names_mapping = {
    "Luc Mbah a Moute": "Luc Mbah",
    "Sheldan Mac": "Sheldon McClellan",
    "James Michael McAdoo": "James Michael",
    "Metta World Peace": "Metta World"
}
for new_name, name_2017 in names_mapping.items():
    players_df.loc[players_df['name'] == new_name, 'name'] = name_2017

df = s2017_df.merge(players_df, how='left', left_on='Player', right_on='Name')
df['name'].isna().any()  # Ensure no misses
```

### 4. Remove Unnecessary Columns
Drop unnecessary columns:
```python
columns_to_drop = ["Year", "PER", "TS%", "3PAr"]
df.drop(columns=columns_to_drop, inplace=True)
```

### 5. Rename Teams
Rename teams to their full names:
```python
team_mapping = {
    "OKC": "Oklahoma City Thunder", "DAL": "Dallas Mavericks", "BRK": "Brooklyn Nets", 
    "SAC": "Sacramento Kings", "NOP": "New Orleans Pelicans", "MIN": "Minnesota Timberwolves", 
    "SAS": "San Antonio Spurs", "IND": "Indiana Pacers", "MEM": "Memphis Grizzlies", 
    "POR": "Portland Trail Blazers", "CLE": "Cleveland Cavaliers", "LAC": "Los Angeles Clippers", 
    "PHI": "Philadelphia 76ers", "HOU": "Houston Rockets", "MIL": "Milwaukee Bucks", 
    "NYK": "New York Knicks", "DEN": "Denver Nuggets", "ORL": "Orlando Magic", 
    "MIA": "Miami Heat", "PHO": "Phoenix Suns", "GSW": "Golden State Warriors", 
    "CHO": "Charlotte Hornets", "DET": "Detroit Pistons", "ATL": "Atlanta Hawks", 
    "WAS": "Washington Wizards", "LAL": "Los Angeles Lakers", "UTA": "Utah Jazz", 
    "BOS": "Boston Celtics", "CHI": "Chicago Bulls", "TOR": "Toronto Raptors"
}
df['Team'] = df['Tm'].replace(team_mapping)
```

### 6. Convert Birthdate to Datetime
Convert the birthdate to a datetime object:
```python
df['birth_date'] = pd.to_datetime(df['birth_date'])
```

### 7. Remove 'TOT' Team
Remove all players from the 'TOT' team:
```python
df = df.loc[df['Tm'] != 'TOT']
```

## Analysis

### 1. Team with the Most Players
Identify the team with the most players:
```python
df['Team'].value_counts().head()
```

### 2. Team with the Lowest Field Goals (FG)
Identify the team with the lowest FG:
```python
df.groupby('Team')['FG'].sum().sort_values().head()
```

### 3. Team with the Best Field Goal Percentage (FG%)
Calculate FG% for each team:
```python
fg_per_team = df.groupby('Team')[['FG', 'FGA']].sum()
fg_per_team['FG%'] = fg_per_team['FG'] / fg_per_team['FGA']
fg_per_team.sort_values(by='FG%', ascending=False).head()
```

### 4. Difference Between Best and Worst 3P Shooters by Position
Calculate the difference in 3P% between the best and worst shooters by position:
```python
pos_3p_acc = df.groupby('Pos')[['3P', '3PA']].sum()
pos_3p_acc['3P%'] = pos_3p_acc['3P'] / pos_3p_acc['3PA']
difference_3p = pos_3p_acc['3P%'].max() - pos_3p_acc['3P%'].min()
print(difference_3p)
```

### 5. Best Scorers in Each Team
Identify the best scorers in each team:
```python
df['Best Score per Team'] = df.groupby('Team')['PTS'].transform('max')
best_scorers_per_team = df.loc[df['PTS'] == df['Best Score per Team'], ['Player', 'Tm', 'PTS']].sort_values(by='PTS', ascending=False)
best_scorers_per_team
```

### 6. Team with the Youngest Squad
Find the team with the youngest squad by average player age:
```python
df.groupby('Team')['birth_date'].mean().sort_values()
```

## What I Learned

Through this project, I learned several key data science concepts and skills, including:

- **Data Wrangling**: Handling mismatches, cleaning data, and merging datasets to ensure data consistency and accuracy.
- **Data Cleaning**: Identifying and correcting data inconsistencies, dealing with missing values, and ensuring the dataset is ready for analysis.
- **Data Exploration and Visualization**: Using exploratory data analysis (EDA) techniques to understand data distribution, patterns, and relationships.
- **Feature Engineering**: Creating new features that help in better understanding and modeling the data.
- **Data Analysis**: Applying grouping, aggregation, and analytical techniques to derive meaningful insights from the data.
- **Pandas Proficiency**: Utilizing the Pandas library for data manipulation, which is a crucial skill for any data scientist.
- **Problem-Solving**: Tackling real-world data issues and finding solutions to ensure accurate and reliable analysis.

## How This Will Help Me Practice Data Science Concepts for the Industry

This project provided practical experience in data science, helping me develop skills that are highly relevant to the industry:

1. **Real-World Data Handling**: By working with real-world data, I learned to navigate the complexities and imperfections that are common in industry datasets. This practice is crucial for preparing me to handle data in a professional environment.
2. **Analytical Thinking**: Performing various analyses helped me hone my ability to think analytically and derive actionable insights from data. This skill is vital for making data-driven decisions in the industry.
3. **Technical Skills**: Gaining proficiency with tools and libraries like Pandas, which are essential for data manipulation and analysis in professional settings. This hands-on experience is directly applicable to industry tasks.
4. **Data-Driven Decision Making**: Understanding how to use data to make informed decisions, a crucial aspect of many roles in data science and analytics. This project helped me practice making decisions based on data insights.
5. **Communication**: Documenting my process and findings in a clear and organized manner, which is important for collaborating with stakeholders and presenting results in the industry. This practice is essential for effectively communicating complex data insights.

## Conclusion

This analysis provides insights into various performance metrics of NBA teams and players during the 2017 season. It can be used to understand trends and make informed decisions based on historical data. Through this project, I have gained valuable experience and skills that will aid my journey in the data science industry.
