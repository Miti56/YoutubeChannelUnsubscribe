import os
import pickle
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Path to the credentials JSON file downloaded in Step 1
CLIENT_SECRET_FILE = 'path/to/client_secret.json'
# Path to store the user's token (will be created if it doesn't exist)
TOKEN_PICKLE_FILE = 'path/to/token.pickle'
# Number of channels to display
NUM_CHANNELS = 5

# Define the scopes required for the YouTube API
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

def get_authenticated_service():
    # Check if the token file exists
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, 'rb') as token:
            credentials = pickle.load(token)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PICKLE_FILE, 'wb') as token:
            pickle.dump(credentials, token)

    return build('youtube', 'v3', credentials=credentials)

def get_watched_videos(service):
    # Retrieve the watched videos using the YouTube API
    response = service.activities().list(part='snippet,contentDetails', mine=True, maxResults=50).execute()

    videos = []
    for item in response['items']:
        if item['snippet']['type'] == 'watch':
            video = {
                'title': item['snippet']['title'],
                'channel_title': item['snippet']['channelTitle']
            }
            videos.append(video)

    return videos

def count_videos_per_channel(videos):
    channel_counts = {}
    for video in videos:
        channel_title = video['channel_title']
        if channel_title in channel_counts:
            channel_counts[channel_title] += 1
        else:
            channel_counts[channel_title] = 1

    return channel_counts

def print_most_least_watched_channels(channel_counts):
    sorted_channels = sorted(channel_counts.items(), key=lambda x: x[1], reverse=True)

    print(f"Most watched channels ({NUM_CHANNELS} channels):")
    for channel, count in sorted_channels[:NUM_CHANNELS]:
        print(f"{channel}: {count} videos")

    print(f"\nLeast watched channels ({NUM_CHANNELS} channels):")
    for channel, count in sorted_channels[-NUM_CHANNELS:]:
        print(f"{channel}: {count} videos")

def main():
    service = get_authenticated_service()
    videos = get_watched_videos(service)
    channel_counts = count_videos_per_channel(videos)
    print_most_least_watched_channels(channel_counts)

if __name__ == '__main__':
    main()
