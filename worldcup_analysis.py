import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("FIFA_World_Cup_2026_Analysis.xlsx", sheet_name="Matches")

print(df.head())

# QUESTION 1
# Which teams scored the most goals, and which teams conceded the fewest?

teams = pd.read_excel("FIFA_World_Cup_2026_Analysis.xlsx", sheet_name="Teams")

# Goals scored by each team
home_goals = df.groupby("home_team_id")["home_score"].sum()
away_goals = df.groupby("away_team_id")["away_score"].sum()

goals_scored = home_goals.add(away_goals, fill_value=0)

# Goals conceded by each team
home_conceded = df.groupby("home_team_id")["away_score"].sum()
away_conceded = df.groupby("away_team_id")["home_score"].sum()

goals_conceded = home_conceded.add(away_conceded, fill_value=0)

# Put the results together
team_goals = teams[["team_id", "team_name"]].copy()

team_goals["goals_scored"] = team_goals["team_id"].map(goals_scored)
team_goals["goals_conceded"] = team_goals["team_id"].map(goals_conceded)

team_goals = team_goals.fillna(0)

print(team_goals.sort_values("goals_scored", ascending=False).head(10))

print(team_goals.sort_values("goals_conceded").head(10))


# Bar chart for goals scored

top_scoring_teams = team_goals.sort_values(
    "goals_scored", ascending=False
).head(10)

plt.figure(figsize=(8, 5))

plt.bar(
    top_scoring_teams["team_name"],
    top_scoring_teams["goals_scored"]
)

plt.xticks(rotation=45)
plt.title("Top 10 Teams by Goals Scored")
plt.xlabel("Team")
plt.ylabel("Goals")

plt.tight_layout()
plt. savefig("top_10_goals_scored.png")


# Teams that conceded the fewest goals

fewest_conceded = team_goals.sort_values(
    "goals_conceded"
).head(10)

print(fewest_conceded)

plt.figure(figsize=(8, 5))

plt.bar(
    fewest_conceded["team_name"],
    fewest_conceded["goals_conceded"]
)

plt.xticks(rotation=45)
plt.title("Teams with the Fewest Goals Conceded")
plt.xlabel("Team")
plt.ylabel("Goals Conceded")

plt.tight_layout()

plt.savefig("fewest_goals_conceded.png")


# QUESTION 2
# How are shots, shots on target, possession and xG related to match outcomes?

team_stats = pd.read_excel(
    "FIFA_World_Cup_2026_Analysis.xlsx",
    sheet_name="Team_Stats"
)

print(team_stats.head())
print(team_stats.columns)

# Match results

matches = pd.read_excel(
    "FIFA_World_Cup_2026_Analysis.xlsx",
    sheet_name="Matches"
)

print(matches.head())
print(matches.columns)
print(team_stats.columns.tolist())


# QUESTION 2
# How are shots, shots on target, possession and xG related to match outcomes?

team_stats = pd.read_excel(
    "FIFA_World_Cup_2026_Analysis.xlsx",
    sheet_name="Team_Stats"
)

matches = pd.read_excel(
    "FIFA_World_Cup_2026_Analysis.xlsx",
    sheet_name="Matches"
)

# Home team results

home = matches[[
    "match_id",
    "home_team_id",
    "home_score",
    "away_score",
    "home_xg"
]].copy()

home["team_id"] = home["home_team_id"]
home["xg"] = home["home_xg"]

home["result"] = "Draw"
home.loc[home["home_score"] > home["away_score"], "result"] = "Win"
home.loc[home["home_score"] < home["away_score"], "result"] = "Loss"

# Away team results

away = matches[[
    "match_id",
    "away_team_id",
    "home_score",
    "away_score",
    "away_xg"
]].copy()

away["team_id"] = away["away_team_id"]
away["xg"] = away["away_xg"]

away["result"] = "Draw"
away.loc[away["away_score"] > away["home_score"], "result"] = "Win"
away.loc[away["away_score"] < away["home_score"], "result"] = "Loss"

# Combine home and away results

results = pd.concat([home, away])

# Join results with team statistics

team_stats = team_stats.merge(
    results[["match_id", "team_id", "result", "xg"]],
    on=["match_id", "team_id"],
    how="left"
)

