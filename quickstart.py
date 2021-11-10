import datetime as dt
from driveAPI import *

def main():
    date = dt.date.today() - dt.timedelta(days=10)
    service = create_token()
    root_folders = get_root_folders(service)
    # print(pd.DataFrame(root_folders)) ## root folders
    sub_folders = get_subfolders(service, root_folders)
    # print(pd.DataFrame(sub_folders)) ## sub folders
    recordings = get_recordings(service, sub_folders, date)
    print(pd.DataFrame(recordings)) ## sub folders
    

if __name__ == '__main__':
    main()