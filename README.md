# xtsv-word

**This module provides a special dataclass-like structure to handle tokens in [xtsv](https://github.com/nytud/xtsv) format. It is meant to be used within `xtsv` modules to make the processing of token attributes (`xtsv` fields) more comfortable and transparent.**

It allows for each token to be represented by a `Word` object which is initialised simply by passing the token in its `xtsv` representation (i.e. a list of strings, one for each field in the input stream) to a `WordFactory` object. This factory object keeps track of the input and target fields of the `xtsv` module, and assigns the items of the list representing the token in `xtsv` to the respective `Word` object attributes which are identified by the name of the corresponding field (i.e. the `xtsv` column header).

Both the input and the target fields can be accessed as attributes of a `Word` object, i.e. they can be both retrieved and modified. (The usual use case is to only read input field attributes and to specify target field attributes. However, the `Word` object does not prevent a user from modifying input field values. This is discouraged but not ruled out by `xtsv`.) When the `xtsv` module is done processing a token, the `Word` object is simply converted into a list which contains the original input fields followed by the target fields, as expected by `xtsv`.

Disclaimer: This is not an official extension of the [xtsv](https://github.com/nytud/xtsv) module.

## Suggested usage

Install `xtsv-word` from `pip`:
```
python3 -m pip install xtsv-word
```

or build locally:
```
make
```

For example, assuming that the internal app object defined in the `xtsv` module `myXtsvModule` is called `InternalApp`, the input stream contains the fields `['form', 'wsafter']` and `myXtsvModule` has a single target field: `['syllables']`:

1. **Create `WordFactory` object:**

```
# myXtsvModule.py

from xtsv_word import WordFactory

class InternalApp:
	...
	def prepare_fields(self, field_names):
		self.wf = WordFactory(field_names, self.target_fields)
		# self.target_fields is normally set in InternalApp.__init__()
```

2. **Use `Word` object:**

```
class InternalApp:
	...
	def process_sentence(self, sen, field_values):
		return_sen = []
		for tok in sen:
			# Get Word object from factory
			word = self.wf.get_word(tok)

			# process token by getting and setting its attributes, e.g.:
			word.syllables = split_syllables(word.form)
			...
			# alternatively access attributes as dict keys:
			word['syllables'] = '-'.join(word['syllables'])

			# convert Word object to list of fields for xtsv output stream
			return_sen.append(list(word))

		...
		return return_sen
```

See docstrings for further details.
