# LangBot Docker Images

Docker images for LangBot infrastructure.

## Structure

Each subdirectory contains a `Dockerfile` for one image. Pushing to `main` auto-builds and pushes changed images to Docker Hub under `rockchin/<dir>`.

## Images

| Directory | Image | Description |
|-----------|-------|-------------|
| `sandbox` | `rockchin/sandbox` | Python 3.12 + Node 22 + common tools (git, vim, curl, wget, jq) for LangBot sandbox environments |

## Adding a new image

1. Create a new directory (e.g. `my-image/`)
2. Add a `Dockerfile` inside it
3. Push to `main` — CI will auto-detect and build `langbot/my-image`

## Manual build

Use the workflow dispatch to build a specific image:

```
gh workflow run build.yml -f image=sandbox
```

## Secrets required

- `DOCKERHUB_USERNAME` — Docker Hub username (rockchin)
- `DOCKERHUB_TOKEN` — Docker Hub access token
