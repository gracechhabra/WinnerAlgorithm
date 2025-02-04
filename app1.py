#Finding the winner using Google Sheets API

from flask import Flask, render_template, jsonify
import pandas as pd
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials


app = Flask(__name__)


#Pandas to display all the lines
pd.set_option('display.max_rows', None)


#endpoint to access google sheets api
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

#Getting the credentials
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
#print(os.getenv("GOOGLE_APPLICATION_CREDENTIALS")) - accessing the keys

#Exception if it is not the credential path
if not credentials_path:
    raise Exception("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set!")
#credentials = ServiceAccountCredentials.from_json_keyfile_name('C:\\Users\\grace\\OneDrive\\Desktop\\secretkey\\techdiva-winner-a034aa76b844.json', scopes = scopes)
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scopes)

#Authorizing the file and opening the workbook
file = gspread.authorize(credentials)
workbook = file.open("Test")
sheet = workbook.get_worksheet(0)

#Accessing the data and making a data frame
data = sheet.get_all_records()
df = pd.DataFrame(data)
headers = ['name', 'school', 'correct']  # Manually define headers


# Group by the "School" column
grouped = df.groupby('school')


'''
max_rows = grouped.apply(lambda group: group.loc[group['correct'].idxmax()]).reset_index(drop=True)
print("Students with the maximum correct answers for each school:")
print(max_rows)
'''


#Function to get the maximum correct answers, if it is tied then see the most correct answers
def get_top_three(group):
    """
    Select the top three scorers from a group (e.g., per school) 
    ensuring that the same person is not chosen more than once.
    """
    top_candidates = []
    df_temp = group.copy()  # Work on a copy so we don't alter the original group

    # --- Step 1: Determine the Winner ---
    max_score = df_temp['correct'].max()
    winner_candidates = df_temp[df_temp['correct'] == max_score]
    winner = winner_candidates.loc[winner_candidates['answered'].idxmax()]
    top_candidates.append(winner)
    df_temp = df_temp[df_temp['name'] != winner['name']]  # Exclude winner

    # --- Step 2: Determine the Runner-up (2nd Place) ---
    if not df_temp.empty:
        second_max = df_temp['correct'].max()
        runner_up_candidates = df_temp[df_temp['correct'] == second_max]
        runner_up = runner_up_candidates.loc[runner_up_candidates['answered'].idxmax()]
        top_candidates.append(runner_up)
        df_temp = df_temp[df_temp['name'] != runner_up['name']]  # Exclude runner-up

    # --- Step 3: Determine the Third Place ---
    if not df_temp.empty:
        third_max = df_temp['correct'].max()
        third_candidates = df_temp[df_temp['correct'] == third_max]
        third = third_candidates.loc[third_candidates['answered'].idxmax()]
        top_candidates.append(third)

    return pd.DataFrame(top_candidates)

def get_overall_top_three(df):
    """
    Select the overall top three scorers from the entire DataFrame,
    ensuring that the same person is not chosen more than once.
    """
    top_candidates = []
    df_temp = df.copy()

    # --- Overall Winner ---
    overall_max = df_temp['correct'].max()
    overall_candidates = df_temp[df_temp['correct'] == overall_max]
    overall_winner = overall_candidates.loc[overall_candidates['answered'].idxmax()]
    top_candidates.append(overall_winner)
    df_temp = df_temp[df_temp['name'] != overall_winner['name']]

    # --- Overall Runner-up ---
    if not df_temp.empty:
        second_max = df_temp['correct'].max()
        second_candidates = df_temp[df_temp['correct'] == second_max]
        overall_runner_up = second_candidates.loc[second_candidates['answered'].idxmax()]
        top_candidates.append(overall_runner_up)
        df_temp = df_temp[df_temp['name'] != overall_runner_up['name']]

    # --- Overall Third Place ---
    if not df_temp.empty:
        third_max = df_temp['correct'].max()
        third_candidates = df_temp[df_temp['correct'] == third_max]
        overall_third = third_candidates.loc[third_candidates['answered'].idxmax()]
        top_candidates.append(overall_third)

    return pd.DataFrame(top_candidates)

# === Part 1: Top three scorers per school ===
# Group by 'school' and apply the get_top_three function.
grouped = df.groupby('school')
top_three_per_school = grouped.apply(get_top_three).reset_index(drop=True)

print("Top three scorers for each school:")
print(top_three_per_school[['name', 'school', 'correct', 'answered']])

# === Part 2: Overall top three scorers from all schools ===
overall_top_three = get_overall_top_three(df)
print("\nOverall Top Three Toppers from all schools:")
print(overall_top_three[['name', 'school', 'correct', 'answered']])

# Route to render index.html
@app.route('/')
def home():
    return render_template("index.html")

# Endpoint: Get top three scorers per school
@app.route('/get_top_three_per_school', methods=['GET'])
def get_top_three_per_school():
    grouped = df.groupby('school')
    top_three_per_school = grouped.apply(get_top_three).reset_index(drop=True)
    # Select only the required columns and convert to list of dictionaries.
    data = top_three_per_school[['name', 'school', 'correct', 'answered']].to_dict(orient='records')
    return jsonify(data)

# Endpoint: Get overall top three scorers from all schools
@app.route('/get_overall_top_three', methods=['GET'])
def get_overall_top_three_endpoint():
    overall_top_three_df = get_overall_top_three(df)
    data = overall_top_three_df[['name', 'school', 'correct', 'answered']].to_dict(orient='records')
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=False)
