#!/usr/bin/env python3
"""Inspect and safely package DaVinci Resolve .drfx archives; inspired by REA's evidence-first workflow."""
import argparse, csv, hashlib, json, re, shutil, subprocess, zipfile
from pathlib import Path
from datetime import datetime, timezone

BRAND = "Kreovant Resource Library packaging note: metadata curation only; original creator attribution and license notices are preserved."
UI_NOTE = "Packaged for Kreovant Resource Library"

def digest(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def inspect(p):
    row={"filename":p.name,"bytes":p.stat().st_size,"sha256":digest(p),"is_zip":False,"entries":0,"settings":0,"previews":0,"authors":[],"unsafe_paths":[],"error":None}
    try:
        with zipfile.ZipFile(p) as z:
            row["is_zip"]=True; infos=z.infolist(); row["entries"]=len(infos)
            settings=[i for i in infos if i.filename.lower().endswith(".setting")]
            row["settings"]=len(settings)
            row["previews"]=sum(i.filename.lower().endswith((".png",".jpg",".jpeg",".webp")) for i in infos)
            for i in infos:
                q=Path(i.filename)
                if q.is_absolute() or ".." in q.parts: row["unsafe_paths"].append(i.filename)
                if i.filename.lower().endswith(".setting"):
                    t=z.read(i.filename).decode("utf-8","replace")
                    for m in re.finditer(r"(?im)^\s*--\s*(?:author|created by|creator)\s*[:=]\s*(.+?)\s*$",t):
                        a=m.group(1).strip()
                        if a and a not in row["authors"]: row["authors"].append(a[:150])
                    for m in re.finditer(r'(?i)Value\s*=\s*"Created by ([^"]+)"',t):
                        a=m.group(1).strip()
                        if a and a not in row["authors"]: row["authors"].append(a[:150])
    except Exception as e: row["error"]=str(e)
    return row

def rewrite(src,dst):
    before=inspect(src)
    if not before["is_zip"] or before["error"] or before["unsafe_paths"]:
        raise ValueError(f"Refusing invalid/unsafe archive {src}: {before['error'] or before['unsafe_paths']}")
    if src.resolve()==dst.resolve(): raise ValueError("Output must not overwrite source")
    dst.parent.mkdir(parents=True,exist_ok=True); tagged=comments=0
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst,"w") as zout:
        zout.comment=zin.comment
        for info in zin.infolist():
            data=zin.read(info.filename)
            if info.filename.lower().endswith(".setting") and b"\0" not in data[:4096]:
                try: text=data.decode("utf-8")
                except UnicodeDecodeError: text=None
                if text is not None:
                    if BRAND not in text:
                        text=f"-- {BRAND} Pack: {src.stem}.\n"+text; tagged+=1
                    def comment(m):
                        nonlocal comments
                        value=m.group(1)
                        if UI_NOTE.casefold() in value.casefold(): return m.group(0)
                        comments+=1
                        return m.group(0).replace(value,value+" | "+UI_NOTE,1)
                    text=re.sub(r'Comments\s*=\s*Input\s*\{\s*Value\s*=\s*"((?:\\.|[^"\\])*)"',comment,text,flags=re.S)
                    data=text.encode("utf-8")
            zout.writestr(info,data)
    after=inspect(dst)
    if not after["is_zip"] or after["error"] or after["unsafe_paths"]: raise ValueError(f"Output failed validation: {dst}")
    with zipfile.ZipFile(src) as a, zipfile.ZipFile(dst) as b:
        if a.namelist()!=b.namelist(): raise ValueError("Archive paths/order changed")
        for name in a.namelist():
            if not name.lower().endswith(".setting") and a.read(name)!=b.read(name):
                raise ValueError(f"Unexpected change to non-setting asset: {name}")
    return {"filename":src.name,"source_sha256":before["sha256"],"updated_sha256":digest(dst),"source_bytes":before["bytes"],"updated_bytes":dst.stat().st_size,"archive_entries":before["entries"],"settings_tagged":tagged,"visible_comment_fields_updated":comments,"original_authors_detected":before["authors"],"archive_verified":True}

