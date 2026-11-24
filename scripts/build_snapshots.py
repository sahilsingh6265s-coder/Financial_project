from pathlib import Path
import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
mpl.rcParams.update({'svg.fonttype':'none','font.size':13,'font.family':'DejaVu Sans','svg.hashsalt':'finops'})
def chart(path,title,subtitle,labels,values,colors,footer):
    fig,ax=plt.subplots(figsize=(9.8,4.3))
    fig.subplots_adjust(left=.23,right=.90,top=.73,bottom=.17)
    fig.text(.04,.90,title,size=21,weight='bold',color='#182a37')
    fig.text(.04,.81,subtitle,size=12,color='#465861')
    bars=ax.barh(labels,values,color=colors,height=.56)
    ax.invert_yaxis()
    ax.set_xlim(0,max(values)*1.16)
    ax.bar_label(bars,labels=[f'{int(v):,}' for v in values],padding=6,weight='bold')
    ax.xaxis.set_visible(False)
    ax.tick_params(left=False)
    for sp in ax.spines.values():sp.set_visible(False)
    fig.text(.04,.055,footer,size=10,color='#465861')
    fig.savefig(path,metadata={'Date':None})
    plt.close(fig)
m=pd.read_csv('exports/reconciliation_matches.csv')
counts=m.status.value_counts()
statuses=['matched','unmatched','amount_mismatch','ambiguous']
assert set(counts.index)==set(statuses)
open_count=len(m)-counts['matched']
chart('docs/findings/cash-reconciliation.svg',f"{counts['matched']} of {len(m)} bank entries cleared",
      f"{open_count} entries remain open for review.",['Cleared','Unmatched','Amount mismatch','Ambiguous'],
      counts[statuses].tolist(),['#13736c','#ad6134','#ad6134','#ad6134'],'Simulated bank transactions · Count of statement entries by reconciliation outcome')
ar=pd.read_csv('exports/ar_aging_report.csv')
order=['1-30 days overdue','31-60 days overdue','61-90 days overdue','91+ days overdue']
late=ar[ar.ar_status=='overdue'].groupby('aging_bucket').num_invoices.sum()
assert set(late.index)==set(order)
pct=100*late[order[-1]]/late.sum()
chart('docs/findings/invoice-aging.svg',f"{pct:.1f}% of overdue invoices are 91+ days late",
      f"{int(late.sum()):,} overdue invoices across all regions.",['1–30 days','31–60 days','61–90 days','91+ days'],
      late[order].tolist(),['#92a6b5']*3+['#244e70'],'Simulated payment history on DataCo orders · Counts exclude paid invoices and invoices not yet overdue')
