const { Pool } = require('pg');
const pool = new Pool({
    connectionString: "postgresql://neondb_owner:npg_O1mLbVXkfEY5@ep-broad-fog-a4ba5mi3-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"
});

async function check() {
    try {
        const res = await pool.query(`
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        `);
        console.log('Tables in DB:', res.rows.map(r => r.table_name));
    } catch (e) {
        console.log('Error:', e.message);
    } finally {
        await pool.end();
    }
}

check();
