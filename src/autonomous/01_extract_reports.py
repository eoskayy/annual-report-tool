"""Runtime PDF extraction. Python 3.12; pypdf==6.21.4. See README.md.
No financial amounts or reference answers are embedded. Definitions below are configurable.
"""
from pathlib import Path
from pypdf import PdfReader
import pypdf
import csv, re, json, hashlib, logging, calendar, sys
from datetime import date, timedelta, datetime, timezone
from decimal import Decimal, ROUND_HALF_UP, localcontext

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'results/autonomous'
LOG = ROOT / 'logs/autonomous'
CONFIG = {
 'bmw_group_report_2025.pdf': dict(title='Income Statement for Group and Segments', revenue='Revenues', profit='Profit/loss before financial result', company=r'BMW Group', columns=12, position=0, note_revenue=True, note_profit=False, units=r'in € million', currency='EUR'),
 'mercedes_benz_group_annual_report_2025.pdf': dict(title='Consolidated Statement of Income', revenue='Revenue', profit='Earnings before interest and taxes (EBIT)', company=r'Mercedes-Benz Group', columns=2, position=0, note_revenue=True, note_profit=True, units=r'In millions of euros', currency='EUR'),
 'toyota_form_20f_fy2025.pdf': dict(title='CONSOLIDATED STATEMENT OF INCOME', revenue='Total sales revenues', profit='Operating income', company=r'TOYOTA MOTOR CORPORATION', columns=3, position=2, note_revenue=True, note_profit=False, units=r'Yen in millions', currency='JPY'),
}
MONTHS = {m:i for i,m in enumerate(calendar.month_name) if m}
DATE_RE = re.compile(r'\b(?:(\d{1,2})\s+('+'|'.join(MONTHS)+r')\s+(\d{4})|('+'|'.join(MONTHS)+r')\s+(\d{1,2}),?\s+(\d{4}))\b')
logging.getLogger('pypdf').setLevel(logging.ERROR)
AUDIT=[]
def log(s):
 print(s, flush=True); AUDIT.append(s)
def select(rows, pred, reason):
 chosen=[r for r in rows if pred(r)]
 log(f'FILTER {len(rows)} -> {len(chosen)}: {reason}')
 return chosen

def unique(rows, context):
 if len(rows)!=1: raise RuntimeError(f'STOP: {context}: expected one candidate, found {len(rows)}')
 return rows[0]

def dates(pages):
 out=[]
 for page,t in pages:
  for m in DATE_RE.finditer(t):
   a,b,c,d,e,f=m.groups()
   try: value=date(int(c or f),MONTHS[b or d],int(a or e))
   except ValueError: continue
   out.append((value,page,m.group()))
 return out

def printed(t):
 f=re.search(r'^\s*(F-\d+)\s*$',t,re.M)
 if f: return f.group(1)
 a=re.search(r'^\s*(\d+)\s+BMW Group Report',t,re.M)
 if a: return a.group(1)
 a=re.search(r'^Annual Report[^\n]*?\s+(\d+)\s*$',t,re.M)
 return a.group(1) if a else 'not found'

def row(t,label,cfg,note):
 lines=select(t.splitlines(),lambda x: bool(re.match(r'^\s*'+re.escape(label)+r'(?:\s|\.)',x)),f'exact row label {label}')
 line=unique(lines,'value row '+label)
 tail=line.strip()[len(label):].lstrip('. ')
 cells=re.findall(r'(?<!\w)(?:[−–-]\s*)?\(?\d[\d,]*(?:\.\d+)?\)?|(?<!\S)[–—-](?!\S)',tail)
 expected=cfg['columns']+int(note)
 if len(cells)!=expected: raise RuntimeError(f'STOP: value-cell layout {label}: expected {expected} cells, found {len(cells)}')
 if note:
  before=len(cells); cells=cells[1:]; log(f'DROP {before} -> {len(cells)}: remove printed note reference for {label}')
 selected=select(list(enumerate(cells)),lambda x:x[0]==cfg['position'],f'current-year consolidated group cell for {label}; other years/segments excluded')
 token=unique(selected,'current value cell')[1]
 if token in ['–','—','-']: raise RuntimeError('STOP: unresolved numeric value cell '+label)
 normalized=token.replace(',','').replace(' ','').replace('−','-').replace('–','-')
 if normalized.startswith('('): normalized='-'+normalized[1:-1]
 Decimal(normalized)
 return line.strip()[:len(label)],normalized,line.strip(),token

