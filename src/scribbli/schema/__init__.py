import graphene

import landing.schema as landing
import scribbli.universe.schema as universe
import scribbli.story.schema as story
from scribbli.utils import get_app_context

from .other import AppContext


class Query(landing.Query, universe.Query, story.Query, graphene.ObjectType):

    app_context = graphene.Field(AppContext)
    def resolve_app_context(root, info):
        return get_app_context(info.context)

class Mutations(universe.Mutations, story.Mutations):
    pass

schema = graphene.Schema(query=Query, mutation=Mutations)
