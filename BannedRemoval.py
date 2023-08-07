from RedditCredentials import reddit
import pandas as pd
import prawcore
import praw
from tqdm import tqdm
import time

def check_subreddit_ban(subreddit_name):
    try:
        subreddit = reddit.subreddit(subreddit_name)
        subreddit.title
        return False  # Subreddit is not banned
    except prawcore.exceptions.UnavailableForLegalReasons:
        print(f"Subreddit '{subreddit_name}' is banned in your location due to legal reasons.")
        return True  # Subreddit is banned
    except praw.exceptions.ClientException as e:
        print(f"Error checking subreddit: {subreddit_name}, Error: {e}")
        return False  # Consider the subreddit as not banned to continue the loop
 

def remove_banned_subreddits(csv_file):
    df_subreddits = pd.read_csv(csv_file)
    banned_subreddits = []

    for _, row in tqdm(df_subreddits.iterrows(), total=len(df_subreddits), desc="Checking Subreddits"):
        subreddit_name = row['Subreddit']
        if check_subreddit_ban(subreddit_name):
            banned_subreddits.append(subreddit_name)
        time.sleep(0.5)
            
    df_subreddits = df_subreddits[~df_subreddits['Subreddit'].isin(banned_subreddits)]

    # Save the updated CSV file without banned subreddits
    df_subreddits.to_csv('updated_subreddits.csv', index=False)

    return banned_subreddits

if __name__ == "__main__":
    csv_file_path = 'subreddit_data.csv'

    banned_subreddits = remove_banned_subreddits(csv_file_path)

    print("Banned Subreddits:")
    for subreddit_name in banned_subreddits:
        print(subreddit_name)
