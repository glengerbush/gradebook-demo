from app.routes.api.docs import api

##########################################
# should this be protected with a login? #
##########################################


@api.route('/', methods=['GET'])
@api.route('/index', methods=['GET'])
def api_docs():
    # redirect to latest version
    return "<body>Docs coming eventually... :(</body>"


@api.route('/v1', methods=['GET'])
def api_docs_v1():
    return "<body>V1 docs coming eventually...:(</body>"
