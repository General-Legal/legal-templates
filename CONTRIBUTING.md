# Contributing

Thanks for your interest in improving these templates. This repository holds attorney-drafted legal templates released under [CC0 1.0](LICENSE), and contributions of every size are welcome — from typo fixes to entirely new templates.

## Ways to Contribute

- **Report a problem.** Typos, broken links, formatting errors, stale statutory references, or clauses that no longer reflect current law.
- **Improve an existing template.** Clarify language, fix conversion artifacts, or bring a template in line with a recent legal development.
- **Add a new template.** Propose it in an issue first so we can confirm scope and that an attorney is available to review it.
- **Improve the tooling.** The scripts in `scripts/` fetch and convert the source `.docx` files.

## Before You Start

Open an issue before doing substantial work — a new template, a rewrite of a section, or a change to the repository structure. Small, self-contained fixes can go straight to a pull request.

## Licensing and Legal Notes

- All contributions are released under **CC0 1.0**. By submitting a pull request you dedicate your contribution to the public domain and confirm you have the right to do so.
- **Do not paste text you do not have the right to release.** That includes clauses copied from proprietary form libraries, paid template services, or another firm's documents.
- **Nothing here is legal advice**, and a contribution does not create an attorney-client relationship. Substantive legal changes are reviewed by an attorney at [General Legal](https://general.legal) before merging.
- Do not include real party names, addresses, or other identifying details from actual agreements. Use bracketed placeholders instead.

## Repository Layout

```
templates/<template-slug>/
  README.md      # Overview, when to use it, key provisions
  template.md    # Full template text in LLM-optimized markdown
docx-originals/  # Original .docx source files
scripts/         # Fetch and conversion tooling
```

## Style Guide

**Template markdown (`template.md`)**

- Wrap every field the user must customize in `<mark>` tags, e.g. `<mark>[COMPANY NAME]</mark>`. This is what makes the templates usable by both humans and LLMs.
- Keep the heading hierarchy and section numbering of the source document intact.
- Use plain markdown. No HTML beyond `<mark>`, and no template engines or variable syntax.
- Preserve defined terms exactly as capitalized in the source ("Confidential Information", not "confidential information").

**Template README (`README.md`)**

Follow the structure used by the existing templates: title, the `**Category:** / **Format:** / **Source:**` block, then `## Overview`, `## When You Need This Template`, `## Why This Template`, and `## Key Provisions`.

**Prose**

- American English, sentence case for headings, Oxford comma.
- Wrap lines naturally; do not hard-wrap at a fixed column.

## Adding a New Template

1. Open an issue describing the template and the situation it covers.
2. Add the source `.docx` to `docx-originals/` named after its slug (e.g. `advisor-agreement.docx`).
3. Generate the markdown:
   ```bash
   pip install -r scripts/requirements.txt
   python3 scripts/convert_docx.py
   ```
4. Review the generated `template.md` by hand — conversion is not perfect. Check numbering, tables, and that every customizable field is wrapped in `<mark>`.
5. Write `templates/<slug>/README.md` following the style guide above.
6. Add a row to the template table in the root `README.md`, keeping it alphabetical.

## Pull Requests

1. Fork the repository and create a branch off `main` (e.g. `fix/nda-typo`, `docs/contributing-guide`).
2. Keep each pull request focused on one template or one concern. Unrelated changes belong in separate pull requests.
3. Write a clear description: what changed, which template, and — for legal changes — why the new language is correct and which statute, regulation, or case prompted it.
4. Do not commit generated `.docx` output or local editor files.
5. A maintainer will review. Substantive legal edits also go through attorney review, which may take a few days.

## Reporting Issues

When opening an issue, include:

- The template and the section or clause involved.
- What is wrong and what you would expect instead.
- For legal issues, the jurisdiction and a citation if you have one.

For anything sensitive, or if you would rather not discuss a legal concern in public, contact [General Legal](https://general.legal) directly instead of opening an issue.

## Code of Conduct

Be respectful and constructive. Assume good faith, keep discussion focused on the templates, and remember that contributors come from a mix of legal and engineering backgrounds. Maintainers may close or lock threads that become unproductive.
