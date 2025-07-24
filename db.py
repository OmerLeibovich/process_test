import psycopg2

def insert(processes,db_config,delete):

    conn = psycopg2.connect(
        database=db_config["dbname"],
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        port=db_config["port"]
    )

    cursor = conn.cursor()
    if delete:
        cursor.execute("DROP TABLE IF EXISTS process_summary;")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS process_summary (
        id SERIAL PRIMARY KEY,
        pid INTEGER NOT NULL,
        name TEXT NOT NULL,
        avg_cpu_usage FLOAT NOT NULL,
        avg_memory_usage FLOAT NOT NULL,
        sample_count INTEGER NOT NULL,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    for process in processes:
        cursor.execute("""
        INSERT INTO process_summary(pid, name, avg_cpu_usage, avg_memory_usage, sample_count, last_updated)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            process.pid,
            process.name,
            process.cpu,
            process.memoryInfo,
            process.count,
            process.date,
        ))
    conn.commit()
    cursor.close()
    conn.close()

