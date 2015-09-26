from django.http import HttpResponse
from django.template import RequestContext, loader

from .models import Articles


def index(request):
    latest_articles_list = Articles().all()
    template = loader.get_template('articles/index.html')
    data = RequestContext(
        request,
        {
            'latest_articles_list': latest_articles_list,
        }
    )
    return HttpResponse(template.render(data))


def read(request, article_id):
    article = Articles().get(id=article_id)
    template = loader.get_template('articles/read.html')
    articles = Articles().get(article=article_id)
    data = RequestContext(
        request,
        {
            'article_list': article,
            'reference_list': articles,
        }
    )
    return HttpResponse(template.render(data))


def references(request, article_id):
    article = Articles().get(article=article_id)
    template = loader.get_template('articles/read.html')
    data = RequestContext(
        request,
        {
            'article_list': article,
        }
    )
    return HttpResponse(template.render(data))
