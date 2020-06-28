import cherrypy


class PodPaperApp:
    def __init__(self, port, static_dir_path, pod_paper):
        self.port = port
        self.static_dir_path = static_dir_path
        self.pod_paper = pod_paper

    def launch(self):
        cherrypy.config.update({'server.socket_port': 8090})
        config = {
            '/': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': self.static_dir_path,
                'tools.staticdir.index': 'index.html'
            }
        }

        return cherrypy.quickstart(self, "/", config)

    # Serves main page
    @cherrypy.expose
    def index(self):
        return open('index.html')

    @cherrypy.expose
    @cherrypy.tools.allow(methods='POST')
    def convert(self, **data):
        print(data)
