import random
import string
from inspect import Parameter

from ..common import ConfigObject, is_primitive


def gen_random_primitive(arg_type: str, arg_len=10):
    if arg_type == 'int':
        if random.randint(1, 10) <= 3:
            return 0
        return random.randint(0, 10 ** arg_len)
    elif arg_type == 'str':
        if random.randint(1, 10) <= 3:
            return ""
        letters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(letters) for _ in range(arg_len))
    elif arg_type == 'bool':
        return bool(random.getrandbits(1))
    elif arg_type == 'float':
        if random.randint(1, 10) <= 3:
            return 0
        return random.uniform(0, 10 ** (arg_len / 2))
    else:
        return None


class FuncTest(object):
    def __init__(self, config: ConfigObject, func_info: list):
        [module_name, class_name, func_name] = func_info
        self.func_name = func_name
        self.config = config
        self.func_args = config.config[module_name][class_name][func_name]
        self.cnt = 0

    def gen_arg(self, arg_type: str, default_val, obj_names, obj_dict):
        # 30% to directly use default value
        if random.randint(1, 10) <= 3 and default_val != '':
            return default_val

        # 70% to automatically generate
        if is_primitive(arg_type):
            return gen_random_primitive(arg_type)
        elif arg_type == 'dict':
            if random.randint(1, 10) <= 3:
                return {}
            return default_val
        elif arg_type == 'list':
            return self.gen_list(default_val, obj_names, obj_dict)
        elif arg_type == 'any':
            return None if default_val == "" else default_val
        else:
            return self.gen_defined_type(arg_type, obj_names, obj_dict)

    def gen_defined_type(self, arg_type: str, obj_names, obj_dict):
        arg_name = 'arg_' + str(self.cnt)
        self.cnt += 1
        arg_obj = Parameter(arg_name, Parameter.KEYWORD_ONLY)
        obj_names[:0] = [arg_name]
        for _, temp in self.config.config.items():
            for key, val in temp.items():
                if key == arg_type:
                    obj_dict[arg_name] = self.gen_list(val['__init__'],
                                                       obj_names, obj_dict)
        return arg_obj

    def gen_list(self, list_args: list, obj_names, obj_dict):
        args_list = []
        for arg in list_args:
            if 'self' in arg.keys():
                continue
            arg_type, default_val = random.choice(list(arg.items()))
            args_list.append(
                self.gen_arg(arg_type, default_val, obj_names, obj_dict))
        return args_list

    def generate_random_test(self):
        obj_names = []
        obj_dict = {}
        arg_list = self.gen_list(self.func_args, obj_names, obj_dict)
        return [obj_names, obj_dict, arg_list]
