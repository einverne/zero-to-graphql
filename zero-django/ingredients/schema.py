#!/usr/bin/env python
# -*- coding: utf-8 -*-

import graphene
from graphene import relay
from graphene_django import DjangoConnectionField

from graphene_django.types import DjangoObjectType

from ingredients.models import Category, Ingredient

from utils.connection import CountableConnectionBase


class CategoryType(DjangoObjectType):
    """
    DjangoObjectType will present all fields on a Model through GraphQL
    """
    class Meta:
        model = Category
        # fields = ('',)
        # exclude = ('',)
        filter_fields = {
            'name': ['exact', 'icontains'],
            'ingredients': ['exact']}
        interfaces = (relay.Node, )
        connection_class = CountableConnectionBase


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'notes': ['exact', 'icontains'],
            'category': ['exact'],
            'category__name': ['exact'],
        }
        interfaces = (relay.Node,)
        connection_class = CountableConnectionBase


class Query(graphene.ObjectType):
    # all_categories = graphene.List(CategoryType)
    # all_ingredients = graphene.List(IngredientType)

    # category = relay.Node.Field(CategoryType)
    # ingredient = relay.Node.Field(IngredientType)

    all_categories = DjangoConnectionField(CategoryType)
    all_ingredients = DjangoConnectionField(IngredientType)
    category = graphene.Field(CategoryType,
                              id=graphene.Int(),
                              name=graphene.String())
    ingredient = graphene.Field(IngredientType,
                                id=graphene.Int(),
                                name=graphene.String())

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_all_ingredients(self, info, **kwargs):
        return Ingredient.objects.select_related('category').all()

    def resolve_category(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Category.objects.get(pk=id)

        if name is not None:
            return Category.objects.get(name=name)

        return None

    def resolve_ingredient(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Ingredient.objects.get(pk=id)

        if name is not None:
            return Ingredient.objects.get(name=name)

        return None


class CreateCategory(graphene.Mutation):
    """
mutation createCategory {
 	createCategory(name: "Milk") {
  	category {
      id
      name
    }
  }
}
    """
    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    def mutate(self, info, **kwargs):
        name = kwargs.get('name')
        category = Category(name=name)
        Category.save(category)
        return CreateCategory(category=category)


class UpdateCategory(graphene.Mutation):
    """
mutation updateCategory {
 	updateCategory(id: "5", name: "MilkV2") {
  	category {
      id
      name
    }
  }
}
    """
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    def mutate(self, info, id, name):
        ca = Category.objects.get(pk=id)
        ca.name = name
        ca.save()
        return UpdateCategory(category=ca)


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
