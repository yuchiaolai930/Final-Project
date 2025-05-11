#!/usr/local/bin/python3
import cgi
import cgitb
import os
import shutil
import sqlite3
from string import Template

# Enable detailed error pages
cgitb.enable(display=True)

# 1) HTTP header
print("Content-Type: text/html")
print()

# 2) Only allow POST via the form
if os.environ.get("REQUEST_METHOD", "").upper() != "POST":
    print('<meta http-equiv="refresh" content="0; url=/ylai38/final/input.html">')
    exit()

# 3) Parse form inputs
form = cgi.FieldStorage()
if "csvfile" not in form:
    print("<h1>Error: No file uploaded.</h1>")
    print('<p>Please <a href="/ylai38/final/input.html">go back</a> and choose a file.</p>')
    exit()

fileitem = form["csvfile"]
if not fileitem.filename:
    print("<h1>Error: No file uploaded.</h1>")
    exit()

log2fc = form.getvalue("log2fc", "1.0")
padj   = form.getvalue("padj",   "0.05")

# 4) Save the uploaded CSV to /tmp
fn       = os.path.basename(fileitem.filename)
tmp_path = f"/tmp/{fn}"
with open(tmp_path, "wb") as f:
    shutil.copyfileobj(fileitem.file, f)

# 5) Open (or create) the SQLite DB in /tmp and ensure the uploads table exists
db_path = "/tmp/final.db"
conn    = sqlite3.connect(db_path)
cur     = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS uploads (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  filename     TEXT     NOT NULL,
  log2fc       REAL,
  padj         REAL,
  uploaded_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")
conn.commit()

# 6) Insert this upload record
cur.execute(
  "INSERT INTO uploads(filename, log2fc, padj) VALUES (?,?,?)",
  (fn, float(log2fc), float(padj))
)
conn.commit()
conn.close()

# 7) Redirect to results via your HTML template
base        = os.path.dirname(__file__)
tpl_path    = os.path.join(base, "templates", "redirect.html")
redirect_to = f"/ylai38/final/process.cgi?file={fn}&log2fc={log2fc}&padj={padj}"

tpl = Template(open(tpl_path).read())
print(tpl.substitute(redirect_url=redirect_to))
