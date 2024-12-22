import sqlite3
import random
import string

def generate_random_name(length=8):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

def generate_random_port(min_port=1000, max_port=8000):
    return random.randint(min_port, max_port)

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

    inbound_name = generate_random_name()
    inbound_port = generate_random_port()

    print(f"Generated Inbound Name: {inbound_name}")
    print(f"Generated Inbound Port: {inbound_port}")

    try:
        destination_cursor.execute(f"INSERT INTO inbounds (listen, port) VALUES (?, ?)", (inbound_name, inbound_port))
        destination_conn.commit()
        print(f"Successfully inserted inbound with name: {inbound_name} and port: {inbound_port}")
    except sqlite3.Error as e:
        print(f"Error inserting into inbounds: {e}")

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
