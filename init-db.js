'use strict';
const db = require('@arangodb').db;
const users = require('@arangodb/users');
const env = require("internal").env;

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
	console.log("Creating the otter database");
	db._createDatabase('otter');
    }
        
    // Create the base collections
    db._useDatabase("otter");

    if (!db._collection("transients")) {
	console.log("Creating the collection otter/transients");
	db._create("transients");
    }
    if (!db._collection("vetting")) {
	console.log("Creating the collection otter/vetting");
	db._create("vetting");
    }

    console.log("Finished setting up the database and collections!");
    console.log("Initializing the users...")
    
    // Generate the necessary users
    if (!users.exists(env.ARANGO_USER_USERNAME)) {
	users.save(env.ARANGO_USER_USERNAME, env.ARANGO_USER_PASSWORD);
	users.grantDatabase(env.ARANGO_USER_USERNAME, 'otter', 'ro');
	users.grantCollection(env.ARANGO_USER_USERNAME, 'otter', 'transients', 'ro');
	users.grantCollection(env.ARANGO_USER_USERNAME, 'otter', 'vetting', 'rw');
	console.log("Finished initializing the guest user!");
    }

    if (!users.exists(env.VETTING_USER)) {
	users.save(env.VETTING_USER, env.VETTING_PASSWORD);
	users.grantDatabase(env.VETTING_USER, 'otter', 'rw');
	users.grantCollection(env.ARANGO_USER_USERNAME, 'otter', 'transients', 'rw');
	users.grantCollection(env.ARANGO_USER_USERNAME, 'otter', 'vetting', 'rw');
	console.log("Finished initializing the vetting user!")
    }

    users.grantCollection("root", "otter", "transients", "rw");
    users.grantCollection("root", "otter", "vetting", "rw");
    console.log("Finished granting write permission to root for the new collections!")
    
    // Finally, Update the passwords, and always do this just in case they have changes
    console.log(env.VETTING_USER, "password is set to: ", env.VETTING_PASSWORD)
    users.update(env.VETTING_USER, env.VETTING_PASSWORD)

    console.log(env.ARANGO_USER_USERNAME, "password is set to: ", env.ARANGO_USER_PASSWORD)
    users.update(env.ARANGO_USER_USERNAME, env.ARANGO_USER_PASSWORD)

    console.log("Root password is set to: ", env.ARANGO_ROOT_PASSWORD)
    users.update("root", env.ARANGO_ROOT_PASSWORD)
    
    console.log("SUCCESS! Finished database and user initialization!")
    
} catch (e) {
    print("ERROR! During database initialization!");
    print(e)
}
