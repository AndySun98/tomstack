import argparse
import hashlib
import itertools
import json
import subprocess
import sys
from pathlib import Path
from project import read_json, write_json, local_file

def inspect(path,decode=False):
    probe=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],timeout=60))
    video=next(s for s in probe["streams"] if s["codec_type"]=="video")
    audio=[s for s in probe["streams"] if s["codec_type"]=="audio"]
    numerator,denominator=map(float,video["avg_frame_rate"].split("/"))
    if decode:
        subprocess.run(["ffmpeg","-v","error","-xerror","-i",str(path),"-f","null","-"],check=True,timeout=600,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    digest=hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b""):
            digest.update(chunk)
    return {"width":video["width"],"height":video["height"],"fps":numerator/denominator,"duration":float(probe["format"]["duration"]),"codec":video["codec_name"],"pixel_format":video.get("pix_fmt"),"color_range":video.get("color_range"),"audio_codecs":[s["codec_name"] for s in audio],"sha256":digest.hexdigest(),"decode":"passed" if decode else "not_run"}

def verify(root,decode=False):
    config=read_json(root/"project.json")
    delivery=read_json(root/"delivery.json")
    expected=set(itertools.product([r["id"] for r in config["variants"]],[r["id"] for r in config["locales"]],[r["id"] for r in config["formats"]]))
    formats={r["id"]:r for r in config["formats"]}
    errors=[]; results=[]; seen=set(); paths=set()
    rows=delivery.get("rows",[])
    if not rows:
        errors.append("No delivered videos")
    for row in rows:
        key=(row.get("id"),row.get("locale"),row.get("format"))
        result={"key":key}
        try:
            if key in seen:
                raise ValueError("Duplicate delivery key")
            seen.add(key)
            if key not in expected:
                raise ValueError("Unexpected variant/locale/format")
            path=local_file(root,row.get("src"))
            if path in paths:
                raise ValueError("One media file reused for multiple delivered cuts")
            paths.add(path)
            poster=local_file(root,row.get("poster"))
            if not path.is_file() or not poster.is_file():
                raise ValueError("Missing media or poster")
            meta=inspect(path,decode); result.update(meta)
            if row.get("sha256") and row["sha256"]!=meta["sha256"]:
                raise ValueError("Declared media hash does not match the file")
            fmt=formats[key[2]]
            if (meta["width"],meta["height"])!=(fmt["width"],fmt["height"]):
                raise ValueError("Wrong dimensions")
            if abs(meta["fps"]-fmt["fps"])>.02:
                raise ValueError("Wrong frame rate")
            if abs(meta["duration"]-fmt["duration_seconds"])>.25:
                raise ValueError("Wrong duration")
            if meta["codec"]!="h264" or meta["pixel_format"]!="yuv420p" or meta["color_range"]=="pc":
                raise ValueError("Expected H.264 / yuv420p")
            if any(c!="aac" for c in meta["audio_codecs"]):
                raise ValueError("Expected AAC audio when present")
            if not row.get("engine"):
                raise ValueError("Missing actual engine provenance")
            result["status"]="passed"
        except (OSError,ValueError,KeyError,TypeError,StopIteration,ZeroDivisionError,subprocess.SubprocessError) as exc:
            result["status"]="failed"; result["error"]=str(exc); errors.append(str(key)+": "+str(exc))
        results.append(result)
    for key in sorted(expected-seen):
        errors.append("Missing cut: "+"/".join(key))
    return {"passed":not errors,"full_decode":decode,"errors":errors,"rows":results,"limits":["Visual locale correctness, native-engine provenance, sound quality and real platform acceptance require separate evidence."]}

def main():
    parser=argparse.ArgumentParser(description="Verify exact requested media matrix and optionally full FFmpeg decode")
    parser.add_argument("project",type=Path)
    parser.add_argument("--decode",action="store_true")
    args=parser.parse_args()
    try:
        report=verify(args.project.resolve(),args.decode)
    except (OSError,ValueError,KeyError,TypeError) as exc:
        report={"passed":False,"errors":[str(exc)]}
    if args.project.is_dir():
        write_json(args.project/"verification.json",report)
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if report["passed"] else 1

if __name__=="__main__":
    sys.exit(main())
