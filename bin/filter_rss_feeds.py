import requests
import xml.etree.ElementTree as ET
import json

ocva_sources_1 = [
        'https://www.psychology.org/feed/',
        'https://www.psychologicalscience.org/feed',
        "https://www.naturalchef.com/feed/",
        "http://hellohealthyeating.com/feed/",
        "https://www.superhealthykids.com/feed/",
        "https://www.ayurveda.com/feed",
        "http://www.loveandlemons.com/feed/",
        "https://kelliesfoodtoglow.com/feed/",
        "https://healthynibblesandbits.com/feed/",
        "https://chocolatecoveredkatie.com/feed/",
        "https://vegbuffet.com/feed/",
        "http://www.acouplecooks.com/feed/",
        "http://onehandedcooks.com.au/feed/",
        "https://www.psychology.org/feed/",
        "https://foodwithfeeling.com/feed/",
        "http://feeds.feedburner.com/FeedMePhoebe",
        "http://feeds.feedburner.com/iowagirleats",
        "http://feeds.feedburner.com/TheHealthyMaven",
        "https://snapkitchen.wpengine.com/feed/",
        "https://cleancookingcaitlin.com/feed/",
        "https://www.twopurplefigs.com/feed/",
        "http://feeds.feedburner.com/blogspot/OOXhN",
        "http://feeds.feedburner.com/ThePickyEaterBlog",
        "https://healthykitch.blogspot.com/feeds/posts/default?alt=rss",
        "https://www.healthyseasonalrecipes.com/feed/",
        "https://www.healthygrocerygirl.com/feed/",
        "https://greenkitchenstories.com/feed/",
        "https://www.joyfulhealthyeats.com/feed/",
        "https://www.melskitchencafe.com/feed/",
        "https://www.myfussyeater.com/feed/",
        "https://ayurmantra.com/feed/",
        "https://lexiscleankitchen.com/feed/",
        "http://feeds.feedburner.com/JeanettesHealthyLiving",
        "https://www.skinnykitchen.com/feed/",
        "https://www.ayurvedsutra.com/ayurveda-news/feed",
        "https://busybuthealthy.com/feed/",
        "https://www.ambitiouskitchen.com/feed/",
        "https://www.andarikiayurvedamonline.in/blog/feed/",
        "https://www.yummyhealthyeasy.com/feed/",
        "https://www.skinnytaste.com/feed/",
        "https://www.foodfaithfitness.com/feed/",
        "https://www.eatyourselfskinny.com/feed/",
        "https://pieceoflulu.com/feed/",
        "https://happyfoodhealthylife.com/feed/",
        "https://fitmencook.com/feed/",
        "https://junkfoodkids.com/feed/",
        "https://www.sciencedaily.com/rss/top/health.xml",
        "http://www.eatsamazing.co.uk/feed",
        "http://feeds.feedburner.com/HealthfoodDesivideshi",
        "http://www.inspiralized.com/feed",
        "https://www.spamellab.com/feed/",
        "https://healthyslowcooking.com/feed/",
        "https://changinghabits.com.au/feed/",
        "http://feeds.feedburner.com/aggieskitchen/snNz",
        "https://plantbasedonabudget.com/feed/",
        "https://20micronsherbal.com/feed/",
        "https://www.fannetasticfood.com/feed/",
        "https://www.makingthymeforhealth.com/feed/",
        "https://nadiashealthykitchen.com/feed/",
        "https://www.realfoodhealthybody.com/feed/",
        "https://thelemonbowl.com/feed/",
        "https://www.deliciousmeetshealthy.com/feed/",
        "https://foodheavenmadeeasy.com/feed/",
        "https://the-fit-foodie.com/feed/",
        "https://www.alittlenutrition.com/feed/",
        "https://lemonsandbasil.com/feed/",
        "https://jessicasepel.com/feed/",
        "https://thehealthyfoodie.com/feed/",
        "https://fitfoodiefinds.com/feed/",
        "https://www.healthshots.com/rss-feeds/healthy-eating/",
        "https://www.healthshots.com/rss-feeds/superfoods/",
    ]


