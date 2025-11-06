import psycopg2
import sqlparse
from urllib.parse import urlparse
import config

def get_conn_from_uri(uri):
    result = urlparse(uri)
    return psycopg2.connect(
        dbname=result.path.lstrip('/'),
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )

def execute_queries_from_file(cursor, filepath):
    with open(filepath, 'r') as file:
        sql_file = file.read()
    
    statements = sqlparse.split(sql_file)
    print(f"Total queries found: {len(statements)}\n")
    
    def is_select_query(query):
        lines = query.splitlines()
        for line in lines:
            stripped = line.strip().lower()
            if stripped == '' or stripped.startswith('--'):
                continue
            return stripped.startswith('select') or stripped.startswith('with')
        return False
    
    for i, query in enumerate(statements, start=1):
        query = query.strip()
        if not query:
            print(f"Skipping empty query {i}")
            continue
        
        print(f"\n--- Executing Query {i} ---\n{query}\n")
        try:
            cursor.execute(query)
            if is_select_query(query):
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
            else:
                print("Query executed.")
        except Exception as e:
            print(f"Error executing query {i}: {e}")

def main():
    print("Starting script...")
    conn = get_conn_from_uri(config.DB_URI)
    cursor = conn.cursor()
    
    # test connection
    cursor.execute("SELECT 1;")
    print(f"Test query output: {cursor.fetchone()}")
    
    execute_queries_from_file(cursor, 'queries.sql')
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
