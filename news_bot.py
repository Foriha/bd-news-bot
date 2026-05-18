import feedparser, smtplib, os
from email.mime.text import MIMEText
from datetime import date

FEEDS = [
    ("The Daily Star", "https://www.thedailystar.net/rss.xml"),
    ("Prothom Alo", "https://en.prothomalo.com/feed"),
    ("bdnews24", "https://bdnews24.com/feed"),
    ("Dhaka Tribune", "https://www.dhakatribune.com/feed"),
]

def fetch_news():
    body = f"Bangladesh Morning News — {date.today()}\n\n"
    for name, url in FEEDS:
        feed = feedparser.parse(url)
        body += f"{'='*40}\n{name}\n{'='*40}\n"
        for entry in feed.entries[:5]:
            body += f"- {entry.title}\n  {entry.link}\n\n"
    return body

def send_email(body):
    sender = os.environ["EMAIL_ADDRESS"]
    password = os.environ["EMAIL_PASSWORD"]
    recipient = os.environ["RECIPIENT_EMAIL"]
    msg = MIMEText(body)
    msg["Subject"] = f"Bangladesh News — {date.today()}"
    msg["From"] = sender
    msg["To"] = recipient
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)

if __name__ == "__main__":
    news = fetch_news()
    send_email(news)
    print("Done! Email sent.")
