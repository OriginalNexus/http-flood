HTTP Flood attack example
---

## Local testing environment

You need Docker with docker-compose to setup a local testing environment.

To start the environment run:

```shell
docker-compose up -d
```

The environment exposes two endpoints:
 * http://localhost:4000 - nginx
 * http://localhost:5000 - apache

To stop the environment run:

```shell
docker-compose down
```

## Exploit script

You need Python 3 to run this exploit

```shell
python3 flood.py <url> <count> <delay> <max_threads>
```

Arguments:
 * `url` - the url to attack
 * `count` - number of checks for measuring response time
 * `delay` - delay in seconds between response time checks
 * `max_threads` - maximum number of flooding threads

Example:

Attack the nginx endpoint using a maximum of 128 threads. Measure the response
time by averaging 10 requests, each made at a 0.1 seconds delay:

```shell
python flood.py http://localhost:4000 10 0.1 128
```
