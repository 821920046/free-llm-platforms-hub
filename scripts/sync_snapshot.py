# -*- coding: utf-8 -*-
"""把 data/leaderboard.json 同步为 index.html 内的离线兜底快照。

定时任务在抓到新榜单后调用，保证「下载 index.html 离线打开」也能看到
与线上一致的数据，而不只是几个月前的旧快照。
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, "index.html")
DATA = os.path.join(ROOT, "data", "leaderboard.json")

data = json.load(open(DATA, encoding="utf-8"))
compact = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
html = open(HTML, encoding="utf-8").read()

pattern = r"(    var SNAPSHOT = )\{.*?\}(;\n    // 22 家厂商官方 Logo)"
new, n = re.subn(pattern, lambda m: m.group(1) + compact + m.group(2),
                  html, count=1, flags=re.S)
if n != 1:
    raise SystemExit("FAILED: SNAPSHOT anchor not found in index.html")

if new == html:
    print("UNCHANGED snapshot (%d models, %s)" %
          (len(data["models"]), data["sourceUpdatedAt"]))
else:
    open(HTML, "w", encoding="utf-8").write(new)
    print("UPDATED snapshot in index.html (%d models, %s)" %
          (len(data["models"]), data["sourceUpdatedAt"]))
