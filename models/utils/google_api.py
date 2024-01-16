
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from models.adapters.form_adapter import FormAdapter




async def upload_files_to_drive(user_id, file_name):
    form_adapter = FormAdapter()
    user_form = await form_adapter.get_fio_by_id(user_id)
    folder_name = user_form.user_fio
    if not folder_name:
        folder_name = "Аноним"

    SCOPES = ["https://www.googleapis.com/auth/drive"]


    CREDENTIALS_FILE = "credentials.json"
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPES)
    httpAuth = credentials.authorize(httplib2.Http())



    try:
        service = build("drive", "v3", http=httpAuth)

        response = service.files().list(
            q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
            spaces="drive"
        ).execute()
        if not response['files']:
            file_metadata = {
                "name": folder_name,
                "mimeType": "application/vnd.google-apps.folder",
                "parents": ["18R5I4oGyoRVGo7E3JQlbKto_LsboWX65"],
                "type": "anyone",
                "role": "reader"
            }
            permissions ={
                "type": "anyone",
                "role": "reader"
            }
            file = service.files().create(body=file_metadata, fields="id").execute()
            folder_id = file.get("id")
            service.permissions().create(fileId=folder_id, body=permissions).execute()

        else:
            folder_id = response['files'][0]['id']

        file_metadata = {
                "name" : file_name,
                "parents": [folder_id],
                "type": "anyone",
                "role": "reader"
            }
        media = f"files/user_documents/{user_id}/{file_name}"
        upload_file = service.files().create(body=file_metadata,
                                                 media_body=media,
                                                 fields="id").execute()

        file_metadata0 = {
            "file_id": upload_file,
            "type": "anyone",
            "role": "reader"
        }
        service.permissions().create(fileId=upload_file["id"], body=file_metadata0).execute()
        print("Backed up file :" + file_name)

    except HttpError as e:
        print("Error " + str(e))

    if folder_id:
        folder_link = f"https://drive.google.com/drive/folders/{folder_id}?usp=drive_link"
    else:
        folder_link = None

    #results = service.files().list(pageSize=1000,
    #                              fields="nextPageToken, files(id, name, mimeType, shared)").execute()

    return folder_link


