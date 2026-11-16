from pathlib import Path
import subprocess,os,sys,json
root=Path(sys.argv[1]).resolve(); rows=[]; log=[]
out=Path(__file__).resolve().parent/'results'
out.mkdir(exist_ok=True)
for p in sorted(root.rglob('test_*.py')):
 runtime=p.parent.parent if p.parent.name=='tests' else p.parent
 env=dict(os.environ,PYTHONPATH=str(runtime))
 r=subprocess.run([sys.executable,str(p)],cwd=runtime,env=env,capture_output=True,text=True,timeout=20)
 rows.append({'file':str(p.relative_to(root)),'exit_code':r.returncode})
 log += [str(p.relative_to(root)),f'exit={r.returncode}',r.stdout,r.stderr]
 print(rows[-1])
(out/'existing_tests.txt').write_text('\n'.join(log))
(out/'existing_tests.json').write_text(json.dumps(rows,indent=2))

sys.exit(1 if any(r["exit_code"] for r in rows) else 0)
