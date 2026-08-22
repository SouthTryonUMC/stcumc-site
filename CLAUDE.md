# South Tryon Community UMC — website

Hand-coded static site for South Tryon Community Missional United Methodist Church,
2516 South Tryon Street, Charlotte, NC 28203. A neighborhood church between Brookhill
Village and Southside Homes.

Live at southtryoncommunityumc.org. Deploys automatically from `main` via Netlify.
A push to `main` publishes to the public site within about a minute.

Maintained by Rev. Darryl Dayson, who is a pastor and not a developer. Explain what
you changed in plain language, not in terms of selectors and DOM nodes.

---

## Hard constraints

**The repo is FLAT. No folders. Ever.**
Every file lives at the root. `style.css` and all `.jpg` files sit alongside the HTML.
Reference them as `style.css` and `hero.jpg`, never `/css/style.css` or `/img/hero.jpg`.
This is not a preference — GitHub's browser uploader could not create folders, and the
paths were rebuilt to be flat. Adding a folder breaks the site.

**No build step.** No npm, no bundler, no framework. Plain HTML and one CSS file.

**No browser storage.** No localStorage or sessionStorage anywhere.

**Images must be compressed before they are committed.** Originals from the photographer
run 5–20 MB. Target ~1200px on the long edge, JPEG quality ~78, progressive. Nothing
above ~350 KB. An earlier draft hit 1.18 MB because images were base64-embedded; don't
do that again.

---

## Files

| File | Purpose |
|---|---|
| `index.html` | Home |
| `visit.html` | Start Here (first-visit questions + contact form at `#contact`) |
| `table.html` | Trinity's Table |
| `about.html` | Vision, values, history of the ground, neighborhood |
| `give.html` | Ways to give |
| `thanks.html` | Form confirmation page |
| `style.css` | All styling |
| `*.jpg` | Photographs by Lisa Stockton Howell, used with permission |

Navigation is four items plus a Give button: Start Here, Trinity's Table, About, Contact.
Keep it at four. The header, nav, and footer are duplicated across pages — when one
changes, change all of them.

---

## Facts (verify before changing; these are load-bearing)

- Sunday Worship: **11:00 AM**, runs about **1 hour 15 minutes**
- Trinity's Table: **Tuesday & Thursday, 11:30 AM** — free, no sign-up
- Communion: first Sunday of the month, open table
- Address: 2516 South Tryon Street, Charlotte, NC 28203
- Phone: **(980) 939-6463** — this is the public number. An older 704 number exists; do not use it.
- Email: exec@southtryoncommunityumc.org
- Giving: https://tithe.ly/give_new/www/#/tithely/give-one-time/189090
- Legal name: South Tryon Community Mission (Charlotte) United Methodist Church
- EIN: 56-2256891

There is no WonderDays program running. Do not add one back.

---

## Design system

Colors:
```
--cream    #FAF5EE   page background
--cream-2  #F3EADC   alternating section background
--ink      #2A2522   body text
--ink-soft #5C4A3A   secondary text
--wine     #4A1A26   headings, dark bands, primary buttons
--wine-lt  #6B2737   subheadings, button hover
--ember    #B8862F   accent on light backgrounds (eyebrows, rules)
--ember-hi #E8A33C   accent on dark backgrounds only
```

Type: **Newsreader** for headings, **Public Sans** for body. Loaded from Google Fonts.

Never use sage green (`#93A47C`) for body text on dark backgrounds — it fails contrast.
That color belongs to *rooted*, the coffee social enterprise, not to the church site.

---

## Voice — read this before writing any copy

The single most common failure is copy that sounds like an AI performing conviction.
The tell is that **every paragraph lands a zinger.** Do not do this.

Avoid:
- Closing epigrams. Don't end paragraphs on a rhetorical turn.
- Parallel reversals. "That is not weather. It is a set of decisions."
- Clipped triads. "Come hungry, come early, bring somebody."
- Em-dash pileups.
- Aphorisms that summarize the paragraph you just wrote.

Do:
- Plain, pastor-voiced prose. Short words. Varied sentence length.
- Let some sentences just be flat and informational and then stop.
- Concrete over abstract. "Plates go out at the serving window" beats "we practice
  radical hospitality."
- Enumerate rather than argue. The welcome statement on `about.html` lists and then
  says the plain thing; that's the register.

Substance:
- Warm but not sentimental. Prophetic but not performative.
- Never split neighbors into "helpers" and "helped." Mutual relational language only.
- Do not sanitize poverty, displacement, addiction, or grief.
- Grace comes first, and hospitality carries accountability. Both are true at once.
- The church does not exist apart from Brookhill Village and Southside Homes. Write
  as though the neighborhood is the congregation, because it substantially is.
- Trinity's Table is a shared meal on the Haywood Street model, not a food line. Never
  call it a soup kitchen, feeding line, or handout. Write from abundance, not scarcity —
  there is always enough, nobody is counted or rationed, and there's no divide between
  who cooked and who's eating. That's a mistake that has already been made once; don't
  make it again.

Primary audience is a neighbor from Brookhill or Southside deciding whether to walk in,
not a suburban church shopper comparing options. Funders and partners are secondary.

---

## Structure principle

The homepage is a directory, not a brochure. Short blocks, clear links, and the service
times high on the page. When something needs more than three or four sentences, it
belongs on its own page with a link from the home page.

Content that changes often should live in an embedded third-party service rather than
in the HTML, so it can be updated without editing code.

---

## Forms

The contact form on `visit.html` uses Netlify Forms (`data-netlify="true"`, honeypot
field named `company`, redirects to `thanks.html`). No backend. If you add a form,
follow the same pattern and keep the hidden `form-name` input.

---

## Working agreement

- Read the relevant file before editing it. Don't work from memory of an earlier version.
- After a change is approved, commit with a short descriptive message.
- This environment has no GitHub credentials configured, so `git push` will fail here.
  Don't try to fix that or work around it — after committing, tell Rev. Dayson the
  commit is ready and ask him to push it himself from the GitHub Desktop app on his Mac.
- Never force-push. Never hard-reset.
- If a change would alter the flat file structure, the palette, the fonts, or any of the
  facts above, stop and ask first.
