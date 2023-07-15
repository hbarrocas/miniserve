#!/bin/bash

if [ ! -f "default.sql" ]; then
  echo "No default.sql found!!! - required to initialise the server's database"
  echo "Aborting..."
  exit 1
fi

rm -f data.db
cat default.sql | sqlite3 data.db && echo "Database has been initialised."

