# Github Poller

This app pools github repo to check if new commits added and notifies Argo Events endpoint

Below variables requried to run container:

```bash
GITHUB_API_URL=https://api.github.com/repos/<username>/<repo name>/commits
GITHUB_TOKEN=<public repo access token>
LAST_COMMIT_FILE=<optional, default is /data/last_commit.txt>
ARGO_EVENT_SOURCE_URL=
```

[Dockerhub](https://hub.docker.com/r/alyvusal/github-poller)
