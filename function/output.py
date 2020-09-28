import json


def information_output(app, data):
    response = app.response_class(json.dumps(data),
                                  status=200,
                                  mimetype='application/json')
    return response
