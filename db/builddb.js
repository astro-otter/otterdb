const { db } = require("@arangodb");

// create the database
db._createDatabase("otter")
db._useDatabase("otter")

// create the tde collection
db._create("tdes")

// create our users
const users = require('@arangodb/users');
users.save('admin@otter', 'insecure'); // for full access
users.save('user@otter', 'insecure'); // for the api

// give admin full access
users.grantDatabase('admin@otter', 'otter', 'rw')
users.grantCollection('admin@otter', 'otter', 'tdes', 'rw')

// give users only read access
users.grantDatabase('user@otter', 'otter', 'ro')
users.grantCollection('user@otter', 'otter', 'tdes', 'ro')
