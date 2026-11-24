import csv,json
from pathlib import Path
from collections import Counter
from html import escape
def rows(name):return list(csv.DictReader(open('exports/'+name+'.csv')))
def bars(items):
    top=max(v for _,v in items)
    return ''.join(f'<div class="bar"><span>{k}</span><i><b style="width:{100*v/top:.2f}%"></b></i><strong>{v:,}</strong></div>' for k,v in items)
def table(headers,records):
    return '<div class="scroll"><table><thead><tr>'+''.join('<th>'+h+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+escape(str(x))+'</td>' for x in row)+'</tr>' for row in records)+'</tbody></table></div>'
def metrics(items):
    return '<div class="metrics">'+''.join(f'<div><span>{k}</span><strong>{v}</strong></div>' for k,v in items)+'</div>'
def panel(title,body):return '<article><h2>'+title+'</h2>'+body+'</article>'
ar=rows('ar_aging_report'); bank=rows('reconciliation_matches');claim=rows('reimbursement_claims');vendors=rows('vendor_invoices'); aging=Counter(); regions=Counter()
for r in ar:
    if r['ar_status']=='overdue':
        aging[r['aging_bucket']]+=int(r['num_invoices']);regions[r['region']]+=int(r['num_invoices'])
late=sum(aging.values());counts=Counter(r['status'] for r in bank)
nb=json.loads(Path('Morphle_FinOps_Project.ipynb').read_text())
out=''.join(nb['cells'][19]['outputs'][0]['text'])
assert 'ROC-AUC: 0.6' in out and '0.10      0.68' in out and '16254' in out
p1=metrics([('Overdue invoices',f'{late:,}'),('91+ days overdue',f"{aging['91+ days overdue']:,}"),('Share aged 91+ days',f"{100*aging['91+ days overdue']/late:.1f}%")])+panel('Overdue invoices by age',bars([(s,aging[s]) for s in ['1-30 days overdue','31-60 days overdue','61-90 days overdue','91+ days overdue']]))+panel('Regional collections queue',bars(regions.most_common()))+panel('Delivery performance','<p>First Class had the highest late-delivery rate in the notebook’s shipping analysis. Rates ranged from <strong>94.7% in LATAM</strong> to <strong>96.2% in Middle East &amp; Africa</strong>.</p>')
p2=metrics([('Holdout ROC-AUC','0.600'),('Overdue recall','68%'),('Overdue precision','10%')])+panel('How to read this model','<p>The model flagged about 68 of every 100 overdue invoices. Only about 10 of every 100 flagged invoices were actually overdue. That trade-off creates a large manual review queue.</p>')+panel('Holdout results',table(['Actual class','Invoices','Precision','Recall'],[('Paid','14,977','94%','45%'),('Overdue','1,277','10%','68%')]))+panel('Which differences appeared in the simulation?',table(['Comparison','Test','p-value'],[('Region vs. overdue status','Chi-square','<0.0001'),('Customer segment vs. overdue status','Chi-square','0.7365'),('Sales value for paid vs. overdue orders','Welch t-test','0.0117')])+'<p class="note">Payment risk was assigned partly by region in the simulator. The region result reflects that assumption. These metrics describe simulated outcomes.</p>')
labels={'matched':'Cleared','unmatched':'Unmatched','amount_mismatch':'Amount mismatch','ambiguous':'Ambiguous'}
exceptions=[(r['bank_txn_id'],r['ledger_txn_id'] or '—',labels[r['status']],r['variance'] or '—') for r in bank if r['status']!='matched']
openap=[r for r in vendors if r['status'] in ['overdue','pending']]
p3=metrics([('Bank entries',len(bank)),('Cleared',counts['matched']),('Open for review',len(exceptions))])+panel('Reconciliation outcomes',bars([(labels[k],v) for k,v in counts.most_common()]))+panel('Open bank entries','<label>Show <select id="filter"><option>All exceptions</option><option>Unmatched</option><option>Amount mismatch</option><option>Ambiguous</option></select></label><p id="shown" aria-live="polite"></p><div id="queue">'+table(['Bank ID','Ledger ID','Outcome','Signed variance'],exceptions)+'</div>')+panel('Other finance controls',f'<p><strong>{len(openap)} of {len(vendors)} vendor invoices</strong> are open. Using the notebook’s illustrative FX rates, USD payables account for ₹92.30 million of exposure.</p><p><strong>{sum(r["processing_status"].startswith("NEEDS_REVIEW") for r in claim)} of {len(claim)} reimbursements</strong> require review under the demo rules.</p>')
pages=[('receivables','Supply chain & receivables','Invoice aging, regional collections and delivery performance.',p1),('payment-risk','Customer payment risk','How well the baseline model identifies overdue invoices.',p2),('controls','Finance operations controls','Bank exceptions, open payables and reimbursement checks.',p3)]
css="""*{box-sizing:border-box}body{margin:0;background:#f3f4ef;color:#182e33;font:16px/1.55 Inter,Arial,sans-serif}header{background:#122f35;color:white;padding:22px max(5vw,20px);display:flex;justify-content:space-between;align-items:center;gap:16px}header strong{letter-spacing:.05em}header small{color:#d0e6de}nav{display:flex;flex-wrap:wrap;gap:8px;padding:14px max(5vw,20px);border-bottom:1px solid #cbd4cf;background:white}nav a{color:#28474b;text-decoration:none;padding:8px 15px;border-radius:6px;font-weight:600}nav a[aria-current=page]{background:#d9eee6;color:#114c42}main{max-width:1150px;margin:0 auto;padding:32px 5vw 64px}h1{font:clamp(32px,5vw,54px)/1.1 Georgia,serif;margin:8px 0 10px}h2{font-size:20px;margin:0 0 18px}section>p{color:#466168}.metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:26px 0}.metrics div,article{background:white;padding:22px;border:1px solid #cfdbd5;border-radius:10px}.metrics strong{display:block;font-size:clamp(23px,4vw,40px);font-variant-numeric:tabular-nums}.metrics span,.note{color:#48646a}article{margin:15px 0}.bar{display:grid;grid-template-columns:minmax(130px,1.1fr) 3fr 58px;align-items:center;gap:14px;margin:12px 0}.bar i{background:#e8efeb;height:12px;border-radius:3px}.bar b{display:block;background:#197568;height:100%;border-radius:3px}.bar strong{text-align:right}table{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums}td,th{text-align:left;padding:10px;border-bottom:1px solid #dce4df}th{background:#edf3ee}.scroll{overflow:auto;max-height:480px}.scroll th{position:sticky;top:0}select{font:inherit;padding:4px}footer{color:#48646a;margin-top:28px;font-size:14px}@media(max-width:600px){.metrics{gap:6px}.metrics div{padding:10px}.metrics span{font-size:12px}article{padding:15px}.bar{grid-template-columns:110px 1fr 44px;gap:7px;font-size:13px}nav a{padding:5px;font-size:13px}header{flex-wrap:wrap}}"""
html='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MediRobo | Finance operations</title><style>'+css+'</style><header><strong>MediRobo Diagnostics</strong><small>Finance operations · Simulated portfolio</small></header><nav aria-label="Workflows">'+''.join(f'<a href="#{k}">{t}</a>' for k,t,_,_ in pages)+'</nav><main>'+''.join(f'<section id="{k}"><h1>{t}</h1><p>{sub}</p>{body}</section>' for k,t,sub,body in pages)+'</main>'
html+="""<script>
function route(){
 const sections=[...document.querySelectorAll('main section')];
 const page=sections.find(s=>s.id===location.hash.slice(1))||sections[0];
 sections.forEach(s=>s.hidden=s!==page);
 document.querySelectorAll('nav a').forEach(a=>a.setAttribute('aria-current',a.hash==='#'+page.id?'page':'false'));
 document.title=page.querySelector('h1').textContent+' | MediRobo';
 window.scrollTo(0,0);
}
function filterQueue(){
 const choice=document.querySelector('#filter').value;
 const rows=[...document.querySelectorAll('#queue tbody tr')];
 rows.forEach(r=>r.hidden=choice!=='All exceptions'&&r.cells[2].textContent!==choice);
 document.querySelector('#shown').textContent=rows.filter(r=>!r.hidden).length+' open entries';
}
window.addEventListener('hashchange',route);
document.querySelector('#filter').addEventListener('change',filterQueue);
route();filterQueue();
</script></html>"""
Path('dashboard.html').write_text(html, encoding='utf-8')
