#!/usr/bin/env python3
"""Read-only source audit; writes privacy_review.md, findings CSV and size list.

Requires pinned pypdf; no financial extraction, workbook scoring, redaction or
source modification. Uses Git's nonignored candidate file list, scans PDF text
and metadata, XLSX XML/metadata and ZIP members. Names are heuristic candidates,
not a guarantee of complete named-entity recognition. Secret values are masked.
"""
import csv,html,io,json,logging,re,subprocess,zipfile
from collections import Counter
from pathlib import Path
from pypdf import PdfReader
logging.getLogger('pypdf').setLevel(logging.ERROR)
ROOT=Path(__file__).resolve().parents[1]
OUTPUTS={'privacy_review.md','privacy_findings.csv','repository_file_sizes.md'}
EMAIL=re.compile(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?\.[A-Za-z]{2,}")
USERPATH=re.compile(r'/(?:Users|home)/[^/\s<>"\'`]+(?:/[^\s<>"\'`|,;)}\]]*)?')
PERSON=re.compile(r"\b[A-ZÀ-ÖØ-Þ][a-zà-öø-ÿ]+(?:[-’'][A-ZÀ-ÖØ-Þ]?[a-zà-öø-ÿ]+)?(?:[ \t]+[A-ZÀ-ÖØ-Þ][a-zà-öø-ÿ]+(?:[-’'][A-ZÀ-ÖØ-Þ]?[a-zà-öø-ÿ]+)?){1,3}\b")
STOP=set('Annual Report Group Financial Statements Statement Consolidated Income Other Information Combined Management Board Directors Shareholders Supervisory Committee Corporate Governance Toyota Motor Corporation Mercedes Benz BMW Independent Auditor Accounting Firm Public Registered International Standards Notes Basis Preparation Financial Services Non Current Assets Liabilities Operating Cash Flows Share Capital Revenue Total Business Businesses Sustainability North South America Europe Asia United States German Germany Japan Commercial Code Section Article General Meeting Date Python Student Project Data Source Printed Page Found Not None Table Summary Fiscal Year Period Development First Last Current President Chairman Chief Executive Officer Audit Risk Control Company The This These New All To For Of In As With From On By At See No During Note Research Question Verification Reflection Analysis Error Errors Privacy Changes Agreed Expected Performance Training Plan Original Results Runtime Scope Model Medium Ask Approval Correct Extraction Required Fields Possible Extensions Supervised Autonomous Fresh Source File Type Value Currency Units Scope Constant Decimal Earnings Interest Taxes Before After Profit Loss Investment Investments Net Increase Decrease Finance Treasury Shareholder Common Stock Retained Tax Deferred Equipment Intangible Property December January March April February June July August September October November May Global Central Following Author Read True False Every Never Use Keep Fix Prefer Follow Work Guide Record Preserve Select Stop Code Without Please Comparability Current Changes Correctly Matched Reasons Selected Generated Chapter Item Link Printed Unrounded Limitations Reasoning According Limited Aktiengesellschaft Research Economic Union European Commission Securities Exchange Independent Registered Public Accounting Firm GmbH Gesellschaft With Respect Tokyo London Important Regarding Content Contents Most When Each Customer Customers Service Foundation Framework'.casefold().split())
SECRETS=[('OpenAI-style key',re.compile(r'\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{20,}')),
 ('GitHub token',re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})')),
 ('AWS access key',re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b')),
 ('private-key header',re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')),
 ('JWT-like token',re.compile(r'\beyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}')),
 ('literal secret assignment',re.compile(r'''(?i)\b(?:api[_-]?key|access[_-]?token|secret[_-]?key|password)\s*[:=]\s*["']([^"'\s]{16,})["']'''))]
FINDINGS=[]
SCANNED=[]
FAILURES=[]

def add(path,loc,kind,value,proposal):
    # Do not duplicate audit findings inside audit output itself.
    if path.split('!')[0] in OUTPUTS:return
    FINDINGS.append((path,str(loc),kind,value,proposal))

def scan_text(path,text,loc='text'):
    SCANNED.append(path+'#'+str(loc))
    for n,line in enumerate(text.splitlines(),1):
        location=f'{loc}:line {n}'
        for m in EMAIL.finditer(line):add(path,location,'email',m.group(),'Review ownership; replace student/private email with <EMAIL> in an approved publication copy; retain public company contact only if intended.')
        for m in USERPATH.finditer(line):
            # Report the issue without copying the login into this audit.
            sanitized=re.sub(r'^(/(?:Users|home)/)[^/]+',r'\1<USER>',m.group())
            add(path,location,'absolute_user_path',sanitized,'Replace with repository-relative path, <PROJECT_ROOT>, or documented python command in an approved copy; do not edit frozen originals.')
        for description,pattern in SECRETS:
            for m in pattern.finditer(line):add(path,location,'possible_secret',description+' [VALUE MASKED]','Do not commit a real secret; confirm false positive or remove from publication and rotate if exposed. No secret value is reproduced here.')
        for m in PERSON.finditer(line):
            words=m.group().split()
            if not any(w.casefold() in STOP for w in words):
                add(path,location,'possible_person_name',m.group(),'Human review required; public report names may be retained knowingly. Replace private/student names with Student in an approved publication copy.')

def scan_bytes(path,data,depth=0):
    suffix=Path(path.split('!')[-1]).suffix.lower()
    try:
        if suffix=='.pdf':
            reader=PdfReader(io.BytesIO(data))
            if reader.metadata:
                scan_text(path,json.dumps(dict(reader.metadata),default=str,ensure_ascii=False),'PDF metadata')
                author=reader.metadata.get('/Author','')
                if author:add(path,'PDF metadata /Author','author_metadata',str(author),'Review author identity; retain public attribution or anonymize metadata in a separate approved publication copy, never the raw original.')
            for number,page in enumerate(reader.pages,1):scan_text(path,page.extract_text() or '',f'PDF {number}')
        elif suffix in {'.xlsx','.xlsm','.docx','.pptx','.zip'}:
            if depth>4:raise ValueError('Archive nesting exceeded audit limit')
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                for member in z.infolist():
                    if member.is_dir():continue
                    nested=path+'!'+member.filename
                    payload=z.read(member)
                    if suffix=='.zip':scan_bytes(nested,payload,depth+1)
                    elif member.filename.endswith(('.xml','.rels')):
                        xml=payload.decode('utf-8',errors='replace')
                        if member.filename.endswith('docProps/core.xml'):
                            for match in re.finditer(r'<(?:\w+:)?(creator|lastModifiedBy)[^>]*>(.*?)</',xml,re.S):
                                add(path,member.filename+':'+match.group(1),'author_metadata',html.unescape(match.group(2)),'Replace private author/last-editor metadata with Student only after approval; keep verification original unchanged and use a publication copy.')
                        scan_text(nested,html.unescape(re.sub(r'<[^>]*>',' ',xml)),'XML text')
                        # Attribute paths can be hyperlinks not visible in cell text.
                        scan_text(nested,xml,'XML attributes')
        else:
            if b'\0' in data[:4096]:
                strings=re.findall(rb'[\x20-\x7e]{5,}',data)
                scan_text(path,'\n'.join(x.decode('ascii') for x in strings),'binary printable strings')
            else:scan_text(path,data.decode('utf-8',errors='replace'))
    except Exception as exc:FAILURES.append((path,type(exc).__name__+': '+str(exc)))

def main():
    result=subprocess.run(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT,capture_output=True,check=True)
    paths=sorted(set(p for p in result.stdout.decode().split('\0') if p))
    for name in paths:
        p=ROOT/name
        if p.is_file():scan_bytes(name,p.read_bytes())
    records=sorted(set(FINDINGS))
    with (ROOT/'privacy_findings.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['file_or_archive_member','location','category','finding','proposed_action']);w.writerows(records)
    counts=Counter(row[2] for row in records)
    by_category={kind:sorted(set(row[0].split('!')[0] for row in records if row[2]==kind)) for kind in counts}
    lines=['# Repository Privacy Review','', 'Date: 2026-11-23. Findings are proposals only; no source, frozen result, workbook, archive or raw report was redacted or changed. This is a local repository audit, not approval to publish.','',
           f'Scanned {len(paths)} nonignored candidate files using Git’s file list. PDF pages/metadata, XLSX XML/author metadata, ZIP members, plain text and printable strings were inspected. Detailed locations and proposed actions are in privacy_findings.csv. The audit outputs are also scanned when present, but their duplicate findings are suppressed.','',
           '| Category | Finding occurrences | Files/archives |','|---|---:|---:|']
    for kind in ['email','possible_person_name','author_metadata','absolute_user_path','possible_secret']:
        lines.append(f'| {kind} | {counts[kind]} | {len(by_category.get(kind,[]))} |')
    lines+=['','## Findings and Proposed Replacements','']
    for kind in ['email','author_metadata','absolute_user_path','possible_secret']:
        lines += [f'### {kind}','']
        values=sorted(set(row[3] for row in records if row[2]==kind))
        lines += ['- '+v.replace('|','\\|') for v in values] if values else ['No pattern matches found.']
        lines += ['', 'Affected files: '+(', '.join('`'+p+'`' for p in by_category.get(kind,[])) or 'none')+'.','']
    lines+=['### Person-name examples','']
    names=sorted(set(row[3] for row in records if row[2]=='possible_person_name' and re.search(r'\b(?:Zipse|Källenius|Toyoda|Sato|Miyazaki|Pandey|Moriyama|Höttges)\b',row[3])))
    lines += ['- '+name for name in names]
    lines += ['', 'These are located name-pattern examples, not an exhaustive or independently verified people list. Author/editor metadata above is a separate direct metadata finding.', '']
    lines+=['### Person-name candidates','',
            'Names were searched with capitalized-name patterns and an exclusion word list, plus explicit author/editor metadata checks. These include corporate/reporting phrases and other false positives; they are not a complete or verified people list. Every candidate and its source location is retained in privacy_findings.csv. Public company officers and the assignment author may legitimately be attributed. Student/private identities need separate review.','',
            'Propose replacing private names/emails with Student / <EMAIL>, login-bearing absolute paths with portable relative paths, and private document-author metadata with Student. For data/raw/ or frozen folders, retain originals unchanged and prepare separate publication copies or approve excluding originals; neither action has been taken. Public report names/contact emails can be retained with an explicit publication decision. Archive copies require the same review as their original members.','',
            'No real secret can safely be committed. Possible-secret hits are masked and require confirmation; pattern checks do not prove the absence of all credentials. Git author identity is handled separately; a neutral local identity can avoid introducing the student’s real email.','',
            '## Limitations','',
            'This searches text and metadata, not text embedded solely in images, scanned signatures, or workbook drawings. No OCR or exhaustive named-entity recognition was performed. A clean automated scan is not a privacy guarantee. Worksheet values were searched for identifiers only; no independent financial verification or scoring was performed.','',
            '## Files not fully scanned','']
    lines+=['- '+name+': '+error for name,error in FAILURES] if FAILURES else ['No read/parse failures reported for the supported text/metadata paths. Image-only content remains outside this check.']
    (ROOT/'privacy_review.md').write_text('\n'.join(lines)+'\n')
    large=[]
    for p in ROOT.rglob('*'):
        if '.git' in p.relative_to(ROOT).parts or not p.is_file():continue
        if p.stat().st_size>50_000_000:large.append((str(p.relative_to(ROOT)),p.stat().st_size))
    size=['# Repository File-Size Check','', '2026-11-23. Threshold: greater than 50,000,000 bytes (50 decimal MB); .git internals excluded. All project files checked, including ignored files.','']
    if large:
        size+=['| File | Bytes | Decimal MB |','|---|---:|---:|']+[f'| {name} | {n} | {n/1_000_000:.2f} |' for name,n in sorted(large)]
    else:size+=['No project file is larger than 50 MB.']
    (ROOT/'repository_file_sizes.md').write_text('\n'.join(size)+'\n')
    print(json.dumps({'candidate_files':len(paths),'categories':dict(counts),'parse_failures':FAILURES,'files_over_50_MB':large}))

if __name__=='__main__':main()
