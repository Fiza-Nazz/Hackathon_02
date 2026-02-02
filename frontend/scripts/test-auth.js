const { betterAuth } = require('better-auth');
const { Pool } = require('pg');

process.on('unhandledRejection', (reason, promise) => {
    console.error('DEBUG: Unhandled Rejection reason:', reason);
});

async function run() {
    try {
        const pool = new Pool({
            connectionString: "postgresql://neondb_owner:npg_O1mLbVXkfEY5@ep-broad-fog-a4ba5mi3-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"
        });

        const auth = betterAuth({
            database: pool
        });
        console.log('Better Auth object created with Pool');
        await new Promise(resolve => setTimeout(resolve, 3000));
        console.log('Finished waiting');
    } catch (e) {
        console.error('Caught error:', e);
    }
}

run();
