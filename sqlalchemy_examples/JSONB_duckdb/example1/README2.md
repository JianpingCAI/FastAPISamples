# JSONB

## Introduction

JSONB stands for "JSON Binary". It is a format that stores JSON data in a decomposed binary format. This means the data is not stored as a plain text JSON document but rather in a binary representation that allows for more efficient querying and manipulation.

<https://sqlite.org/draft/jsonb.html>

The advantage of JSONB over ordinary text RFC 8259 JSON is that JSONB is both slightly smaller (by between 5% and 10% in most cases) and can be processed in less than half the number of CPU cycles. The built-in JSON SQL functions of SQLite can accept either ordinary text JSON or the binary JSONB encoding for any of their JSON inputs.

The "JSONB" name is inspired by PostgreSQL, but the on-disk format for SQLite's JSONB is not the same as PostgreSQL's. The two formats have the same name, but they have wildly different internal representations and are not in any way binary compatible.

The central idea behind this JSONB specification is that each element begins with a header that includes the size and type of that element. The header takes the place of punctuation such as double-quotes, curly-brackes, square-brackets, commas, and colons. Since the size and type of each element is contained in its header, the element can be read faster since it is no longer necessary to carefully scan forward looking for the closing delimiter. The payload of JSONB is the same as for corresponding text JSON. The same payload bytes occur in the same order. The only real difference between JSONB and ordinary text JSON is that JSONB includes a binary header on each element and omits delimiter and separator punctuation.

### Differences Between JSON and JSONB

PostgreSQL supports two JSON-related data types: JSON and JSONB.

- JSON type stores an exact copy of the input text, which preserves whitespace, the order of object keys, and is generally used when the JSON data is simply to be stored and retrieved without being modified or queried intensively.
- JSONB, in contrast, stores data in a decomposed binary format and not as original JSON text. It removes duplicate keys in the JSON object, only keeping the last value of each key set. It does not preserve whitespace, nor the order of object keys, but it allows indexing, which can significantly improve the performance of various operations.

### Advantages of JSONB

- Efficient Queries: JSONB supports GIN (Generalized Inverted Index) indexing, which can make searching within JSON documents very fast.
- Data Manipulation: With JSONB, you can use a variety of operators to manipulate the JSON data directly in the database—for example, adding or deleting keys from JSON objects.
- Space Efficiency: Although JSONB typically requires more disk space than plain JSON due to its binary format, it can be more space-efficient when it comes to eliminating redundancy in JSON keys and array elements.

## JSONB Suport

### PostgreSQL

Supports two JSON-related data types: JSON and JSONB.

### SQLite

Beginning with version 3.45.0 (pending), SQLite supports an alternative binary encoding of JSON which we call "JSONB".
<https://sqlite.org/draft/jsonb.html>

### DuckDB
