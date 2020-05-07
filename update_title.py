from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from time import sleep
# Imported necessary libraries

CLIENT_SECRETS_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

# Building the API
flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
credentials = flow.run_console()
youtube = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def update_video(video_id, old_title):
    # Executing the request for video statistics
    request = youtube.videos().list(part="statistics", id=video_id)
    response = request.execute()
    response = response['items'][0]['statistics']

    # Creating new title
    data = {'views': response['viewCount'], 'likes': response['likeCount'], 'dislikes': response['dislikeCount'],
            'comments': response['dislikeCount']}
    title = f'This Video Has {data["views"]} Views, {data["likes"]} Likes, {data["dislikes"]} Dislikes and {data["comments"]} Comments'

    if old_title != title:
        # Executing the request to update the title
        video_response = youtube.videos().list(id=video_id, part='snippet').execute()
        video_snippet = video_response['items'][0]['snippet']
        video_snippet['title'] = title
        published_at = video_snippet['publishedAt']
        if len(published_at) == 20:
            published_at = published_at[:19] + '.000' + published_at[19]
            video_snippet['publishedAt'] = published_at
        video_update_response = youtube.videos().update(part='snippet', body=dict(snippet=video_snippet, id=video_id)).execute()

        # Printing the title
        print('The Updated Title is: ' + video_update_response['snippet']['title'])
    else:
        # Printing that the title didn't change
        print("The title didn't change.")
    return title


if __name__ == '__main__':
    # Getting old title
    video_response = youtube.videos().list(id='VIDEO ID', part='snippet').execute()  # Put video ID here
    video_snippet = video_response['items'][0]['snippet']
    old_title = video_snippet['title']
    while True:
        try:
            old_title = update_video('VIDEO ID', old_title)  # Put video ID here
        except HttpError as e:
            print('An HTTP error {} occurred: {}'.format(e.resp.status, e.content))
        sleep(600)  # Waiting to prevent reaching the quota maximum
