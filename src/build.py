"""build.py  data/*.txt の問題を検査して src/template.html に差し込み、index.html を作る

使い方:  python src/build.py
各行: 分野|問題|正解|誤答1|誤答2|誤答3|出題年度|解説   （# で始まる行はコメント）
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'

# id, ファイル名, 表示名, グループ（ホームでの並び）
SUBJECTS = [
    ('eigo', 'eigo.txt', '英語', '英語・国語'),
    ('kobun', 'kobun.txt', '古文', '英語・国語'),
    ('kanbun', 'kanbun.txt', '漢文', '英語・国語'),
    ('nihonshi', 'nihonshi.txt', '日本史', '地歴・公民'),
    ('sekaishi', 'sekaishi.txt', '世界史', '地歴・公民'),
    ('chiri', 'chiri.txt', '地理', '地歴・公民'),
    ('rinri', 'rinri.txt', '倫理', '地歴・公民'),
    ('seikei', 'seikei.txt', '政治・経済', '地歴・公民'),
    ('seibutsu', 'seibutsu.txt', '生物', '理科・情報'),
    ('kagaku', 'kagaku.txt', '化学', '理科・情報'),
    ('chigaku', 'chigaku.txt', '地学', '理科・情報'),
    ('joho', 'joho.txt', '情報Ⅰ', '理科・情報'),
]
YEAR_OK = re.compile(r'^(2022|2023|2024|2025|2026|試作)$')


def check(sid, text):
    """不正な行を落とし、(残す行, 警告) を返す"""
    keep, warn, seen = [], [], set()
    for no, line in enumerate(text.splitlines(), 1):
        t = line.strip()
        if not t or t.startswith('#'):
            continue
        f = [x.strip() for x in t.split('|')]
        where = f'{sid}:{no}'
        if len(f) != 8:
            warn.append(f'{where} 列数{len(f)} → 除外: {t[:40]}')
            continue
        area, q, a, w1, w2, w3, years, ex = f
        if not (area and q and a and w1 and w2 and w3):
            warn.append(f'{where} 空欄あり → 除外')
            continue
        opts = [a, w1, w2, w3]
        if len(set(opts)) != 4:
            warn.append(f'{where} 選択肢が重複 → 除外: {opts}')
            continue
        ys = [y.strip() for y in years.replace('、', ',').split(',') if y.strip()]
        bad = [y for y in ys if not YEAR_OK.match(y)]
        if not ys or bad:
            warn.append(f'{where} 年度が不正 {years} → 除外')
            continue
        if q in seen:
            warn.append(f'{where} 問題文が重複 → 除外')
            continue
        seen.add(q)
        if len(q) > 50 or len(a) > 20:
            warn.append(f'{where} 長め(問{len(q)}字/答{len(a)}字): {q}')
        keep.append('|'.join([area, q, a, w1, w2, w3, ','.join(ys), ex]))
    return keep, warn


def main():
    out, warns, total = [], [], 0
    for sid, fn, name, group in SUBJECTS:
        p = DATA / fn
        if not p.exists():
            warns.append(f'{fn} がありません（科目を省略）')
            continue
        rows, w = check(sid, p.read_text(encoding='utf-8-sig'))
        warns += w
        if rows:
            out.append({'id': sid, 'name': name, 'group': group, 'raw': '\n'.join(rows)})
            total += len(rows)
            print(f'{name:<8} {len(rows):>4} 問')
    html = (ROOT / 'src' / 'template.html').read_text(encoding='utf-8')
    data = json.dumps(out, ensure_ascii=False).replace('</', '<\\/')
    html = html.replace('/*__DATA__*/[]', data, 1)
    (ROOT / 'index.html').write_text(html, encoding='utf-8', newline='\n')
    print(f'合計 {total} 問 → index.html')
    for w in warns:
        print('  !', w)
    return 0


if __name__ == '__main__':
    sys.exit(main())
