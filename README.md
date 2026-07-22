# LibrePlate

A free and open-source food tracker and meal planner.

librePlate exists because many existing food tracking services are closed source, web-only or app-only, have limited features, or lock users into their platform. This project aims to provide a modern, feature-rich, and transparent alternative that anyone can use, self-host, and contribute to.

## Getting Started

### Install

LibrePlate uses [Python UV](https://docs.astral.sh/uv/getting-started/installation/) to manage its updates and instalation.

To install LibrePlate run:

```
uv sync
uv run invoke init
```

To update LibrePlate and all its dependencies run:
```
uv run invoke update
```


To see how to do other things with the server, type:
```
uv run invoke --help
```

### Configuration

The server needs an `.env` file to be configured in the root directory. This can be coppied over from the `.env_example`. Read the instructions in the file
on how to configure it further.

```
cp .env_example .env
```

### Running the server

The `serve` task starts the LibrePlate website server.

- In development mode, it runs Django's development server.
- In release mode, it runs the production Gunicorn WSGI server. A reverse proxy
  is still required in front of Gunicorn to serve public traffic.

Run:
```
uv run invoke serve
```