Mnem is a middle-man server which can provide search results or query responses.

It was born out of frustration with the lack of an open and extensible search
framework and the difficulty of maintaining useful search agents in a browser extension.
It occurred to me that this service should not be bound up with another application
and should be separate and available to all clients.

## Running the server

The server is a RESTful web server. It was designed this way so that it would
be usable easily by a wide range of clients, from browser plugins and desktop
widgets to native programs and even remote clients.

The server requires `flask-restful`, which can be installed with `pip`.

Then, running the server is as simple as `python3 mnem-rest.py`

## Clients

A program wishing to have access to the Mnem search providers has two options:

* Hit the REST API provided by a running server
* Use the Mnem library directly internally.

It is probably easier to use the REST API, as this is less likely to "churn" as
the program undergoes initial development. One day, there might be a more
formal API freeze or versioning on the library API, but for now, if you use the
library, be prepared for it to change often. Or don't, I'm a README, not a cop.

A primary advantage of the REST API is that the client can be remote from the
server, and thus the client needs only very basic capabilities - just enough to
form URLs, send/receive HTTP traffic and decode JSON. This means that Mnem can
even provide search services to otherwise extremely limited devices, including
embedded devices.
