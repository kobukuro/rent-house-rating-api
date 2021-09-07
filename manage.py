#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import unittest
from tests.setting import setting


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rent_house_rating_api.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # custom test
    if sys.argv[1] == 'test':
        from tests.metaclass import AvoidSameMethodNameMetaclass
        import django
        os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                              "rent_house_rating_api.settings")
        django.setup()
        if setting.IS_EXECUTE_ALL_TEST:
            # region 取得apps底下所有test class
            apps = os.listdir('apps')
            app_test_classes = []
            for app in apps:
                test_file_path = f'apps.{app}.tests'
                import inspect
                import importlib
                for name, cls in inspect.getmembers(importlib.import_module(test_file_path), inspect.isclass):
                    # 為了在所有test function名稱後面加上module名以及class名（為了讓test function名稱不重複）
                    # 因為一旦重複，只會執行先繼承的那個
                    test_class_with_metaclass = AvoidSameMethodNameMetaclass(name, (object,), cls.__dict__)
                    app_test_classes.append(test_class_with_metaclass)
            app_test_classes = tuple(app_test_classes)
            # endregion
            # region 取得test_roles.py底下所有class，並繼承所有test class
            role_classes = []
            role_file_name = 'tests.test_roles'
            for name, cls in inspect.getmembers(importlib.import_module(role_file_name), inspect.isclass):
                if cls.__module__ == role_file_name:
                    cls.__bases__ += app_test_classes
                    role_classes.append(cls)
            # endregion
            role_classes_to_run = role_classes
            loader = unittest.TestLoader()
            suites_list = []
            for role_class_to_run in role_classes_to_run:
                suite = loader.loadTestsFromTestCase(role_class_to_run)
                suites_list.append(suite)
            result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(suites_list))
        else:
            from tests.test_roles import SuperUser, NormalUserOne
            from apps.location.tests import Location, Country, Rating
            user_class = NormalUserOne
            user_class.__bases__ += (Location, Country, Rating)
            single_test = unittest.TestSuite()
            single_test.addTest(user_class('test_get_specific_rating'))
            result = unittest.TextTestRunner(verbosity=2).run(single_test)
        return exit(1) if result.errors else exit(0)
    else:
        execute_from_command_line(sys.argv)
    # python manage.py test tests/ --pattern="test_roles.py" -v 2


if __name__ == '__main__':
    main()
