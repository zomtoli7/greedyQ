# Connection policy and researcher-guide update

[한국어](./connection-and-guide-update-2026-10-25(kor).md)

Release: `0.2_2026-10-25_f2afa11`.

## Changes

- Keep the established Vercel/Supabase researcher journey. Prefer an existing authorized official Vercel connection after account/team checks; retain the supported CLI/integration route for unavailable connections or operations. Onboard your agent remains optional.
- Record the observed separate team grant: login may succeed while team listing is empty. Request the specific team consent and retry on the same connection rather than reconnecting or silently bypassing a denial. Onboarding/read success does not prove deployment or response storage through the new route.
- Add 17 Simplified Chinese entry/user/AI guides, reciprocal language links and maintenance rules. English remains normative. Chinese full-guide code is byte-identical to the English/Korean canonical bundle, and release stamping covers all three languages. Not every developer document is translated.
- Rewrite Korean/English/Chinese website instructions around researcher actions. Define quoted Survey/Results/Preview terms, explain where to send each link, how to distinguish practice from research responses, and how to download/keep data. Preserve the gallery and its assets; put code names behind optional details.
- Remove smooth automatic scrolling that let a small-screen sticky header obstruct prompt copying. Separate participant and administrator database connections in the local journey test to prevent an in-flight participant role from affecting administrative assertions. These changes do not alter live study resources.

## Verification

- Full Python suite: 187 passed, no skips.
- Full Node/browser suite: 41 passed, no skips.
- Chinese guide relative links: 119 checked, none missing.
- Three-language website navigation, mobile menu and prompt-copy fallback checked at phone and computer widths, including a restricted embed.
- Release headers, generated survey provenance, registry hashes and the three verbatim full-guide bundles checked.
- GitHub commit `b3a9aa0` published the stamped release. The GitHub Pages website artifact matched all 703603 source bytes exactly: SHA-256 `ef1f244ce5952986a1806141ad4879a264fdcaebc9db7edc2e0409bdf4d0be63`.

## Publication boundary

The updated website is reviewable at <https://zomtoli7.github.io/greedyQ/website/google-sites-embed.html>. Publication to the existing Google Sites homepage is pending: its Safari editor is open, but the operator Mac reached its lock screen before the final replacement/save. The owner was asked to unlock that Mac. Do not claim the Google Sites homepage changed until its public embed is independently compared after publication.

No live Vercel/Supabase study deployment, database migration, participant recruitment or payment was changed in this update. The paid Prolific pilot remains under its previously recorded review status.
