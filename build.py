#!/usr/bin/env python3
"""
Build static wiki site from markdown articles.
Run: python3 build.py
Output: index.html (self-contained, Cloudflare Pages ready)
"""
import json, os, re, sys
from pathlib import Path
from datetime import datetime

DOCS_DIR = Path(__file__).parent.parent / "custom-c2" / "server" / "docs"
OUT_DIR   = Path(__file__).parent

CATEGORY_ORDER = [
    "Getting Started", "Framework", "Reconnaissance", "Initial Access",
    "Windows PrivEsc", "Linux PrivEsc", "Active Directory", "Lateral Movement",
    "Persistence", "Post-Exploitation", "Credential Access",
    "Defense Evasion", "Evasion", "Network Attacks", "Web Attacks",
    "Cloud Attacks", "Phishing", "Social Engineering", "WiFi & Network",
    "Wireless", "Mobile", "Hardware & Physical", "Exploit Development",
    "Red Team Ops", "Reporting",
]

def parse_frontmatter(text):
    meta = {"title": "", "category": "", "slug": ""}
    if not text.startswith("---"):
        return meta, text
    end = text.index("---", 3)
    fm = text[3:end].strip()
    body = text[end+3:].strip()
    for line in fm.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip("'\"")
    return meta, body

def collect_articles():
    articles = []
    for md_file in sorted(DOCS_DIR.rglob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        if not meta["slug"]:
            meta["slug"] = md_file.stem
        if not meta["title"]:
            for line in body.splitlines():
                if line.startswith("# "):
                    meta["title"] = line[2:].strip()
                    break
            if not meta["title"]:
                meta["title"] = md_file.stem.replace("-", " ").title()
        if not meta["category"]:
            meta["category"] = md_file.parent.name.replace("-", " ").title()
        mtime = datetime.fromtimestamp(md_file.stat().st_mtime).strftime("%Y-%m-%d")
        articles.append({
            "slug": meta["slug"],
            "title": meta["title"],
            "category": meta["category"],
            "content": body,
            "last_updated": mtime,
        })
    return articles

def build_categories(articles):
    cats = {}
    for a in articles:
        cats.setdefault(a["category"], []).append({"slug": a["slug"], "title": a["title"]})
    ordered = []
    for name in CATEGORY_ORDER:
        if name in cats:
            ordered.append({"name": name, "articles": cats.pop(name)})
    for name, arts in sorted(cats.items()):
        ordered.append({"name": name, "articles": arts})
    return ordered

def build():
    articles = collect_articles()
    categories = build_categories(articles)
    articles_map = {a["slug"]: a for a in articles}
    data = {"categories": categories, "articles": articles_map}
    print(f"[+] {len(articles)} articles, {len(categories)} categories")

    template = (Path(__file__).parent / "_template.html").read_text()
    html = template.replace("__WIKI_DATA__", json.dumps(data, ensure_ascii=False))
    out = OUT_DIR / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"[+] Written: {out}  ({out.stat().st_size // 1024} KB)")

if __name__ == "__main__":
    build()
