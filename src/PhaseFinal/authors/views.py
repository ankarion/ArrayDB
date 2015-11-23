from django.http import HttpResponse
from django.template import RequestContext, loader

from .models import Authors
from articles.models import Articles


def index(request, page=0):
    authorList = []
    post = request.POST
    find = post.get('find', '')
    if find:
        authorList = Authors.get(id=find)
        authorList.extend(
            filter(lambda x: x.id not in [j.id for j in authorList], Authors.get(name=find))
        )
        authorList.sort()
        if (authorList) and (page*10 < len(authorList)):
            authorList = authorList[page*10:][:10]
    else:
        authorList = Authors.get()
        authorList.sort()
        if (authorList) and (page*10 < len(authorList)):
            authorList = authorList[page*10:][:10]
    template = loader.get_template('authors/index.html')
    data = RequestContext(
        request,
        {
            'latest_authors_list': authorList,
        }
    )
    return HttpResponse(template.render(data))


def read(request, author_id):
    author = Authors().get(id=author_id)
    template = loader.get_template('authors/read.html')
    articles = Articles().get(author_id=author_id)
    data = RequestContext(
        request,
        {
            'author_list': author,
            'article_list': articles,
        }
    )
    return HttpResponse(template.render(data))
