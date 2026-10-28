
# Docker Security Assessment

A secure three-tier web application deployed using Docker Compose, with a Python Flask backend, PostgreSQL database, and Nginx frontend. This project demonstrates container hardening, vulnerability scanning, image publishing, and cryptographic image signing.

## Student Details

| Field               | Details             |
| ------------------- | ------------------- |
| Name                | Ayush Raj           |
| Registration Number | `202401100100083` |
| Application Port    | `163`             |
| GitHub Username     | `Ayushraj2319`    |
| Docker Hub Username | `ayushraj2319`    |

## Project Overview

The application uses a containerized architecture consisting of three services:

- **Frontend:** Nginx serves the web interface and proxies API requests to the backend.
- **Backend:** Python Flask handles application logic and API requests.
- **Database:** PostgreSQL stores application registration data persistently.

Docker Compose manages the services, networking, health checks, and persistent storage.

## Technology Stack

- Docker and Docker Compose
- Python and Flask
- PostgreSQL
- Nginx
- Trivy
- Cosign
- Git and GitHub
- Docker Hub

## Project Structure

```text
202401100100083-docker-assessment/
├── backend/
│   ├── .dockerignore
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   └── index.html
├── reports/
│   ├── trivy-before.txt
│   └── trivy-after.txt
├── screenshots/
├── .env                  # Local secrets; do not commit
├── .env.example          # Environment variable template
├── .gitignore
├── compose.yaml
├── cosign.pub            # Public verification key
└── nginx.conf
```

The private Cosign key (`cosign.key`) is kept locally and must never be committed to GitHub.

## Application Architecture

```text
Browser
   |
   | HTTP :163
   v
Nginx Frontend
   |
   | API proxy
   v
Flask Backend
   |
   | PostgreSQL connection
   v
PostgreSQL Database
   |
   v
Persistent Named Volume
```

The frontend and backend communicate over a dedicated Docker network. PostgreSQL is connected to the internal backend network, limiting direct access from the frontend network.

## Prerequisites

Install the following tools before running the project:

- Docker Desktop
- Git
- A web browser

## Configuration

The application uses environment variables for database configuration.

1. Copy `.env.example` to `.env`.
2. Set the required database credentials and configuration values in `.env`.
3. Keep `.env` out of version control.

Never publish real passwords, tokens, or other credentials in the repository.

## Running the Application

Start the application from the project root:

```bash
docker compose up -d
```

Check service status:

```bash
docker compose ps
```

View application logs:

```bash
docker compose logs
```

Check the backend health endpoint through Nginx:

```bash
curl http://localhost:163/api/health
```

The expected health response contains the registration number, a healthy status, and the database connection status.

Open the application in a browser:

http://localhost:163

## Database Persistence

The PostgreSQL database uses a named Docker volume to preserve registration records across container recreation.

To test persistence:

```bash
docker compose down
docker compose up -d
```

Verify that previously created registration records remain available after the services restart.

Do not use `docker compose down -v` for this test because the `-v` option removes named volumes.

## Container Security Hardening

The backend image was hardened to improve its security posture.

Security measures include:

- Using a Python slim base image.
- Pinning application dependency versions.
- Installing Python dependencies without retaining pip's download cache.
- Running the application as a non-root user.
- Setting Python environment variables to improve container behavior.
- Using `.dockerignore` to exclude unnecessary build-context files.
- Keeping secrets outside the image and source repository.

The image was rebuilt and scanned with Trivy after the hardening changes.

## Trivy Vulnerability Scanning

Trivy was used to scan the backend container image before and after hardening.

Reports:

- `reports/trivy-before.txt`
- `reports/trivy-after.txt`

### Vulnerability Comparison

Replace the placeholders below with the actual counts from your Trivy reports.

