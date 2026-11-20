# Lab 3 – Git Branch and Merge Record

A feature branch was created to isolate the Lab 3 workflow documentation before merging it into the repository's `master` branch.

## Branch sequence

```bash
git checkout -b feature/lab3-git-workflow
git add LAB3/GIT_WORKFLOW.md
git commit -m "Document Lab 3 Git workflow"
git push -u origin feature/lab3-git-workflow
```

A pull request was then opened from `feature/lab3-git-workflow` into `master` and merged.

## What this demonstrates

- Creating a feature branch from the default branch.
- Committing a focused change on the feature branch.
- Proposing the change through a pull request.
- Merging the feature branch into the default branch.

This is a GitHub-side record of the branch/merge workflow. For a lab that requires screenshots of local Git commands, capture those separately from the student's terminal.
