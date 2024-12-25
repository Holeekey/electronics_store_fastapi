import jsonpickle

def manager_created_projector(ch, method, properties, body):
    event = jsonpickle.decode(body)