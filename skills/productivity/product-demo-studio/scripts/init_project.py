import argparse
import shutil
import sys
from pathlib import Path
from project import read_json, write_json

def main():
    parser=argparse.ArgumentParser(description="Create a new demo workspace; interview stays unapproved")
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--name",required=True)
    args=parser.parse_args()
    root=args.output.expanduser().resolve()
    if root.exists():
        parser.error("Output already exists; preserve it and choose a new directory")
    skill=Path(__file__).resolve().parents[1]
    shutil.copytree(skill/"assets/starter",root)
    (root/"support").mkdir()
    for name in ("project.py","check_project.py"):
        shutil.copy2(skill/"scripts"/name,root/"support"/name)
    config=read_json(root/"project.json")
    config["product"]["name"]=args.name
    write_json(root/"project.json",config)
    for folder in ("public/captures","public/audio","outputs","receipts"):
        (root/folder).mkdir(parents=True,exist_ok=True)
    status={name:shutil.which(name) is not None for name in ("python3","git","node","npm","ffmpeg","ffprobe")}
    print(str(root))
    print("Interview pending; approved=false")
    print("Local tools: "+", ".join(name+"="+("ready" if ready else "missing") for name,ready in status.items()))
    return 0

if __name__=="__main__":
    sys.exit(main())
