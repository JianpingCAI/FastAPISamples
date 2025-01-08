
# DuckDB issues

## ondelete="CASCADE" is not supported by duckdb, explain and revise the implementation

```bash
sqlalchemy.exc.ProgrammingError: (duckdb.duckdb.ParserException) Parser Error: FOREIGN KEY constraints cannot use CASCADE, SET NULL or SET DEFAULT
[SQL:
CREATE TABLE file_system (
        id VARCHAR NOT NULL,
        name VARCHAR NOT NULL,
        parent_id VARCHAR,
        PRIMARY KEY (id),
        FOREIGN KEY(parent_id) REFERENCES file_system (id) ON DELETE CASCADE
)

]
```

### Reference: <https://duckdb.org/docs/sql/statements/create_table.html>

Foreign keys have the following limitations.

- Foreign keys with cascading deletes (FOREIGN KEY ... REFERENCES ... ON DELETE CASCADE) are not supported.

- Inserting into tables with self-referencing foreign keys is currently not supported and will result in the following error:

Constraint Error: Violates foreign key constraint because key "..." does not exist in the referenced table.
Generated Columns
