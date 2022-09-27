"""
A special dataclass-like structure to handle tokens in xtsv format.
The WordFactory should be instantiated in the prepare_fields() method
of the internal app object of an xtsv module and stored as an attribute
value of the internal app.
The get_word() method should be called in the process_sentence() method
of the internal app, and each input token in the xtsv sentence stream
should be passed to it.
"""

from types import SimpleNamespace


class WordFactory:
    """
    Factory class that produces Word objects according
    to the specified settings.
    Initialize with the value of the field_names argument of the
    prepare_fields() method and with either the value of
    self.target_fields, which is a list of output fields added by
    the current xtsv module, or with a dict that contains
    'field: initial value' pairs for each target field.
    If only the target_fields list is passed, the values of
    these fields are all initialized to target_value_default.
    """

    def __init__(self, xtsv_field_names, /,
                 target_fields=None, *,
                 target_value_default='',
                 target_field_inits=None):
        if target_field_inits is not None:
            self.target_fields = target_field_inits
        else:
            self.target_fields = {field: target_value_default
                                         for field in target_fields}

        self.input_fields = [field
                             for field in xtsv_field_names
                             if (isinstance(field, str)
                                 and field not in self.target_fields)]

    def __repr__(self):
        return (f"WordFactory(input_fields={self.input_fields!r}, "
                + f"target_fields={self.target_fields!r})")

    def get_word(self, values):
        """
        Return a Word object the input fields of which are
        initialised to the specified values.
        The target fields are initialised according to the
        settings of the factory object.
        Raise a ValueError if the number of input fields and
        the length of the provided iterable of values do not match.
        """

        try:
            input_values = dict(zip(self.input_fields, values, strict=True))
        except ValueError as exc:
            raise ValueError(
                f"{len(self.input_fields)} values expected, "
                + f"{len(values)} provided:\n"
                + f"Features: {self.input_fields}\n"
                + f"Values: {values}") from exc
        return Word(input_values | self.target_fields)


class Word(SimpleNamespace):
    """
    Convenience class to access (get and set) the fields
    (i.e. features) of an xtsv token as attributes or
    alternatively as dictionary keys.
    Yields the values of each field in order when used
    as an iterable.
    Additional attributes can be freely added to a Word
    object. They are ignored in the string representation,
    the iterable, and the dict functions, so they will not
    break the integrity of the xtsv output.
    """

    def __init__(self, value_dict):
        super().__init__(**value_dict)
        self._word_attrs = list(value_dict.keys())

    def __repr__(self):
        return "Word({})".format(', '.join(f"{k}={v!r}" for k, v
                                           in self.__dict__.items()
                                           if k != '_word_attrs'))

    def __iter__(self):
        return iter(self.__dict__[key] for key in self._word_attrs)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __len__(self):
        return len(self._word_attrs)

    def keys(self):
        '''Get names of features'''
        return {key: self.__dict__[key] for key in self._word_attrs}.keys()

    def values(self):
        '''Get value of each feature'''
        return {key: self.__dict__[key] for key in self._word_attrs}.values()

    def items(self):
        '''Get feature-value pairs'''
        return {key: self.__dict__[key] for key in self._word_attrs}.items()
