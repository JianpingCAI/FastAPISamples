import duckdb

# 1. Create an in-memory DuckDB database and connect
conn = duckdb.connect(database=":memory:")

# 2. Create parent and child tables
conn.execute(
    """
    CREATE TABLE parent (
        parent_id INTEGER PRIMARY KEY,
        parent_name VARCHAR
    );
"""
)

conn.execute(
    """
    CREATE TABLE child (
        child_id INTEGER PRIMARY KEY,
        parent_id INTEGER NOT NULL,
        child_value VARCHAR,
        FOREIGN KEY (parent_id) REFERENCES parent(parent_id)
    );
"""
)

# 3. Insert sample data
conn.execute(
    """
    INSERT INTO parent (parent_id, parent_name) VALUES
        (1, 'Parent A'),
        (2, 'Parent B'),
        (3, 'Parent C');
"""
)

conn.execute(
    """
    INSERT INTO child (child_id, parent_id, child_value) VALUES
        (11, 1, 'Child of A'),
        (12, 1, 'Another Child of A'),
        (21, 2, 'Child of B'),
        (31, 3, 'Child of C'),
        (32, 3, 'Another Child of C');
"""
)

print("\n--- Before Deletion ---")
print("Parent table:")
print(conn.execute("SELECT * FROM parent;").fetchall())
print("\nChild table:")
print(conn.execute("SELECT * FROM child;").fetchall())

# 4. Manual "cascade" delete with transaction
parent_to_delete = 1

# Use one transaction for both deletions
conn.execute("BEGIN;")
conn.execute("DELETE FROM child WHERE parent_id = ?;", [parent_to_delete])
conn.execute("DELETE FROM parent WHERE parent_id = ?;", [parent_to_delete])
conn.execute("COMMIT;")
conn.execute("CHECKPOINT;")
print("\nDeletion succeeded. Transaction committed.")

print("\n--- After Attempted Deletion of Parent A ---")
print("Parent table:")
print(conn.execute("SELECT * FROM parent;").fetchall())
print("\nChild table:")
print(conn.execute("SELECT * FROM child;").fetchall())
