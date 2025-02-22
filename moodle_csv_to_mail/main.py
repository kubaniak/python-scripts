import pandas as pd

# Load the CSV file
df = pd.read_csv("courseid_24581_participants.csv", delimiter=",")

# Extract the emails and join them with a semicolon
emails = ";".join(df["E-Mail-Adresse"].dropna())

# Print the result
print(emails)