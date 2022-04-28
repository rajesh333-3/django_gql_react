from re import M
import graphene
import api.schema

class Mutation(api.schema.Mutation, graphene.ObjectType):
    pass
class Query(api.schema.Query, graphene.ObjectType):
    pass
schema = graphene.Schema(query = Query, mutation = Mutation)

