## Sync upstream v0.4.0

Automatically generated from `options.json` v0.4.0.

### ✨ New Parameters

- `detect_tables` — Detect and extract Markdown tables as structured data

### Auto-updated Files

- [x] `document_loaders.py` — SYNCED PARAMS, ASSIGNMENTS, CONVERT KWARGS
- [x] `README.md` — Parameters Reference table
- [x] `pyproject.toml` — dependency version bumped

### Review Checklist

**Auto-generated code verification:**
- [ ] SYNCED PARAMS: types and defaults are correct
- [ ] SYNCED ASSIGNMENTS: all new params assigned
- [ ] SYNCED CONVERT KWARGS: all new params passed to extract()
- [ ] README table: new rows accurate, existing rows unchanged

**New parameters (manual work needed):**
- [ ] Add test for `detect_tables` (at minimum: mock kwargs pass-through)
- [ ] Docstring Args section updated for: `detect_tables`

**Wrapper logic impact check:**
- [ ] `split_sections` logic: does any new param affect section splitting?
- [ ] Error handling in `lazy_load`: any new failure modes?
- [ ] Metadata fields: should new param appear in Document metadata?

**Before merge:**
- [ ] All tests pass: `pytest tests/ -v --disable-socket`
- [ ] CHANGELOG updated
- [ ] Bump MINOR version

**After merge:**
- [ ] Tag push: `git tag vX.Y.Z && git push --tags`
- [ ] PyPI deployment verified