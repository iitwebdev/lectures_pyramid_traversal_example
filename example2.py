from wsgiref.simple_server import make_server

from pyramid.config import Configurator
from pyramid.renderers import JSON


def traverse_koshey(context, request):
    return context


class СмертьКощея(object):

    def __json__(self, request):

        return {
            'имя': 'кощей',
            'статус': request.context == self and 'мертв' or 'жив ещё',
        }


def my_factory(request):
    return {
        'остров': {
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

    # Make app and serve
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
