import types


def dict_get(data_dict, data_key, default=None):
    tmp = data_dict
    for k, v in tmp.items():
        if k == data_key:
            return v
        else:
            if type(v) is types.DictType:
                ret = dict_get(v, data_key, default)
                if ret is not default:
                    return ret
    return default