# List of RSS feed URLs to test
rss_feed_urls_0 = [
    'https://www.psychology.org/feed/',  # Psychology.org
    'https://20micronsherbal.com/feed/',
    'https://www.sciencedaily.com/rss/top/health.xml',
    'https://www.andarikiayurvedamonline.in/blog/feed/',
    'https://ayurmantra.com/feed/',
    'https://www.ayurveda.com/feed',
    'https://www.ayurvedsutra.com/ayurveda-news/feed',
    "http://www.acouplecooks.com/feed/",
    "https://www.alittlenutrition.com/feed/",
    "http://feeds.feedburner.com/aggieskitchen/snNz",
    "https://www.ambitiouskitchen.com/feed/",
    "https://busybuthealthy.com/feed/",
    "https://changinghabits.com.au/feed/",
    "https://chocolatecoveredkatie.com/feed/",
    "https://cleancookingcaitlin.com/feed/",
    "https://www.naturalchef.com/feed/",
    "https://cooktoria.com/feed/",
    "https://www.deliciousmeetshealthy.com/feed/",
    "https://dwardcooks.com/feed/",
    "https://www.eatyourselfskinny.com/feed/",
    "http://www.eatsamazing.co.uk/feed",
    "https://www.fannetasticfood.com/feed/",
    "http://feeds.feedburner.com/FeedMePhoebe",
    "https://fitfoodiefinds.com/feed/",
    "https://fitmencook.com/feed/",
    "https://www.foodfaithfitness.com/feed/",
    "https://foodheavenmadeeasy.com/feed/",
    "https://kelliesfoodtoglow.com/feed/",
    "https://foodwithfeeling.com/feed/",
    "https://greenkitchenstories.com/feed/",
    "https://happyfoodhealthylife.com/feed/",
    "http://feeds.feedburner.com/HealthfoodDesivideshi",
    "http://feeds.feedburner.com/blogspot/OOXhN",
    "https://www.healthygrocerygirl.com/feed/",
    "https://healthykitch.blogspot.com/feeds/posts/default?alt=rss",
    "https://healthynibblesandbits.com/feed/",
    "https://www.healthyseasonalrecipes.com/feed/",
    "https://healthyslowcooking.com/feed/",
    "http://hellohealthyeating.com/feed/",
    "http://www.inspiralized.com/feed",
    "http://feeds.feedburner.com/iowagirleats",
    "http://feeds.feedburner.com/JeanettesHealthyLiving",
    "https://www.joyfulhealthyeats.com/feed/",
    "https://jessicasepel.com/feed/",
    "https://junkfoodkids.com/feed/",
    "https://lemonsandbasil.com/feed/",
    "https://lexiscleankitchen.com/feed/",
    "https://www.lizshealthytable.com/feed/",
    "http://www.loveandlemons.com/feed/",
    "https://www.makingthymeforhealth.com/feed/",
    "https://maryannjacobsen.com/feed/",
    "https://www.melskitchencafe.com/feed/",
    "https://www.myfussyeater.com/feed/",
    "https://nadiashealthykitchen.com/feed/",
    "https://onceafoodie.com/feed/",
    "http://onehandedcooks.com.au/feed/",
    "https://pieceoflulu.com/feed/",
    "https://plantbasedonabudget.com/feed/",
    "https://www.realfoodhealthybody.com/feed/",
    "https://www.skinnykitchen.com/feed/",
    "https://www.skinnytaste.com/feed/",
    "https://snapkitchen.wpengine.com/feed/",
    "https://www.spamellab.com/feed/",
    "https://www.superhealthykids.com/feed/",
    "https://the-fit-foodie.com/feed/",
    "https://thehealthyfoodie.com/feed/",
    "http://feeds.feedburner.com/TheHealthyMaven",
    "https://thelemonbowl.com/feed/",
    "https://littlegreenspoon.ie/feed/",
    "http://feeds.feedburner.com/ThePickyEaterBlog",
    "https://www.twopurplefigs.com/feed/",
    "https://vegbuffet.com/feed/",
    "https://www.yummyhealthyeasy.com/feed/"
]

def is_valid_rss(url):
    """Checks if the given URL returns valid RSS or Atom XML."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/58.0.3029.110 Safari/537.3"
        ),
        "Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8",
    }
    try:
        response = requests.get(url, headers=headers, timeout=20, allow_redirects=True)
        response.raise_for_status()
        # Parse XML to check if it's valid RSS or Atom feed
        root = ET.fromstring(response.content)
        # Common root tags for RSS and Atom
        if root.tag.lower() == 'rss' or 'feed' in root.tag.lower():
            print(f"Valid RSS/Atom feed for URL: {url}")
            return True
        else:
            print(f"Invalid RSS/Atom feed structure for URL: {url}")
            return False
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error validating URL: {url}, Error: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error validating URL: {url}, Error: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error validating URL: {url}, Error: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request exception validating URL: {url}, Error: {req_err}")
    except ET.ParseError as parse_err:
        print(f"XML parse error for URL: {url}, Error: {parse_err}")
    except Exception as e:
        print(f"Unexpected error validating URL: {url}, Error: {e}")
    return False

def remove_duplicates(urls):
    """Removes duplicate URLs from the list."""
    return list(set(urls))

def save_to_json(data, file_name):
    """Saves the given data to a JSON file."""
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def main():
    print("Testing RSS feed URLs...")

    # Validate URLs
    valid_rss_urls = [url for url in ocva_sources_1 if is_valid_rss(url)]

    # Remove duplicates
    unique_valid_rss_urls = remove_duplicates(valid_rss_urls)

    print(f"Valid RSS feeds ({len(unique_valid_rss_urls)}):", unique_valid_rss_urls)

    # Save the results to a JSON file
    save_to_json(unique_valid_rss_urls, "valid_ocva_rss_feeds.json")
    print("Valid RSS feed URLs saved to valid_rss_feeds.json")

if __name__ == "__main__":
    main()