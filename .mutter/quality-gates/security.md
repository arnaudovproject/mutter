# Quality gate — security

## Must include

- [ ] Threat model one-liner (asset + attacker capability)
- [ ] Least privilege / secrets handling reviewed
- [ ] `python3 scripts/mutter.py scan-secrets` on touched files before merge
- [ ] Verify includes security-relevant tests or static checks you rely on

## Notes

Never commit real tokens; use placeholders and secret manager integration.