# Average statistics by match result

result_stats = team_stats.groupby("result")[[
    "possession_pct",
    "total_shots",
    "shots_on_target",
    "xg"
]].mean()

print(result_stats)


# Question 2: How do match statistics relate to match outcomes?

result_stats.plot(kind="bar")

plt.title("Match Statistics by Result")
plt.xlabel("Result")
plt.ylabel("Average")
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig("match_statistics_by_result.png")


# QUESTION 2:
# How are possession, shots, shots on target and xG related to match outcomes?

# Calculate correlation between the main performance variables
correlation = team_stats[
    ["possession_pct", "total_shots", "shots_on_target", "xg"]
].corr()

print("\nCorrelation between possession, shots, shots on target and xG:")
print(correlation)


# Correlation heatmap for Question 2

plt.figure(figsize=(8, 6))

plt.imshow(correlation, cmap="coolwarm", interpolation="nearest")

plt.colorbar(label="Correlation")

plt.xticks(
    range(len(correlation.columns)),
    correlation.columns,
    rotation=45
)

plt.yticks(
    range(len(correlation.columns)),
    correlation.columns
)

# Add correlation values to the heatmap
for i in range(len(correlation.columns)):
    for j in range(len(correlation.columns)):
        plt.text(
            j,
            i,
            f"{correlation.iloc[i, j]:.2f}",
            ha="center",
            va="center"
        )

plt.title("Correlation Between Possession, Shots and xG")
plt.tight_layout()

plt.savefig("question_2_correlation_heatmap.png")



# QUESTION 3: PLAYER PERFORMANCE
# Load player statistics
player_stats = pd.read_excel(
    "FIFA_World_Cup_2026_Analysis.xlsx",
    sheet_name="Player_Stats"
)


print("\nQUESTION 3: PLAYER PERFORMANCE")

# Make a clean copy of player statistics
players = player_stats.copy()

# Convert reliable player statistics to numeric
numeric_columns = [
    "goals",
    "assists",
    "minutes_played",
    "matches_played",
    "matches_started"
]

for col in numeric_columns:
    if col in players.columns:
        players[col] = pd.to_numeric(players[col], errors="coerce")

# Remove players without names
players = players[players["player_name"].notna()].copy()

# Fill missing values in the reliable statistics with 0
for col in numeric_columns:
    if col in players.columns:
        players[col] = players[col].fillna(0)


# 1. TOP 10 PLAYERS BY GOALS

print("\nTop 10 players by goals:")

top_goals = (
    players[
        ["player_name", "goals", "assists",
         "minutes_played", "matches_played", "matches_started"]
    ]
    .sort_values("goals", ascending=False)
    .head(10)
)

print(top_goals.to_string(index=False))


# 2. TOP 10 PLAYERS BY ASSISTS

print("\nTop 10 players by assists:")

top_assists = (
    players[
        ["player_name", "goals", "assists",
         "minutes_played", "matches_played", "matches_started"]
    ]
    .sort_values("assists", ascending=False)
    .head(10)
)

print(top_assists.to_string(index=False))


# 3. TOP 10 PLAYERS BY GOAL CONTRIBUTIONS

players["goal_contributions"] = (
    players["goals"] + players["assists"]
)

print("\nTop 10 players by goal contributions:")

top_contributions = (
    players[
        ["player_name", "goals", "assists",
         "goal_contributions", "minutes_played"]
    ]
    .sort_values(
        ["goal_contributions", "goals"],
        ascending=[False, False]
    )
    .head(10)
)

print(top_contributions.to_string(index=False))


# 4. GOAL CONTRIBUTIONS PER 90 MINUTES

# Avoid division by zero
players["goal_contributions_per_90"] = 0.0

players.loc[
    players["minutes_played"] > 0,
    "goal_contributions_per_90"
] = (
    players.loc[
        players["minutes_played"] > 0,
        "goal_contributions"
    ]
    / players.loc[
        players["minutes_played"] > 0,
        "minutes_played"
    ]
    * 90
)

# Only include players who played at least 180 minutes
# This avoids ranking players based on very small playing time.

players_90 = players[
    players["minutes_played"] >= 180
].copy()

