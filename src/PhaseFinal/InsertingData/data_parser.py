import re
from authors.models import Authors
from articles.models import Articles as ArticleModel


def get_data(tagged):
    article = Article()
    local = tagged.split('author')
    if len(local) > 2:
        article.key = local[0]
        article.author = local[1]
    local = tagged.split('title')
    if len(local) > 2:
        article.title = local[1]
    local = tagged.split('pages')
    if len(local) > 2:
        article.pages = local[1]
    local = tagged.split('volume')
    if len(local) > 2:
        article.volume = local[1]
    local = tagged.split('year')
    if len(local) > 2:
        article.year = local[1]
    local = tagged.split('number')
    if len(local) > 2:
        article.number = local[1]
    local = tagged.split('journal>')
    if len(local) > 2:
        article.journal = local[1]
    local = tagged.split('url')
    if len(local) > 2:
        article.url = local[1]
    local = tagged.split('ee')
    if len(local) > 2:
        article.ee = local[1]
    return article


def deApost(data):
    return ''.join(data.split("'"))


class Article(object):
    key = ""
    author = ""
    title = ""
    pages = ""
    year = ""
    volume = ""
    journal = ""
    number = ""
    url = ""
    ee = ""

    def __str__(self):
        sql = 'insert into articles(year,venue,title) values('
        if self.year:
            tmp = re.findall('[0-9][0-9][0-9][0-9]', self.year)
            if len(tmp) > 0:
                sql += tmp[0]+', '
        else:
            sql += '1900, '
        if self.journal:
            tmp = self.journal.split('journal>')
            if len(tmp) > 1:
                tmp = tmp[1][:-2]
                sql += "'" + deApost(tmp) + "', "
            else:
                sql += "'" + ''.join(tmp[0][:-2].split("'")) + "', "
        else:
            sql += "'unknown', "
        if self.title:
            tmp = self.title.split('title')
            if len(tmp) > 1:
                sql += '\''+deApost(tmp[1][1:][:-2])+'\' '
            else:
                sql += '\''+deApost(tmp[0][1:][:-2])+'\' '
        else:
            sql += "'unknown'"
        sql += ');\n'
        if (sql != "insert into articles(year,venue,title) values(1900, 'unknown', 'unknown');\n") and ('\\' not in sql):
            return sql
        else:
            return ""

print "opening file..."
with open("InsertingData/dblp1.xml", buffering=200000) as input:
    output = open("dump.data", "w")
    for line in input:
        article = get_data(line)
        if article.__str__():
            if article.author:
                author = Authors().get(name=article.author)
                if author:
                    article.author_id = author.id
                else:
                    author = Authors()
                    author.name = article.author[1:][:-1]
                    author.save()
                    author = Authors().get(name=author.name)[0]
                    article.author = [author.id, ]
                    output.write(article.__str__())
                    for i in article.author:
                        sql = '''
                        insert into authorlists(author_id,article_id) values
                        ({author},{article});
                        '''.format(author=i, article=ArticleModel().get(title=article.title))

#  '''output = open("dump.data", "w")
#  string = input.read().split('<article')
#
#    print "starting parsing..."
#    result = []
#    for cursor in string:
#        article = get_data(cursor)
#        if article:
#            output.write(article.__str__())
#            result.append(1)
#    print "SQL-scripts generated."
#    print "Total: %s articles inserts generated" % len(result)
# '''
output.close()
print "--fin--"
