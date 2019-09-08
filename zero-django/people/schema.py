#!/usr/bin/env python
# -*- coding: utf-8 -*-
import graphene
from django.db.models import Q
from graphene import relay
from graphene_django import DjangoConnectionField

from people.models import Person


class PersonType(graphene.ObjectType):
    class Meta:
        description = "用户基本类型"

    email = graphene.String(description='Like a phone number, but often longer')
    first_name = graphene.String()
    friends = graphene.List(lambda: PersonType,
                            first=graphene.Int(),
                            description='Mostly less strange people')
    full_name = graphene.String(description='Pretty much all of your name')
    id = graphene.String()
    last_name = graphene.String()
    username = graphene.String(required=True,description='Something you forget often')

    def resolve_friends(self, info, **args):
        first = args.get("first")
        if first is not None:
            return self.friends.all()[:first]
        else:
            return self.friends.all()

    def resolve_full_name(self, info, **args):
        return '{} {}'.format(self.first_name, self.last_name)


class QueryType(graphene.ObjectType):
    all_people = graphene.List(PersonType,
                               description='A few billion people',
                               query_name=graphene.String(),
                               )
    person = graphene.Field(
        PersonType,
        id=graphene.ID(),
        name=graphene.String(),
        description='Just one person belonging to an ID',
    )


    def resolve_all_people(self, info, **args):
        """
        info holds useful information，For Graphene-Django, info.context attribute is the `HTTPRequest`
        :param info:
        :param args:
        :return:
        """
        query_name = args.get("query_name")
        if info.context.user.is_authenticated():
            ft = (
                Q(username__icontains=query_name)
            )
            return Person.objects.filter(ft)
        else:
            return Person.objects.none()

    def resolve_person(self, info, **args):
        id = args.get('id')
        if id is not None:
            return Person.objects.get(pk=id)

        name = args.get('name')
        if name is not None:
            return Person.objects.get(username=name)
        return None



class Mutation(graphene.ObjectType):
    pass
