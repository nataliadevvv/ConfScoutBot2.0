"""
Enhanced Conference Bot with Web Scraping
Automatically discovers conferences from multiple sources
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from typing import List, Dict, Optional

class ConferenceScraperMixin:
    """Mixin class to add web scraping capabilities to the bot"""
    
    def scrape_confs_tech(self) -> List[Dict]:
        """
        Scrape conferences from confs.tech
        Note: They have an API which would be better to use in production
        """
        conferences = []
        
        try:
            # Confs.tech has a JSON API
            url = "https://confs.tech/conferences.json"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                for conf in data:
                    # Filter for Europe and relevant topics
                    if self._is_relevant_conference(conf):
                        conferences.append({
                            'name': conf.get('name', ''),
                            'url': conf.get('url', ''),
                            'start_date': conf.get('startDate', ''),
                            'end_date': conf.get('endDate', ''),
                            'city': conf.get('city', ''),
                            'country': conf.get('country', ''),
                            'topics': conf.get('topics', []),
                            'source': 'confs.tech'
                        })
        
        except Exception as e:
            print(f"Error scraping confs.tech: {e}")
        
        return conferences
    
    def _is_relevant_conference(self, conf: Dict) -> bool:
        """Check if conference is relevant (Europe, QA/IT topics)"""
        # European countries
        european_countries = [
            'Germany', 'France', 'UK', 'United Kingdom', 'Spain', 'Italy',
            'Netherlands', 'Belgium', 'Poland', 'Sweden', 'Norway', 'Denmark',
            'Finland', 'Austria', 'Switzerland', 'Portugal', 'Czech Republic',
            'Greece', 'Ireland', 'Romania', 'Hungary', 'Croatia', 'Slovenia'
        ]
        
        country = conf.get('country', '')
        if not any(eu_country.lower() in country.lower() for eu_country in european_countries):
            return False
        
        # Relevant topics
        relevant_topics = [
            'testing', 'qa', 'quality', 'software', 'dev', 'tech',
            'agile', 'javascript', 'python', 'java', 'devops',
            'cloud', 'security', 'mobile', 'web', 'data'
        ]
        
        # Check topics
        topics = conf.get('topics', [])
        name = conf.get('name', '').lower()
        
        if topics:
            topic_str = ' '.join(topics).lower()
            if any(topic in topic_str for topic in relevant_topics):
                return True
        
        # Check name
        if any(topic in name for topic in relevant_topics):
            return True
        
        return False
    
    def scrape_eventbrite(self, query: str = "IT conference") -> List[Dict]:
        """
        Scrape Eventbrite for conferences
        Note: Better to use their API with authentication
        """
        conferences = []
        
        try:
            # This is a simplified example - Eventbrite requires API access
            # for proper integration
            url = f"https://www.eventbrite.com/d/europe--berlin/{query.replace(' ', '-')}/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Parse event listings
                # Implementation would depend on Eventbrite's HTML structure
                pass
        
        except Exception as e:
            print(f"Error scraping Eventbrite: {e}")
        
        return conferences
    
    def check_early_bird_status(self, url: str) -> Optional[bool]:
        """
        Check if early bird tickets are available
        This is a basic implementation - would need to be customized per site
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                content = response.text.lower()
                
                # Keywords that indicate early bird availability
                early_bird_keywords = [
                    'early bird',
                    'earlybird',
                    'super early',
                    'early registration',
                    'early rate'
                ]
                
                for keyword in early_bird_keywords:
                    if keyword in content:
                        # Check if it's not expired
                        if 'sold out' not in content and 'expired' not in content:
                            return True
                
                return False
        
        except Exception as e:
            print(f"Error checking early bird status: {e}")
            return None
    
    def discover_new_conferences(self) -> List[Dict]:
        """
        Main method to discover conferences from multiple sources
        """
        all_conferences = []
        
        # Scrape from confs.tech
        print("Scraping confs.tech...")
        confs_tech_conferences = self.scrape_confs_tech()
        all_conferences.extend(confs_tech_conferences)
        
        # Could add more sources here:
        # - Eventbrite API
        # - Meetup API
        # - Specific conference sites
        
        # Deduplicate based on URL
        seen_urls = set()
        unique_conferences = []
        
        for conf in all_conferences:
            url = conf.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                
                # Check early bird status
                if url:
                    early_bird = self.check_early_bird_status(url)
                    if early_bird is not None:
                        conf['early_bird_available'] = early_bird
                
                unique_conferences.append(conf)
        
        return unique_conferences
    
    def get_upcoming_conferences_from_sources(self, months_ahead: int = 3) -> List[Dict]:
        """
        Get conferences happening in the next X months
        """
        conferences = self.discover_new_conferences()
        
        # Filter by date
        cutoff_date = datetime.now()
        end_date = cutoff_date.replace(month=cutoff_date.month + months_ahead)
        
        upcoming = []
        for conf in conferences:
            start_date_str = conf.get('start_date', '')
            if start_date_str:
                try:
                    start_date = datetime.fromisoformat(start_date_str.split('T')[0])
                    if cutoff_date <= start_date <= end_date:
                        upcoming.append(conf)
                except:
                    pass
        
        return sorted(upcoming, key=lambda x: x.get('start_date', ''))


# Example usage as a standalone script
if __name__ == '__main__':
    """
    Test the scraper independently
    """
    
    class TestScraper(ConferenceScraperMixin):
        pass
    
    scraper = TestScraper()
    
    print("Discovering conferences...")
    conferences = scraper.discover_new_conferences()
    
    print(f"\nFound {len(conferences)} conferences:\n")
    
    for i, conf in enumerate(conferences[:10], 1):
        print(f"{i}. {conf['name']}")
        print(f"   📍 {conf.get('city', 'N/A')}, {conf.get('country', 'N/A')}")
        print(f"   📅 {conf.get('start_date', 'N/A')}")
        print(f"   🔗 {conf.get('url', 'N/A')}")
        if conf.get('early_bird_available'):
            print(f"   🎟️ Early Bird Available!")
        print()
