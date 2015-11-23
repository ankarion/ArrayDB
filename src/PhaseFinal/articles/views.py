from django.http import HttpResponse
from django.template import RequestContext, loader

from .models import Articles
from authors.models import Authors
from .models import AuthorLists


def index(request, page=0):
    articleList = []
    post = request.POST
    find = post.get('find', '')
    if find:
        articleList = Articles.get(id=find)
        articleList.extend(
            filter(lambda x: x.id not in [j.id for j in articleList], Articles.get(title=find))
        )
        articleList.sort()
        if (articleList) and (page*10 < len(articleList)):
            articleList = articleList[page*10:][:10]
    else:
        articleList = Articles.get()
        articleList.sort()
        if (articleList) and (page*10 < len(articleList)):
            articleList = articleList[page*10:][:10]
    template = loader.get_template('articles/index.html')
    data = RequestContext(
        request,
        {
            'latest_articles_list': articleList,
        }
    )
    return HttpResponse(template.render(data))


def read(request, article_id):
    article = Articles.get(id=article_id)
    template = loader.get_template('articles/read.html')
    articles = Articles.get(article_id=article_id)
    data = RequestContext(
        request,
        {
            'article_list': article,
            'reference_list': articles,
        }
    )
    return HttpResponse(template.render(data))


def update(request, article_id):
    article = Articles.get(id=article_id)
    if article:
        article = article[0]
        template = loader.get_template('articles/create.html')
        data = RequestContext(
            request,
            {
                'article': article,
                'authors': article.authors(),
            })
        return HttpResponse(template.render(data))
    else:
        return editWindow(request)


def editWindow(request):
    template = loader.get_template('articles/create.html')
    data = RequestContext(request, {})
    return HttpResponse(template.render(data))


def save(request, **kwargs):
    post = request.POST
    article = Articles()
    article.title = post.get("title", "")
    article.venue = post.get('venue', "")
    article.year = post.get('year', "")
    article.save()
    authors = post.get('authors', "")
    if authors:
        newAuthorList = []
        authors = authors.replace('\t', ', ')
        authors = authors.replace('\n', ', ')
        authors = authors.replace(';', ', ')
        newAuthorList.extend(authors.split(', '))
        for author in newAuthorList:
            DBAuthor = Authors.get(name=author)
            if not DBAuthor:
                DBAuthor = Authors()
                DBAuthor.name = author
                DBAuthor.save()
                print DBAuthor.id

            if DBAuthor:
                connect = AuthorLists()
                connect.article_id = article.id
                connect.author_id = DBAuthor.id
    return index(request)