print("\nTop 10 players by goal contributions per 90 minutes")
print("(Minimum 180 minutes played):")

top_per_90 = (
    players_90[
        ["player_name", "goals", "assists",
         "goal_contributions", "minutes_played",
         "goal_contributions_per_90"]
    ]
    .sort_values("goal_contributions_per_90", ascending=False)
    .head(10)
)

print(top_per_90.to_string(index=False))


# 5. MOST EXPERIENCED PLAYERS BY MATCHES PLAYED

print("\nTop 10 players by matches played:")

top_matches = (
    players[
        ["player_name", "matches_played",
         "matches_started", "minutes_played",
         "goals", "assists"]
    ]
    .sort_values("matches_played", ascending=False)
    .head(10)
)
print(top_matches.to_string(index=False))

# Step 8: Create a chart for Question 3 - Player Performance

import matplotlib.pyplot as plt

# Calculate goal contributions
player_stats["goal_contributions"] = (
    player_stats["goals"] + player_stats["assists"]
)

# Select the top 10 players by goal contributions
top_10_players = (
    player_stats
    .sort_values("goal_contributions", ascending=False)
    .head(10)
)

# Create the bar chart
top_10_players.plot(
    x="player_name",
    y="goal_contributions",
    kind="bar",
    figsize=(10, 6),
    legend=False
)

plt.title("Top 10 Players by Goal Contributions")
plt.xlabel("Player")
plt.ylabel("Goals + Assists")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# Step 9: Save the chart
plt.savefig(
    "question_3_player_performance.png",
    dpi=300,
    bbox_inches="tight"
)

# Step 10: Display the chart
plt.show()


# QUESTION 4: How did team performance differ between group and knockout stages?
# Load the tournament stages data

stages = pd.read_excel(

    "FIFA_World_Cup_2026_Analysis.xlsx",

    sheet_name="Stages"

)

# Step 2: Create clean copies of the required datasets

# Step 1: Create clean copies of the matches, team statistics and stage data
print("\nQUESTION 4: TEAM PERFORMANCE — GROUP VS KNOCKOUT")

matches_q4 = matches.copy()
team_stats_q4 = team_stats.copy()
stages_q4 = stages.copy()

# Step 2: Convert match ID and stage/team ID columns to numeric values
for col in ["match_id", "stage_id", "home_team_id", "away_team_id"]:
    if col in matches_q4.columns:
        matches_q4[col] = pd.to_numeric(
            matches_q4[col],
            errors="coerce"
        )

# Step 3: Convert team statistics IDs to numeric values
for col in ["match_id", "team_id"]:
    if col in team_stats_q4.columns:
        team_stats_q4[col] = pd.to_numeric(
            team_stats_q4[col],
            errors="coerce"
        )

# Step 4: Add stage information to each match
matches_q4 = matches_q4.merge(
    stages_q4[["stage_id", "stage_name", "is_knockout"]],
    on="stage_id",
    how="left"
)

# Step 5: Display the different tournament stages
print("\nStage summary:")

print(
    matches_q4[
        ["stage_name", "is_knockout"]
    ]
    .drop_duplicates()
    .sort_values("is_knockout")
    .to_string(index=False)
)

# Step 6: Add the stage information to the team statistics
team_stats_q4 = team_stats_q4.merge(
    matches_q4[
        ["match_id", "stage_name", "is_knockout"]
    ],
    on="match_id",
    how="left"
)

# Step 7: Separate group-stage statistics from knockout-stage statistics
group_stats = team_stats_q4[
    team_stats_q4["is_knockout"] == False
].copy()

knockout_stats = team_stats_q4[
    team_stats_q4["is_knockout"] == True
].copy()

# Step 8: Count the number of team-match observations in each stage
print("\nNumber of team-match observations:")

print("Group Stage:", len(group_stats))
print("Knockout Stage:", len(knockout_stats))

# Step 9: Select the main performance variables to compare
performance_columns = [
    "possession_pct",
    "total_shots",
    "shots_on_target",
    "xg"
]

# Step 10: Keep only performance variables that exist in the dataset
available_columns = [
    col for col in performance_columns
    if col in team_stats_q4.columns
]

# Step 11: Calculate the average performance for each stage
stage_comparison = (
    team_stats_q4
    .groupby("is_knockout")[available_columns]
    .mean()
    .reset_index()
)

