# 🎯 Complete Setup Guide - Job Scraper

## Overview

This is a **completely FREE** job scraper that:
- ✅ Monitors job websites (Indeed, Glassdoor, LinkedIn)
- ✅ Searches for your keywords (e.g., "data engineer")
- ✅ Runs every 10 minutes automatically (in the cloud)
- ✅ Sends you email notifications for new jobs
- ✅ Uses GitHub Actions (0 cost)
- ✅ No servers or credit cards needed

**Total Setup Time: 10 minutes**

---

## Step 1: Create a GitHub Account (2 minutes)

If you don't have GitHub:
1. Go to [github.com](https://github.com)
2. Click **Sign up**
3. Complete the process

---

## Step 2: Get Gmail App Password (3 minutes)

We'll use Gmail to send you notifications. You need an **App Password**:

### Do This:
1. Open [myaccount.google.com](https://myaccount.google.com)
2. Left sidebar → **Security**
3. Scroll down and enable **2-Step Verification** (if not already enabled)
4. Go back to **Security**
5. Search for **"App passwords"** in the search bar
6. Select:
   - **Mail** from dropdown 1
   - **Windows Computer** (or your device) from dropdown 2
7. Click **Generate**
8. Google shows a 16-character password like: `abcd efgh ijkl mnop`
9. **Copy this password** (you'll need it in Step 4)

### Note:
- This password is ONLY for this app
- It's safe to use here
- Keep it secret like your regular password

---

## Step 3: Create Your Repository on GitHub (3 minutes)

### Do This:
1. Go to [github.com/new](https://github.com/new)
2. **Repository name**: `job-scraper` (or any name you like)
3. **Description**: "Automated job alerts for [your keywords]"
4. Choose **Public** (easier setup) or **Private**
5. ✅ Check "Add a README file"
6. Click **Create repository**

---

## Step 4: Upload Files to Your Repository (2 minutes)

You have 2 options:

### Option A: Simple Upload (Recommended for beginners)

1. Go to your new repository on GitHub
2. Click **Add file** → **Upload files**
3. Download these files from the package:
   ```
   job_scraper.py
   config.json
   requirements.txt
   QUICK_REFERENCE.md
   ```
4. Drag & drop them into GitHub
5. Commit message: "Initial job scraper setup"
6. Click **Commit changes**

### Option B: Git Command Line

```bash
# Clone the repo you just created
git clone https://github.com/YOUR-USERNAME/job-scraper.git
cd job-scraper

# Copy the files from the package here
# Then:
git add .
git commit -m "Initial job scraper setup"
git push origin main
```

---

## Step 5: Create Folders for GitHub Actions (1 minute)

1. In your GitHub repo, click **Add file** → **Create new file**
2. Type in the filename box: `.github/workflows/job_scraper.yml`
3. Copy-paste this content:

```yaml
name: Job Scraper

on:
  schedule:
    - cron: '*/10 * * * *'
  workflow_dispatch:

jobs:
  scrape-jobs:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests beautifulsoup4
    
    - name: Create config file
      env:
        CONFIG_JSON: ${{ secrets.CONFIG_JSON }}
      run: |
        echo "$CONFIG_JSON" > config.json
    
    - name: Run job scraper
      run: python job_scraper.py
    
    - name: Commit changes
      run: |
        git config --global user.email "action@github.com"
        git config --global user.name "GitHub Action"
        git add found_jobs.json
        git commit -m "Update found jobs - $(date)" || echo "No changes to commit"
        git push || echo "Nothing to push"
```

4. Click **Commit changes**

---

## Step 6: Create Your Config File (2 minutes)

1. In your GitHub repo, go to **Settings** → **Secrets and variables** → **Actions**

2. Click **New repository secret**

3. **Name:** `CONFIG_JSON`

4. **Value:** Copy-paste this (replace YOUR VALUES):

```json
{"keywords":["data engineer","machine learning engineer","python developer"],"websites":["indeed","glassdoor"],"recipient_email":"your-email@gmail.com","smtp_email":"your-email@gmail.com","smtp_password":"your-16-char-app-password","smtp_server":"smtp.gmail.com","smtp_port":587,"check_interval_minutes":10}
```

**Replace these:**
- `your-email@gmail.com` → Your actual Gmail address
- `your-16-char-app-password` → The password from Step 2
- `data engineer`, `machine learning engineer` → Your job keywords

5. Click **Add secret**

---

## Step 7: Edit config.json in Your Repo

This is for reference (the actual config is in the Secret):

1. Click on **config.json** in your repo
2. Click the **pencil icon** to edit
3. Update it with your preferences:

```json
{
  "keywords": [
    "data engineer",
    "machine learning engineer",
    "python developer",
    "backend engineer"
  ],
  "websites": [
    "indeed",
    "glassdoor"
  ],
  "recipient_email": "your-email@gmail.com",
  "smtp_email": "your-email@gmail.com",
  "smtp_password": "your-16-char-app-password",
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "check_interval_minutes": 10
}
```

4. Click **Commit changes**

---

## Step 8: Enable GitHub Actions (1 minute)

1. Go to **Actions** tab in your repo
2. On the left, you'll see **All workflows** → Click **Job Scraper**
3. If it says "This workflow has a failed run", click the blue banner → **Enable workflow**
4. You should see "Job Scraper" with a green checkmark

**Done!** ✅ Your scraper will now run automatically every 10 minutes!

---

## Testing It Works

### Option 1: Wait (10 minutes)
The scraper runs every 10 minutes automatically.

### Option 2: Trigger Manually (2 minutes)
1. Go to **Actions** → **Job Scraper**
2. Click **Run workflow** button
3. Click **Run workflow** (green button)
4. Wait 1-2 minutes
5. You should get an email if jobs were found!

### Option 3: Check the Logs
1. **Actions** tab → **Job Scraper** → Latest run
2. Click **scrape-jobs** job
3. Scroll down to see what happened

---

## Understanding Your First Email

You'll get an email like this:

```
🎯 New Job Opportunities Found! (3 jobs)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Senior Data Engineer
Company: Tech Corp
Source: Indeed
Keyword Match: data engineer

[View Job →]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Each job shows:
- **Title**: The job position
- **Company**: Where it's posted
- **Source**: Which website (Indeed, Glassdoor, etc.)
- **Keyword Match**: Which of your keywords it matched
- **View Job**: Click to see the actual job posting

---

## Customizing Your Search

### Change Keywords
Edit `config.json` in your repo → `keywords` array

```json
"keywords": [
  "data engineer",
  "machine learning",
  "AI engineer"
]
```

### Change How Often It Runs
Edit `.github/workflows/job_scraper.yml`:

```yaml
- cron: '*/10 * * * *'  # Every 10 minutes
- cron: '*/30 * * * *'  # Every 30 minutes
- cron: '0 * * * *'     # Every hour
- cron: '0 9 * * MON'   # Every Monday at 9 AM
```

### Only Search Specific Sites
Edit `config.json` → `websites`:

```json
"websites": ["indeed"]  # Only Indeed
"websites": ["indeed", "glassdoor"]  # Indeed + Glassdoor
```

---

## Troubleshooting

### "I haven't received any emails"

**Option 1: No jobs found**
- Keywords might be too specific
- Try broader keywords like "engineer" instead of "senior data engineer"

**Option 2: Email not sending**
- Check the Gmail app password is correct (16 characters, no spaces)
- Verify 2-Step Verification is ON in Google Account
- Check recipient email is spelled correctly

**Check logs:**
1. Go to **Actions** → **Job Scraper** → Latest run
2. Click **scrape-jobs**
3. Scroll to "Run job scraper" section
4. Look for error messages

### "Getting duplicate jobs"

This shouldn't happen, but if it does:
1. Delete `found_jobs.json` from your repo
2. GitHub will recreate it
3. Next run will find "new" jobs again

### "GitHub Actions not running"

1. Check **Actions** tab → **Job Scraper**
2. If workflow is disabled, click it and enable
3. Try clicking **Run workflow** → **Run workflow** manually

---

## Cost Breakdown

| Feature | Cost |
|---------|------|
| GitHub Actions (2,000 min/month) | **FREE** |
| Email sending (Gmail) | **FREE** |
| Job websites (scraping) | **FREE** |
| Hosting | **FREE** |
| **Total** | **$0.00** ✅ |

---

## Advanced: Run Locally Instead

If you want to run this on your own computer:

1. Install Python 3.7+
2. Run in terminal:
   ```bash
   pip install -r requirements.txt
   python3 job_scraper.py
   ```

3. To run every 10 minutes:
   ```bash
   python3 local_scheduler.py
   ```

---

## Security & Privacy

✅ **Your credentials are safe:**
- Stored as GitHub **Secrets** (encrypted)
- Never appear in logs
- Only your GitHub Actions can see them

✅ **No data collection:**
- All processing happens in your repo
- No external services involved
- No analytics

✅ **You control everything:**
- Your keywords
- Your email
- Your frequency
- Your job sites

---

## Next Steps

1. ✅ Complete all 8 steps above
2. ✅ Test manually via Actions tab
3. ✅ Wait for first automated run
4. ✅ Customize keywords as needed
5. ✅ Save this guide for reference

---

## Common Questions

**Q: Will this work forever?**
A: Yes! As long as GitHub Actions is free (it is) and the job sites allow scraping (they do).

**Q: Can I change my keywords later?**
A: Yes! Edit config.json anytime, no restart needed.

**Q: What if a job site blocks me?**
A: Unlikely, but we only check every 10 mins with proper delays. If needed, we can add rotating user agents.

**Q: Can I share my GitHub repo?**
A: Yes, but keep your Secrets private! Don't push the real config.json.

**Q: Can I use this with Outlook instead of Gmail?**
A: Yes! See QUICK_REFERENCE.md for alternative email providers.

---

## Got Stuck?

1. **Check QUICK_REFERENCE.md** - answers common questions
2. **Read job_scraper.log** - shows what went wrong
3. **Check GitHub Actions logs** - detailed error info
4. **Create an issue** on GitHub if you need help

---

## You Did It! 🎉

You now have a **free, automated job scraper** that runs 24/7 in the cloud!

Happy job hunting! 🚀

---

**Version**: 1.0  
**Updated**: 2024  
**Status**: Fully functional and tested ✅
