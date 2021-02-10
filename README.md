# Akibox Tutorial - Django REST Framework

This is a tutorial project to help you get to know the Akita/Django
integration.  It contains a server built using Django REST Framework that
implements a toy Dropbox-like file server.

You can use Akita to generate a spec describing the Akibox APIs.  Normally, you
would do this by starting the Akita Client and sending traffic to the server --
the Akita Client captures network traffic, which it uses to build a spec.

But how to generate API traffic?  You could send requests manually, but you may
also have another good source of traffic -- integration tests!  Django offers
handy testing tools that avoid starting a server and sending traffic over the
network, but that means the normal Akita method of packet capture won't work. 

The Akita/Django integration lets you use integration tests you've written for
your Django application as the source of API traffic that Akita will use to
build the spec.  It works by wrapping the Django test client with an extra
layer that captures requests and responses and sends them to Akita.

## Installing Dependencies

```bash
# Create a python virtual environment and install dependencies
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

## Running the Server

```bash
python manage.py runserver
```

## Running the Tests

Akibox uses `akita_django.test.Client` in place of `django.test.Client` in
order to capture requests and responses from integration tests into an HTTP
Archive (HAR) file, which Akita can use to generate a spec for Akibox.

Run the tests:
```bash
./manage.py test
```

Look for `akita_trace.file.har` and `akita_trace.user.har`, which capture
requests and responses against the `/files` and `/users` endpoints.

## Adding New Tests

The integration tests live in `akiboxImpl/tests.py`.  Try creating some new
tests and look for the corresponding traffic in the HAR files.