# Step 12: Replace True and False with readable stage names
stage_comparison["stage"] = stage_comparison["is_knockout"].map({
    False: "Group Stage",
    True: "Knockout Stage"
})

# Step 13: Arrange the results into an easy-to-read table
stage_comparison = stage_comparison[
    ["stage"] + available_columns
]

# Step 14: Display the average performance comparison
print("\nAverage team performance by stage:")

print(
    stage_comparison.to_string(index=False)
)

# Step 15: Compare total goals scored in the two stages
if "goals" in team_stats_q4.columns:

    print("\nGoals scored by stage:")

    goal_comparison = (
        team_stats_q4
        .groupby("is_knockout")["goals"]
        .sum()
        .reset_index()
    )

    # Step 16: Add readable stage names to the goal results
    goal_comparison["stage"] = goal_comparison["is_knockout"].map({
        False: "Group Stage",
        True: "Knockout Stage"
    })

    # Step 17: Display total goals for each stage
    print(
        goal_comparison[
            ["stage", "goals"]
        ].to_string(index=False)
    )
    print(comparison.to_string())

  
    # Step 3: Create a chart for the Group Stage and Knockout Stage comparison


stage_comparison.set_index("stage")[
    ["possession_pct", "total_shots", "shots_on_target", "xg"]
].plot(
    kind="bar",
    figsize=(10, 6)
)

plt.title("Team Performance: Group Stage vs Knockout Stage")
plt.xlabel("Tournament Stage")
plt.ylabel("Average Value")
plt.xticks(rotation=0)

plt.legend(
    ["Possession (%)", "Total Shots", "Shots on Target", "xG"]
)

plt.tight_layout()

# Step 4: Save the chart
plt.savefig(
    "question_4_team_performance.png",
    dpi=300,
    bbox_inches="tight"
)

# Step 5: Display the chart
plt.show()

# QUESTION 5: Is xG a useful indicator of actual goals in the tournament?

# Step 1: Create a clean copy of the match data
matches_q5 = matches.copy()

# Step 2: Check the available columns in the Matches dataset
print("\nQuestion 5: xG vs Actual Goals")
print("\nMatches columns:")
print(matches_q5.columns.tolist())

# Step 3: Select xG and actual goals for the home teams
home_data = matches_q5[
    ["home_xg", "home_score"]
].copy()

# Step 4: Select xG and actual goals for the away teams
away_data = matches_q5[
    ["away_xg", "away_score"]
].copy()

# Step 5: Rename the columns so both teams use the same names
home_data.columns = [
    "xg",
    "actual_goals"
]

away_data.columns = [
    "xg",
    "actual_goals"
]

# Step 6: Combine the home and away team observations
q5_data = pd.concat(
    [home_data, away_data],
    ignore_index=True
)

# Step 7: Convert xG and actual goals to numeric values
q5_data["xg"] = pd.to_numeric(
    q5_data["xg"],
    errors="coerce"
)

q5_data["actual_goals"] = pd.to_numeric(
    q5_data["actual_goals"],
    errors="coerce"
)

# Step 8: Remove rows with missing xG or actual goals
q5_data = q5_data.dropna(
    subset=["xg", "actual_goals"]
)

# Step 9: Calculate the correlation between xG and actual goals
correlation = q5_data["xg"].corr(
    q5_data["actual_goals"]
)

# Step 10: Display the number of observations
print(
    "\nNumber of team-match observations:",
    len(q5_data)
)

# Step 11: Display the correlation
print(
    "\nCorrelation between xG and actual goals:",
    round(correlation, 3)
)

# Step 12: Display a sample of the data
print("\nSample of xG and actual goals:")
print(
    q5_data.head(10).to_string(index=False)
)

# Step 13: Create a scatter plot
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))

plt.scatter(
    q5_data["xg"],
    q5_data["actual_goals"]
)

plt.title(
    "Expected Goals (xG) vs Actual Goals"
)

plt.xlabel(
    "Expected Goals (xG)"
)

plt.ylabel(
    "Actual Goals"
)

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()

# Step 14: Save the chart
plt.savefig(
    "question_5_xg_vs_actual_goals.png",
    dpi=300,
    bbox_inches="tight"
)

