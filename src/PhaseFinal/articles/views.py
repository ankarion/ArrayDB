from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required

from .models import Articles


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
            articleList[page*10:][:10]
    else:
        articleList = Articles.get(offset=page, limit=10)
        articleList.sort()
        print [x.id for x in articleList]
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


@login_required
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
    article.title = post.get("title", "")
    article.venue = post.get('venue', "")
    article.year = post.get('year', "")
    article.save()
    return index(request)
