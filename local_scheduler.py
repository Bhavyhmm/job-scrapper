#!/usr/bin/env python3
"""
Local Job Scraper Scheduler
Runs job_scraper.py every 10 minutes locally (useful for testing or local deployment)
"""

import schedule
import time
import subprocess
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_scraper():
    """Run the job scraper script"""
    logger.info("=" * 60)
    logger.info("🚀 Starting scheduled job scraper run...")
    logger.info("=" * 60)
    
    try:
        result = subprocess.run(['python3', 'job_scraper.py'], 
                              capture_output=True, 
                              text=True,
                              timeout=300)  # 5 minute timeout
        
        if result.returncode == 0:
            logger.info("✅ Scraper completed successfully")
        else:
            logger.error(f"❌ Scraper failed with return code {result.returncode}")
            logger.error(f"Error output: {result.stderr}")
    
    except subprocess.TimeoutExpired:
        logger.error("❌ Scraper timeout (exceeded 5 minutes)")
    except Exception as e:
        logger.error(f"❌ Error running scraper: {e}")


def main():
    """Main scheduler loop"""
    logger.info("=" * 60)
    logger.info("🎯 Job Scraper Scheduler Started")
    logger.info(f"Started at: {datetime.now()}")
    logger.info("Will run every 10 minutes")
    logger.info("=" * 60)
    logger.info("")
    
    # Schedule the job
    schedule.every(10).minutes.do(run_scraper)
    
    # Run the scheduler
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute if a job is pending
    
    except KeyboardInterrupt:
        logger.info("")
        logger.info("=" * 60)
        logger.info("🛑 Scheduler stopped by user")
        logger.info("=" * 60)


if __name__ == '__main__':
    main()
