import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.models import User as UserModel, db


class UserType(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        exclude_fields = ("password",)

class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, user_id=graphene.ID(required=True))
    search_users = graphene.List(UserType, username=graphene.String(), email=graphene.String())

    def resolve_users(root, info):
        return db.session.execute(db.select(UserModel)).scalars()

    def resolve_user(root, info, user_id):
        user = db.session.get(UserModel, user_id)
        return user

    def resolve_search_users(root, info, username=None, email=None):
        query = db.select(UserModel)
        if username:
            query = query.where(UserModel.username.ilike(f"%{username}%"))
        if email:
            query = query.where(UserModel.email.ilike(f"%{email}%"))
        results = db.session.execute(query).scalars()
        return results


class AddNewUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(root, info, username, email, password):
        new_user = UserModel(username=username, email=email, password=password)
        return AddNewUser(user=new_user)


class UpdateUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        username = graphene.String()
        email = graphene.String()

    user = graphene.Field(UserType)

    def mutate(roote, info, user_id, username=None, email=None):
        # Query db for user with user_id
        user = db.session.get(UserModel, user_id)
        # If no user with user_id, return None
        if user is None:
            return None
        # If the username argument
        if username:
            # Set the user's username to the username arg
            user.username = username
        # If the email argument
        if email:
            # Set the user's email to the email arg
            user.email = email
        # Commit any changes to the database
        db.session.commit()
        # Return the updated user as the "user" field output
        return UpdateUser(user=user)


class Mutation(graphene.ObjectType):
    add_new_user = AddNewUser.Field()
    update_user = UpdateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
