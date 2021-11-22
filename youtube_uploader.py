import os
import pprint

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
import google.oauth2.credentials

scopes = ["https://www.googleapis.com/auth/youtube.upload"]
user_cred_json = 'qqqwtf.json'


def upload_media_file(filename: str, title: str, description: str):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "/Users/dipaolo/Downloads/client_secret_448446771119-fljo991dmq35ge7qk0ohchpqdl8acqeu.apps.googleusercontent.com.json"
    # "/Users/dipaolo/repos/watchdog-yt-uploader/client_secret_148455518759-u47f4culv97siandr4da4mg1vupghiuq.apps.googleusercontent.com.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)

    if not os.path.exists(user_cred_json):
        credentials = flow.run_local_server()
        print('Got new credentials')
        pprint.pprint(credentials)

        with open(user_cred_json, 'wt+') as f:
            f.write(credentials.to_json())
    else:
        print('Use previously saved credentials')
        credentials = google.oauth2.credentials.Credentials.from_authorized_user_file(user_cred_json)

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.videos().insert(
        body=dict(
            snippet=dict(
                title=title,
                description=description,
                # "tags": ["surfing", "Santa Cruz"],
                # categoryId="22",
            ),
            status=dict(
                privacyStatus="private"
            )
        ),

        # statistics,contentDetails,fileDetails,processingDetails,suggestions
        part="snippet,status",
        media_body=MediaFileUpload(filename)
    )

    print('Sending request...')
    try:
        response = request.execute()
        print('Got the response:')
        pprint.pprint(response)
    except googleapiclient.errors.HttpError as e:
        print(f'ERROR failed to upload video. Reason: {e.reason}')