# Step 15: Display the chart
plt.show()

# QUESTION 6: Do possession and shot volume correspond with winning more matches?

# Step 1: Create clean copies of the match and team statistics data
matches_q6 = matches.copy()
team_stats_q6 = team_stats.copy()

# Step 2: Merge match information with team statistics
q6_data = team_stats_q6.merge(
    matches_q6[
        [
            "match_id",
            "home_team_id",
            "away_team_id",
            "home_score",
            "away_score"
        ]
    ],
    on="match_id",
    how="left"
)

# Step 3: Create a column showing whether the team was home or away
q6_data["team_location"] = q6_data.apply(
    lambda row:
        "Home" if row["team_id"] == row["home_team_id"]
        else "Away",
    axis=1
)

# Step 4: Calculate the result for each team
def get_result(row):

    if row["team_location"] == "Home":

        if row["home_score"] > row["away_score"]:
            return "Win"

        elif row["home_score"] < row["away_score"]:
            return "Loss"

        else:
            return "Draw"

    else:

        if row["away_score"] > row["home_score"]:
            return "Win"

        elif row["away_score"] < row["home_score"]:
            return "Loss"

        else:
            return "Draw"


q6_data["result"] = q6_data.apply(
    get_result,
    axis=1
)

# Step 5: Convert possession and shots to numeric values
q6_data["possession_pct"] = pd.to_numeric(
    q6_data["possession_pct"],
    errors="coerce"
)

q6_data["total_shots"] = pd.to_numeric(
    q6_data["total_shots"],
    errors="coerce"
)

# Step 6: Display average possession and shots by result
q6_summary = (
    q6_data
    .groupby("result")[
        ["possession_pct", "total_shots"]
    ]
    .mean()
    .round(2)
)

print("\nQuestion 6: Possession and Shot Volume vs Match Outcome")
print("\nAverage possession and shots by result:")
print(q6_summary)

# Step 7: Create box plots
import matplotlib.pyplot as plt

fig, axes = plt.subplots(
    1,
    2,
    figsize=(12, 5)
)

q6_data.boxplot(
    column="possession_pct",
    by="result",
    ax=axes[0]
)

axes[0].set_title("Possession by Match Result")
axes[0].set_xlabel("Match Result")
axes[0].set_ylabel("Possession (%)")

q6_data.boxplot(
    column="total_shots",
    by="result",
    ax=axes[1]
)

axes[1].set_title("Total Shots by Match Result")
axes[1].set_xlabel("Match Result")
axes[1].set_ylabel("Total Shots")

plt.suptitle("")
plt.tight_layout()

# Step 8: Save the chart
plt.savefig(
    "question_6_possession_shots_vs_result.png",
    dpi=300,
    bbox_inches="tight"
)

# Step 9: Display the chart
plt.show()


# QUESTION 7: What match/event patterns stand out for cards, penalties and goals?

# Step 1: Load the Events sheet from the Excel workbook
events_q7 = pd.read_excel(
    "FIFA_World_Cup_2026_Analysis.xlsx",
    sheet_name="Events"
)

# Step 2: Display the available columns
print("\nQuestion 7: Match and Event Patterns")

print("\nEvents columns:")
print(events_q7.columns.tolist())

# Step 3: Check the event types
print("\nEvent types:")

print(
    events_q7["event_type"]
    .value_counts()
)

# Step 4: Count each type of event
event_counts = (
    events_q7["event_type"]
    .value_counts()
    .reset_index()
)

event_counts.columns = [
    "event_type",
    "count"
]

# Step 5: Display the event counts
print("\nEvent counts:")

print(
    event_counts.to_string(index=False)
)

# Step 6: Convert event type to text
event_text = (
    events_q7["event_type"]
    .astype(str)
    .str.lower()
)

# Step 7: Count goal events
goal_events = events_q7[
    event_text.str.contains("goal")
]

# Step 8: Count card events
card_events = events_q7[
    event_text.str.contains("card")
]

# Step 9: Count penalty events
penalty_events = events_q7[
    event_text.str.contains("penalty")
]

# Step 10: Display the number of goals, cards and penalties
print("\nNumber of goals:", len(goal_events))

