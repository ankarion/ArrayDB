import re


def get_data(tagged):
    if len(tagged.split('author')) > 2:
        local = tagged.split('author')
        article = Article()
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
        sql = ''
        if article.year:
            tmp = re.findall('[0-9][0-9][0-9][0-9]', article.year)
        if len(tmp) > 0:
            sql += tmp[0]+', '
        if article.journal:
            tmp = article.journal.split('journal>')
            if len(tmp) > 1:
                tmp = tmp[1][:-2]
                sql += "'" + deApost(tmp) + "', "
            else:
                sql += "'" + ''.join(tmp[0][:-2].split("'")) + "', "
        if article.title:
            tmp = article.title.split('title')
            if len(tmp) > 1:
                sql += '\''+deApost(tmp[1][1:][:-2])+'\' '
            else:
                sql += '\''+deApost(tmp[0][1:][:-2])+'\' '
        sql += ');\n'
        if (sql != 'insert into articles() values ();\n') and ('\\' not in sql):
            return sql
        else:
            return ""

print "opening file..."

output = open("dump.data", "w")
input = open("dblp1.xml", "r")
string = input.read().split('<article')

print "starting parsing..."
result = []
output.write("insert into articles(year,venue,title) values (2010,'Innopolis','Testing')")
for cursor in string:
    article = get_data(cursor)
    if article:
        output.write(',(')
        output.write(article.__str__())
        output.write(')')
        result.append(1)
output.write(';')
print "SQL-scripts generated."
print "Total: %s articles inserts generated" % len(result)
output.close()
print "--fin--"
