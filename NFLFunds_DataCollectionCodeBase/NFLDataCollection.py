import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

weeks = [9, 10, 11, 12]
all_weeks_df = pd.DataFrame()  # Initialize an empty DataFrame to hold all weeks' data

for week in weeks:
    url = f"https://www.pro-football-reference.com/years/2023/week_{week}.htm"

    # Regex pattern for NFL team names
    team_name_regex = r'\b(49ers|Bears|Bengals|Bills|Broncos|Browns|Buccaneers|Cardinals|Chargers|Chiefs|Colts|Cowboys|Dolphins|Eagles|Falcons|Giants|Jaguars|Jets|Lions|Packers|Panthers|Patriots|Raiders|Rams|Ravens|Redskins|Saints|Seahawks|Steelers|Texans|Titans|Vikings)\b'

    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response was an HTTP error

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")
        tables = soup.find_all('table')

        # List to hold the DataFrames
        dfs = []
        for table in tables:
            df = pd.read_html(str(table))[0]

            # Check if column 0 exists and contains a team name
            if 0 in df.columns and any(re.search(team_name_regex, str(team)) for team in df[0]):
                df['Week'] = f"""Week {week}"""
                df['Date'] = df[0][0]
                df.rename(columns={0: 'Team', 1: 'Score'}, inplace=True)
                df = df[['Week','Date', 'Team', 'Score']]
                dfs.append(df)

        # Concatenate all DataFrames in the list
        final_df = pd.concat(dfs, ignore_index=True)

        date_day_regex = r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b \d{1,2}, \d{4}|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday'

        # Filter out rows where the 'Team' column matches the date or day regex
        filtered_df = final_df[~final_df['Team'].str.contains(date_day_regex, na=False)]

        points_allowed = []

        for i in range(0, len(filtered_df), 2):
            points_allowed.append(filtered_df.iloc[i + 1]['Score'])  # Add the score of the next team
            points_allowed.append(filtered_df.iloc[i]['Score'])      # Add the score of the current team

        filtered_df['Points Allowed'] = points_allowed

        # Append the week's data to the all_weeks_df DataFrame
        all_weeks_df = pd.concat([all_weeks_df, filtered_df], ignore_index=True)

        print(filtered_df)

    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

# Write the complete DataFrame to a CSV file
all_weeks_df.to_csv(r'C:\Users\anura\OneDrive\Documents\Python Scripts\FoolAround\nfl_scores.csv', index=False)