print("Number of cards:", len(card_events))

print("Number of penalties:", len(penalty_events))

# Step 11: Create a chart of the most common event types
import matplotlib.pyplot as plt

top_events = event_counts.head(10)

plt.figure(figsize=(10, 6))

plt.bar(
    top_events["event_type"],
    top_events["count"]
)

plt.title(
    "Most Common Match Events"
)

plt.xlabel(
    "Event Type"
)

plt.ylabel(
    "Number of Events"
)

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

# Step 12: Save the chart
plt.savefig(
    "question_7_match_event_patterns.png",
    dpi=300,
    bbox_inches="tight"
)

# Step 13: Display the chart
plt.show()

# QUESTION 8: What match/event patterns stand out for cards, penalties and goals?

# Step 1: Load the Events dataset from the Excel workbook
events = pd.read_excel(
    "FIFA_World_Cup_2026_Analysis.xlsx",
    sheet_name="Events"
)

# Step 2: Display the Events columns
print("\nQuestion 8: Match/Event Patterns")
print("\nEvents columns:")
print(events.columns.tolist())

# Step 3: Check the first few rows of the Events dataset
print("\nFirst few event records:")
print(events.head().to_string(index=False))

# Step 4: Count how many times each event type occurred
event_counts = events["event_type"].value_counts()

# Step 5: Display the frequency of each event type
print("\nNumber of events by type:")
print(event_counts.to_string())

# Step 6: Calculate the number of goals
number_of_goals = event_counts.get("Goal", 0)

# Step 7: Calculate the number of yellow cards
number_of_yellow_cards = event_counts.get("Yellow Card", 0)

# Step 8: Calculate the number of red cards
number_of_red_cards = event_counts.get("Red Card", 0)

# Step 9: Calculate the number of penalty shootout misses
number_of_penalty_shootout_misses = event_counts.get(
    "Penalty Shootout Miss",
    0
)

# Step 10: Calculate the number of penalty shootout goals
number_of_penalty_shootout_goals = event_counts.get(
    "Penalty Shootout Goal",
    0
)

# Step 11: Calculate the number of own goals
number_of_own_goals = event_counts.get("Own Goal", 0)

# Step 12: Display the key event statistics
print("\nKey match/event statistics:")
print("Number of goals:", number_of_goals)
print("Number of yellow cards:", number_of_yellow_cards)
print("Number of red cards:", number_of_red_cards)
print("Number of penalty shootout misses:", number_of_penalty_shootout_misses)
print("Number of penalty shootout goals:", number_of_penalty_shootout_goals)
print("Number of own goals:", number_of_own_goals)

# Step 13: Select the main match events for the chart

main_events = [
    "Goal",
    "Assist",
    "Yellow Card",
    "Penalty Shootout Goal",
    "Own Goal",
    "Red Card",
    "Penalty Shootout Miss",
    "VAR Review"
]

event_chart = event_counts[
    event_counts.index.isin(main_events)
].sort_values()

# Step 14: Create a clear horizontal bar chart

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))

bars = plt.barh(
    event_chart.index,
    event_chart.values
)

plt.title("Main Match Event Patterns")
plt.xlabel("Number of Events")
plt.ylabel("Event Type")

# Step 15: Add the event numbers to the bars

for bar in bars:
    width = bar.get_width()

    plt.text(
        width + 2,
        bar.get_y() + bar.get_height() / 2,
        str(int(width)),
        va="center"
    )

plt.tight_layout()

# Step 16: Save the Question 8 chart

plt.savefig(
    "question_8_match_event_patterns.png",
    dpi=300,
    bbox_inches="tight"
)

# Step 17: Display the chart

plt.show()

# Step 16: Save the Question 8 results to Excel
q8_summary = pd.DataFrame({
    "Event Type": event_counts.index,
    "Number of Events": event_counts.values
})

with pd.ExcelWriter(
    "FIFA_World_Cup_2026_Analysis.xlsx",
    engine="openpyxl",
    mode="a",
    if_sheet_exists="replace"
) as writer:

    q8_summary.to_excel(
        writer,
        sheet_name="Q8_Event_Patterns",
        index=False
    )

print("\nQuestion 8 analysis completed successfully.")