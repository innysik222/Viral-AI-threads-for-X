import subprocess
import os
from datetime import datetime

def sync_to_gitlab(repo_path, commit_message=None):
    """
    Automates the git add, commit, and push process.
    """
    try:
        # Change to the repo directory
        os.chdir(repo_path)
        
        # Check if there are changes
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if not status.stdout.strip():
            print("No changes to sync.")
            return True

        if not commit_message:
            date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            commit_message = f"Auto-sync: Generated content {date_str}"

        print(f"Syncing to GitLab: {commit_message}")
        
        # Git commands
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        
        # Phase 78: Git Push Retry Logic (handle network timeouts)
        import time
        for attempt in range(3):
            try:
                subprocess.run(["git", "push"], check=True)
                print("Successfully pushed to GitLab.")
                return True
            except subprocess.CalledProcessError as e:
                if attempt < 2:
                    print(f"Git push failed (Attempt {attempt+1}/3). Retrying in 5s...")
                    time.sleep(5)
                else:
                    raise e
    except subprocess.CalledProcessError as e:
        print(f"Git sync failed: {e}")
        return False
    except Exception as e:
        print(f"An error occurred during git sync: {e}")
        return False

if __name__ == "__main__":
    # Test run (assuming current directory is the repo)
    sync_to_gitlab(os.getcwd())
