import os
import requests

GITHUB_API_URL = os.getenv("GITHUB_API_URL")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
LAST_COMMIT_FILE = os.getenv("LAST_COMMIT_FILE", "/data/last_commit.txt")
ARGO_EVENT_SOURCE_URL = os.getenv("ARGO_EVENT_SOURCE_URL")

def get_latest_commit():
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(GITHUB_API_URL, headers=headers)
    if response.status_code == 200:
        return response.json()[0]['sha']
    else:
        print(f"Error fetching commits: {response.status_code} - {response.text}")
        return None

def read_last_commit():
    """Reads the last commit from the file."""
    if os.path.exists(LAST_COMMIT_FILE):
        with open(LAST_COMMIT_FILE, 'r') as file:
            return file.read().strip()
    return None

def write_last_commit(commit_sha):
    """Writes the latest commit to the file."""
    with open(LAST_COMMIT_FILE, 'w') as file:
        file.write(commit_sha)

def trigger_argo_event():
    """Triggers the Argo event."""
    response = requests.post(ARGO_EVENT_SOURCE_URL, json={"event": "new_commit"})
    if response.status_code == 200:
        print("Successfully triggered Argo event.")
    else:
        print(f"Failed to trigger Argo event: {response.status_code} - {response.text}")

def main():
    # Get the latest commit
    latest_commit = get_latest_commit()
    if latest_commit:
        last_commit = read_last_commit()
        if latest_commit != last_commit:
            print(f"New commit detected: {latest_commit}")
            trigger_argo_event()
            write_last_commit(latest_commit)
        else:
            print("No new commits detected.")

if __name__ == "__main__":
    main()
