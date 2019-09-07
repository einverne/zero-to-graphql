import graphene

import ingredients.schema
import people.schema



# class CreateUser(graphene.Mutation):
#     class Arguments:
#         username = graphene.String()
#
#     person = graphene.Field(Person)
#
#     def mutate(self, info, username):
#         person = Person(username=username)
#         return CreateUser(person=person)
#
#
class Mutation(
    ingredients.schema.Mutation):
    pass


class Query(people.schema.QueryType,
        ingredients.schema.Query):
    pass


# schema = graphene.Schema(query=Query)
schema = graphene.Schema(query=Query, mutation=Mutation)
# not use camel case style
# schema = graphene.Schema(query=QueryType, auto_camelcase=False)
