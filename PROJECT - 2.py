import pyshorteners

def shorten_url(long_url):
    s = pyshorteners.Shortener()
    short_url = s.tinyurl.short(long_url)
    return short_url

if __name__ == "__main__":
    long_url = input("Enter the long URL to shorten: ")
    shortened_url = shorten_url(long_url)
    print(f"Shortened URL: {shortened_url}")
