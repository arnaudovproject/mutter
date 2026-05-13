# Quality gate — migration

## Must include

- [ ] Backup plan (what is copied / snapshotted before apply)
- [ ] Rollback SQL or down migration referenced
- [ ] Tested on staging (or equivalent)
- [ ] Data integrity check described (counts, checksums, spot queries)
- [ ] Task/plan text mentions **rollback**, **backup**, or **backward compatibility**

## Notes

Run `python3 scripts/mutter.py validate-migrations` when migration paths appear in git diff.
