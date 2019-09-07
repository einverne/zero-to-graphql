#!/usr/bin/env python
# -*- coding: utf-8 -*-
import graphene

from people.models import Person


class PersonType(graphene.ObjectType):
    email = graphene.String(description='Like a phone number, but often longer')
    first_name = graphene.String()
    friends = graphene.List(lambda: PersonType, description='Mostly less strange people')
    full_name = graphene.String(description='Pretty much all of your name')
    id = graphene.String()
    last_name = graphene.String()
    username = graphene.String(description='Something you forget often')

    def resolve_friends(self, info, **args):
        return self.friends.all()

    def resolve_full_name(self, info, **args):
        return '{} {}'.format(self.first_name, self.last_name)


class QueryType(graphene.ObjectType):
    all_people = graphene.List(PersonType, description='A few billion people')
    person = graphene.Field(
        PersonType,
        id=graphene.ID(),
        description='Just one person belonging to an ID',
    )

    def resolve_all_people(self, info, **args):
        """
        info holds useful information，For Graphene-Django, info.context attribute is the `HTTPRequest`
        :param info:
        :param args:
        :return:
        """
        if info.context.user.is_authenticated():
            return Person.objects.all()
        else:
            return Person.objects.none()

    def resolve_person(self, info, **args):
        id = args.get('id')
        return Person.objects.get(pk=id)


class Mutation(graphene.ObjectType):
    pass