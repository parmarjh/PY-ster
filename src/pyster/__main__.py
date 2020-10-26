import sys
import argparse
from generator.getClassInfo import UserModule
from generator.generateRandomInput import TestCase

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Unit Tests')
    parser.add_argument('path',
                        metavar='path',
                        type=str,
                        help='the path to source files')
    parser.add_argument('--timeout',
                        metavar='timeout',
                        type=int,
                        default=20,
                        help='user defined time limit for the program to run in seconds')
    parser.add_argument('--coverage',
                        metavar='coverage_target',
                        type=int,
                        default=80,
                        choices=range(1, 101),
                        help='target coverage for the generated tests in percentage')
    args = parser.parse_args()
    file_path = args.path
    print("timeout: " + str(args.timeout))
    print("coverage_target: " + str(args.coverage))

    module_item = UserModule(file_path)
    print(module_item)

    print(getattr(getattr(module_item.mod, 'Foo'), '__init__'))
    test_case = TestCase(getattr(getattr(module_item.mod, 'Foo'), '__init__'),
                         getattr(getattr(module_item.mod, 'Foo'), 'foo_func'),
                         module_item.module_classes['Foo'].class_funcs[0])
    test_case.generate_random_test()

