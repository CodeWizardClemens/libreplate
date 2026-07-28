# LibrePlate

A free and open-source food tracker and meal planner.

librePlate exists because many existing food tracking services are closed source, web-only or app-only, have limited features, or lock users into their platform. This project aims to provide a modern, feature-rich, and transparent alternative that anyone can use, self-host, and contribute to.

## Getting Started

### Install

LibrePlate uses [Python UV](https://docs.astral.sh/uv/getting-started/installation/) to manage its updates and instalation.

To install LibrePlate run:

To see how to use the serve run the following command:
```
uv run invoke --help
```

Or check out the generated manual here: [Invoke Task Manual](INVOKE_MANUAL.md).

### Configuration

The server needs an `.env` file to be configured in the root directory. This can be coppied over from the `.env_example`. Read the instructions in the file
on how to configure it further.

```
cp .env_example .env
```