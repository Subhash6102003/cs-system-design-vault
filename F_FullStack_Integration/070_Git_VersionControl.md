================================================================================
  FILE 070: GIT & VERSION CONTROL
  Section: F - Full-Stack Integration
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Git Deep Dive: Internals, Branching, and Collaboration
  This file takes you beyond basic git commit and git push to understand how Git actually works under the hood. You will learn about Git's object model (blob, tree, commit), the DAG (Directed Acyclic Graph), advanced commands like rebase, cherry-pick, and bisect, and standard industry workflows like GitFlow and Pull Requests. Prerequisite: Basic knowledge of command-line operations.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

GIT AREAS
    
  WORKING DIRECTORY
    Your actual files on disk.
  STAGING AREA (INDEX)
    The files you've marked with git add to be included in the next commit.
  LOCAL REPOSITORY
    The .git folder containing your local commit history.
  REMOTE REPOSITORY
    A server (e.g., GitHub) storing the canonical version.
  GIT OBJECTS
    
  BLOB
    File contents.
  TREE
    Directory structure (pointers to blobs and other trees).
  COMMIT
    Metadata (author, timestamp, message) + pointer to a root tree + pointer to parent commit(s).
  DAG (DIRECTED ACYCLIC GRAPH)
    The mathematical structure used by Git to track the history of commits.
  HEAD
    A pointer to the current commit/branch you are viewing.
  REBASE
    Rewriting history by moving a sequence of commits to a new base commit.
  MERGE
    Combining two branch histories together, preserving the original timeline.
  CHERRY-PICK
    Applying the changes introduced by a specific existing commit to the current branch.
  SQUASH
    Combining multiple commits into a single commit for a cleaner history.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

┌─────────────────────────────────────────────────────────────────────────┐
  │  GIT DAG AND BRANCHING                                                  │
  │                                                                         │
  │        A---B---C (feature-branch)                                       │
  │       /                                                                 │
  │  D---E---F---G (main)                                                   │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  MERGE VS REBASE                                                        │
  │                                                                         │
  │  INITIAL STATE:                                                         │
  │        A---B---C (feature)                                              │
  │       /                                                                 │
  │  D---E---F---G (main)                                                   │
  │                                                                         │
  │  AFTER MERGE (git checkout main; git merge feature):                    │
  │        A---B---C                                                        │
  │       /         \                                                       │
  │  D---E---F---G---H (main)  <-- H is a merge commit (2 parents)          │
  │                                                                         │
  │  AFTER REBASE (git checkout feature; git rebase main):                  │
  │                A'---B'---C' (feature)                                   │
  │               /                                                         │
  │  D---E---F---G (main)      <-- Linear history, commits rewritten        │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  4. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

[Language: Bash]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Git Bisect (Finding the commit that introduced a bug)                │
  │                                                                          │
  │  # Start the bisect process                                              │
  │  git bisect start                                                        │
  │                                                                          │
  │  # Tell git the current commit is bad (contains the bug)                 │
  │  git bisect bad                                                          │
  │                                                                          │
  │  # Tell git an older commit (e.g., v1.0 tag) that you know was good      │
  │  git bisect good v1.0                                                    │
  │                                                                          │
  │  # Git will checkout a commit in the middle. Test your app...            │
  │  # If bug is present:                                                    │
  │  git bisect bad                                                          │
  │  # If bug is NOT present:                                                │
  │  git bisect good                                                         │
  │                                                                          │
  │  # Git repeats until it prints: "abc1234 is the first bad commit"        │
  │  git bisect reset # End the bisect process                               │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

