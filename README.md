# Miniserve

This is a super minimalistic http interface to SQLITE. It uses
JSON as the data format to communicate to and from the server.

Normal file serving has been minimally added. It can serve small
html documents and its images, javascript, css as a normal web
server, however, it doesn't support any kind of security and
authentication methods at this point.

This project is a proof of concept; a fun self-imposed challenge
that could serve a small offline lab environment, where a simple backend
would be needed in minutes and security is not a concern.

## Using for the first time

Before running for the first time, create a sqlite3 database to serve.

The `miniserve` script and the `default.sql` file have been added for
your convenience. Running `miniserve` will show a help message with all
the available options. These include creating a new miniserve project,
running the current project's server, resetting the project and creating
backups of the database.

## Running the server

To use the server, open a terminal and run:

```
python3 server
```

It will use port 9000 to listen to incoming requests.
Future versions will have more flexibility allowing the choice of a
different port and settings for future functionality.

## Testing:

To test, you can use 'curl'. curl communicates with http servers and
can talk in several ways. This server works as follows:

- Send a request on http://localhost:9000/database/<nameoftable>
  where <nameoftable> is the name of a table in the sqlite database
  (in this case, the data.db file included)

- This request has to be done using the HTTP POST method, since we're
  going to send the json string as input. The normal HTTP GET method
  can only encode information in the url itself, like so:
  http://localhost:9000/database/people?varname=value&othervar=otherval

So, to test the server with curl, open another terminal and run:

```
curl -X POST -d '{"action":"select", "data": {}}' http://localhost:9000/database/people
```

This sends the json data after the -d switch to the server using the
HTTP POST method.

If all works well, you should get a json response in the terminal:

```
{"status": "Ok", "data": [{"name": "Heli", "surname": "Barrocas"}], "affectedRows": -1, "insertId": 0}
```

This response shows a status: Ok, meaning we didn't have any errors querying
the database, and the data is an array of dictionaries, each representing a
row, where the key of the dictionary is the field name and the value is the
value for that field on that row.

I've implemented the return of information that would be useful after a sql
query, such as the rows affected,  and for inserts, the insertId of the newly
created row.

## Test further:

I've described in the following paragraphs, some bits of json code you can
try to test it more. The json I've wrote here has indentation, but I think
it would be best if you compact it before sending it with curl, like this:

```
{
  "action": "insert",
  "data": {
    "name": "John",
    "surname": "Doe"
  }
}
```

would be compacted like:

```
{"action":"insert", "data": {"name":"John", "surname":"Doe"}}
```

Included in this repo, are some tests for the `client.py` client library
that simplifies connecting and interfacing with this server from any Python3
application.

## File structure

- __server/__  holds the server module that can run independently as explained
at the beginning of this file.
- __files/__ holds any files that Miniserve can serve upon a GET request.
- __tests/__ holds some test scripts. At the moment they're broken.
- __client.py__ is the only file part of the client library.


## More Documentation

Check out the technical [documentation](docs/database-technical-overview.md)
