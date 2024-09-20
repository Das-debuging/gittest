#!/usr/bin/python3

import subprocess
import os

def run_git_command(cmd):
    """Helper function to run git commands and capture output."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

def get_git_status():
    """Check for new, modified, or deleted files."""
    status_output = run_git_command(["git", "status", "--short"])
    return status_output

def get_new_files(status):
    """Parse git status to identify new or modified files."""
    new_files = []
    for line in status.splitlines():
        if line.startswith("??"):  # Untracked files
            new_files.append(line[3:])
        elif line.startswith(" M"):  # Modified files
            new_files.append(line[3:])
    return new_files

def ignore_files(files, extensions):
    """Ignore files with certain extensions."""
    return [f for f in files if not any(f.endswith(ext) for ext in extensions)]

def add_files_to_git(files):
    """Add files to git staging area."""
    for file in files:
        choice = input(f"Do you want to add {file} to the repository? (y/n): ").lower()
        if choice == 'y':
            run_git_command(["git", "add", file])

def commit_changes():
    """Commit changes to the repository."""
    commit_message = input("Enter a commit message (leave blank for 'Updated project files'): ").strip()
    if not commit_message:
        commit_message = "Updated project files"
    run_git_command(["git", "commit", "-m", commit_message])

def push_changes():
    """Push the changes to the remote repository."""
    branch = run_git_command(["git", "branch", "--show-current"])
    run_git_command(["git", "push", "origin", branch])

def main():
    ignored_extensions = input("Enter the file extensions to ignore (comma-separated, e.g., '.txt,.log'): ").split(',')
    ignored_extensions = [ext.strip() for ext in ignored_extensions if ext.strip()]

    print("Checking git status...")
    status = get_git_status()

    if not status:
        print("No changes detected.")
        return

    new_files = get_new_files(status)

    if not new_files:
        print("No new or modified files detected.")
        return

    new_files = ignore_files(new_files, ignored_extensions)

    if not new_files:
        print("No files to add after applying the ignore filter.")
        return

    print(f"New or modified files: {', '.join(new_files)}")

    add_files_to_git(new_files)

    if run_git_command(["git", "diff", "--cached"]):  # Check if any files are staged
        commit_changes()
        push_changes()
        print("Changes pushed to the repository.")
    else:
        print("No files were added. Exiting without committing.")

if __name__ == "__main__":
    main()




