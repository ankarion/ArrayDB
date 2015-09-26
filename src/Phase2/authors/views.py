from django.http import HttpResponse
from django.template import RequestContext, loader

from .models import Authors
from articles.models import Articles


def index(request):
    latest_authors_list = Authors().all()
    template = loader.get_template('authors/index.html')
    data = RequestContext(
        request,
        {
            'latest_authors_list': latest_authors_list,
        }
    )
    return HttpResponse(template.render(data))


def read(request, author_id):
    author = Authors().get(id=author_id)
    template = loader.get_template('authors/read.html')
    articles = Articles().get(author=author_id)
    data = RequestContext(
        request,
        {
            'author_list': author,
            'article_list': articles,
        }
    )
    return HttpResponse(template.render(data))
