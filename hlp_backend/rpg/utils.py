from django.core import serializers
import json


def serialize_one(param):
    return json.loads(serializers.serialize('json', [param]))[0]


def serialize_set(params):
    return json.loads(serializers.serialize('json', params))


def deserialize_one(json_serialized):
    for result in serializers.deserialize('json', json.dumps([json_serialized])):
        return result.object


def deserialize_set(json_serialized):
    return [value.object for value in serializers.deserialize('json', json.dumps(json_serialized))]