def writecsv(path,rows):
 with path.open('x',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def main():
 for name in ['extracted_fields.csv','calculated_margins.csv','initial_report.md']:
  if (OUT/name).exists(): raise RuntimeError('Frozen output already exists; refusing overwrite: '+name)
 # Only identifiers/source names/field names are read; reference-answer columns are never used.
 with (ROOT/'verification/reference_table_template.csv').open(newline='') as f:
  template=[{k:r[k] for k in ['field_id','source_file','field_name']} for r in csv.DictReader(f)]
 assert len(template)==36 and len({r['field_id'] for r in template})==36
 assert len({(r['source_file'],r['field_name']) for r in template})==36
 log('KEY CHECK: 36 unique field_id and source_file/field_name keys; no merges')
 all_pages={}; hashes={}; evidence={}; source={}; margins=[]; fields=[]
 for fn in [*CONFIG,'toyota_integrated_report_2025.pdf']:
  p=ROOT/'data/raw'/fn; hashes[fn]=hashlib.sha256(p.read_bytes()).hexdigest()
  reader=PdfReader(p)
  all_pages[fn]=[(i+1,p.extract_text(extraction_mode='layout')) for i,p in enumerate(reader.pages)]
  log(f'READ {fn}: {len(reader.pages)} pages from original PDF at runtime')
 for fn,cfg in CONFIG.items():
  pages=all_pages[fn]
  candidates=select(pages,lambda p: cfg['title'] in p[1] and 'Condensed' not in p[1] and bool(re.search(r'^\s*'+re.escape(cfg['revenue'])+r'(?:\s|\.)',p[1],re.M)) and bool(re.search(r'^\s*'+re.escape(cfg['profit'])+r'(?:\s|\.)',p[1],re.M)),fn+' full statement title and both exact target rows')
  page,t=unique(candidates,'income statement page '+fn)
  rev,rv,rline,rtoken=row(t,cfg['revenue'],cfg,cfg['note_revenue'])
  prof,pv,pline,ptoken=row(t,cfg['profit'],cfg,cfg['note_profit'])
  company=unique(list(dict.fromkeys(re.findall(cfg['company'],t))),fn+' reporting entity')
  units=unique(list(dict.fromkeys(re.findall(cfg['units'],t))),fn+' statement units')
  # Header years precede the revenue row. Latest year must occupy the configured group position.
  header=t[:t.find(rline)]
  years=re.findall(r'\b20\d{2}\b',header)
  # Exclude report navigation years by taking the last complete table year block.
  before=len(years); years=years[-cfg['columns']:]; log(f'FILTER {before} -> {len(years)}: last statement column-year header block for {fn}')
  if len(years)!=cfg['columns']: raise RuntimeError('STOP: unresolved year-column header '+fn)
  year=max(map(int,years))
  if int(years[cfg['position']])!=year: raise RuntimeError('STOP: configured current-year column inconsistent '+fn)
  ds=dates(pages)
  if fn.startswith('toyota'):
   ends=select(dates([(page,t)]),lambda x:x[0].year==year,'current-year statement end date')
  else:
   ends=select(ds,lambda x:x[0].year==year and x[0].month==12 and x[0].day==31,'calendar-year closing-date candidates for statement year')
  distinct=sorted(set(x[0] for x in ends)); log(f'DROP {len(ends)} -> {len(distinct)}: duplicate closing dates; retain all evidence')
  end=unique(distinct,'distinct reporting end date')
  expected=date(end.year-1,end.month,end.day)+timedelta(days=1)
  starts=select(ds,lambda x:x[0]==expected,'document dates matching end minus twelve calendar months plus one day')
  distinct_starts=sorted(set(x[0] for x in starts)); log(f'DROP {len(starts)} -> {len(distinct_starts)}: duplicate opening dates; retain all evidence')
  start=distinct_starts[0].isoformat() if len(distinct_starts)==1 else 'not found'
  values=dict(company_name=company,period_start=start,period_end=end.isoformat(),currency=cfg['currency'],units='millions',revenue_label_as_printed=rev,revenue_value_current_year=rv,profit_measure_label_as_printed=prof,profit_measure_value_current_year=pv,income_statement_pdf_page=str(page),scope='consolidated group')
  source[fn]=dict(values=values,page=page,printed=printed(t),title=cfg['title'],year=year,units=units)
  evidence[fn]=dict(statement_pdf_page=page,statement_printed_page=printed(t),statement_text=t,revenue_row=rline,profit_row=pline,revenue_printed_token=rtoken,profit_printed_token=ptoken,year_headers=years,period_end_candidates=[(d.isoformat(),p,s) for d,p,s in ends],period_start_candidates=[(d.isoformat(),p,s) for d,p,s in starts])
  with localcontext() as ctx:
   ctx.prec=50
   margin=Decimal(pv)/Decimal(rv)*Decimal(100) if Decimal(rv)!=0 else None
  margins.append(dict(source_file=fn,company_name=company,period_start=start,period_end=end.isoformat(),margin_name=prof+' margin',numerator_label=prof,numerator=pv,denominator_label=rev,denominator=rv,currency=values['currency'],units=values['units'],scope=values['scope'],status='reported; current-year',source_pdf_page=page,margin_unrounded=str(margin) if margin is not None else 'not found',margin_rounded_half_up_1dp=str(margin.quantize(Decimal('0.1'),rounding=ROUND_HALF_UP)) if margin is not None else 'not found',unrounded_precision='50 significant digits; no presentation quantization',exact_fraction=f'{pv} * 100 / {rv}',calculation_status='calculated' if margin is not None else 'unavailable: zero revenue'))
 fn='toyota_integrated_report_2025.pdf'; pages=all_pages[fn]
 summaries=select(pages,lambda p:bool(re.search(r'^\s*Financial Summary \(Consolidated\)',p[1],re.M)),'integrated report financial-summary headings')
 full=select(pages,lambda p:bool(re.search(r'^\s*CONSOLIDATED STATEMENT[S]? OF (INCOME|CASH FLOWS|FINANCIAL POSITION)\s*$',p[1],re.M|re.I)),'integrated report full consolidated statement headings')
 cover=pages[0][1]
 if 'INTEGRATED REPORT' not in cover or not summaries or full: raise RuntimeError('STOP: hard-case classification ambiguous')
 evidence[fn]=dict(classification='summary-only',summary_pdf_pages=[p for p,t in summaries],full_statement_heading_pages=[p for p,t in full],reason='Integrated report cover and financial-summary headings; full-document heading search located no full consolidated statements. No numerical extraction from this source.')
 for r in template:
  fn=r['source_file']; name=r['field_name']; s=source.get(fn)
  if s:
   val=s['values'][name]; reason=''
   ep=str(s['page']); pp=s['printed']; section=s['title']; exact=''; excerpt=''
   if name=='period_start':
    ev=evidence[fn]['period_start_candidates']; ep=';'.join(str(p) for p in sorted(set(x[1] for x in ev)))
    pp=';'.join(printed(all_pages[fn][int(p)-1][1]) for p in ep.split(';')) if ep else 'not found'
    exact=ev[0][2] if ev else ''; excerpt=exact
    if val=='not found': reason='No unique distinct document date satisfies twelve-month opening-date rule; candidates='+json.dumps(ev)
   elif name=='period_end':
    ev=evidence[fn]['period_end_candidates']; ep=str(ev[0][1]); pp=printed(all_pages[fn][ev[0][1]-1][1]); exact=ev[0][2]; excerpt=exact
   elif name.startswith('revenue_'): exact=s['values']['revenue_label_as_printed']; excerpt=evidence[fn]['revenue_row']
   elif name.startswith('profit_'): exact=s['values']['profit_measure_label_as_printed']; excerpt=evidence[fn]['profit_row']
   elif name in ['currency','units']: exact=s['units']; excerpt=exact
   else: exact=val; excerpt=val
   fields.append(dict(**r,value=val,status='not found' if val=='not found' else 'extracted',reason=reason,company_name=s['values']['company_name'],financial_year=s['year'],source_pdf_page=ep,source_printed_page=pp,table_section=section,exact_source_label=exact,currency=s['values']['currency'],units=s['values']['units'],scope='consolidated group',reported_adjusted_restated='reported; current-year; no adjusted/restated substitute',evidence=excerpt))
  else:
   val={'document_type_summary_only':'summary-only','absence_of_full_audited_statements_reported':'Full audited financial statements not found in this integrated report','no_value_presented_as_audited':'No integrated-report value presented as audited'}[name]
   fields.append(dict(**r,value=val,status='document assessment',reason=evidence[fn]['reason'],company_name='',financial_year='',source_pdf_page=';'.join(str(p) for p in evidence[fn]['summary_pdf_pages']),source_printed_page=';'.join(printed(all_pages[fn][p-1][1]) for p in evidence[fn]['summary_pdf_pages']),table_section='Financial Summary (Consolidated)',exact_source_label='Financial Summary (Consolidated)',currency='',units='',scope='summary-only',reported_adjusted_restated='not an audited numerical source',evidence=evidence[fn]['reason']))
 assert len(fields)==36 and len({r['field_id'] for r in fields})==36
 writecsv(OUT/'extracted_fields.csv',fields); writecsv(OUT/'calculated_margins.csv',margins)
 # Generate report from saved result files, not in-memory or hand-entered financial amounts.
 with (OUT/'calculated_margins.csv').open() as f: saved=list(csv.DictReader(f))
 with (OUT/'extracted_fields.csv').open() as f: saved_fields=list(csv.DictReader(f))
 report=['# Autonomous initial report','', 'Agent-completed first pass; frozen before reference comparison. Correct fields / 36: unscored, awaiting the user’s independent reference. Extraction accuracy and arithmetic accuracy are not established by successful execution.','', '| Reporting entity | Period | Currency / units | Revenue label: value | Printed profit label: value | Named margin | PDF / printed page |','|---|---|---|---|---|---|---|']
 for m in saved:
  s=source[m['source_file']]
  report.append(f"| {m['company_name']} | {m['period_start']} to {m['period_end']} | {m['currency']} / {m['units']} | {m['denominator_label']}: {m['denominator']} | {m['numerator_label']}: {m['numerator']} | {m['margin_name']}: {m['margin_rounded_half_up_1dp']}% | {s['page']} / {s['printed']} |")
 report+=['','Comparability flags: Toyota’s fiscal period differs from the calendar-year reporters. The printed profit measures have different definitions; equivalence is not assumed. Currencies differ; no conversion or absolute monetary comparison is made. Margins use matching current-year group numerator/denominator units, but do not support an unqualified ranking.','', 'Hard case: Toyota’s integrated report supplies summary financial information; no full audited statements were located. It supplies no comparison-table amounts or margins.','',f"Explicit abstentions: {sum(r['status']=='not found' for r in saved_fields)} of {len(saved_fields)} required fields; presence and correctness remain unverified. Any abstention reason is retained in extracted_fields.csv.",'', 'Limitations: This is pilot evidence on development examples, with prior structural/financial-text exposure disclosed in the plan. This chat also inspected source pages while developing selectors; this is not a holdout test. The plan records development revisions to opening-date and field-abstention rules; this run applies both from the outset. PDF text and manually configured selectors can introduce errors. No reference comparison, user claim checks, independent margin recomputation, supervised comparison, or clean-copy fresh-session comparison has been completed here.','', 'Sources: extracted_fields.csv and calculated_margins.csv in results/autonomous/, both generated by src/autonomous/01_extract_reports.py. Unrounded decimal outputs and exact calculation fractions are saved separately. Source text/candidates and hashes are retained in runtime_evidence.json.']
 (OUT/'initial_report.md').write_text('\n'.join(report)+'\n')
 (OUT/'runtime_evidence.json').write_text(json.dumps(dict(generating_script='src/autonomous/01_extract_reports.py',python=sys.version,pypdf=pypdf.__version__,raw_sha256=hashes,sources=evidence,required_fields=len(fields),denominator=36,explicit_abstentions=sum(r['status']=='not found' for r in fields),comparability_flags=dict(period_mismatch=True,different_profit_definitions=True,currency_differences_no_conversion=True),accuracy='unscored',utc=datetime.now(timezone.utc).isoformat()),indent=2))
 log('COMPLETE: 36 unique fields and three margin rows; no reference scoring. Outputs frozen; overwrite refused.')
 # Hash the first-pass outputs and implementation for later comparisons.
 targets=[Path(__file__),*sorted(OUT.iterdir())]
 (LOG/'freeze_manifest.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in targets},indent=2))

if __name__=='__main__':
 try: main()
 finally:
  with (LOG/'execution_log.txt').open('a') as f: f.write('\n'.join(AUDIT)+'\n')
