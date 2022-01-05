import graphene

import landing.schema as landing
import scribbli.universe.schema as universe
from scribbli.utils import get_app_context

from .other import AppContext


class Query(landing.Query, universe.Query, graphene.ObjectType):

    app_context = graphene.Field(AppContext)
    def resolve_app_context(root, info):
        return get_app_context(info.context)

class Mutations(universe.Mutations):
    pass

schema = graphene.Schema(query=Query, mutation=Mutations)
