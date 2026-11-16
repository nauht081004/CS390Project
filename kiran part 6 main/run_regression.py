"""Run actual CLI programs in isolated processes; Python standard library only."""
import argparse, hashlib, json, platform, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parent
ap=argparse.ArgumentParser()
ap.add_argument('--runtime',type=Path,default=ROOT/'reference_runtime')
ap.add_argument('--output',type=Path,default=ROOT/'results')
args=ap.parse_args(); runtime=args.runtime.resolve(); args.output.mkdir(parents=True,exist_ok=True)
rows=[]
for case in json.loads((ROOT/'tests/manifest.json').read_text()):
 command=[sys.executable,str(runtime/'main.py'),str(ROOT/'tests'/f"{case['name']}.anvi")]
 try:
  r=subprocess.run(command,capture_output=True,text=True,timeout=10)
  ok=r.returncode==case['exit_code'] and r.stdout==case['stdout']
  ok=ok and (case['stderr_contains'] in r.stderr and 'Traceback' not in r.stderr if case['stderr_contains'] else r.stderr=='')
  row={**case,'actual_stdout':r.stdout,'actual_stderr':r.stderr,'actual_exit_code':r.returncode,'passed':ok}
 except subprocess.TimeoutExpired:
  row={**case,'actual_stdout':'','actual_stderr':'TIMEOUT after 10 seconds','actual_exit_code':None,'passed':False}
 rows.append(row)
 print(('PASS' if row['passed'] else 'FAIL')+' '+case['name'])
passed=sum(r['passed'] for r in rows)
summary=f'{passed}/{len(rows)} passed; {len(rows)-passed} failed'
print(summary)
report={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),'runtime':str(runtime),'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(runtime.glob('*.py'))},'summary':summary,'tests':rows}
(args.output/'regression.json').write_text(json.dumps(report,indent=2))
lines=['ANVI CLI REGRESSION',summary,'Runtime: '+str(runtime),'Python: '+platform.python_version(),'']
for r in rows:
 lines += [('PASS' if r['passed'] else 'FAIL')+' '+r['name'],'Expected stdout: '+repr(r['stdout']),'Actual stdout:   '+repr(r['actual_stdout']),'Expected error:  '+repr(r['stderr_contains']),'Actual stderr:   '+repr(r['actual_stderr']),'Exit: '+str(r['actual_exit_code']),'']
(args.output/'regression.txt').write_text('\n'.join(lines))
sys.exit(0 if passed==len(rows) else 1)
