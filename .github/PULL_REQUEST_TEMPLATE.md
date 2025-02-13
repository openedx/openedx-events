<!--

Please give your pull request a short but descriptive title.
Use conventional commits to separate and summarize commits logically:
https://open-edx-proposals.readthedocs.io/en/latest/oep-0051-bp-conventional-commits.html

Use this template as a guide. Omit sections that don't apply.
You may link to information rather than copy it, but only if the link is publicly readable.
If the linked information must be private (because it contains secrets), clearly label the link as private.

For more details on the Hooks Extension Framework contribution process, see:

https://docs.openedx.org/en/latest/developers/concepts/hooks_extension_framework.html

-->

## Description

Describe what this pull request changes, and why. Include implications for people using this change.
Design decisions and their rationales should be documented in the repo (docstring / ADR), per
[OEP-19](https://open-edx-proposals.readthedocs.io/en/latest/oep-0019-bp-developer-documentation.html), and can be
linked here.

Useful information to include:

- Motivation and context of the implementation
- What's the intended use of this change?
- Use cases and usage examples available

## Supporting information

Link to other information about the change, such as Jira issues, GitHub issues, or Discourse discussions. Also, link to any relevant documentation useful for reviewers.
Be sure to check they are publicly readable, or if not, repeat the information here.

## Testing instructions

Please provide detailed step-by-step instructions for testing this change, including any necessary setup, e.g., additional requirements, plugins, configuration variables, etc, and environment details to ensure the reviewer can test the change.

## Deadline

"None" if there's no rush, or provide a specific date or event (and reason) if there is one.

## Other information

Include anything else that will help reviewers and consumers understand the change.

- Any other PRs or issues that should be linked here? Any related PRs?
- Any special concerns or limitations? For example: deprecations, security, or anything you think should be noted.

## Checklists

Check off if complete *or* not applicable:

**Merge Checklist:**
- [ ] All reviewers approved
- [ ] Reviewer tested the code following the testing instructions
- [ ] CI build is green
- [ ] Version bumped
- [ ] Changelog record added with short description of the change and current date
- [ ] Documentation updated (not only docstrings)
- [ ] Integration with other services reviewed
- [ ] Fixup commits are squashed away
- [ ] Unit tests added/updated
- [ ] Noted any: Concerns, dependencies, migration issues, deadlines, tickets

**Post Merge:**
- [ ] Create a tag
- [ ] Create a release on GitHub
- [ ] Check new version is pushed to PyPI after tag-triggered build is
      finished.
- [ ] Delete working branch (if not needed anymore)
- [ ] Upgrade the package in the Open edX platform requirements (if applicable)
