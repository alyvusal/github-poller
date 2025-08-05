# GitHub Poller

A lightweight Python application that monitors GitHub repositories for new commits and triggers Argo Events when changes are detected. This tool is designed for GitOps workflows and CI/CD pipelines that need to react to repository changes.

## Features

- 🔍 **Repository Monitoring**: Polls GitHub API to check for new commits
- 🔄 **State Persistence**: Tracks the last seen commit to avoid duplicate notifications
- 🚀 **Argo Events Integration**: Triggers Argo Events endpoints when new commits are detected
- 🐳 **Containerized**: Ready-to-use Docker image
- ⚙️ **Configurable**: Environment-based configuration for flexibility

## Quick Start

### Using Docker

```bash
docker run -d \
  --name github-poller \
  -e GITHUB_API_URL="https://api.github.com/repos/username/repo-name/commits" \
  -e GITHUB_TOKEN="your_github_token" \
  -e ARGO_EVENT_SOURCE_URL="http://argo-events-webhook:12000/github-poller" \
  -v /path/to/data:/data \
  alyvusal/github-poller
```

### Using Docker Compose

```yaml
version: '3.8'
services:
  github-poller:
    image: alyvusal/github-poller
    environment:
      - GITHUB_API_URL=https://api.github.com/repos/username/repo-name/commits
      - GITHUB_TOKEN=${GITHUB_TOKEN}
      - ARGO_EVENT_SOURCE_URL=http://argo-events-webhook:12000/github-poller
      - LAST_COMMIT_FILE=/data/last_commit.txt
    volumes:
      - ./data:/data
    restart: unless-stopped
```

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GITHUB_API_URL` | ✅ | - | GitHub API endpoint for commits (e.g., `https://api.github.com/repos/username/repo-name/commits`) |
| `GITHUB_TOKEN` | ✅ | - | GitHub personal access token or OAuth token |
| `ARGO_EVENT_SOURCE_URL` | ✅ | - | Argo Events webhook endpoint URL |
| `LAST_COMMIT_FILE` | ❌ | `/data/last_commit.txt` | Path to file storing the last seen commit SHA |

### GitHub Token Setup

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with `repo` scope (for private repos) or `public_repo` (for public repos)
3. Use the token as `GITHUB_TOKEN` environment variable

### Argo Events Integration

The application sends a POST request to the specified Argo Events endpoint with the following payload:

```json
{
  "event": "new_commit"
}
```

## Usage Examples

### Basic Usage

```bash
# Set environment variables
export GITHUB_API_URL="https://api.github.com/repos/myorg/myapp/commits"
export GITHUB_TOKEN="ghp_your_token_here"
export ARGO_EVENT_SOURCE_URL="http://argo-events-webhook:12000/github-poller"

# Run the container
docker run --rm \
  -e GITHUB_API_URL \
  -e GITHUB_TOKEN \
  -e ARGO_EVENT_SOURCE_URL \
  -v $(pwd)/data:/data \
  alyvusal/github-poller
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: github-poller
spec:
  replicas: 1
  selector:
    matchLabels:
      app: github-poller
  template:
    metadata:
      labels:
        app: github-poller
    spec:
      containers:
      - name: github-poller
        image: alyvusal/github-poller
        env:
        - name: GITHUB_API_URL
          value: "https://api.github.com/repos/username/repo-name/commits"
        - name: GITHUB_TOKEN
          valueFrom:
            secretKeyRef:
              name: github-token-secret
              key: token
        - name: ARGO_EVENT_SOURCE_URL
          value: "http://argo-events-webhook:12000/github-poller"
        - name: LAST_COMMIT_FILE
          value: "/data/last_commit.txt"
        volumeMounts:
        - name: data-volume
          mountPath: /data
      volumes:
      - name: data-volume
        persistentVolumeClaim:
          claimName: github-poller-pvc
```

## Development

### Local Development

```bash
# Clone the repository
git clone <repository-url>
cd github-poller

# Install dependencies
pip install requests

# Set environment variables
export GITHUB_API_URL="https://api.github.com/repos/username/repo-name/commits"
export GITHUB_TOKEN="your_token"
export ARGO_EVENT_SOURCE_URL="http://localhost:12000/github-poller"

# Run the application
python poller.py
```

### Building the Docker Image

```bash
docker build -t github-poller .
```

## Architecture

The application follows a simple polling pattern:

1. **Fetch Latest Commit**: Queries GitHub API for the most recent commit
2. **Compare with Previous**: Checks against the last known commit SHA
3. **Trigger Event**: If a new commit is detected, triggers Argo Events
4. **Update State**: Stores the new commit SHA for future comparisons

## Troubleshooting

### Common Issues

**Error: "Error fetching commits: 401"**
- Check that your `GITHUB_TOKEN` is valid and has the correct permissions
- Ensure the repository URL is correct

**Error: "Failed to trigger Argo event: 404"**
- Verify the `ARGO_EVENT_SOURCE_URL` is correct
- Ensure the Argo Events webhook is properly configured

**No new commits detected**
- Check the `LAST_COMMIT_FILE` to see the last processed commit
- Verify the GitHub API URL points to the correct repository

### Logs

The application provides basic logging:
- `New commit detected: <sha>` - When a new commit is found
- `No new commits detected.` - When no changes are detected
- `Successfully triggered Argo event.` - When Argo Events is notified
- Error messages for API failures

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Docker Hub

The image is available on Docker Hub: [alyvusal/github-poller](https://hub.docker.com/r/alyvusal/github-poller)

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
