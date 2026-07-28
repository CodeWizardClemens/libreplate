
<!-- AUTOMATICALLY GENERATED FILE, CHECK INVOKE HOW TO UPDATE. -->

# Invoke tasks documentation

To use invoke you will have to create a virtual environment first, and use its
python shell. Install [Python UV](https://docs.astral.sh/uv/getting-started/installation/) and run.
```
cd backend && uv sync
source ./venv/bin/activate
cd ../
```

To run a task you can run:
```
invoke <task> <flags>
```

To learn more about that invoke task you can run:

```
invoke --help <task>
```

If you are new to invoke you can also run:

```
invoke -help
```



## `db.migrate`

```text

Usage: inv[oke] [--core-opts] db.migrate [other tasks here ...]

Docstring:
  Create and apply Django migrations.

Options:
  none


```


## `db.sync-default-data`

```text

Usage: inv[oke] [--core-opts] db.sync-default-data [other tasks here ...]

Docstring:
  Synchronize default application data.

Options:
  none


```


## `dev.check`

```text

Usage: inv[oke] [--core-opts] dev.check [--options] [other tasks here ...]

Docstring:
  Run code quality checks.

Options:
  -v, --verbose   Show stdout output from commands.


```


## `dev.format`

```text

Usage: inv[oke] [--core-opts] dev.format [--options] [other tasks here ...]

Docstring:
  Automatically format the codebase.

Options:
  -v, --verbose   Show stdout output from commands.


```


## `dev.serve-backend`

```text

Usage: inv[oke] [--core-opts] dev.serve-backend [other tasks here ...]

Docstring:
  Start the backend development server.

Options:
  none


```


## `dev.serve-frontend`

```text

Usage: inv[oke] [--core-opts] dev.serve-frontend [other tasks here ...]

Docstring:
  Start the frontend development server.

Options:
  none


```


## `dev.test`

```text

Usage: inv[oke] [--core-opts] dev.test [--options] [other tasks here ...]

Docstring:
  Run the LibrePlate automated test suite.

Options:
  -v, --verbose   Show stdout output from commands.


```


## `dev.user-add-dummy`

```text

Usage: inv[oke] [--core-opts] dev.user-add-dummy [other tasks here ...]

Docstring:
  Create a dummy LibrePlate user account.

Options:
  none


```


## `dev.verify`

```text

Usage: inv[oke] [--core-opts] dev.verify [--options] [other tasks here ...]

Docstring:
  Run all code quality checks and tests.

Options:
  -v, --verbose   Show stdout output from commands.


```


## `maintenance.migrate`

```text

Usage: inv[oke] [--core-opts] maintenance.migrate [other tasks here ...]

Docstring:
  Create and apply Django migrations.

Options:
  none


```


## `maintenance.update`

```text

Usage: inv[oke] [--core-opts] maintenance.update [other tasks here ...]

Docstring:
  Update LibrePlate dependencies, source code, and database state.

Options:
  none


```


## `setup.add-usda-api-key`

```text

Usage: inv[oke] [--core-opts] setup.add-usda-api-key [--options] [other tasks here ...]

Docstring:
  Configure the USDA API key.

Options:
  -k STRING, --key=STRING


```


## `setup.init`

```text

Usage: inv[oke] [--core-opts] setup.init [other tasks here ...]

Docstring:
  Initialize LibrePlate.

Options:
  none


```


## `setup.migrate`

```text

Usage: inv[oke] [--core-opts] setup.migrate [other tasks here ...]

Docstring:
  Create and apply Django migrations.

Options:
  none


```


## `setup.sync-default-data`

```text

Usage: inv[oke] [--core-opts] setup.sync-default-data [other tasks here ...]

Docstring:
  Synchronize default application data.

Options:
  none


```


## `setup.user-add`

```text

Usage: inv[oke] [--core-opts] setup.user-add [--options] [other tasks here ...]

Docstring:
  Create a new LibrePlate user account.

Options:
  -e STRING, --email=STRING
  -f STRING, --first-name=STRING
  -l STRING, --last-name=STRING
  -p STRING, --password=STRING
  -s, --skip-password-validation   Skip password validation.
  -u STRING, --username=STRING


```


## `setup.user-remove`

```text

Usage: inv[oke] [--core-opts] setup.user-remove [--options] [other tasks here ...]

Docstring:
  Remove an existing LibrePlate user account.

Options:
  -u STRING, --username=STRING


```
