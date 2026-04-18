#!/bin/bash

# Job Scraper Quick Setup Script

echo "================================"
echo "🎯 Job Scraper Setup"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Create directories
echo "📁 Creating folder structure..."
mkdir -p .github/workflows
echo "✅ Folders created"
echo ""

# Copy workflow file
echo "⚙️  Setting up GitHub Actions workflow..."
if [ -f ".github_workflows_job_scraper.yml" ]; then
    mv .github_workflows_job_scraper.yml .github/workflows/job_scraper.yml
    echo "✅ Workflow file placed in .github/workflows/"
fi
echo ""

echo "================================"
echo "✅ Setup Complete!"
echo "================================"
echo ""
echo "📋 Next steps:"
echo ""
echo "1️⃣  Edit config.json with your settings:"
echo "   - Add your keywords"
echo "   - Set your recipient email"
echo "   - Add your Gmail app password"
echo ""
echo "2️⃣  Test locally (optional):"
echo "   python3 job_scraper.py"
echo ""
echo "3️⃣  Push to GitHub:"
echo "   git add ."
echo "   git commit -m 'Initial job scraper setup'"
echo "   git push origin main"
echo ""
echo "4️⃣  Set GitHub Secret (CONFIG_JSON):"
echo "   - Go to repo Settings → Secrets and variables → Actions"
echo "   - Create new secret: CONFIG_JSON"
echo "   - Paste your config.json contents"
echo ""
echo "5️⃣  Enable GitHub Actions:"
echo "   - Go to Actions tab → Job Scraper workflow → Enable"
echo ""
echo "🎉 Done! Your scraper will run every 10 minutes."
echo ""
echo "📖 Full guide in README.md"
echo ""
