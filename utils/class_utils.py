def get_all_class_fields(cls):
    return [i for i in cls.__class__.__dict__.keys() if i[:1] != '_']


def py_access(code, dictionary=None, result_variable="_exec_result"):
    if dictionary is None:
        dictionary = {}

    variable_code_ = "%s = %s" % (result_variable, code)
    exec(variable_code_, globals(), dictionary)
    return dictionary[result_variable]


def py_shell(shell, dictionary):
    print(">>> " + shell)
    try:
        return exec(shell, globals(), dictionary)
    except Exception as e:
        print(e)


# def field_wipe(obj, obj_field=None, compare=None, addr="obj", parent=None):
#     if not parent: parent = obj
#     fields = dict_from_class(obj.__class__)
#     dictionary = {'obj': parent}
#
#     for field in fields:
#         try:
#             template_class_object = py_access("obj.%s" % field, dictionary={'obj': obj})
#             from configuration_model import Config
#             is_it_object = isinstance(template_class_object, Config.__base_section__)
#             if is_it_object:
#                 print(
#                     field_wipe(template_class_object, obj_field=field, compare=compare, parent=parent,
#                                addr="%s.%s" % (addr, field)))
#             else:
#                 py_shell("%s.%s = %s" % (addr, field, UNDEF), dictionary=dictionary)
#                 print("affected object: %s" % addr)
#
#         except Exception as e: pass
#
#     return obj, dictionary
