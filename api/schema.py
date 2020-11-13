import graphene
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
import graphql_jwt

from database.models import CustomUser, Menu

class CustomUserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = ("id", "first_name", "last_name",
        "email", "role", "is_active", "date_joined")

class MenuType(DjangoObjectType):
    class Meta:
        model = Menu
        fields = ("id", "title", 
        "details", "picture",
        "price", "is_available")


class Query(graphene.ObjectType):
    all_users = graphene.List(CustomUserType)
    user_by_id = graphene.Field(CustomUserType, id=graphene.String())
    all_menus = graphene.List(MenuType)
    menu_by_id = graphene.Field(MenuType, id=graphene.String())

    def resolve_all_users(self, info, **kwargs):
        return CustomUser.objects.all()

    def resolve_user_by_id(self, info, id):
        return CustomUser.objects.get(pk=id)

    def resolve_all_menus(self, info, **kwargs):
        # Querying a list
        return Menu.objects.all()

    def resolve_menu_by_id(self, info, id):
        # Querying a single menu
        return Menu.objects.get(pk=id)


class CreateUser(graphene.Mutation):
    custom_user = graphene.Field(CustomUserType)

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        confirm_password = graphene.String(required=True)


    def mutate(self, info, first_name, last_name, email, password, confirm_password):
        custom_user = CustomUser(
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        custom_user.set_password(password)
        custom_user.save()

        return CreateUser(custom_user=custom_user)
        # pass


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(CustomUserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)

class Mutation(graphene.ObjectType):
    # Mutation variables for authentication
    token_auth = ObtainJSONWebToken.Field()
    veriry_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    delete_token_cookie = graphql_jwt.DeleteJSONWebTokenCookie.Field()

    # Long running refresh tokens
    delete_refresh_token_cookie = graphql_jwt.DeleteRefreshTokenCookie.Field()


    # Mutation for creating a user
    create_user = CreateUser.Field()
