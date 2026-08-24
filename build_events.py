#!/usr/bin/env python3
"""
Reads the STCUMC public Google Calendar and writes the "What's coming up"
section into index.html, between the EVENTS:START and EVENTS:END markers.

Run daily by .github/workflows/events.yml. Only rewrites the file when the
rendered output actually changed, so Netlify does not redeploy every day.

Calendar conventions (documented for the admin in EVENTS-HOWTO.md):
  web: <sentence>        the public description; anything above it stays private
  announce: 12 weeks     show earlier than the default 8-week window
  announce: none         keep off the website entirely
Recurring events are always skipped. The weekly rhythm is hard-coded below.
"""

import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

CALENDAR_ID = "c_b52797966718bdf6c2c67560916af2b137214253632474248f71cf37cc2b827f@group.calendar.google.com"
TZ = ZoneInfo("America/New_York")
DEFAULT_WEEKS = 8
LOOKAHEAD_WEEKS = 52          # how far we fetch; per-event windows filter it down
MAX_SHOWN = 6                 # keep the section from turning into a wall
PAGE = "index.html"
START_MARK = "<!-- EVENTS:START -->"
END_MARK = "<!-- EVENTS:END -->"

WEEKLY_NOTE = (
    "Every week besides: worship Sunday at 11:00, Trinity's Table Tuesday and "
    "Thursday at 11:30, and Bible study Wednesday at 7:00 PM."
)


def fetch_events(api_key):
    now = datetime.now(TZ)
    params = {
        "key": api_key,
        "timeMin": now.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "timeMax": (now + timedelta(weeks=LOOKAHEAD_WEEKS))
        .astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "singleEvents": "true",
        "orderBy": "startTime",
        "maxResults": "250",
    }
    url = (
        "https://www.googleapis.com/calendar/v3/calendars/"
        + urllib.parse.quote(CALENDAR_ID, safe="")
        + "/events?"
        + urllib.parse.urlencode(params)
    )
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r).get("items", [])


def strip_html(text):
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"</p>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text)


def parse_description(raw):
    """Return (public_text, announce_weeks_or_None, suppressed)."""
    if not raw:
        return "", None, False
    text = strip_html(raw)

    suppressed = bool(re.search(r"^\s*announce:\s*none\s*$", text, re.I | re.M))

    weeks = None
    m = re.search(r"^\s*announce:\s*(\d+)\s*weeks?\s*$", text, re.I | re.M)
    if m:
        weeks = int(m.group(1))

    m = re.search(r"^\s*web:\s*(.+)$", text, re.I | re.M)
    if m:
        public = m.group(1).strip()
    else:
        # No marker: use the description but drop any announce lines.
        lines = [
            ln.strip() for ln in text.splitlines()
            if ln.strip() and not re.match(r"^\s*announce:", ln, re.I)
        ]
        public = " ".join(lines)

    return public.strip(), weeks, suppressed


def event_start(ev):
    s = ev.get("start", {})
    if "dateTime" in s:
        return datetime.fromisoformat(s["dateTime"]).astimezone(TZ)
    if "date" in s:
        return datetime.fromisoformat(s["date"]).replace(tzinfo=TZ)
    return None


def select(events):
    now = datetime.now(TZ).replace(hour=0, minute=0, second=0, microsecond=0)
    chosen = []
    for ev in events:
        if ev.get("status") == "cancelled":
            continue
        if ev.get("recurringEventId"):
            continue                      # weekly rhythm lives in WEEKLY_NOTE
        title = (ev.get("summary") or "").strip()
        if not title:
            continue
        start = event_start(ev)
        if start is None or start < now:
            continue
        public, weeks, suppressed = parse_description(ev.get("description", ""))
        if suppressed:
            continue
        if start > now + timedelta(weeks=weeks or DEFAULT_WEEKS):
            continue
        chosen.append({"start": start, "title": title, "desc": public})
    chosen.sort(key=lambda e: e["start"])
    return chosen[:MAX_SHOWN]


def render(events):
    if not events:
        return ""
    rows = []
    for e in events:
        desc = (
            f'\n            <p class="event-desc">{html.escape(e["desc"])}</p>'
            if e["desc"] else ""
        )
        rows.append(
            f"""        <li class="event">
          <div class="event-date">
            <span class="event-month">{e['start'].strftime('%b')}</span>
            <span class="event-day">{e['start'].day}</span>
          </div>
          <div class="event-body">
            <h3 class="event-title">{html.escape(e['title'])}</h3>{desc}
          </div>
        </li>"""
        )
    return f"""
  <section class="sec" id="events">
    <div class="wrap">
      <span class="eyebrow">What's coming up</span>
      <h2>Beyond the usual week.</h2>
      <ul class="events">
{chr(10).join(rows)}
      </ul>
      <p class="events-note">{html.escape(WEEKLY_NOTE)}</p>
    </div>
  </section>
"""


def main():
    api_key = os.environ.get("GOOGLE_CALENDAR_API_KEY")
    if not api_key:
        sys.exit("GOOGLE_CALENDAR_API_KEY is not set.")

    try:
        events = select(fetch_events(api_key))
    except Exception as exc:
        # Never wipe the section because the API had a bad morning.
        print(f"Calendar fetch failed, leaving the page alone: {exc}")
        return

    page = open(PAGE, encoding="utf-8").read()
    if START_MARK not in page or END_MARK not in page:
        sys.exit(f"Markers not found in {PAGE}. Add {START_MARK} / {END_MARK}.")

    head, rest = page.split(START_MARK, 1)
    _, tail = rest.split(END_MARK, 1)
    updated = head + START_MARK + render(events) + END_MARK + tail

    if updated == page:
        print(f"No change ({len(events)} events). Nothing to commit.")
        return

    open(PAGE, "w", encoding="utf-8").write(updated)
    print(f"Wrote {len(events)} events:")
    for e in events:
        print(f"  {e['start']:%b %d}  {e['title']}")


if __name__ == "__main__":
    main()
