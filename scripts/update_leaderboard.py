# -*- coding: utf-8 -*-
"""抓取 AIHOT 大模型综合榜，生成 data/leaderboard.json。

设计要点：
- 官网服务端渲染，直接解析 <table>，不依赖任何第三方 Python 包。
- 只有「官网更新时间 + 榜单内容」真正变化时才写文件，避免定时任务产生无意义提交。
- 抓取或校验失败时以非零码退出，GitHub Actions 会保留上一份可用数据。
"""
import datetime as dt
import html as htmllib
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "leaderboard.json")
SOURCE = "https://aihot.news/leaderboard"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0 Safari/537.36")

CN_MAKERS = {"DeepSeek", "Z.ai", "Alibaba", "Moonshot AI", "Tencent",
             "Xiaomi", "MiniMax", "StepFun", "Baidu", "01.AI", "Huawei"}

# 厂商 -> 与本站收录的免费额度的关系（用于「与免费额度的关系」列和 free 筛选）
FREE_NOTES = {
    "DeepSeek": "DeepSeek 新用户赠金 / V4.1 Flash 空闲时段 ¥1 输入",
    "Z.ai": "智谱 Flash 免费档 + 5000 万 Token",
    "Alibaba": "阿里云百炼每模型 100 万 Token",
    "Google": "Google AI Studio 提供免费调用额度",
    "Tencent": "腾讯云新人 100 万 / 云开发 10 亿 Token",
    "Xiaomi": "开源权重，魔搭 / AMD 免费档可试用同系模型",
    "MiniMax": "MiniMax Code 每日积分（限产品内使用）",
    "Mistral AI": "Mistral Free Tier（需在控制台申请）",
    "NVIDIA": "NVIDIA NIM 赠送 Credits",
}
NO_FREE = "暂无直接免费额度，可看本站低价替代"


def fetch():
    req = urllib.request.Request(SOURCE, headers={"User-Agent": UA, "Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def strip_tags(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", htmllib.unescape(s)).strip()


def num(s, default=0.0):
    m = re.search(r"-?\d+(?:\.\d+)?", strip_tags(s).replace(",", ""))
    return float(m.group()) if m else default


def parse(raw):
    table = re.search(r"<table.*?</table>", raw, re.S)
    if not table:
        raise ValueError("leaderboard table not found (page structure changed)")
    trs = re.findall(r"<tr.*?</tr>", table.group(0), re.S)
    rows = []

    for tr in trs:
        if "data-slug" not in tr:
            continue
        tds = re.findall(r"<td.*?</td>", tr, re.S)
        if len(tds) < 8:
            continue
        name_m = re.search(r"<strong[^>]*>(.*?)</strong>", tds[1], re.S)
        if not name_m:
            continue
        name = strip_tags(name_m.group(1))
        smalls = [strip_tags(x) for x in re.findall(r"<small.*?</small>", tds[1], re.S)]
        maker = next((s for s in smalls if "上线" not in s and s), "")
        if not maker:
            maker = name.split()[0]
        date_m = re.search(r'date[Tt]ime="(\d{4}-\d{2}-\d{2})"', tds[2])
        coverage = re.search(r"覆盖\s*(\d+)\s*%", strip_tags(tds[3]))
        # 评分单元格形如 "81.0 覆盖 71%"，取开头的数字
        score_txt = strip_tags(tds[7])
        score_m = re.match(r"\s*(\d+\.\d+)", score_txt)
        score = float(score_m.group(1)) if score_m else num(tds[7])
        oss = "开源权重" in tds[1]
        note = FREE_NOTES.get(maker, NO_FREE)
        # AI Studio 免费层只覆盖 Flash 系列，避免把付费新旗舰误标为「有免费额度」
        if maker == "Google" and "Flash" not in name:
            note = NO_FREE
        tags = []
        if maker in CN_MAKERS:
            tags.append("cn")
        if oss:
            tags.append("oss")
        if note != NO_FREE:
            tags.append("free")
        rows.append({
            "rank": int(num(tds[0])),
            "slug": re.search(r'data-slug="([^"]+)"', tr).group(1),
            "name": name,
            "maker": maker,
            "date": date_m.group(1) if date_m else "",
            "evals": int(num(tds[3])),
            "coverage": int(coverage.group(1)) if coverage else 0,
            "cache": num(tds[4]),
            "in": num(tds[5]),
            "out": num(tds[6]),
            "score": score,
            "oss": oss,
            "tags": tags,
            "freeNote": note,
        })

    if len(rows) < 20:
        raise ValueError("only %d rows parsed, expected >= 20" % len(rows))
    ranks = [r["rank"] for r in rows]
    if ranks != list(range(1, len(rows) + 1)):
        raise ValueError("rank sequence broken: %s" % ranks[:8])
    if any(rows[i]["score"] < rows[i + 1]["score"] for i in range(len(rows) - 1)):
        raise ValueError("scores are not descending")

    text = strip_tags(raw)
    upd = re.search(r"(\d{1,2})/(\d{1,2})\s+(\d{1,2}:\d{2})\s*更新", text)
    if not upd:
        raise ValueError("site update timestamp not found")
    now = dt.datetime.now(dt.timezone(dt.timedelta(hours=8)))
    month, day, hm = upd.group(1), upd.group(2), upd.group(3)
    source_updated = "%d-%02d-%02d %s" % (now.year, int(month), int(day), hm)
    evals_m = re.search(r"(\d+)\s*项评测.*?(\d+)\s*家机构", text)
    fx_m = re.search(r"(\d{4}-\d{2}-\d{2})\s*汇率折算", text)

    return {
        "source": SOURCE,
        "sourceUpdatedAt": source_updated,
        "fetchedAt": now.isoformat(timespec="seconds"),
        "evals": int(evals_m.group(1)) if evals_m else None,
        "orgs": int(evals_m.group(2)) if evals_m else None,
        "fxDate": fx_m.group(1) if fx_m else None,
        "method": "第三方实测成绩折算，编程 38% / 科研 19% / 专业办公 19% / 知识问答 14% / 真人盲选 10% 加权；价格不参与排序",
        "models": rows,
    }


def main():
    data = parse(fetch())
    # 内容无变化则不写文件（fetchedAt 不参与比较），避免定时任务刷提交
    content = {k: v for k, v in data.items() if k != "fetchedAt"}
    if os.path.exists(OUT):
        old = json.load(open(OUT, encoding="utf-8"))
        old_content = {k: v for k, v in old.items() if k != "fetchedAt"}
        if old_content == content:
            print("UNCHANGED %s · %d models · source %s" %
                  (data["sourceUpdatedAt"], len(data["models"]), SOURCE))
            return 0
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("UPDATED %s · %d models · %s evals / %s orgs · %s" %
          (data["sourceUpdatedAt"], len(data["models"]), data["evals"],
           data["orgs"], OUT))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print("FAILED: %s: %s" % (type(e).__name__, e), file=sys.stderr)
        sys.exit(1)
