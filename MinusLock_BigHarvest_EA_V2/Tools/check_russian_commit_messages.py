#!/usr/bin/env python3
"""Reject empty, generic or non-Cyrillic messages in a supplied commit range."""
import argparse,re,subprocess
BAD={"правки","изменения","обновление","готово","финал"}
def main():
 p=argparse.ArgumentParser();p.add_argument("--base",required=True);p.add_argument("--head",required=True);a=p.parse_args()
 messages=subprocess.check_output(["git","log","--format=%s",f"{a.base}..{a.head}"],text=True).splitlines()
 bad=[m for m in messages if len(m.split())<3 or not re.search("[А-Яа-яЁё]",m) or m.strip().lower() in BAD]
 if bad: print("Недопустимые сообщения:",*bad,sep="\n");return 1
 print(f"Проверены русскоязычные сообщения: {len(messages)}");return 0
if __name__=="__main__":raise SystemExit(main())
