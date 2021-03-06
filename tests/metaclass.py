import types


class AvoidSameMethodNameMetaclass(type):
    def __new__(self, class_name, bases, attrs):
        new_attrs = {}
        for name, value in attrs.items():
            # test開頭的method才改名
            if not name.startswith('__') and isinstance(value, types.FunctionType) and name.startswith('test'):
                new_attrs[name + '_' + attrs['__module__'] + '.' + class_name] = value
            else:
                new_attrs[name] = value
        return type(class_name, bases, new_attrs)
