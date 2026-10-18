"""Fetch pinned third-party sources, never install or execute their code."""
import argparse
import json
import subprocess
import sys
from pathlib import Path
from project import read_json

def git(path,*args):
    return subprocess.check_output(["git","-C",str(path),*args],text=True,stderr=subprocess.PIPE,timeout=180).strip()

def check(path,row):
    if git(path,"rev-parse","HEAD")!=row["commit"]:
        raise ValueError("Existing checkout is not the pinned commit: "+str(path))
    if git(path,"status","--porcelain"):
        raise ValueError("Existing checkout has local changes: "+str(path))
    actual=git(path,"remote","get-url","origin").removesuffix(".git").rstrip("/")
    if actual!=row["url"].removesuffix(".git").rstrip("/"):
        raise ValueError("Repository identity mismatch: "+str(path))
    for entry in row["entrypoints"]:
        if not (path/entry).is_file():
            raise ValueError("Missing upstream entrypoint "+entry)

def main():
    parser=argparse.ArgumentParser(description="Plan/fetch selected exact upstream commits without running installers")
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--ids",nargs="+",default=["C03","C05"])
    parser.add_argument("--apply",action="store_true")
    args=parser.parse_args()
    rows=read_json(Path(__file__).resolve().parents[1]/"dependencies.lock.json")["workflows"]
    selected={r["id"] for r in rows} if args.ids==["all"] else set(args.ids)
    if selected-{r["id"] for r in rows}:
        parser.error("Unknown workflow ID")
    rows=[r for r in rows if r["id"] in selected]
    output=args.output.expanduser().resolve()
    plan={"apply":args.apply,"output":str(output),"workflows":rows}
    if not args.apply:
        print(json.dumps(plan,ensure_ascii=False,indent=2))
        return 0
    output.mkdir(parents=True,exist_ok=True)
    try:
        for row in rows:
            path=output/row["slug"]
            if path.exists():
                check(path,row)
                print(row["id"]+": verified existing source",flush=True)
                continue
            path.mkdir()
            subprocess.run(["git","init","-q",str(path)],check=True,timeout=20)
            subprocess.run(["git","-C",str(path),"remote","add","origin",row["url"]],check=True,timeout=20)
            subprocess.run(["git","-C",str(path),"fetch","--depth","1","origin",row["commit"]],check=True,timeout=180,stdout=subprocess.DEVNULL)
            subprocess.run(["git","-C",str(path),"checkout","--detach","-q","FETCH_HEAD"],check=True,timeout=60)
            check(path,row)
            print(row["id"]+": fetched verified pinned source",flush=True)
    except (OSError,ValueError,subprocess.SubprocessError) as exc:
        print("Source fetch stopped: "+str(exc),file=sys.stderr)
        print("Existing files preserved; inspect any partial checkout before recovery.",file=sys.stderr)
        return 1
    return 0

if __name__=="__main__":
    sys.exit(main())
