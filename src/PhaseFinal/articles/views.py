from django.http import HttpResponse
from django.template import RequestContext, loader

from .models import Articles


def index(request, page=0):
    filtered_articles_list = Articles.get(offset=int(page), limit=10)
    template = loader.get_template('articles/index.html')
    data = RequestContext(
        request,
        {
            'latest_articles_list': filtered_articles_list,
        }
    )
    return HttpResponse(template.render(data))


def find(request, find, page=0):
    filtered_articles_list = Articles.get(offset=page, limit=10, id=find.split()[0])
    template = loader.get_template('articles/index.html')
    data = RequestContext(
        request,
        {
            'latest_articles_list': filtered_articles_list,
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


def references(request, article_id):
    article = Articles.get(article_id=article_id)
    template = loader.get_template('articles/read.html')
    data = RequestContext(
        request,
        {
            'article_list': article,
        }
    )
    return HttpResponse(template.render(data))


def update(request, article_id):
    article = Articles.get(id=id)
    if article:
        article = article[0]
        template = loader.get_template('articles/detail.html')
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
    article.title = post.get("title","")
    article.venue = post.get('venue',"")
    article.year = post.get('year',"")
    article.save()
    return index(request)
