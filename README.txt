* NEIP: NGS Expression Integration Portal *

Web-based RNA-seq Differential Expression Browser

---

* Project Overview *
NEIP lets users upload a precomputed DESeq2 CSV, filter by log₂FC & adjusted p-value, and instantly view:
- A tabular report of all genes passing thresholds
- An interactive Chart.js bar-chart of log₂FC values
All upload events are logged to a SQLite audit table so analysis history can be revisited.

---

* Technologies & File Structure *

final/
├─ input.html         # upload form (no inline CSS/JS)
├─ upload.cgi         # handles file upload & DB logging
├─ process.cgi        # filters CSV & renders results
├─ css/
│   └─ style.css      # layout & styling
├─ js/
│   └─ chart.js       # Chart.js helper functions
└─ templates/
    └─ results.html   # HTML template for table + chart

- Python 3 CGI (/usr/local/bin/python3)
- SQLite database at /tmp/final.db (uploads table)
- string.Template for content-separated HTML
- Chart.js for client-side visualization
- Apache with ExecCGI enabled

---

* Installation & Initialization *

Copy the entire final/ directory under your web root: /var/www/html/ylai38/final/

Set permissions:
chmod 755 upload.cgi process.cgi
chmod 644 css/*.css js/*.js templates/*.html

Initialize SQLite (only once):
python3 - << 'EOF'
import sqlite3
db = sqlite3.connect("/tmp/final.db")
db.execute("""
  CREATE TABLE IF NOT EXISTS uploads (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    filename     TEXT NOT NULL,
    log2fc       REAL,
    padj         REAL,
    uploaded_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
""")
db.commit()
db.close()
print("Initialized /tmp/final.db")
EOF

---

* Usage *

1. Open the upload form
http://<host>/ylai38/final/input.html

2. Choose your DESeq2 CSV
Must include headers:
gene_symbol, gene_description, log2fc, p_value, padj

3. Set thresholds
Min log₂FC (default 1.0)
Max padj (default 0.05)

4. Click “Analyze”
CSV is saved to /tmp
Entry is logged in SQLite (/tmp/final.db)
You are redirected to the results page

5. View results
Filtered gene table
Interactive bar chart

6. Example URL with sample data: http://bfx3.aap.jhu.edu/ylai38/final/process.cgi?file=test_DESeq2_results_with_passed_genes.csv&log2fc=1&padj=0.05

---

* Database Schema *

CREATE TABLE uploads (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  filename     TEXT    NOT NULL,
  log2fc       REAL,
  padj         REAL,
  uploaded_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
Justification: A lightweight audit-log schema preserves every analysis run for reproducibility, history lookups, and future caching of enrichment results.