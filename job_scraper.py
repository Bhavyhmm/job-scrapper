import requests
from bs4 import BeautifulSoup
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('job_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class JobScraper:
    def __init__(self, config_file='config.json'):
        self.config = self.load_config(config_file)
        self.jobs_db_file = 'found_jobs.json'
        self.found_jobs = self.load_found_jobs()
        
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Config file '{config_file}' not found")
            return {}
    
    def load_found_jobs(self):
        """Load previously found jobs to avoid duplicates"""
        if os.path.exists(self.jobs_db_file):
            try:
                with open(self.jobs_db_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_found_jobs(self):
        """Save found jobs to avoid sending duplicate emails"""
        with open(self.jobs_db_file, 'w') as f:
            json.dump(self.found_jobs, f, indent=2)
    
    def search_linkedin(self, keywords):
        """Search LinkedIn jobs (using Google search as LinkedIn blocks bots)"""
        jobs = []
        for keyword in keywords:
            try:
                # Using Google search to find LinkedIn jobs
                search_query = f"site:linkedin.com/jobs {keyword}"
                url = f"https://www.google.com/search?q={search_query}&num=10"
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = requests.get(url, headers=headers, timeout=10)
                logger.info(f"LinkedIn search for '{keyword}' - Status: {response.status_code}")
                
            except Exception as e:
                logger.warning(f"Error searching LinkedIn for '{keyword}': {e}")
        
        return jobs
    
    def search_indeed(self, keywords):
        """Scrape Indeed.com for jobs"""
        jobs = []
        
        for keyword in keywords:
            try:
                url = f"https://www.indeed.com/jobs?q={keyword}&sort=date"
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = requests.get(url, headers=headers, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                job_cards = soup.find_all('div', class_='job_seen_beacon')
                
                for card in job_cards[:10]:  # Get top 10
                    try:
                        title = card.find('h2', class_='jobTitle').text.strip()
                        company = card.find('span', class_='companyName')
                        company_name = company.text.strip() if company else "Unknown"
                        
                        link = card.find('a', class_='jcs-JobTitle')
                        job_url = link.get('href', '') if link else ""
                        
                        job_id = f"indeed_{keyword}_{title}_{company_name}"
                        
                        job = {
                            'title': title,
                            'company': company_name,
                            'url': f"https://www.indeed.com{job_url}" if job_url else "",
                            'source': 'Indeed',
                            'keyword': keyword,
                            'found_at': datetime.now().isoformat(),
                            'id': job_id
                        }
                        
                        if job_id not in self.found_jobs:
                            jobs.append(job)
                            self.found_jobs[job_id] = True
                        
                    except Exception as e:
                        logger.debug(f"Error parsing Indeed job card: {e}")
                
                logger.info(f"Found {len([j for j in jobs if j.get('keyword') == keyword])} jobs on Indeed for '{keyword}'")
                
            except Exception as e:
                logger.warning(f"Error scraping Indeed for '{keyword}': {e}")
        
        return jobs
    
    def search_glassdoor(self, keywords):
        """Scrape Glassdoor for jobs"""
        jobs = []
        
        for keyword in keywords:
            try:
                url = f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={keyword}"
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = requests.get(url, headers=headers, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                job_cards = soup.find_all('div', {'data-test': 'JobCard'})
                
                for card in job_cards[:10]:
                    try:
                        title_elem = card.find('a', {'data-test': 'job-title'})
                        company_elem = card.find('a', {'data-test': 'employer-name'})
                        
                        if not title_elem or not company_elem:
                            continue
                        
                        title = title_elem.text.strip()
                        company = company_elem.text.strip()
                        job_url = title_elem.get('href', '')
                        
                        job_id = f"glassdoor_{keyword}_{title}_{company}"
                        
                        job = {
                            'title': title,
                            'company': company,
                            'url': f"https://www.glassdoor.com{job_url}" if job_url else "",
                            'source': 'Glassdoor',
                            'keyword': keyword,
                            'found_at': datetime.now().isoformat(),
                            'id': job_id
                        }
                        
                        if job_id not in self.found_jobs:
                            jobs.append(job)
                            self.found_jobs[job_id] = True
                        
                    except Exception as e:
                        logger.debug(f"Error parsing Glassdoor job card: {e}")
                
                logger.info(f"Found {len([j for j in jobs if j.get('keyword') == keyword])} jobs on Glassdoor for '{keyword}'")
                
            except Exception as e:
                logger.warning(f"Error scraping Glassdoor for '{keyword}': {e}")
        
        return jobs
    
    def search_github_jobs(self, keywords):
        """Search GitHub Jobs (now part of LinkedIn)"""
        jobs = []
        # GitHub Jobs is deprecated, but we can try to get some results
        for keyword in keywords:
            try:
                url = f"https://api.github.com/search/repositories?q={keyword}+language:python&sort=stars"
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(url, headers=headers, timeout=10)
                logger.info(f"GitHub search for '{keyword}' - Status: {response.status_code}")
            except Exception as e:
                logger.warning(f"Error searching GitHub for '{keyword}': {e}")
        
        return jobs
    
    def send_email(self, jobs, recipient_email):
        """Send email with found jobs"""
        if not jobs:
            return
        
        try:
            sender_email = self.config.get('smtp_email')
            sender_password = self.config.get('smtp_password')
            smtp_server = self.config.get('smtp_server', 'smtp.gmail.com')
            smtp_port = self.config.get('smtp_port', 587)
            
            if not sender_email or not sender_password:
                logger.error("SMTP credentials not configured")
                return
            
            # Create email
            msg = MIMEMultipart('html')
            msg['Subject'] = f"🎯 New Job Opportunities Found! ({len(jobs)} jobs)"
            msg['From'] = sender_email
            msg['To'] = recipient_email
            
            # Create HTML body
            html_body = """
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <h2 style="color: #2c3e50;">🎯 New Job Opportunities Found!</h2>
                    <p>Hello,</p>
                    <p>We found <strong>{}</strong> new job(s) matching your keywords:</p>
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                    {}
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                    <p style="font-size: 12px; color: #7f8c8d;">
                        This is an automated message from your Job Scraper.<br>
                        Check time: {}
                    </p>
                </body>
            </html>
            """
            
            jobs_html = ""
            for job in jobs:
                jobs_html += f"""
                <div style="background: #f8f9fa; padding: 15px; margin: 10px 0; border-left: 4px solid #3498db; border-radius: 4px;">
                    <h3 style="margin-top: 0; color: #2c3e50;">{job['title']}</h3>
                    <p style="margin: 5px 0;"><strong>Company:</strong> {job['company']}</p>
                    <p style="margin: 5px 0;"><strong>Source:</strong> {job['source']}</p>
                    <p style="margin: 5px 0;"><strong>Keyword Match:</strong> {job['keyword']}</p>
                    <p style="margin: 5px 0;">
                        <a href="{job['url']}" style="color: #3498db; text-decoration: none; font-weight: bold;">
                            View Job →
                        </a>
                    </p>
                </div>
                """
            
            html_content = html_body.format(len(jobs), jobs_html, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            msg.attach(MIMEText(html_content, 'html'))
            
            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {recipient_email} with {len(jobs)} job(s)")
            
        except Exception as e:
            logger.error(f"Error sending email: {e}")
    
    def run(self):
        """Run the scraper"""
        logger.info("=" * 50)
        logger.info("Starting Job Scraper")
        logger.info("=" * 50)
        
        keywords = self.config.get('keywords', ['data engineer', 'software engineer'])
        recipient_email = self.config.get('recipient_email')
        websites = self.config.get('websites', ['indeed', 'glassdoor'])
        
        if not recipient_email:
            logger.error("Recipient email not configured")
            return
        
        all_jobs = []
        
        # Scrape different websites
        if 'indeed' in websites:
            logger.info("Scraping Indeed...")
            all_jobs.extend(self.search_indeed(keywords))
            time.sleep(2)  # Be respectful to servers
        
        if 'glassdoor' in websites:
            logger.info("Scraping Glassdoor...")
            all_jobs.extend(self.search_glassdoor(keywords))
            time.sleep(2)
        
        if 'linkedin' in websites:
            logger.info("Scraping LinkedIn...")
            all_jobs.extend(self.search_linkedin(keywords))
            time.sleep(2)
        
        if 'github' in websites:
            logger.info("Scraping GitHub...")
            all_jobs.extend(self.search_github_jobs(keywords))
        
        # Save found jobs
        self.save_found_jobs()
        
        # Send email if new jobs found
        if all_jobs:
            logger.info(f"Found {len(all_jobs)} new job(s). Sending email...")
            self.send_email(all_jobs, recipient_email)
        else:
            logger.info("No new jobs found")
        
        logger.info("=" * 50)


if __name__ == '__main__':
    scraper = JobScraper()
    scraper.run()
