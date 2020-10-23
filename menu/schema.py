import graphene
from graphene_django import DjangoObjectType

from .models import Menu

class MenuType(DjangoObjectType):
    class Meta:
        model = Menu
        fields = ("id", "title", 
        "details", "picture",
        "price", "is_available")

class Query(graphene.ObjectType):
    all_menus = graphene.List(MenuType)
    menu_by_id = graphene.Field(MenuType, id=graphene.String())

    def resolve_all_menus(root, info, **kwargs):
        # Querying a list
        return Menu.objects.all()

    def resolve_menu_by_id(root, info, id):
        # Querying a single menu
        return Menu.objects.get(pk=id)
