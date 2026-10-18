import argparse
import sys
from pathlib import Path
from project import read_json, validate_brief

def main():
    parser=argparse.ArgumentParser(description="Validate the approved brief and locale-specific capture inputs")
    parser.add_argument("project",type=Path)
    args=parser.parse_args()
    try:
        errors=validate_brief(args.project,read_json(args.project/"project.json"))
    except (OSError,ValueError,KeyError,TypeError) as exc:
        errors=[str(exc)]
    for error in errors:
        print("ERROR: "+error)
    if errors:
        return 1
    print("Brief and capture inputs ready. Semantic/visual attestations require real inspection.")
    return 0

if __name__=="__main__":
    sys.exit(main())
