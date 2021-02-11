# Akibox Tutorial - Flask

This is a tutorial project to help you get to know Akita.  It contains a
Flask server implementing a toy Dropbox-like file server.  You can use Akita
to generate a spec for its API, make some changes, and see how API-impacting
changes show up in Akita's semantic diffs.

To try out the tutorial, head over
[here](https://docs.akita.software/docs/get-to-know-akita).


## Install dependencies

```bash
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

## Run integration tests

```bash
pytest -v
```

The Akibox integration tests also generate a HAR file, which you can use with
Akita's [`apispec`](https://docs.akita.software/docs/from-traffic-to-specs) to
generate a spec for your service based in its integration tests.

Look for the HAR file in the current working directory, e.g.
`akita_trace_1304812.har`.

## Fire up the service!

Get it running:
```bash
./run.sh
```

In another window, make some requests:
```bash
./test.sh
```

You can use Akita's packet capture agent to build a spec based on network
traffic to your service.  Take a look at [the
docs](https://docs.akita.software/docs/get-started-with-superlearn) for more
details.

## Building Docker Container

Optionally, you can build Akibox into a Docker container.

```
docker build -t akibox-tutorial .
```

## Limitations

* Does not yet handle cookies.
* Does not yet handle redirects in responses.
* Does not yet handle status text in responses.

