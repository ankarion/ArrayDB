from authors.models import Authors
from articles.models import Articles
from articles.models import AuthorLists
from articles.models import References

from structure.TablesHandler import TablesHandler


TablesHandler.createTable(Authors)
TablesHandler.createTable(Articles)
TablesHandler.createTable(References)
TablesHandler.createTable(AuthorLists)
