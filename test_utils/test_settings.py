"""
These settings are here to use during tests, because django requires them.
In a real-world use case, apps in this project are installed into other
Django applications, so these settings will not be used.
"""

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "default.db",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
    "read_replica": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "read_replica.db",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}


INSTALLED_APPS = (
    "openedx_events",
)

SECRET_KEY = "not-so-secret-key"
EVENT_BUS_PRODUCER_CONFIG = {
    'org.openedx.content_authoring.xblock.published.v1':
        {
            'enabled_topic_a': {'event_key_field': 'xblock_info.usage_key', 'enabled': True},
            'enabled_topic_b': {'event_key_field': 'xblock_info.usage_key', 'enabled': True},
            'disabled_topic': {'event_key_field': 'xblock_info.usage_key', 'enabled': False}
        },
    'org.openedx.content_authoring.xblock.deleted.v1':
        {
            'content-authoring-xblock-lifecycle': {'event_key_field': 'xblock_info.usage_key', 'enabled': True},
        }
}
