import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.models import User as UserModel, db


class UserType(SQLAlchemyObjectType):
    class Meta:
        model = UserModel

class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(root, info):
        return db.session.execute(db.select(UserModel)).scalars()
    


schema = graphene.Schema(query=Query)