| Metric                   | Before hardening | After hardening |
| ------------------------ | ---------------: | --------------: |
| CRITICAL vulnerabilities |    [Enter count] |   [Enter count] |
| HIGH vulnerabilities     |    [Enter count] |   [Enter count] |
| Image size               |     [Enter size] |    [Enter size] |

### CRITICAL Vulnerability Gate

The following command was used to test the required security gate:

```bash
trivy image --severity CRITICAL --ignore-unfixed --exit-code 1 fest-backend:0.2
echo $?
```

**Observed result:** Exit code `0`.

This means the image passed this configured gate: Trivy did not find any CRITICAL vulnerabilities matching the selected criteria and `--ignore-unfixed` filter. It does not mean the image has zero vulnerabilities of every severity.

## Docker Hub Image Publishing

The backend image was published to Docker Hub.

- Docker Hub repository: [ayushraj2319/fest-backend](https://hub.docker.com/r/ayushraj2319/fest-backend)
- Published version: `1.0.0`
- Additional tag: `1.0`

### Published Image Digest

The published `1.0.0` image index digest recorded during inspection was:

```text
sha256:4fbdf86d13b38d4b0015886384bef7acadd2dfc748701d5dcacc4341a7a5c1cc
```

The Compose configuration uses the published image:

```yaml
image: ayushraj2319/fest-backend:1.0.0
```

The registry deployment was tested by pulling the backend image and starting the application using Docker Compose.

## Image Signing and Verification with Cosign

Cosign was used to sign the published image and verify its signature using a public key.

### Key Pair

- `cosign.key`: private signing key; stored locally and excluded from Git.
- `cosign.pub`: public verification key; included in the repository.

The private-key password must never be published or shared.

### Signed Image Verification

The published `1.0.0` image was signed using its digest and verified with the public key.

Verification command:

```bash
cosign verify --key cosign.pub \
  ayushraj2319/fest-backend@sha256:4fbdf86d13b38d4b0015886384bef7acadd2dfc748701d5dcacc4341a7a5c1cc
```

**Observed result:** Verification succeeded. Cosign validated the claims, verified the transparency log entry, and verified the signature against the specified public key.

### Unsigned Image Rejection Test

A distinct image was published as `1.0.1` without signing it.

- Tag: `ayushraj2319/fest-backend:1.0.1`
- Digest recorded after pushing: `sha256:97a26258f5be637ce37512e8b7d9d98524bb1785d00b120b4601855badc1131c`

Verification command:

```bash
cosign verify --key cosign.pub \
  ayushraj2319/fest-backend:1.0.1
```

**Observed result:** Cosign returned `Error: no signatures found`, as expected for the unsigned test image.

## Evidence and Screenshots

The `screenshots/` directory is intended to contain genuine screenshots of the assessment, including:

- Backend build and health check.
- Docker Compose services running.
- Frontend and registration records.
- Database persistence verification.
- Trivy before and after scan results.
- Trivy security-gate exit code.
- Docker Hub image tags.
- Successful Cosign verification.
- Unsigned image rejection.
- Final GitHub repository.

Add the required original screenshots to this directory before submission.

## AI Tool Usage

AI assistance was used for guidance with Docker configuration, container hardening, vulnerability scanning, Cosign signing and verification, Git troubleshooting, and project documentation.

Commands were executed and results were checked in the local development environment. The submitted implementation and evidence should reflect the actual tests performed.

## Limitations and Final Notes

- Replace the vulnerability-count and image-size placeholders with measured values.
- Confirm all required screenshots are present before submission.
- Confirm the README and reports are pushed to GitHub.
- Keep `.env` and `cosign.key` out of version control.
- Recheck the published image digest if the image is rebuilt or republished.

## Links

- **GitHub Repository:** [202401100100083-docker-assessment](https://github.com/Ayushraj2319/202401100100083-docker-assessment)
- **Docker Hub Image:** [ayushraj2319/fest-backend](https://hub.docker.com/r/ayushraj2319/fest-backend)
