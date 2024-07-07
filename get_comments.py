import pandas as pd
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Replace 'YOUR_API_KEY' with your actual API key
API_KEY = 'your actual API key'
# Video ID for the YouTube video you want to get comments from
VIDEO_ID = 'eogpIG53Cis'

# Function to get all comment threads for a given video ID
def get_all_comment_threads(api_key, video_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    comment_threads = []
    next_page_token = None
    retries = 5

    while True:
        try:
            # Request comment threads from the YouTube API
            response = youtube.commentThreads().list(
                part='snippet,replies',
                videoId=video_id,
                maxResults=100,
                pageToken=next_page_token
            ).execute()

            # Add retrieved comment threads to the list
            comment_threads.extend(response['items'])

            # Check for next page token
            next_page_token = response.get('nextPageToken')
            if next_page_token is None:
                break

        except HttpError as e:
            if e.resp.status in [403, 500, 503]:
                # Retry in case of server errors
                print(f"Server error: {e}. Retrying in 5 seconds...")
                time.sleep(5)
                retries -= 1
                if retries == 0:
                    print("Maximum retries reached. Exiting.")
                    break
            else:
                # Break for other errors
                print(f"An error occurred: {e}")
                break

    return comment_threads

# Function to get replies for a given parent comment ID
def get_replies(youtube, parent_id):
    replies = []
    next_page_token = None
    retries = 5

    while True:
        try:
            # Request replies from the YouTube API
            response = youtube.comments().list(
                part='snippet',
                parentId=parent_id,
                maxResults=100,
                pageToken=next_page_token
            ).execute()

            # Add retrieved replies to the list
            replies.extend(response['items'])

            # Check for next page token
            next_page_token = response.get('nextPageToken')
            if next_page_token is None:
                break

        except HttpError as e:
            if e.resp.status in [403, 500, 503]:
                # Retry in case of server errors
                print(f"Server error: {e}. Retrying in 5 seconds...")
                time.sleep(5)
                retries -= 1
                if retries == 0:
                    print("Maximum retries reached. Exiting.")
                    break
            else:
                # Break for other errors
                print(f"An error occurred: {e}")
                break

    return replies

# Function to extract comments from comment threads
def extract_comments(comment_threads, youtube):
    parent_comments = []
    replied_comments = []

    for thread in comment_threads:
        # Extract top-level (parent) comment
        top_level_comment = thread['snippet']['topLevelComment']['snippet']
        parent_comments.append({
            'comment_id': thread['id'],
            'author': top_level_comment['authorDisplayName'],
            'text': top_level_comment['textDisplay'],
            'like_count': top_level_comment['likeCount'],
            'published_at': top_level_comment['publishedAt'],
            'parent_comment': None  # No parent comment for top-level comments
        })

        # Fetch replies for each parent comment
        if 'replies' in thread:
            replies = get_replies(youtube, thread['id'])
            for reply in replies:
                reply_snippet = reply['snippet']
                replied_comments.append({
                    'comment_id': reply['id'],
                    'author': reply_snippet['authorDisplayName'],
                    'text': reply_snippet['textDisplay'],
                    'like_count': reply_snippet['likeCount'],
                    'published_at': reply_snippet['publishedAt'],
                    'parent_comment': top_level_comment['textDisplay']
                })

    return parent_comments, replied_comments

# Function to get all comments (both parent and replied) for a given video ID
def get_all_comments(api_key, video_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    comment_threads = get_all_comment_threads(api_key, video_id)
    parent_comments, replied_comments = extract_comments(comment_threads, youtube)

    # Convert lists of comments to DataFrames
    parent_df = pd.DataFrame(parent_comments)
    replied_df = pd.DataFrame(replied_comments)

    # Convert 'published_at' column to datetime
    parent_df['published_at'] = pd.to_datetime(parent_df['published_at'])
    replied_df['published_at'] = pd.to_datetime(replied_df['published_at'])

    return parent_df, replied_df

if __name__ == "__main__":
    # Get all comments for the specified video ID
    parent_df, replied_df = get_all_comments(API_KEY, VIDEO_ID)
    # Save comments to CSV files
    parent_df.to_csv('parent_comments_test.csv', index=False)
    replied_df.to_csv('children_comments_test.csv', index=False)
    # Print summary information
    print(f"Saved {len(parent_df)} parent comments to parent_comments.csv")
    print(f"Saved {len(replied_df)} replied comments to replied_comments.csv")
    print(parent_df.head())
    print(replied_df.head())
