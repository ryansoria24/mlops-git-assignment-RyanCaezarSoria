# Assignment 1 Report - Git Branching & Collaboration

**Student:** Ryan Caezar Soria
**Student ID:** 131930257
**Course:** MAI201 MLOps
**Repository:** https://github.com/ryansoria24/mlops-git-assignment-RyanCaezarSoria

---

## 1. GitHub Network Graph

The network graph below shows all branches (`develop`, `feature/add-readme-details`,
`feature/add-dockerignore`, `feature/add-code-of-conduct`, `feature/update-readme`)
and the merges back into `develop`, including the merge-conflict resolution.



<img width="1230" height="892" alt="image" src="https://github.com/user-attachments/assets/594fdae0-c7ee-42af-b64a-8aa2cf9d1f8c" />

---

## 2. Branch Protection Rules

Branch protection was configured on the `main` branch with the following settings:

- Require a pull request before merging
- Require at least one approval
- Dismiss stale pull request approvals when new commits are pushed
- Require linear history
- Force pushes disabled
- Branch deletion disabled

<img width="1080" height="815" alt="image" src="https://github.com/user-attachments/assets/533de771-13b7-4b3f-90a0-fb0011af826b" />


---

## 3. Output of `git log --oneline --graph`

```
*   dd73832 (HEAD -> develop, origin/develop) Merge pull request #5 from ryansoria24/feature/update-readme
|\
| *   d50ace7 (origin/feature/update-readme) Merge branch 'develop' into feature/update-readme
| |\
| |/
|/|
* | ca34457 Add course code and date to README
| * 5b0ab3e (feature/update-readme) Add student name and ID to README
|/
*   4603e6b Merge pull request #4 from ryansoria24/feature/add-code-of-conduct
|\
| * f609896 (origin/feature/add-code-of-conduct, feature/add-code-of-conduct) Add enforcement section with contact email
| * b096656 Add Contributor Covenant code of conduct
|/
*   49a27db Merge pull request #3 from ryansoria24/feature/add-dockerignore
|\
| * 5d106e3 (origin/feature/add-dockerignore, feature/add-dockerignore) Add build, docs, and data exclusions to .dockerignore
| * 804c0f5 Add .dockerignore with Python and venv exclusions
* | 0ddeba6 Merge pull request #2 from ryansoria24/feature/add-readme-details
|\ \
| * | 634be27 (origin/feature/add-readme-details, feature/add-readme-details) Add setup instructions and prerequisites
* | | 60d2c9a Merge pull request #1 from ryansoria24/feature/add-readme-details
|\| |
|/|
| * 002fd0b Add project description to README
|/
* 9ddfa9e (origin/main, origin/HEAD, main) Initial commit
```

---

## 4. Reflection: Resolving Merge Conflicts

The most challenging part of this assignment was understanding why a merge conflict
happens in the first place. At first it was not obvious that a conflict only occurs when
two branches change the same (or adjacent) lines of a file. When I edited the README on
`feature/update-readme` (adding my name and student ID) and then edited the README again
on `develop` (adding the course code and date), I had to deliberately place both edits near
the top of the file so that Git could not merge them automatically.

When I opened the pull request, GitHub reported that the branch "has conflicts that must be
resolved." Opening the conflict editor, I saw the conflict markers for the first time:
`<<<<<<<`, `=======`, and `>>>>>>>`. Initially these looked confusing, but once I understood
that the section above the `=======` was my branch's version and the section below it was
develop's version, it became clear. Because the assignment required keeping both changes, I
used GitHub's "Accept both changes" option, which preserved both sets of lines and removed
all the conflict markers automatically.

What I found most challenging was the mental model rather than the mechanics: realizing that
a conflict is Git asking the human to make a decision it cannot make on its own, and that
"resolving" a conflict simply means cleaning up the file so that only the intended content
remains, with no leftover markers. Once that clicked, the process felt straightforward, and
the resulting merge appears cleanly in the network graph as the join between the two README
edits.
