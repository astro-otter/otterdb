'use strict';
const db = require('@arangodb').db;
const users = require('@arangodb/users');

// First check connection
try {
  db._version(); // Try an API call
  print("Connected to ArangoDB");
} catch (e) {
  print("ERROR: Could not connect to ArangoDB");
  quit(1);
  throw e;  // This ensures arangosh exits non-zero
}

// Then try to setup
try {
    // Create the OTTER database
    if (!db._databases().includes("otter")) {
	db._createDatabase('otter');
    }
    
    // Generate the necessary users
    if (!users.exists("user-guest")) {
	users.save('user-guest', '');
	users.grantDatabase('user-guest', 'otter', 'ro');
    }

    if (!users.exists("vetting-user")) {
	console.log("vetting-user password is set to: ", process.env.VETTING_PASSWORD)
	users.save('vetting-user', process.env.VETTING_PASSWORD);
	users.grantDatabase('vetting-user', 'otter', 'rw');
    }
    
    // Create the base collections
    db._useDatabase("otter");

    if (!db._collection("transients")) {
	db._create("transients");
    }
    if (!db._collection("vetting")) {
	db._create("vetting");
    }

    // Finally, Update the root password
    console.log("Root password is set to: ", process.env.ARANGO_ROOT_PASSWORD)
    users.update("root", process.env.ARANGO_ROOT_PASSWORD)
    
} catch (e) {
    print("ERROR! During database initialization!");
    print(e)
}
