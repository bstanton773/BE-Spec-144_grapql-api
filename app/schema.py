import graphene


class Query(graphene.ObjectType):
    test = graphene.String()

    def resolve_test(root, info):
        return 'This is a string that I wrote and am returning to you now'
    


schema = graphene.Schema(query=Query)