def reports(out,rows,mode):
    out.mkdir(parents=True,exist_ok=True)
    data={"schema_version":"1.0","tool":"Kreovant Resolve Pack Manager (REA-inspired)","generated_utc":datetime.now(timezone.utc).isoformat(),"mode":mode,"policy":"Transparent packaging notes; detected creator names and license notices are retained.","packages":rows}
    (out/"metadata-manifest.json").write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    fields=["filename","source_sha256","updated_sha256","source_bytes","updated_bytes","archive_entries","settings_tagged","visible_comment_fields_updated","original_authors_detected","archive_verified"]
    with (out/"metadata-audit.csv").open("w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore"); w.writeheader()
        for r in rows:
            x=dict(r); x["original_authors_detected"]="; ".join(x.get("original_authors_detected",[])); w.writerow(x)
    lines=["# Resolve Pack Metadata Audit","","| Package | Settings tagged | Visible comments updated | Verified |","|---|---:|---:|:---:|"]
    for r in rows: lines.append(f"| {r['filename']} | {r['settings_tagged']} | {r['visible_comment_fields_updated']} | yes |")
    lines += ["","Notes identify metadata curation only, not authorship. All non-.setting assets were checked for byte-for-byte equality. Test every output in DaVinci Resolve before production use.",""]
    (out/"METADATA_CHANGELOG.md").write_text("\n".join(lines),encoding="utf-8")

def main():
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest="cmd",required=True)
    i=sub.add_parser("inspect"); i.add_argument("paths",nargs="+",type=Path); i.add_argument("--report-dir",type=Path,default=Path("audit"))
    r=sub.add_parser("rewrite"); r.add_argument("paths",nargs="+",type=Path); r.add_argument("--output-dir",required=True,type=Path); r.add_argument("--report-dir",required=True,type=Path); r.add_argument("--push-repo",type=Path); r.add_argument("--commit-message",default="Add metadata-tagged Resolve packs")
    a=p.parse_args(); sources=[]
    for x in a.paths: sources.extend(sorted(x.glob("*.drfx")) if x.is_dir() else [x])
    sources=[x for x in sources if x.is_file()]
    if not sources: p.error("No .drfx files found")
    rows=[]
    if a.cmd=="inspect":
        rows=[inspect(x) for x in sources]; reports(a.report_dir,rows,"inspect")
        print(f"Inspected {len(rows)} package(s); report saved to {a.report_dir}")
        return int(any(not x["is_zip"] or x["error"] or x["unsafe_paths"] for x in rows))
    out=Path(a.output_dir)
    for src in sources:
        row=rewrite(src,out/src.name); rows.append(row)
        print(f"{src.name}: {row['settings_tagged']} settings tagged, {row['visible_comment_fields_updated']} visible comments updated, verified")
    report=Path(a.report_dir); reports(report,rows,"rewrite")
    if a.push_repo:
        repo=a.push_repo
        if not (repo/".git").exists(): raise ValueError(f"Not a Git checkout: {repo}")
        target=repo/"release-assets"/"resolve-packs"; target.mkdir(parents=True,exist_ok=True)
        for src in out.glob("*.drfx"): shutil.copy2(src,target/src.name)
        metadir=repo/"metadata-updates"/"resolve-packs"; metadir.mkdir(parents=True,exist_ok=True)
        for f in report.iterdir():
            if f.is_file(): shutil.copy2(f,metadir/f.name)
        subprocess.run(["git","-C",str(repo),"add","release-assets/resolve-packs","metadata-updates/resolve-packs"],check=True)
        if subprocess.run(["git","-C",str(repo),"diff","--cached","--quiet"]).returncode:
            subprocess.run(["git","-C",str(repo),"commit","-m",a.commit_message],check=True)
            subprocess.run(["git","-C",str(repo),"push"],check=True)
        print("Push finished through the authenticated local Git checkout.")
    return 0
if __name__=="__main__": raise SystemExit(main())
