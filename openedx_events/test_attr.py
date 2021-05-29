import attr

from openedx_events.data import *
from django.contrib.auth.models import User


# Creating student student data
user = User.objects.get(id=1)
dict_student = [
    user.username,
    user.email,
    user.profile.meta,
    False,
    'Fullname',
]
student_data = StudentData(*dict_student)
print(student_data)
# RESULT: StudentData(username='ecommerce_worker', email='ecommerce_worker@example.com', profile_meta='', is_active=False, fullname='Fullname')
print(attr.asdict(student_data))
# RESULT: {'username': 'ecommerce_worker', 'email': 'ecommerce_worker@example.com', 'profile_meta': '', 'is_active': False, 'fullname': 'Fullname'}
dict_student_v2 = StudentDataV2()
print(dict_student_v2)
# RESULT: StudentDataV2(profile_meta={})
dict_student_v2.profile_meta['ci'] = 123467
print(dict_student_v2)
# RESULT: StudentDataV2(profile_meta={'ci': 123467})
# ERROR: dict_student_v2.profile_meta = 123467
#   File "/edx/src/edxapp/attrs/src/attr/_make.py", line 628, in _frozen_setattrs
#    raise FrozenInstanceError()
# attr.exceptions.FrozenInstanceError
student_data_v3 = StudentDataV3(
    username='username',
    email='email@gmail.com',
    profile_meta={'ci': 123456789},
    is_active=True,
)
print(student_data_v3)
# ERROR: email validation
# student_data_v3 = StudentDataV3(
#    username='username',
#    email='email@gmail.com',
#    profile_meta={'ci': 123456789},
#    is_active=True,
# )
#   raise ValueError("email must be valid.")
#    ValueError: email must be valid.
# StudentDataV3(username='username', email='email', profile_meta={'ci': 123456789}, is_active=True)
# ERROR: missing keyword argument:
# student_data_v3 = StudentDataV3(
#    'username',
#    email='email',
#    profile_meta={'ci': 123456789},
#    is_active=True,
# )
#   File "<string>", line 46, in <module>
# TypeError: __init__() takes 1 positional argument but 2 positional arguments (and 3 keyword-only arguments) were given
# student_data_v3 = StudentDataV3(
#     username=1,
#     email='email',
#     profile_meta={'ci': 123456789},
#     is_active=True,
# )
# TypeError: ("'username' must be <class 'str'> (got 1 that is a <class 'int'>)."
#
