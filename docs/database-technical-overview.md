# Miniserve communications

## How does it work?

The Miniserve database http interface communicates by JSON messages
sent between client and server, using http method POST. Internally,
Miniserve generates SQL queries in text form, as they would be sent
to the sqlite3 python API. A brief example shows what happens internally
with each call:

* A message structure is created on the client
```
structure = {
  "action": "insert",
  "data": {
    "title": "This is a task",
    "completed": False,
    "priority": 3
  }
}
```

* The structure is converted to json format and sent to the server by
the `Client.query('tasks', structure)` function (in this example, to
a table on the server database, called 'tasks'.

* The server receives this message, unpacks the JSON string back into
the original structure and decodes its parts

  * `action = "insert"` tells the interpreter it is an INSERT query

  * the `data = {...}` contains a dictionary, where each key is a field
on that table, and the corresponding values are, in this case, values
to be inserted on that table.

* The resulting SQL query for this example would be:
```
INSERT INTO tasks (title, completed, priority) VALUES (?, ?, ?)
```

Note that the SQL statements generated here, use interrogation symbols
instead of the actual data. While it's doable, generating the statement
with the data is more complicated, due to the different possible types
and, sqlite3 can process _prepared statements_ which take care of field
data types, invalid characters and SQL injection.

The function that generates this statement returns a tuple with the
statement as a string, and the corresponding data as a list. Those are
then fed into the sqlite3 execute() method of the prepared statement.

After execution, the result is returned as a second structure:

```
response = {
  "status": "Ok",
  "data": [],
  "affectedRows": -1,
  "insertId": 349
}
```

This response is then converted to JSON and sent as a response to the client.

## SQL query level of complexity

Miniserve only does simple queries; simple INSERT, UPDATE, SELECT, DELETE statements.
More complex things like JOINS are not supported. Transactions are also not
supported at the moment. This project has been built as a hobby, as a self
dare-you-can-do-it, and at this point the author does not have the intention
of growing its complexity.

With that said, where conditional statements can be used, Miniserve uses a
similar approach to that of //graphql//, where statements like `WHERE a = b`,
`WHERE title like "%word%"`, `WHERE age <= 3` are all possible.

## Message structure

```
{
  "action": // One of insert, update, select, delete
  "data": {
     // Dictionary of { field: value } pairs representing a row
     // These could be a partial row (in the case of an update, or
     // an insert that omits default values.
  },
  "cond": {
     // a dictionary of { field: { operator: value } } pairs.
     // all conditions are ANDed. A future version may implement
     // combinations of AND and OR
  }
}
```

The above structure describes all the allowed attributes, however, some
operations may not use some of the attributes. An example is DELETE:

```
DELETE FROM tasks WHERE id = 45;
```

With no mention of any fields and values other than the id in the WHERE
section, there's no need for the structure to include "data".

```
{
  "action": "delete",
  "cond": {
    "id": {"_eq": 45}
  }
}
```

Another example is INSERT

```
INSERT INTO tasks (title, completed, priority) VALUES ('New Task', False, 3);
```

Inserting a new value doesn't need to refer to any existing field, making
the "cond" attribute useless for this case

```
{
  "action": "insert",
  "data": {
    "title": "New task",
    "completed": False,
    "priority": 3
  }
}
```

However, UPDATE can use the three attributes in full

```
{
  "action": "update",
  "data": {"completed": True},
  "cond": {
    "rowid": {"_eq": 46}
  }
}
```

and so can SELECT

```
SELECT * FROM tasks WHERE title like '%task%';
```

The difference with select is that the "data" dictionary won't pay attention
to the value of the fields included. Also, an empty  "data" dictionary will
generate a `SELECT *` (all fields).

```
{
  "action": "select",
  "data": {},
  "cond": {
    "title": {"_like": "%task%"}
  }
}
```

To choose fields for the SELECT statement, I found the most "correct" way
of doing so is by using pairs of `{field: True}`. I haven't tried this, but
using `{field: False}` should still use the field, as all it checks for is
its presence and not its value.

```
{
  "action": "select",
  "data": {
    "rowid": True,
    "title": True,
    "completed": True
  }
}
```

With no condition defined, the SELECT statement will just return **all elements
of the list**.

**A WORD OF WARNING:** This is also valid for **DELETE** statements: with 
**no conditional attributes**, the DELETE query **will delete all values 
from the table**.

