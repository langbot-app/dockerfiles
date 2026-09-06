# LangBot Docker Images

Docker images for LangBot infrastructure.

## Structure

Each subdirectory contains a `Dockerfile` for one image. Pushing to `main` auto-builds and pushes changed images to Docker Hub under `rockchin/<dir>`.

## Images

| Directory | Image | Description |
|-----------|-------|-------------|
| `langbot-sandbox` | `rockchin/langbot-sandbox` | Python 3.12 + Node 22 + common tools (git, vim, curl, wget, jq) for LangBot langbot-sandbox environments |

## Sandbox chart support

`rockchin/langbot-sandbox` includes Matplotlib, pandas, and Noto CJK fonts.
Matplotlib defaults to the headless Agg backend and a CJK-capable sans-serif font,
so ordinary plotting scripts can render simplified/traditional Chinese without
installing packages or setting a font on every invocation. These defaults apply
to both root and non-root users. Scripts that explicitly replace the font settings
(including some styles) must select a CJK font themselves; `Noto Sans CJK JP` is
the family Matplotlib discovers in Debian's bundled Noto collection.

The dependency versions are pinned in `langbot-sandbox/requirements.txt`.
Every image build runs `langbot-sandbox/tests/smoke_test.py`, checking pandas CSV
processing, default-font glyph coverage (including the Unicode minus), and real
Chinese PNG rendering with missing-glyph warnings treated as errors. Pull requests
build/test both amd64 and arm64 without publishing.

To verify locally:

```sh
docker build -t langbot-sandbox:test ./langbot-sandbox
docker run --rm --network none \
  -v "$PWD/langbot-sandbox/tests/smoke_test.py:/tmp/smoke_test.py:ro" \
  langbot-sandbox:test python /tmp/smoke_test.py
```

Existing installations must pull the updated image on the Docker host used by
LangBot Box, then recreate their **sandbox sessions/containers**. Updating LangBot
alone or restarting an existing sandbox does not replace its image:

```sh
docker pull rockchin/langbot-sandbox:latest
```

Back up any needed files installed or written only inside an old container before
recreating it. Bind-mounted workspace data is separate from the container image.

## Adding a new image

1. Create a new directory (e.g. `my-image/`)
2. Add a `Dockerfile` inside it
3. Push to `main` — CI will auto-detect and build `langbot/my-image`

## Manual build

Use the workflow dispatch to build a specific image:

```
gh workflow run build.yml -f image=langbot-sandbox
```

## Secrets required

- `DOCKERHUB_USERNAME` — Docker Hub username (rockchin)
- `DOCKERHUB_TOKEN` — Docker Hub access token
