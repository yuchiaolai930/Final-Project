#!/usr/local/bin/python3
import sqlite3, os
os.makedirs("database", exist_ok=True)
conn = sqlite3.connect("database/final.db")
cur  = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS uploads (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  filename     TEXT     NOT NULL,
  log2fc       REAL,
  padj         REAL,
  uploaded_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS enrichments (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  upload_id    INTEGER   NOT NULL,
  term         TEXT,
  pvalue       REAL,
  description  TEXT,
  FOREIGN KEY(upload_id) REFERENCES uploads(id)
);
""")

conn.commit()
conn.close()

print("Initialized database at database/final.db")
