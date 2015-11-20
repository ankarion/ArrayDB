from articles.models import Articles


articles = Articles.get(id="1")
for article in articles:
    s = ""
    for i in article.__fields__:
        s += article.__getattribute__(i)
        s += " "
    print s
