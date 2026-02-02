const Database = require('better-sqlite3');
const db = new Database('auth.db');
console.log('Database initialized at auth.db');
db.close();
