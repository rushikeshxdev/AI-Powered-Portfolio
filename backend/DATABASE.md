# Database Setup Guide

This document explains how to set up and manage the PostgreSQL database for the AI Portfolio application.

## Prerequisites

- PostgreSQL 14 or higher installed
- Python 3.11+ with all dependencies from `requirements.txt`

## Database Schema

### chat_messages Table

Stores all chat conversations between users and the AI assistant.

| Column      | Type                      | Constraints | Description                          |
|-------------|---------------------------|-------------|--------------------------------------|
| id          | INTEGER                   | PRIMARY KEY | Auto-incrementing message ID         |
| session_id  | VARCHAR(100)              | NOT NULL    | Groups messages by conversation      |
| role        | VARCHAR(20)               | NOT NULL    | 'user' or 'assistant'                |
| content     | TEXT                      | NOT NULL    | The message content                  |
| timestamp   | TIMESTAMP WITH TIME ZONE  | NOT NULL    | When message was created             |
| ip_address  | VARCHAR(45)               | NULL        | User's IP address for rate limiting  |

### Indexes

- `idx_session_timestamp`: Composite index on (session_id, timestamp) for fast history retrieval
- `idx_timestamp`: Index on timestamp for analytics queries
- `ix_chat_messages_session_id`: Index on session_id for session lookups

## Setup Instructions

### 1. Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE ai_portfolio;

# Create user (optional)
CREATE USER ai_portfolio_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE ai_portfolio TO ai_portfolio_user;

# Exit psql
\q
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update the DATABASE_URL:

```bash
cp .env.example .env
```

Edit `.env`:
```
DATABASE_URL=postgresql+asyncpg://ai_portfolio_user:your_password@localhost:5432/ai_portfolio
```

### 3. Run Migrations

Initialize the database by running migrations:

```bash
python scripts/init_db.py
```

This will:
- Create the `chat_messages` table
- Create all necessary indexes
- Set up the database schema

### 4. Verify Setup

Verify that the database is properly configured:

```bash
python scripts/verify_db.py
```

This will check:
- Database connectivity
- Table existence
- Column structure
- Index creation

## Migration Management

### Create a New Migration

When you need to modify the database schema:

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "description of changes"

# Or create an empty migration
alembic revision -m "description of changes"
```

### Apply Migrations

```bash
# Upgrade to latest version
alembic upgrade head

# Upgrade by one version
alembic upgrade +1

# Upgrade to specific revision
alembic upgrade <revision_id>
```

### Rollback Migrations

```bash
# Downgrade by one version
alembic downgrade -1

# Downgrade to specific revision
alembic downgrade <revision_id>

# Downgrade to base (empty database)
alembic downgrade base
```

### View Migration History

```bash
# Show current version
alembic current

# Show migration history
alembic history

# Show verbose history
alembic history --verbose
```

## Development vs Production

### Development

For local development, you can use a local PostgreSQL instance:

```
DATABASE_URL=postgresql+asyncpg://localhost/ai_portfolio_dev
```

### Production (Railway)

For production deployment on Railway:

1. Create a PostgreSQL database in Railway
2. Railway will provide a DATABASE_URL
3. Add it to your environment variables in Railway dashboard
4. Migrations will run automatically on deployment

## Troubleshooting

### Connection Issues

If you can't connect to the database:

1. Check PostgreSQL is running:
   ```bash
   # Linux/Mac
   sudo systemctl status postgresql
   
   # Mac with Homebrew
   brew services list
   ```

2. Verify connection details:
   ```bash
   psql -U ai_portfolio_user -d ai_portfolio -h localhost
   ```

3. Check firewall settings allow connections on port 5432

### Migration Issues

If migrations fail:

1. Check current migration state:
   ```bash
   alembic current
   ```

2. View migration history:
   ```bash
   alembic history
   ```

3. If stuck, you can manually set the version:
   ```bash
   alembic stamp head
   ```

### Reset Database

To completely reset the database (⚠️ destroys all data):

```bash
# Drop and recreate database
psql -U postgres -c "DROP DATABASE ai_portfolio;"
psql -U postgres -c "CREATE DATABASE ai_portfolio;"

# Run migrations
python scripts/init_db.py
```

## Backup and Restore

### Backup

```bash
# Backup entire database
pg_dump -U ai_portfolio_user ai_portfolio > backup.sql

# Backup with compression
pg_dump -U ai_portfolio_user ai_portfolio | gzip > backup.sql.gz
```

### Restore

```bash
# Restore from backup
psql -U ai_portfolio_user ai_portfolio < backup.sql

# Restore from compressed backup
gunzip -c backup.sql.gz | psql -U ai_portfolio_user ai_portfolio
```

## Performance Monitoring

### Check Index Usage

```sql
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan as index_scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
WHERE tablename = 'chat_messages'
ORDER BY idx_scan DESC;
```

### Check Table Size

```sql
SELECT 
    pg_size_pretty(pg_total_relation_size('chat_messages')) as total_size,
    pg_size_pretty(pg_relation_size('chat_messages')) as table_size,
    pg_size_pretty(pg_total_relation_size('chat_messages') - pg_relation_size('chat_messages')) as indexes_size;
```

### Analyze Query Performance

```sql
EXPLAIN ANALYZE
SELECT * FROM chat_messages 
WHERE session_id = 'test_session' 
ORDER BY timestamp DESC 
LIMIT 50;
```

## Security Best Practices

1. **Never commit .env files** - Use .env.example as template
2. **Use strong passwords** - Generate with `openssl rand -hex 32`
3. **Limit database user permissions** - Grant only necessary privileges
4. **Use SSL in production** - Add `?ssl=require` to DATABASE_URL
5. **Regular backups** - Automate daily backups in production
6. **Monitor access logs** - Review PostgreSQL logs regularly

## Additional Resources

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [asyncpg Documentation](https://magicstack.github.io/asyncpg/)
