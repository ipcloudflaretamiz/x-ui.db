import sqlite3

def transfer_data():
    destination_db = input("Enter the destination database path (e.g., /etc/x-ui/x-ui.db): ")
    num_backups = int(input("Enter the number of backup databases: "))
    
    backup_dbs_input = input("Enter the names of backup databases (comma separated, e.g., x-ui1.db,x-ui2.db): ")
    backup_dbs = backup_dbs_input.split(',')
    
    base_path = '/etc/x-ui/'
    
    for i in range(len(backup_dbs)):
        backup_dbs[i] = base_path + backup_dbs[i]

    destination_conn = sqlite3.connect(destination_db)
    destination_cursor = destination_conn.cursor()

    for db in backup_dbs:
        source_conn = sqlite3.connect(db)
        source_cursor = source_conn.cursor()

        source_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = source_cursor.fetchall()

        for table in tables:
            table_name = table[0]
            source_cursor.execute(f"SELECT * FROM {table_name};")
            rows = source_cursor.fetchall()

            destination_cursor.execute(f"PRAGMA foreign_keys=off;")
            source_cursor.execute(f"PRAGMA foreign_keys=off;")
            
            source_cursor.execute(f"PRAGMA table_info({table_name});")
            columns = source_cursor.fetchall()
            columns_str = ', '.join([col[1] for col in columns])
            placeholders = ', '.join(['?' for _ in range(len(columns))])

            for row in rows:
                destination_cursor.execute(f"INSERT OR IGNORE INTO {table_name} ({columns_str}) VALUES ({placeholders})", row)

            destination_conn.commit()

        source_conn.close()

    destination_conn.close()

    print("Data transfer from multiple backups completed successfully!")

if __name__ == "__main__":
    transfer_data()
