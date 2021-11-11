import datetime as dt
from driveAPI import *
from db import connection as sql

pd.set_option("display.max_rows", None, "display.max_columns", None)

def main():
    date = dt.date.today() - dt.timedelta(days=3)
    service = create_token()
    root_folders = get_root_folders(service)
    # # print(pd.DataFrame(root_folders)) ## root folders
    sub_folders = get_subfolders(service, root_folders)
    # # print(pd.DataFrame(sub_folders)) ## sub folders
    recordings = get_recordings(service, sub_folders, date)
    df = pd.DataFrame(recordings) ## sub folders
    df = df.applymap(str)
    df['date'] = df['name'].str.extract('.*\((.*)\).*')
    df['id_employee'] = df['name'].str.extract('(\d{6})')
    df['id_registry'] = df['name'].str.extract('(\d{8})')

    engine = sql.get_connection()
    df.to_sql('tbl_recording_drive_temp', con = engine, if_exists = 'replace')
    sql.conn_close(engine)    

if __name__ == '__main__':
    main()