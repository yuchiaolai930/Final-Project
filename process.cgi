#!/usr/local/bin/python3
import cgi, cgitb, os, csv, html, math, json
from string import Template

cgitb.enable(display=True)
print("Content-Type: text/html")
print()

# 1) parse parameters
form   = cgi.FieldStorage()
fn     = form.getvalue('file')
log2fc = float(form.getvalue('log2fc', '1.0'))
padj   = float(form.getvalue('padj',   '0.05'))

tmp_path = f"/tmp/{fn}"
if not os.path.exists(tmp_path):
    print(f"<h1>Error: File not found: {html.escape(tmp_path)}</h1>")
    exit()

# 2) read & filter CSV
rows    = []
with open(tmp_path, newline='') as fh:
    reader = csv.DictReader(fh)
    headers = reader.fieldnames
    for r in reader:
        try:
            fc = abs(float(r['log2fc']))
            p  = float(r['padj'])
        except:
            continue
        if fc >= log2fc and p <= padj:
            rows.append(r)

# 3) build HTML table or no‐results message
if rows:
    ths = ''.join(f"<th>{h}</th>" for h in headers)
    trs = "".join(
        "<tr>" + "".join(f"<td>{html.escape(r[h])}</td>" for h in headers) + "</tr>"
        for r in rows
    )
    table_html = f"<table><thead><tr>{ths}</tr></thead><tbody>{trs}</tbody></table>"
else:
    table_html = "<p>No genes passed the specified thresholds.</p>"

# 4) prepare chart data
js_labels = json.dumps([r['gene_symbol'] for r in rows])
js_values = json.dumps([float(r['log2fc']) for r in rows])

# 5) render the results template
base     = os.path.dirname(__file__)
tpl_path = os.path.join(base, 'templates', 'results.html')
tpl      = Template(open(tpl_path).read())
print(tpl.substitute(
    log2fc     = log2fc,
    padj       = padj,
    table_html = table_html,
    js_labels  = js_labels,
    js_values  = js_values
))
