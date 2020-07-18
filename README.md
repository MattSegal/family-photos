# Family Photos

Currently at [memories.ninja](https://memories.ninja)

## Local development

Requires an AWS account.

Create a .env file at the repository root

```bash
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
```

Ensure invoke is installed

```bash
pip3 install --user invoke
```

Build the Docker container

```bash
inv build
```

Build the Docker container

```bash
inv build
```

Setup the database

```bash
./scripts/clean-db.sh
```

Run the web container

```bash
inv web
```

View the worker logs

```bash
inv logs
```
