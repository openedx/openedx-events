1 Schema Implementation decisions
---------------------------------

1.1 Context
~~~~~~~~~~~

HELP!!, what context does this decision need???????
I’m thinking of adding links to issues, but otherwise, I don’t know what context would go for such a implementation related ADR

1.2 Decision
~~~~~~~~~~~~

- Signal classes in \_ will define the schema for event bus messages

  - the “data” attribute will specify the exact data to be sent over the wire.

    - The ’data’ attribute will be a data dict

      - The keys in the data will be strings

      - The values can be: python primitives(int, str, dict, list ...), attrs decorated classes defined in openedx-events repository, or custom classes that have extensions defined in AvroAttrsBridge class.

        - Ideally, the values are attrs decorated classes, other types are supported for convenience.

  - The metadata (topic name, version information) for an event will be defined as attributes in signal class. If is unclear exactly what metadata will be needed.

- All the keywords in “data” attribute in signal classes will be required.

- Once an attrs decorated class is defined in openedx-events, it should not change.

- If you need to add more information to a message, add it as an additional field in “data” attribute in your signal class.
