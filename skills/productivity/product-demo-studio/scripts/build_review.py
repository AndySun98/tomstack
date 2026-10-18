import argparse
import hashlib
import shutil
import sys
from pathlib import Path
from project import read_json, write_json, local_file, identifier
from verify_media import verify

def main():
    parser=argparse.ArgumentParser(description="Build an isolated static review folder containing final media only")
    parser.add_argument("project",type=Path)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    root=args.project.expanduser().resolve(); output=args.output.expanduser().resolve()
    if output.exists():
        parser.error("Output exists; use a new directory to preserve existing work")
    try:
        report=verify(root)
        if not report["passed"]:
            raise ValueError("; ".join(report["errors"]))
        config=read_json(root/"project.json"); delivery=read_json(root/"delivery.json")
        prepared=[]
        for row in delivery["rows"]:
            if not all(identifier(row[k]) for k in ("id","locale","format")):
                raise ValueError("Invalid gallery ID")
            media=local_file(root,row["src"]); poster=local_file(root,row["poster"])
            key="-".join(row[k] for k in ("id","locale","format"))
            prepared.append((row,media,poster,key))
        template=Path(__file__).resolve().parents[1]/"assets/review"
        shutil.copytree(template,output)
        (output/"media").mkdir(); (output/"posters").mkdir()
        rows=[]
        for row,media,poster,key in prepared:
            media_name=key+".mp4"; poster_name=key+poster.suffix.lower()
            shutil.copy2(media,output/"media"/media_name); shutil.copy2(poster,output/"posters"/poster_name)
            rows.append({k:row.get(k) for k in ("id","name","locale","format","engine")} | {"src":"media/"+media_name,"poster":"posters/"+poster_name,"sha256":hashlib.sha256(media.read_bytes()).hexdigest()})
        write_json(output/"videos.json",{"product":config["product"]["name"],"brand":config["product"].get("brand",{}),"messages":config.get("review_messages",{}),"locales":config["locales"],"formats":config["formats"],"rows":rows})
        print(str(output))
        print("Static viewer built. Hosting authentication must protect HTML and media separately.")
    except (OSError,ValueError,KeyError,TypeError) as exc:
        print("Review build failed: "+str(exc),file=sys.stderr); return 1
    return 0

if __name__=="__main__":
    sys.exit(main())
