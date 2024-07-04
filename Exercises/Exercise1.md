# Exercise 1: Basic Git Commands

## Objective:
Practice the fundamental Git commands: `git init`, `git clone`, `git add`, `git commit`, `git status`, and `git log`.

## Instructions:

### Part 1: Setting Up a New Repository

1. **Initialize a New Git Repository:**
   - Create a new directory on your local machine named `git-basic-exercise`.
     ```bash
     mkdir git-basic-exercise
     cd git-basic-exercise
     ```
   - Initialize a new Git repository in this directory.
     ```bash
     git init
     ```

2. **Create a New File:**
   - Inside the `git-basic-exercise` directory, create a new file named `hello.py`.
     ```bash
     echo 'print("Hello, World!")' > hello.py
     ```

3. **Add the File to the Staging Area:**
   - Add `hello.py` to the staging area.
     ```bash
     git add hello.py
     ```

4. **Commit the File:**
   - Commit the staged file to the repository with a descriptive commit message.
     ```bash
     git commit -m "Add hello.py with a Hello, World! script"
     ```

5. **Check the Status and Log:**
   - Check the status of the repository to ensure it is clean.
     ```bash
     git status
     ```
   - View the commit log to see your commit.
     ```bash
     git log
     ```

### Part 2: Cloning an Existing Repository

1. **Create a Remote Repository:**
   - On GitHub, create a new repository named `git-basic-exercise`.

2. **Push Local Repository to GitHub:**
   - Add the GitHub repository as a remote.
     ```bash
     git remote add origin https://github.com/YOUR_USERNAME/git-basic-exercise.git
     ```
   - Push your local repository to GitHub.
     ```bash
     git push -u origin main
     ```

3. **Clone the Repository:**
   - Clone the repository you just pushed to GitHub into a new directory named `git-basic-exercise-clone`.
     ```bash
     git clone https://github.com/YOUR_USERNAME/git-basic-exercise.git git-basic-exercise-clone
     ```

4. **Verify the Clone:**
   - Navigate to the `git-basic-exercise-clone` directory.
     ```bash
     cd git-basic-exercise-clone
     ```
   - List the files to ensure `hello.py` is present.
     ```bash
     ls
     ```
   - Check the log to verify that the commit history is intact.
     ```bash
     git log
     ```
