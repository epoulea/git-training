# Exercise 2: Git Branch and Merge

## Objective:
Understand how to work with branches, handle merges, and resolve conflicts

## Instructions:

### Part 1: Setting Up a New Git Branch

1. **Create a new branch:**
   - Create a new branch on your local machine named `feature-branch-1`.
     ```bash
     git branch feature-branch-1
     ```
   - Confirm that you have created a new branch.
     ```bash
     git branch
     ```
   - Check out the new branch.
     ```bash
     git checkout feature-branch-1
     ``` 

2. **Make some changes:**
   - Add a new line in the main.py file: 'print("New line from feature branch 1")'
   - Add a new file feature_1.py with line: 'print("Hello from feature branch 1")'

3. **Check the status of the current branch:**
   - Interpret the output of status command.
     ```bash
     git status
     ```

4. **Add both files to the Staging Environment for this branch**
  - Add files and check status
    ```bash
    git add --all
    git status
    ```

5. **Commit the changes:**
   - Commit the staged changes to the repository with a descriptive commit message.
     ```bash
     git commit -m "Add feature_1.py and new line in main.py"
     ```

### Part 2: Setting Up an Emergency Fix Branch

1. **Check out the main branch**
   - Check out the main branch
     ```bash
     git checkout main
     ```

1. **Create a an emergency fix branch:**
   - Create a new branch on your local machine named `fix-branch-1`.
     ```bash
     git checkout -b fix-branch-1
     ```
2. **Make some changes:**
   - Add a new line in the main.py file: 'print("New line from fix branch 1")' and check the status

4. **Add and commit:**
  - Add file and commit
    ```bash
    git add main.py
    git commit -m "updated main.py with emergency fix"
    ```

### Part 3: Merge Emergency Fix 

1. **Check out the main branch**
   - Check out the main branch
     ```bash
     git checkout main
     ```
2. **Merge the current branch (main) with fix-branch-1:**
  - Merge fix-branch-1 to main
     ```bash
     git merge fix-branch-1
     ```
3. **Delete emergency-fix:**
  - Delete the fix branch as it is no longer needed.
     ```bash
     git branch -d fix-branch-1
     ```

### Part 4: Merge Feature branch

1. **Check out the feature branch**
   - Check out the feature-branch-1
     ```bash
     git checkout feature-branch-1
     ```
2. **Make some changes:**
   - Add a new line in the main.py file: 'print("New line from feature branch 1 after fix 1")'

3. **Stage and commit for this branch:**
  - Stage and commit the changes
     ```bash
     git add --all
     git commit -m "Added new line in main.py"
     ```
4. **Check out the main branch**
   - Check out the main branch
     ```bash
     git checkout main
     ```
5. **Merge the current branch (main) with feature-branch-1:**
  - Merge feature-branch-1 to main
     ```bash
     git merge feature-branch-1
     ```
6. **Resolve conficts:**
  - Resolve conflicts from files
  - Stage and check status
     ```bash
     git add --all
     git status
     ```
  - Commit changes
    ```bash
    git commit -m "Merging feature branch after fixing conflicts"
    ```
7. **Delete feature-branch-1:**
  - Delete the feature branch as it is no longer needed.
     ```bash
     git branch -d feature-branch-1
     ```