
#!pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import json

# Email of the Service Account
#SERVICE_ACCOUNT_EMAIL ='<some-id>@developer.gserviceaccount.com'

#Path to the Service Account's Private Key file
SERVICE_ACCOUNT_KEY_FILE_PATH = ''

#Rename email account
def rename_email():
    None

#Suspend email account
def suspend_email():
    None

#Create email group
def create_email_group():
    None

#Update email group's owner
def update_email_group_owner():
    None

#Create a matter
def create_matter():
    None

#Create an Email Export
def create_email_export():
    None

#Create a Drive Export
def create_drive_export():
    None

#Download export files from Cloud Storage
def download_export_files():
    None

#Upload export files to Google Drive
def upload_export_files():
    None

#List exports
def list_exports(service, matter_id):
    return service.matters().exports().list(matterId=matter_id).execute()

#Get an export
def get_export_by_id(service, matter_id, export_id):
    return service.matters().exports().get(
        matterId=matter_id, exportId=export_id).execute()

#Delete an export
def delete_export_by_id(service, matter_id, export_id):
    return service.matters().exports().delete(
    matterId=matter_id, exportId=export_id).execute()

def create_credentials(service_name, service_version, service_scopes, admin_email):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        filename = SERVICE_ACCOUNT_KEY_FILE_PATH,
        scopes = service_scopes
    )

    credentials = credentials.create_delegated(admin_email)

    return build(service_name, service_version, credentials=credentials)


    """Build and returns and Admin SDK Directory service object authorized with the 
    service accounts that act on behalf of the given user.

    Args:
        user_email: The email of the user. Needs permissions to access the Admin APIs.
    Returns:
        Admin SDK directory service object.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        filename = SERVICE_ACCOUNT_KEY_FILE_PATH,
                scopes=['https://www.googleapis.com/auth/admin.directory.user']
    )

    credentials = credentials.create_delegated(user_email)

    return build('admin','directory_v1', credentials=credentials)

def main():
    #Administration account
    admin_email = ''

    #GOOGLE DIRECTORY SERVICE Scopes
    directory_srv_scopes = ['https://www.googleapis.com/auth/admin.directory.user'] 
    
    #GOOGLE VAULT SERVICE Scopes
    vault_srv_scopes = ['https://www.googleapis.com/auth/ediscovery']

    #GOOGLE CLOUD STORAGE Scopes
    storage_srv_scopes = []

    #GOOGLE DRIVE Scopes
    drive_srv_scopes = []
    
    directory_service = create_credentials('admin','directory_v1', directory_srv_scopes, admin_email)
    vault_service = create_credentials('vault', 'v1',vault_srv_scopes, admin_email)
    storage_service = None
    drive_service = None



    # Call the Admin SDK Directory API
    # print('Getting the first 10 users in the domain')
    # obj_directory = directory_service.users().list(customer='my_customer', maxResults=10,
    #                             orderBy='email').execute()
    # users = obj_directory.get('users', [])

    # print(users[2])
    # if not users:
    #     print('No users in the domain.')
    # else:
    #     print('Users:')
    #     for user in users:
    #         print(u'{0} ({1})'.format(user['primaryEmail'],
    #             user['name']['fullName']))


    # Call the Vault API

    print('\n\n\nGetting all matters from in Google Vault')
    obj_vault = vault_service.matters().list(pageSize=10).execute()
    matters = obj_vault.get('matters', [])

    if not matters:
        print('No matters found.')
    else:
        print('Matters:')
        for matter in matters:
            print(u'{} ({})'.format(matter.get('name'), matter.get('matterId')))

    print('\n\nList of exports')
    exports = list_exports(vault_service,matters[0].get('matterId')).get('exports',[])
    print(u'\n\nExport Id: \n{}'.format(exports[0]['id']))

    
    export_obj = get_export_by_id(vault_service, matters[0].get('matterId'), exports[0]['id'])
    print(u'\nGetting first export...\n{}'.format(export_obj))

if __name__ == '__main__':
    main()
