# Archive implementation status

Historical local-implementation checkpoint. Superseded by [live repeat-user acceptance](./repeat-user-acceptance.md).

[한국어](./archive-implementation-status(kor).md)

Implemented locally on 2026-09-10; not a new stamped release or a live pause acceptance result.

- Promoted verified TLS, migration checksums/retry ledger, separate deployment bundles and all-alias results protection into reusable cloud helpers.
- Added an operator archive CLI: close a study, export complete private data, generate verified ZIP and separate real/test CSV, require download confirmation, then request and verify provider pauses.
- Added safeguards for mismatched IDs, changed files, shared studies, pending data requests, partial failures and retries; no project deletion.
- Linked English/Korean user instructions and operator contracts through the core guide, registry and attachment fallback; synchronized golden guide locks.
- Local archive tests and mocked provider tests pass. Database closure SQL and provider pause/restore still require a separately authorized live acceptance test. Current online test projects remain active.

Do not treat locally passing tests as proof of a newly installed account-management integration. The existing Marketplace-only credentials may still need additional Supabase management authorization.