[Language: Bash]

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Standard Pull Request Workflow (Terminal)                            │
  │                                                                          │
  │  # 1. Update local main                                                  │
  │  git checkout main                                                       │
  │  git pull origin main                                                    │
  │                                                                          │
  │  # 2. Create feature branch                                              │
  │  git checkout -b feat/user-auth                                          │
  │                                                                          │
  │  # 3. Work and commit using Conventional Commits                         │
  │  git add .                                                               │
  │  git commit -m "feat(auth): implement JWT login"                         │
  │                                                                          │
  │  # 4. Stay up to date with main (using rebase to avoid merge commits)    │
  │  git fetch origin                                                        │
  │  git rebase origin/main                                                  │
  │  # (Resolve any conflicts, git add, git rebase --continue)               │
  │                                                                          │
  │  # 5. Push to remote                                                     │
  │  git push -u origin feat/user-auth                                       │
  │                                                                          │
  │  # 6. (In GitHub UI) Open PR, request review, Squash and Merge to main.  │
  │                                                                          │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

Q1: Explain the difference between git merge and git rebase.

  ANSWER:
    merge creates a new merge commit combining two histories, preserving exact chronological order. rebase rewrites history by placing your branch's commits at the tip of the target branch, creating a clean linear history but changing commit hashes.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: What does git fetch do compared to git pull?

  ANSWER:
    fetch only downloads data from the remote repository to your local .git folder, updating remote-tracking branches. pull runs fetch and immediately attempts to merge (or rebase) the fetched changes into your current working branch.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: How do you undo a commit that has already been pushed to a public branch?

  ANSWER:
    Use git revert <commit-hash>. This creates a *new* commit that applies the inverse of the changes, preserving history. You should not use reset or rebase on public branches as it rewrites history for others.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What is the Git Staging Area (Index) for?

  ANSWER:
    It allows you to craft commits precisely. You can stage specific files or even specific lines within a file (git add -p), separating logical changes into distinct commits rather than committing everything in the working directory at once.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is git reflog?

  ANSWER:
    The reflog tracks every movement of the HEAD pointer locally (even rewrites and resets). If you accidentally delete a branch or perform a bad rebase, you can use reflog to find the lost commit hash and reset back to it.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Explain the Conventional Commits specification.

  ANSWER:
    A lightweight convention on top of commit messages. E.g., type(scope): description. Common types are feat (new feature), fix (bug fix), docs (documentation), and chore (maintenance). It allows automated changelog generation and semantic versioning.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is git cherry-pick?

  ANSWER:
    It takes the changes from a specific commit on one branch and applies them as a new commit on your current branch. Useful for backporting a hotfix from main to an older release branch.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What are the three Git object types stored in the .git/objects directory?

  ANSWER:
    Blobs (file content), Trees (directory listings), and Commits (metadata pointing to a tree).

────────────────────────────────────────────────────────────────────────────────
  7. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

CHALLENGE 1: Riddle

  I rewrite the past to make the future look clean. But if you use me on a shared timeline, your colleagues will scream. What am I?

  SOLUTION:
    git rebase

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 2: Riddle

  I am a time machine powered by binary search, hunting down the exact moment perfection was ruined. What am I?

  SOLUTION:
    git bisect

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 3: 

  echo "secret_key=123" > .env
  git add .
  git commit -m "add env"
  # Oh no, I didn't mean to commit the .env file!
  echo ".env" >> .gitignore
  git commit -am "ignore env"
  # Why is .env still being tracked on GitHub?

  SOLUTION:
    Adding a file to .gitignore only prevents *untracked* files from being added. Since .env was already committed, Git continues to track it. Fix: git rm --cached .env and commit.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─


  CHALLENGE 4: 

  git checkout main
  git pull
  git rebase feature-branch
  git push origin main --force

  SOLUTION:
    You rebased main onto feature-branch instead of the other way around, and then force-pushed to main. This rewrites the canonical history of main, breaking the repository for all other developers.

────────────────────────────────────────────────────────────────────────────────
  8. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Source control is the foundation of team collaboration. Mastering Git prevents code loss (via reflog), prevents buggy deployments (via clean PR workflows and CI), and makes debugging significantly faster (via bisect and clear commit histories).

────────────────────────────────────────────────────────────────────────────────
  9. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

-> File 069: 069 FullStack Deployment (Deploying code using Git tags and branches.)

================================================================================
  END OF FILE 070
================================================================================
