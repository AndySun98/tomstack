"""Shared local path and brief contracts. No network or rendering."""
import json
import math
import re
from pathlib import Path

def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def local_file(root, relative):
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise ValueError("Expected a local relative media path")
    p = Path(relative)
    if p.is_absolute() or ".." in p.parts or ":" in relative or "?" in relative or "#" in relative:
        raise ValueError("Unsafe local media path: "+relative)
    resolved = (Path(root)/p).resolve()
    if not resolved.is_relative_to(Path(root).resolve()):
        raise ValueError("Media path escapes the project")
    return resolved

def identifier(value):
    return isinstance(value,str) and bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", value))

def number(value):
    return isinstance(value,(int,float)) and not isinstance(value,bool) and math.isfinite(value)

def scene_times(scene, fmt):
    return fmt.get("timing",{}).get(scene["id"], [scene["start"],scene["end"]])

def validate_brief(root, data):
    errors=[]
    if data.get("approved") is not True:
        errors.append("The interview brief must be approved before production")
    product=data.get("product",{})
    for key in ("name","audience","goal","cta"):
        if not isinstance(product.get(key),str) or not product[key].strip():
            errors.append("Missing product."+key)
    locales=data.get("locales",[])
    formats=data.get("formats",[])
    variants=data.get("variants",[])
    scenes=data.get("scenes",[])
    for label, rows in (("locales",locales),("formats",formats),("variants",variants),("scenes",scenes)):
        ids=[row.get("id") for row in rows]
        if not rows or not all(identifier(v) for v in ids) or len(set(ids))!=len(ids):
            errors.append(label+" needs nonempty, unique portable IDs")
    for fmt in formats:
        for key in ("width","height","fps","duration_seconds"):
            if not number(fmt.get(key)) or fmt[key]<=0:
                errors.append("Invalid format "+str(fmt.get("id"))+"."+key)
        if any(not isinstance(fmt.get(k),int) or fmt[k]%2 for k in ("width","height")):
            errors.append("Format width/height must be positive even integers")
        margins=fmt.get("safe_area",{})
        if any(not number(margins.get(k)) or margins[k]<0 for k in ("top","right","bottom","left")):
            errors.append("Format needs nonnegative safe_area margins")
        elif all(number(fmt.get(k)) for k in ("width","height")):
            if margins["left"]+margins["right"]>=fmt["width"] or margins["top"]+margins["bottom"]>=fmt["height"]:
                errors.append("Safe area has no usable space")
        cursor=0
        for scene in scenes:
            times=scene_times(scene,fmt)
            if not isinstance(times,list) or len(times)!=2 or not all(number(v) for v in times) or abs(times[0]-cursor)>.001 or times[1]<=times[0]:
                errors.append("Scene timeline has a gap/overlap/invalid interval in "+str(fmt.get("id")))
                break
            cursor=times[1]
        if number(fmt.get("duration_seconds")) and abs(cursor-fmt["duration_seconds"])>.001:
            errors.append("Scene timeline must fill format "+str(fmt.get("id"))+"; use format.timing for a different duration")
    for scene in scenes:
        if scene.get("kind") not in ("hook","product","cta"):
            errors.append("Scene kind must be hook, product or cta")
        for locale in locales:
            copy=scene.get("copy",{}).get(locale.get("id"),{})
            if not isinstance(copy.get("headline"),str) or not copy["headline"].strip():
                errors.append("Missing scene copy "+str(scene.get("id"))+"/"+str(locale.get("id")))
    if not any(scene.get("kind")=="product" for scene in scenes):
        errors.append("A real product-footage scene is required by this starter")
    for locale in locales:
        key=locale.get("id")
        recording=data.get("recordings",{}).get(key,{})
        try:
            if not local_file(Path(root)/"public",recording.get("src")).is_file():
                errors.append("Missing source recording for "+str(key))
        except ValueError as exc:
            errors.append(str(exc))
        neutral=recording.get("language_neutral") is True and bool(recording.get("neutral_evidence"))
        if not neutral and (recording.get("ui_locale")!=key or recording.get("data_locale")!=key):
            errors.append("Recording UI/data locale mismatch for "+str(key))
        if recording.get("ui_reviewed") is not True or recording.get("data_reviewed") is not True:
            errors.append("Recording UI/data review is pending for "+str(key))
        if not recording.get("evidence"):
            errors.append("Recording needs inspected frame evidence for "+str(key))
        for relative in recording.get("evidence",[]):
            try:
                if not local_file(Path(root)/"public",relative).is_file():
                    errors.append("Missing recording evidence for "+str(key))
            except ValueError as exc:
                errors.append(str(exc))
        if recording.get("source_kind") not in ("real-ui-synthetic-data","real-ui-test-backend","supplied-recording"):
            errors.append("Document source_kind for "+str(key))
    music=data.get("audio",{}).get("music")
    if music:
        try:
            if not local_file(Path(root)/"public",music).is_file():
                errors.append("Missing music asset")
        except ValueError as exc:
            errors.append(str(exc))
        if not data.get("audio",{}).get("rights"):
            errors.append("Document music rights")
    return errors
