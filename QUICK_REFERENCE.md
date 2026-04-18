# 🚀 Job Scraper - Quick Reference

## 📋 Files Explained

```
job-scraper/
├── job_scraper.py          # Main scraper script
├── local_scheduler.py      # Optional: Run locally with scheduling
├── config.json             # Your configuration (DON'T COMMIT)
├── found_jobs.json         # Database of found jobs (auto-managed)
├── requirements.txt        # Python dependencies
├── setup.sh               # Quick setup script
├── README.md              # Full documentation
├── .gitignore             # What to not commit to GitHub
├── .github/
│   └── workflows/
│       └── job_scraper.yml # GitHub Actions automation
└── job_scraper.log        # Logs from runs
```

## 🔧 Common Tasks

### Change Keywords
Edit `config.json`:
```json
"keywords": ["data engineer", "machine learning engineer"]
```

### Change Run Frequency (GitHub Actions)
Edit `.github/workflows/job_scraper.yml`:
```yaml
- cron: '*/15 * * * *'  # Every 15 minutes
- cron: '0 * * * *'     # Every hour
```

### Run Locally (for testing)
```bash
python3 job_scraper.py
```

### Run Locally with Auto-Scheduling
```bash
python3 local_scheduler.py
```

### Check GitHub Actions Logs
1. Go to your repo → Actions tab
2. Click latest "Job Scraper" run
3. Click "scrape-jobs" job
4. Scroll down to "Run job scraper"

### Reset Found Jobs (to get duplicate notifications)
Delete `found_jobs.json` and push to GitHub:
```bash
rm found_jobs.json
git add found_jobs.json
git commit -m "Reset found jobs"
git push
```

### Disable Automatic Runs
1. Go to repo → Actions → Job Scraper
2. Click menu → "Disable workflow"

## 🔐 Gmail App Password Setup (Full Steps)

1. Open [Google Account](https://myaccount.google.com)
2. Left sidebar → Security
3. Enable 2-Step Verification (if not done)
4. Search bar → "App passwords"
5. Select "Mail" → "Windows Computer" (or your device)
6. Google shows 16-char password → Copy it
7. Paste into config.json as `smtp_password`

## 🐛 Troubleshooting

### "Email sending failed"
```
✅ Check Gmail app password (16 characters)
✅ Verify 2-Step Verification is ON
✅ Check recipient_email matches smtp_email
✅ Check smtp_server is "smtp.gmail.com"
```

### "No jobs found but I expected results"
```
✅ Check keywords in config.json
✅ Try running locally: python3 job_scraper.py
✅ Check job_scraper.log for errors
✅ Websites might have changed structure
```

### "GitHub Actions won't run"
```
✅ Go to Actions → Job Scraper → Enable workflow
✅ Check CONFIG_JSON secret exists
✅ Verify secret value is valid JSON
✅ Try manual trigger: Actions → Job Scraper → Run workflow
```

### "Getting duplicate emails"
```
✅ Check found_jobs.json exists in repo
✅ If jobs repeat, delete found_jobs.json
✅ Ensure git is configured: git config user.email/user.name
```

## 📊 How to Understand the Email

You'll receive emails like:

```
🎯 New Job Opportunities Found! (3 jobs)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 Data Engineer
Company: Tech Corp
Source: Indeed
Keyword Match: data engineer

[View Job →]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Check time: 2024-01-15 10:30:45
```

## 🎯 Config.json Reference

```json
{
  "keywords": ["job title 1", "job title 2"],  // What to search for
  "websites": ["indeed", "glassdoor"],         // Which sites
  "recipient_email": "you@gmail.com",          // Where to send alerts
  "smtp_email": "you@gmail.com",               // Gmail to send FROM
  "smtp_password": "16-char-app-password",     // Gmail app password
  "smtp_server": "smtp.gmail.com",             // Don't change for Gmail
  "smtp_port": 587,                            // Don't change for Gmail
  "check_interval_minutes": 10                 // How often (info only)
}
```

## 💡 Pro Tips

### 1. Multiple Recipients (Advanced)
Currently sends to one email. To send to multiple:
- Add to your Gmail filters to forward
- OR modify job_scraper.py line 195 to send to multiple emails

### 2. Filter by Location
Add location to keywords:
```json
"keywords": ["data engineer Toronto", "ML engineer Canada"]
```

### 3. Use Gmail Labels for Auto-Sorting
Create Gmail rule:
- From: your-email@gmail.com
- Label: "Job Alerts"
- Auto-archive if desired

### 4. Disable Notifications for Specific Job Sites
Remove from config.json websites array:
```json
"websites": ["indeed"]  // Only Indeed
```

## 📱 Alternative Email Providers

### Outlook
```json
{
  "smtp_server": "smtp.office365.com",
  "smtp_email": "your@outlook.com",
  "smtp_password": "your-password"
}
```

### Yahoo Mail
```json
{
  "smtp_server": "smtp.mail.yahoo.com",
  "smtp_email": "your@yahoo.com",
  "smtp_password": "your-app-password"
}
```

## 🚀 Next Steps

1. ✅ Set up config.json with your keywords
2. ✅ Get Gmail app password
3. ✅ Test locally: `python3 job_scraper.py`
4. ✅ Push to GitHub
5. ✅ Add CONFIG_JSON secret
6. ✅ Enable workflow in Actions tab
7. 🎉 Start getting job alerts!

---

**Need help?** Check README.md or create an issue on GitHub!
