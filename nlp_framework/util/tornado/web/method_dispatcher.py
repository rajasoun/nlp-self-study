import tornado.web


class MethodDispatcher(tornado.web.RequestHandler):

    def _dispatch(self):
        """
        Load up the requested URL if it matches one of our own methods.
        Skip methods that start with an underscore (_).
        """
        path = self.request.uri.split('?')[0]
        method = path.split('/')[-1]
        if not method.startswith('_'):
            func = getattr(self, method, None)
            if func:
                return func()
            else:
                raise tornado.web.HTTPError(404)
        else:
            raise tornado.web.HTTPError(404)

    def get(self):
        """Returns self._dispatch()"""
        return self._dispatch()

    def post(self):
        """Returns self._dispatch()"""
        return self._dispatch()
