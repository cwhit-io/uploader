# Uploader API

This repository provides a minimal Flask-based web API that accepts image and video uploads and saves them into a host folder mounted into the container.

Files created:

- `app.py` – Flask app with `/upload` and `/health` endpoints.
- `Dockerfile` – builds container image.
- `docker-compose.yml` – example compose file that mounts a host folder into the container.
- `entrypoint.sh` – ensures upload directory exists and is writable.
- `requirements.txt` – Python dependencies.

Environment and host folder

- The container uses the environment variable `UPLOAD_DIR` (default `/app/uploads`) as the internal path where files are stored.
- When running with Docker, mount a host folder into `/app/uploads` so uploaded files are preserved on the host.

Using docker-compose (recommended):

1. Option A — use a host path from an env var named `HOST_UPLOAD_DIR`:

```bash
# set HOST_UPLOAD_DIR to an absolute or relative host path (e.g. /data/uploads)
export HOST_UPLOAD_DIR=/path/on/host/uploads
docker compose up --build
```

If `HOST_UPLOAD_DIR` is not set, compose will default to `./uploads` inside repository.

2. Option B — docker run directly:

```bash
# create host folder
mkdir -p /path/on/host/uploads
# run container and mount host folder
docker build -t uploader:latest .
docker run -p 8000:8000 -e UPLOAD_DIR=/app/uploads -v /path/on/host/uploads:/app/uploads uploader:latest
```

API documentation

1. Health check

- GET /health

Response: 200 OK

2. Upload file

- POST /upload
- Content type: `multipart/form-data`
- Form fields:
  - `file` (required): the file to upload (image or video)
  - `subdir` (optional): a simple alphanumeric/dash/underscore subfolder name to place the file in

Example curl (image):

```bash
curl -X POST -F "file=@/path/to/photo.jpg" http://localhost:8000/upload
```

Example curl (video into subdir):

```bash
curl -X POST -F "file=@/path/to/movie.mp4" -F "subdir=events" http://localhost:8000/upload
```

Response (success):

```json
{ "success": true, "saved_as": "20260101T120000000000_filename.jpg" }
```

Notes

- The container's `UPLOAD_DIR` path is independent of the host: make sure to mount your desired host directory into `/app/uploads` inside the container using the `-v` option or `docker-compose`.
- The server allows common image and video extensions and also checks MIME types returned by the client.

Security considerations

- This is a simple example for local or internal use. For production, run behind TLS, add authentication, validate file contents more thoroughly, and limit allowed sizes.
