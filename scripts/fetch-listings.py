#!/usr/bin/env python3
"""Rebuild listings-data.js from the Ray White Manukau listings API.

The site used to ship a hand-made snapshot of the office feed, which went
stale silently while the page still claimed the data was live. This pulls
the same feed the office website itself uses, so a scheduled run keeps the
site honest.

Usage:  python3 scripts/fetch-listings.py [--out listings-data.js]
"""

import argparse
import datetime
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

try:
    from zoneinfo import ZoneInfo
    NZ = ZoneInfo("Pacific/Auckland")
except Exception:            # no tzdata on the runner
    NZ = None

API = "https://rwmanukau.co.nz/api/proxy/v1/listings"
# The office group the public rwmanukau.co.nz property search covers.
ORG = "organisationId:!(925,2369,1459,3298,1930)"
PAGE = 50
SOLD_WINDOW_DAYS = 183          # the "last six months" the page promises
AGENT = "arvic gonzales"        # used only to flag which listings are his
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
)
# Ray White's CDN resizes on the fly; ask for a card-sized webp.
IMG_PARAMS = (
    "?anchor=middlecenter&mode=crop&scale=both"
    "&width=760&height=500&quality=82&format=webp"
)


def fetch(status, sort, frm, retries=3):
    q = (
        f"from:{frm},{ORG},size:{PAGE},"
        f"sort:!({urllib.parse.quote(sort)}),"
        f"statusCode:{status},typeCode:SAL"
    )
    url = f"{API}?q={q}"
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.load(resp)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            if attempt == retries - 1:
                raise SystemExit(f"listings API failed after {retries} tries: {exc}")
            time.sleep(2 * (attempt + 1))


def nz_today():
    """The runner is UTC; the cron fires early morning NZ time, so a plain
    utcnow() stamps yesterday's date all day for New Zealand readers."""
    now = datetime.datetime.now(datetime.timezone.utc)
    return (now.astimezone(NZ) if NZ else now).date()


def street(addr):
    formatted = (addr.get("formatted") or "").strip()
    if formatted:
        # First line is the street address and already includes any unit.
        return formatted.splitlines()[0].strip()
    unit = addr.get("unitNumber")
    number = addr.get("streetNumber")
    lead = f"{unit}/{number}" if unit and number else (number or unit or "")
    parts = [lead, addr.get("streetName"), addr.get("streetType")]
    return " ".join(str(p) for p in parts if p).strip()


def is_agents(value):
    return any(
        AGENT in (a.get("fullName") or "").lower()
        for a in value.get("agents") or []
    )


def safe_url(url):
    return url if isinstance(url, str) and url.startswith(("http://", "https://")) else None


def link_for(value):
    links = value.get("links") or []
    # "PRL" is the property page. Listings can also carry VID (YouTube) links,
    # and those sometimes come first — taking links[0] sent 38% of cards to
    # a video instead of the listing.
    for link in links:
        if link.get("code") == "PRL" and safe_url(link.get("url")):
            return link["url"]
    for link in links:
        if safe_url(link.get("url")):
            return link["url"]
    return f"https://rwmanukau.co.nz/{value.get('id', '')}"


def image_for(value):
    images = value.get("images") or []
    url = safe_url(images[0].get("url")) if images else None
    return url + IMG_PARAMS if url else None


def shape(value, kind):
    addr = value.get("address") or {}
    suburb = addr.get("suburb") or addr.get("region") or ""
    line = street(addr)
    if not addr.get("streetName"):
        # House-and-land packages have no street address; four of them would
        # otherwise render as identical "Te Kauwhata ..." cards.
        line = (value.get("title") or "").strip() or line
    record = {
        "id": value.get("id"),
        "address": ", ".join(p for p in [line, suburb] if p),
        "suburb": suburb,
        "status": value.get("displayPrice") or value.get("status") or "",
        "beds": value.get("bedrooms"),
        "baths": value.get("bathrooms"),
        "cars": value.get("carSpaces"),
        "href": link_for(value),
        "type": kind,
        "image": image_for(value),
        "mine": is_agents(value),
    }
    if kind == "sold" and value.get("soldDate"):
        record["soldDate"] = value["soldDate"]
    return record


def collect_for_sale():
    first = fetch("CUR", "'creationTime desc'", 0)
    total = int(first.get("hits") or 0)
    out = [shape(i["value"], "for-sale") for i in first.get("data", [])]
    for frm in range(PAGE, total, PAGE):
        page = fetch("CUR", "'creationTime desc'", frm)
        out += [shape(i["value"], "for-sale") for i in page.get("data", [])]
    return out, total


def collect_sold():
    cutoff = (nz_today() - datetime.timedelta(days=SOLD_WINDOW_DAYS)).isoformat()
    out = []
    frm = 0
    while True:
        page = fetch("SLD", "'soldDate desc'", frm)
        rows = page.get("data", [])
        if not rows:
            break
        for item in rows:
            value = item["value"]
            sold_date = value.get("soldDate")
            if not sold_date:
                continue          # undated sale: skip it, don't stop the walk
            if sold_date < cutoff:
                return out, cutoff
            out.append(shape(value, "sold"))
        frm += PAGE
        if frm > 4000:      # guard against an unbounded loop
            break
    return out, cutoff


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="listings-data.js")
    args = ap.parse_args()

    for_sale, total_listed = collect_for_sale()
    sold, cutoff = collect_sold()

    if not for_sale and not sold:
        raise SystemExit("refusing to write: the API returned nothing")

    listings = []
    seen = set()
    for record in for_sale + sold:
        # Two ids can point at one property page (the office lists a section
        # twice); those render as identical cards, so key on the URL as well.
        keys = {("id", record["type"], record.get("id")),
                ("href", record["type"], record.get("href"))}
        if record.get("id") is not None and keys & seen:
            continue
        seen |= keys
        listings.append(record)
    today = nz_today().isoformat()
    mine = sum(1 for r in listings if r["mine"])
    with_photo = sum(1 for r in listings if r["image"])

    body = (
        "// Generated by scripts/fetch-listings.py — do not edit by hand.\n"
        f"// Source: Ray White Manukau listings feed. Fetched {today}.\n"
        f"const LISTINGS_UPDATED = {json.dumps(today)};\n"
        f"const OFFICE_LISTINGS = {json.dumps(listings, indent=2, ensure_ascii=False)};\n"
    )
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(body)

    print(
        f"wrote {args.out}: {len(for_sale)} for sale (of {total_listed} listed), "
        f"{len(sold)} sold since {cutoff}, {mine} Arvic's, {with_photo} with photos"
    )


if __name__ == "__main__":
    sys.exit(main())
