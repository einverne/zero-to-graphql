#!/usr/bin/env python
# -*- coding: utf-8 -*-

import graphene
from graphene import relay

from graphene_django.types import DjangoObjectType

from ingredients.models import Category, Ingredient


class CategoryType(DjangoObjectType):
    """
    DjangoObjectType will present all fields on a Model through GraphQL
    """
    class Meta:
        model = Category
        # fields = ('',)
        # exclude = ('',)


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        interfaces = (relay.Node,)


class IngredientConnection(relay.Connection):
    class Meta:
        node = IngredientType


class Query(object):
    all_categories = graphene.List(CategoryType)
    all_ingredients = graphene.List(IngredientType)

    a_ingredients = relay.ConnectionField(IngredientConnection)

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

    def resolve_a_ingredient(self, info, **kwargs):
        return Ingredient.objects.all()


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
