import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.models import User as UserModel, db


class UserType(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        exclude_fields = ("password",)

class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(root, info):
        return db.session.execute(db.select(UserModel)).scalars()


class AddNewUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(root, info, username, email, password):
        new_user = UserModel(username=username, email=email, password=password)
        return AddNewUser(user=new_user)


class Mutation(graphene.ObjectType):
    add_new_user = AddNewUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
