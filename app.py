import os
import socket
import random
import subprocess
from datetime import datetime

# -------------------------------
# 1. Check if Internet is Available
# -------------------------------
def is_connected():
    try:
        # Google's public DNS server - always online
        socket.create_connection(("8.8.8.8", 53))
        return True
    except OSError:
        return False


# -------------------------------
# 2. Randomly Edit 10 Files
# -------------------------------
def edit_random_files(folder, n=10):
    # Get all files in the folder (ignore directories)
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    # Pick n random files (or fewer if not enough files exist)
    selected = random.sample(files, min(n, len(files)))

    backup = {}  # To store original file content

    for file in selected:
        path = os.path.join(folder, file)

        # Read the original content
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        backup[file] = content

        # Append a fake edit line to simulate change
        with open(path, 'a', encoding='utf-8') as f:
            f.write("\n# automated edit\n")

    return backup


# -------------------------------
# 3. Git Add, Commit, Push
# -------------------------------
def git_commit_push(message="Auto contribution"):
    # Add all files
    subprocess.run(["git", "add", "."], check=True)
    # Commit with message
    subprocess.run(["git", "commit", "-m", message], check=True)
    # Push to GitHub
    subprocess.run(["git", "push"], check=True)


# -------------------------------
# 4. Restore the Files Back
# -------------------------------
def restore_files(folder, backup):
    for file, content in backup.items():
        path = os.path.join(folder, file)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)


# -------------------------------
# 5. Main Code Logic
# -------------------------------
if __name__ == "__main__":
    # 👇 CHANGE THIS TO YOUR LOCAL REPO PATH 👇
    REPO_PATH = r"D:\VSCode\Python\Githubscript>"  # Update this

    os.chdir(REPO_PATH)  # Go to your repo folder

    if is_connected():
        print(f"[{datetime.now()}] ✅ Internet detected. Starting automation...")

        # Edit files & back up originals
        backup = edit_random_files(REPO_PATH, 10)

        # Commit & Push to GitHub
        git_commit_push("Daily auto contribution")

        # Restore files
        restore_files(REPO_PATH, backup)

        print(f"[{datetime.now()}] ✅ Done! Contributions pushed.")
    else:
        print(f"[{datetime.now()}] ❌ No internet. Skipping.")

# automated edit
