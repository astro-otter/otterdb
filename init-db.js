'use strict';
const db = require('@arangodb').db;
const users = require('@arangodb/users');

db._createDatabase('otter');

users.save('user-guest', '');
users.grantDatabase('user-guest', 'otter', 'ro');

users.save('vetting-user', '');
users.grantDatabase('vetting-user', 'otter', 'ro');
