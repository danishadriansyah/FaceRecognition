# Backups Directory

Automatic backups of dataset and attendance records.

## Backup Contents

Each backup includes:
- **dataset/** - All person data (photos, encodings, metadata)
- **logs/attendance.csv** - Attendance records
- **config.json** - System configuration

## Backup Format

```
backup_YYYYMMDD_HHMMSS/
├── dataset/
│   ├── encodings.pkl
│   ├── metadata.json
│   └── [Person Folders]/
├── attendance.csv
└── config.json
```

## Automatic Backups

**Schedule:**
- Daily at midnight (if auto-backup enabled)
- Before major operations (delete person, bulk updates)
- Manual: Settings → Backup → Create Backup

**Retention:**
- Default: Keep last 30 days
- Configurable in settings
- Old backups auto-deleted

## Restore Backup

**Via GUI:**
1. Settings → Backup → Restore
2. Select backup folder
3. Confirm restoration
4. Application restarts

**Manual Restore:**
```bash
# 1. Close application
# 2. Copy backup files
copy backups\backup_20251220_120000\dataset\* dataset\
copy backups\backup_20251220_120000\attendance.csv logs\
# 3. Restart application
```

## Best Practices

✅ **Regular backups** before major changes
✅ **Test restore** periodically
✅ **External backup** for critical data
✅ **Keep old backups** for compliance

⚠️ **Never delete backups** while app is running
⚠️ **Verify backup** before major operations

## Size Management

**Typical Sizes:**
- Small (1-10 persons): 10-100 MB
- Medium (10-50 persons): 100-500 MB
- Large (50-100 persons): 500 MB - 1 GB

**Cleanup:**
- Delete old backups manually
- Adjust retention days in settings
- Archive to external drive for long-term storage

---

**Week 8 - Final Project**
