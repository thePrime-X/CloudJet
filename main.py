import psycopg2
import sqlparse

def execute_queries_from_file(cursor, filepath):
    with open(filepath, 'r') as file:
        sql_file = file.read()
    
    import sqlparse
    statements = sqlparse.split(sql_file)
    print(f"Total queries found: {len(statements)}\n")
    
    def is_select_query(query):
        lines = query.splitlines()
        for line in lines:
            stripped = line.strip()
            if stripped == '' or stripped.startswith('--'):
                continue
            return stripped.lower().startswith('select')
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
    conn = psycopg2.connect(
        dbname="CloudJet",
        user="postgres",
        password="000989",
        host="localhost",
        port="5432"
    )
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
