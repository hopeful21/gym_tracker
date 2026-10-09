(.venv) him@him:~/Documents/py/gym_tracker$ source .venv/bin/activate
python manage.py check
python manage.py test
System check identified no issues (0 silenced).
Found 14 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
EE..Assigned 1 legacy workout(s) and 1 preference row(s) to athlete-one.
...EELoaded 8 muscle groups and connected images for 15 exercises.
EEEE.
======================================================================
ERROR: test_authenticated_pages_render_for_owner (tracker.tests.TrackerTests.test_authenticated_pages_render_for_owner)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/him/Documents/py/gym_tracker/tracker/tests.py", line 65, in test_authenticated_pages_render_for_owner
    self.assertEqual(client.get(reverse('home')).status_code, 200)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 1127, in get
    response = super().get(
               ^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 475, in get
    return self.generic(
           ^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 671, in generic
    return self.request(**r)
           ^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 1085, in request
    response = self.handler(environ)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 173, in __call__
    self.load_middleware()
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/core/handlers/base.py", line 40, in load_middleware
    middleware = import_string(middleware_path)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/utils/module_loading.py", line 30, in import_string
    return cached_import(module_path, class_name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/utils/module_loading.py", line 15, in cached_import
    module = import_module(module_path)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/importlib/__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'whitenoise'

======================================================================
ERROR: test_completed_workout_detail_history_and_analytics (tracker.tests.TrackerTests.test_completed_workout_detail_history_and_analytics)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/him/Documents/py/gym_tracker/tracker/tests.py", line 97, in test_completed_workout_detail_history_and_analytics
    self.assertEqual(client.get(reverse('workout_detail', args=[self.workout.pk])).status_code, 200)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 1127, in get
    response = super().get(
               ^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 475, in get
    return self.generic(
           ^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 671, in generic
    return self.request(**r)
           ^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 1085, in request
    response = self.handler(environ)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 173, in __call__
    self.load_middleware()
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/core/handlers/base.py", line 40, in load_middleware
    middleware = import_string(middleware_path)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/utils/module_loading.py", line 30, in import_string
    return cached_import(module_path, class_name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/utils/module_loading.py", line 15, in cached_import
    module = import_module(module_path)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/importlib/__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'whitenoise'

======================================================================
ERROR: test_private_pages_redirect_anonymous_users (tracker.tests.TrackerTests.test_private_pages_redirect_anonymous_users)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/him/Documents/py/gym_tracker/tracker/tests.py", line 119, in test_private_pages_redirect_anonymous_users
    response = client.get(reverse(name))
               ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 1127, in get
    response = super().get(
               ^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 475, in get
    return self.generic(
           ^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 671, in generic
    return self.request(**r)
           ^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 1085, in request
    response = self.handler(environ)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 173, in __call__
    self.load_middleware()
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/core/handlers/base.py", line 40, in load_middleware
    middleware = import_string(middleware_path)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/utils/module_loading.py", line 30, in import_string
    return cached_import(module_path, class_name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/utils/module_loading.py", line 15, in cached_import
    module = import_module(module_path)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/importlib/__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'whitenoise'

======================================================================
ERROR: test_registration_login_logout_use_hashed_passwords (tracker.tests.TrackerTests.test_registration_login_logout_use_hashed_passwords)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/him/Documents/py/gym_tracker/tracker/tests.py", line 103, in test_registration_login_logout_use_hashed_passwords
    response = client.post(reverse('register'), {'username':'new-athlete', 'password1':'AnotherStrong123!', 'password2':'AnotherStrong123!'})
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 1156, in post
    response = super().post(
               ^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 499, in post
    return self.generic(
           ^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 671, in generic
    return self.request(**r)
           ^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 1085, in request
    response = self.handler(environ)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 173, in __call__
    self.load_middleware()
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/core/handlers/base.py", line 40, in load_middleware
    middleware = import_string(middleware_path)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/utils/module_loading.py", line 30, in import_string
    return cached_import(module_path, class_name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/utils/module_loading.py", line 15, in cached_import
    module = import_module(module_path)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/importlib/__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'whitenoise'

======================================================================
ERROR: test_seed_command_maps_matching_local_exercise_photos (tracker.tests.TrackerTests.test_seed_command_maps_matching_local_exercise_photos)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/him/Documents/py/gym_tracker/tracker/tests.py", line 29, in test_seed_command_maps_matching_local_exercise_photos
    response = client.get(reverse('exercises'))
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 1127, in get
    response = super().get(
               ^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 475, in get
    return self.generic(
           ^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 671, in generic
    return self.request(**r)
           ^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 1085, in request
    response = self.handler(environ)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 173, in __call__
    self.load_middleware()
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/core/handlers/base.py", line 40, in load_middleware
    middleware = import_string(middleware_path)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/utils/module_loading.py", line 30, in import_string
    return cached_import(module_path, class_name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/utils/module_loading.py", line 15, in cached_import
    module = import_module(module_path)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/importlib/__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'whitenoise'

======================================================================
ERROR: test_workout_and_favorite_data_are_isolated_between_users (tracker.tests.TrackerTests.test_workout_and_favorite_data_are_isolated_between_users)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/him/Documents/py/gym_tracker/tracker/tests.py", line 134, in test_workout_and_favorite_data_are_isolated_between_users
    history_response = client.get(reverse('history'))
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 1127, in get
    response = super().get(
               ^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 475, in get
    return self.generic(
           ^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 671, in generic
    return self.request(**r)
           ^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 1085, in request
    response = self.handler(environ)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 173, in __call__
    self.load_middleware()
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/core/handlers/base.py", line 40, in load_middleware
    middleware = import_string(middleware_path)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/utils/module_loading.py", line 30, in import_string
    return cached_import(module_path, class_name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/utils/module_loading.py", line 15, in cached_import
    module = import_module(module_path)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/importlib/__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'whitenoise'

======================================================================
ERROR: test_workout_data_creation_uses_logged_in_user (tracker.tests.TrackerTests.test_workout_data_creation_uses_logged_in_user)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/him/Documents/py/gym_tracker/tracker/tests.py", line 164, in test_workout_data_creation_uses_logged_in_user
    response = client.post(reverse('start_workout'), {'title':'Pull day', 'muscle_groups':[self.group.pk]})
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 1156, in post
    response = super().post(
               ^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 499, in post
    return self.generic(
           ^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 671, in generic
    return self.request(**r)
           ^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 1085, in request
    response = self.handler(environ)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 173, in __call__
    self.load_middleware()
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/core/handlers/base.py", line 40, in load_middleware
    middleware = import_string(middleware_path)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/utils/module_loading.py", line 30, in import_string
    return cached_import(module_path, class_name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/utils/module_loading.py", line 15, in cached_import
    module = import_module(module_path)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/importlib/__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'whitenoise'

======================================================================
ERROR: test_workout_flow_and_invalid_set (tracker.tests.TrackerTests.test_workout_flow_and_invalid_set)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/him/Documents/py/gym_tracker/tracker/tests.py", line 77, in test_workout_flow_and_invalid_set
    start = client.post(reverse('start_workout'), {'title': 'Leg day', 'muscle_groups': [self.group.pk]})
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 1156, in post
    response = super().post(
               ^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 499, in post
    return self.generic(
           ^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 671, in generic
    return self.request(**r)
           ^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 1085, in request
    response = self.handler(environ)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/test/client.py", line 173, in __call__
    self.load_middleware()
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/core/handlers/base.py", line 40, in load_middleware
    middleware = import_string(middleware_path)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/utils/module_loading.py", line 30, in import_string
    return cached_import(module_path, class_name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/him/Documents/py/gym_tracker/.venv/lib/python3.12/site-packages/django/utils/module_loading.py", line 15, in cached_import
    module = import_module(module_path)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/importlib/__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'whitenoise'

----------------------------------------------------------------------
Ran 14 tests in 3.602s

FAILED (errors=8)
Destroying test database for alias 'default'...
(.venv) him@him:~/Documents/py/gym_tracker$ 
