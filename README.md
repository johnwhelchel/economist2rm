### _This code is not tested and is for my personal use, leverage at your own risk_

I use this small repo and a launchd script to scrape The Economist every Friday and load it on to my Remarkable.

# Overall setup
- Uses `economist2rm` python virtualenv
- Runs against `~/Library/LaunchAgents/com.johnwhelchel.economist2rm.plist`
- main.py is executed every Friday at 6 PM
- Logs are in `~/Library/Logs/economist2rm`, can view in `Console.app`
- Work is in `economist2rm` Asana project
- Can test/run/debug parts of pipeline using scripts, and `scrapy crawl Economist` in `./scraping`
    - The scraper was created with the default project format, so many default unused files there
