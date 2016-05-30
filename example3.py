from wsgiref.simple_server import make_server

from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.renderers import JSON


def traverse_koshey(context, request):
    """
    http://localhost:8080/mytraversal/остров/дуб/сундук/заяц/утка/яйцо/игла
    """
    return context


def traverse_hello(context, request):
    """
    http://localhost:8080/mytraversal/первед/Пирамид
    """
    return Response('Превед ' + context.__parent__.name + ' ' + context.name)


class Человек(object):

    name = 'Человек'

    def __getitem__(self, name):
        return Имя(name)

    def __json__(self, request):
        return {'name': self.name}


class Имя(object):

    __parent__ = Человек()

    def __init__(self, name):
        self.name = name

    def __json__(self, request):
        return {'name': self.name}


class СмертьКощея(object):

    def __json__(self, request):

        return {
            'имя': 'кощей',
            'статус': request.context == self and 'мертв' or 'жив ещё',
        }


def my_factory(request):
    return {
        'превед': Человек(),
        'остров': {
            'ясень': {
                'что то здесь': 'не так!'
            },
            'дуб': {
                'сундук': {
                    'заяц': {
                        'утка': {
                            'яйцо': {
                                'игла': СмертьКощея()
                            }
                        }
                    }
                }
            }
        }
    }


if __name__ == '__main__':
    config = Configurator()

    # ensure_ascii JSON renderer
    config.add_renderer('myjson', JSON(indent=4, ensure_ascii=False))

    # Traversal routing
    config.add_route('koshey', '/mytraversal/*traverse', factory=my_factory)
    config.add_view(traverse_koshey, route_name='koshey', renderer='myjson')

    # Traversal routing with context constraint
    config.add_route('koshey_context', '/mytraversal_context/*traverse',
                     factory=my_factory)
    config.add_view(traverse_koshey, route_name='koshey_context',
                    renderer='myjson',
                    context=СмертьКощея)
    config.add_view(traverse_hello, route_name='koshey_context',
                    renderer='text',
                    context=Имя)

    # Make app and serve
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
