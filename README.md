# 🎯 Job Scraper - Automated Job Alerts

A completely **free** Python script that monitors multiple job websites and sends you email notifications when new jobs matching your keywords are found. Runs automatically every 10 minutes using GitHub Actions.

## Features

✅ **Multiple Job Sites**: Indeed, Glassdoor, LinkedIn, GitHub  
✅ **Custom Keywords**: Search for "data engineer", "machine learning", etc.  
✅ **Email Alerts**: Get instant notifications for new jobs  
✅ **100% Free**: Uses GitHub Actions (free tier)  
✅ **No Server Needed**: Runs in the cloud automatically  
✅ **Smart Duplicate Detection**: Won't send duplicate emails  

## Setup Instructions

### Step 1: Clone & Setup Repository

```bash
# Clone this repo
git clone https://github.com/YOUR-USERNAME/job-scraper.git
cd job-scraper

# Install dependencies locally (optional, for testing)
pip install -r requirements.txt
```

### Step 2: Set Up Gmail for Email Sending

Since we're using Gmail for free email sending, you need to create an **App Password**:

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Factor Authentication** if not already enabled
3. Search for "App passwords" (appears when 2FA is on)
4. Select "Mail" and "Windows Computer" (or your device)
5. Google will generate a **16-character password**
6. **Save this password** - you'll need it in Step 3

### Step 3: Configure Your Settings

Edit `config.json`:

```json
{
  "keywords": [
    "data engineer",
    "machine learning engineer",
    "python developer"
  ],
  "websites": [
    "indeed",
    "glassdoor",
    "linkedin"
  ],
  "recipient_email": "your-email@gmail.com",
  "smtp_email": "your-email@gmail.com",
  "smtp_password": "your-16-char-app-password",
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "check_interval_minutes": 10
}
```

**Fields:**
- `keywords`: Job titles to search for
- `websites`: Which sites to scrape (indeed, glassdoor, linkedin)
- `recipient_email`: Your email to receive alerts
- `smtp_email`: Your Gmail address
- `smtp_password`: The 16-char app password from Step 2
- `check_interval_minutes`: How often to run (default: 10 mins)

### Step 4: Set Up GitHub Secrets

**GitHub Actions needs your credentials securely:**

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `CONFIG_JSON`
5. Value: Copy-paste your entire `config.json` file as one line:

```
{"keywords":["data engineer","machine learning engineer"],"websites":["indeed","glassdoor"],"recipient_email":"your-email@gmail.com","smtp_email":"your-email@gmail.com","smtp_password":"your-app-password","smtp_server":"smtp.gmail.com","smtp_port":587,"check_interval_minutes":10}
```

### Step 5: Create GitHub Actions Folder

Create the folder structure if it doesn't exist:

```bash
mkdir -p .github/workflows
mv .github_workflows_job_scraper.yml .github/workflows/job_scraper.yml
```

Or manually create `.github/workflows/job_scraper.yml` with the workflow file content.

### Step 6: Push to GitHub

```bash
git add .
git commit -m "Initial job scraper setup"
git push origin main
```

### Step 7: Enable GitHub Actions

1. Go to your GitHub repo
2. Click **Actions** tab
3. You should see "Job Scraper" workflow
4. Click **Enable workflow**

**Done!** ✅ The scraper will now run every 10 minutes automatically.

## Testing Locally

Before pushing to GitHub, test the script locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the scraper
python job_scraper.py
```

Check `job_scraper.log` for details.

## How It Works

1. **GitHub Actions triggers** the script every 10 minutes
2. **Script scrapes** Indeed, Glassdoor, and other sites
3. **Compares results** against `found_jobs.json` to avoid duplicates
4. **Sends email** with new matching jobs
5. **Updates database** so you don't get duplicate alerts

## Viewing Logs

1. Go to GitHub repo → **Actions** tab
2. Click the latest **Job Scraper** run
3. Click **scrape-jobs** job
4. Scroll to **Run job scraper** step to see output

## Customization

### Add More Keywords
Edit `config.json`:
```json
"keywords": [
  "data engineer",
  "machine learning",
  "software engineer",
  "cloud architect"
]
```

### Change Run Frequency
Edit `.github/workflows/job_scraper.yml`:
```yaml
- cron: '*/30 * * * *'  # Every 30 minutes
- cron: '0 * * * *'     # Every hour
- cron: '0 9 * * MON'   # Every Monday at 9 AM
```

### Add More Job Sites
Edit `config.json` websites array. Script supports:
- `indeed`
- `glassdoor`
- `linkedin`

## Troubleshooting

### "Email failed to send"
- ✅ Check your **16-char app password** is correct
- ✅ Verify **2-Factor Authentication** is enabled
- ✅ Check email address is correct

### "No jobs found"
- ✅ Keywords might be too specific
- ✅ Job sites might be blocking requests (use rotating user agents)
- ✅ Check GitHub Actions logs for errors

### "Duplicate emails"
- ✅ Clear `found_jobs.json` to reset
- ✅ Restart the workflow

## Cost

**100% FREE** 🎉
- GitHub Actions: Free tier includes 2,000 minutes/month
- Email: Free with Gmail
- No hidden costs or paid services needed

## Privacy & Safety

✅ Your credentials are stored as **GitHub Secrets** (encrypted)  
✅ No data is sent to third-party services  
✅ All processing happens in your repo  
✅ You control all settings  

## Advanced: Use Different Email Provider

**Using Outlook:**
```json
{
  "smtp_server": "smtp.office365.com",
  "smtp_port": 587,
  "smtp_email": "your-email@outlook.com"
}
```

**Using SendGrid (free tier):**
```json
{
  "smtp_server": "smtp.sendgrid.net",
  "smtp_port": 587,
  "smtp_email": "apikey",
  "smtp_password": "SG.your-api-key"
}
```

## Contributing

Found a bug? Want to add a job site? Create an issue or PR!

## License

MIT - Free to use and modify

---

**Questions?** Check the logs in GitHub Actions or open an issue!

Happy job hunting! 🚀
