# Disaster Recovery Plan

This document outlines the procedures for backing up and restoring critical system data (specifically the SQLite database).

## Database Backups

The main SQLite database is stored in the `data/` directory.

A backup script `backend/scripts/backup_db.sh` is provided. This script creates a safe hot backup using the `sqlite3 .backup` command and rotates old backups, keeping the last 7 copies.

### Running Backups Manually

From the root repository directory, run:

```bash
make db-backup
```
*Note: Ensure `sqlite3` is installed on your system for safe hot backups. If not, it falls back to a standard file copy.*

### Automated Backups

To automate backups, add a cron job on your server to run this daily. Open crontab with `crontab -e`:

```cron
# Run backup at 2:00 AM every day
0 2 * * * cd /path/to/repo && make db-backup >> data/backups/backup.log 2>&1
```

## Database Restoration

If the main database gets corrupted or lost, you can restore from a backup:

1. Stop all bot services (to prevent concurrent writes):
   ```bash
   make stop
   ```

2. Locate the most recent good backup in `data/backups/`.

3. Copy the backup file over the active database file:
   ```bash
   cp data/backups/trading_bot_YYYYMMDD_HHMMSS.db data/trading_bot.db
   ```

4. Restart the bot services:
   ```bash
   make start
   ```

5. Verify logs and check the UI to confirm trades/positions history is intact.
