const { Pool } = require('pg');
const pool = new Pool({
    connectionString: "postgresql://neondb_owner:npg_O1mLbVXkfEY5@ep-broad-fog-a4ba5mi3-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"
});

async function check() {
    try {
        const res = await pool.query("SELECT * FROM \"user\" LIMIT 5");
        console.log('Current users:', res.rows);
    } catch (e) {
        console.log('Error or table not found:', e.message);
    } finally {
        await pool.end();
    }
}

check();
