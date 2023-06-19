import random
from googleapiclient.discovery import build
# Update the list of analytics categories
analytics_categories = [
    "Total videos watched",
    "Most viewed category",
    "Average watch time",
    "Longest video watched",
    "Shortest video watched",
    "Favorite video",
    "Most watched day of the week",
    "Most watched month",
    "Top watched channels",
    "Top watched playlists",
    "Most common video length",
    "Most liked video",
    "Most disliked video",
    "Average likes per video",
    "Average dislikes per video",
    "Total comments posted",
    "Most commented video",
    "Top commented channels",
    "Average comments per video",
    "Most subscribed channel",
    "Average views per video",
    "Top watch time by category",
    "Most active hour of the day",
    "Oldest video watched",
    "Newest video watched",
    "Favorite playlist",
    "Average videos watched per day",
    "Top recommended channels",
    "Most shared video"
]

def get_random_analytics():
    """
    Retrieves a random analytics category.
    """
    return random.choice(analytics_categories)

def main():
    subscribed_channels = get_subscribed_channels()

    # Retrieve and print channel view counts
    channel_view_counts = []
    for channel_id in subscribed_channels:
        view_count = get_channel_view_count(channel_id)
        channel_view_counts.append((channel_id, view_count))

    channel_view_counts.sort(key=lambda x: x[1], reverse=True)

    print("Channels You Watch the Most:")
    for channel_id, view_count in channel_view_counts[:5]:
        channel_title = get_channel_title(channel_id)
        print(f"{channel_title}: {view_count} views")

    print("\nChannels You Watch the Least:")
    for channel_id, view_count in channel_view_counts[-5:]:
        channel_title = get_channel_title(channel_id)
        print(f"{channel_title}: {view_count} views")

    # Prompt the user to select the number of analytics to receive
    while True:
        try:
            num_analytics = int(input("\nEnter the number of analytics you want to receive (0 for all): "))
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    if num_analytics == 0:
        analytics_list = analytics_categories
    else:
        analytics_list = random.sample(analytics_categories, num_analytics)

    print("\nAdditional Analytics:")
    for analytics_category in analytics_list:
        print(analytics_category)

if __name__ == "__main__":
    main()
