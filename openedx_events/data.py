import attr

from opaque_keys.edx.keys import CourseKey
from typing import Dict, FrozenSet, List, Optional


import re

# Make a regular expression
# for validating an Email
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'


@attr.s(frozen=True, auto_attribs=True)
class StudentData:
    """
    Attributes defined for Open edX User object.

    Findings while testing:
    1. Optional arguments have defaults
    2. Default is defined after the equal sign
    3. Dict[type1, type2]: {type1: type2}
    4. Optional != than optional arguments
    5. Optional is used when explicit values of None are allowed. Definition: Optional[X] is
    equivalent to Union[X, None]
    6. For advanced features use attr.ib not var: type
    7. auto_attribs=True means attrs need type --> var: type
    8. Type validation: https://www.attrs.org/en/stable/api.html#attr.validators.instance_of
    9. Other validations: https://www.attrs.org/en/stable/api.html#validators
    10. Add different type to username: nothing happens (see 12)
    11. frozen=True creates immutable objects. Use case: Sometimes you have instances that shouldn’t be
    changed after instantiation
    12. Please note that types – however added – are only metadata that can be queried from the class and they aren’t
    used for anything out of the box!
    """
    username: str
    email: str
    profile_meta: Dict[str, str]
    is_active: bool
    fullname: Optional[str]

@attr.s(frozen=True)
class StudentDataV2:
    """
    Attributes defined for Open edX User object.
    """
    profile_meta = attr.ib(factory=dict, type=Dict[str, str])


@attr.s(frozen=True)
class StudentDataV3:
    """
    Attributes defined for Open edX User object.
    """
    username = attr.ib(type=str, kw_only=True, validator=attr.validators.instance_of(str))
    email = attr.ib(type=str, kw_only=True)
    profile_meta = attr.ib(factory=dict, type=Dict[str, str], kw_only=True)
    is_active = attr.ib(type=bool, kw_only=True)

    @email.validator
    def _email_validator(self, attribute, value):
        if not re.search(regex, value):
            raise ValueError("email must be valid.")

    @is_active.default
    def _is_active_default(self):
        return True

@attr.s(frozen=True, auto_attribs=True)
class CourseData:
    """
    Attributes defined for Open edX course object.
    """
    course_key: CourseKey
    display_name: str


@attr.s(frozen=True, auto_attribs=True)
class EnrollmentData:
    """
    Attributes defined for Open edX Course Enrollment object.
    """
    student: StudentData
    course: CourseData
    mode: str
