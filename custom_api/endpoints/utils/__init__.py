from custom_api.models import db
from datetime import datetime

def mongo_to_dict(obj, depth=0):
    """ Turn a mongoengine object into a jsonible python object
    """
    return_data = []

    if isinstance(obj, db.Document) or isinstance(obj, db.DynamicDocument):
        obj.select_related(max_depth=depth)
        return_data.append(("id", str(obj.id)))

    if obj is None:
        return ""

    if not hasattr(obj, '_fields'):
        try:
            resp = str(obj.id)
        except AttributeError:
            resp = str(obj)
        return resp

    for field_name in obj._fields:
        try:
            data = obj._data[field_name]
        except KeyError:
            continue
        if data is None:
            continue

        if isinstance(obj._fields[field_name], db.DateTimeField):
            time = ""
            if data and hasattr(data, 'isoformat'):
                time = str(data.isoformat())[:10]
            return_data.append((field_name, time))

        elif isinstance(obj._fields[field_name], db.StringField):
            return_data.append((field_name, str(data)))

        elif isinstance(obj._fields[field_name], db.FloatField):
            return_data.append((field_name, float(data)))

        elif isinstance(obj._fields[field_name], db.IntField):
            if data is not None:
                return_data.append((field_name, int(data)))

        elif isinstance(obj._fields[field_name], db.ListField):
            new_list = []
            for e in data:
                new_list += [mongo_to_dict(e, depth)]
            return_data.append((field_name, new_list))

        elif isinstance(obj._fields[field_name], db.EmbeddedDocumentField):

            return_data.append((field_name, mongo_to_dict(data, depth)))

        elif isinstance(obj._fields[field_name], db.ObjectIdField):
            return_data.append((field_name, str(data)))

        elif isinstance(obj._fields[field_name], db.DynamicField):
            return_data.append((field_name, data))

        elif isinstance(obj._fields[field_name], db.ReferenceField):
            new_depth = 0
            if depth-1 > 0:
                new_depth = depth - 1
            if depth > 0:
                return_data.append((field_name, mongo_to_dict(data, new_depth)))
            else:
                try:
                    element = str(data.id)
                except:
                    element = str(data)
                return_data.append((field_name, element))

        elif isinstance(obj._fields[field_name], db.BooleanField):
            return_data.append((field_name, data))

        elif isinstance(obj._fields[field_name], db.DictField):
            return_data.append((field_name, dict(data)))

        else:
            print(type(obj._fields[field_name]))

    return dict(return_data)