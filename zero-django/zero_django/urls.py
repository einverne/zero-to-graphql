from django.conf.urls import url, include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView


from .schema import schema

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^graphiql', include('django_graphiql.urls')),
    url(r'^graphiqlv2', GraphQLView.as_view(graphiql=True)),
    url(r'^graphql', csrf_exempt(GraphQLView.as_view(schema=schema))),
    url(r'^', include('people.urls')),
]
