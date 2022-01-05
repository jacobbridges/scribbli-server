def get_universe_by_id(id_: str):
    from scribbli.universe.models import Universe
    return Universe.objects.get(id=id_)


def get_universe_by_graphql_id(graphql_id: str):
    from graphql_relay import from_global_id
    from scribbli.universe.models import Universe
    universe_id = from_global_id(graphql_id)[1]
    return Universe.objects.get(id=universe_id)
