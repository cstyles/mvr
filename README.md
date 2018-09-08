# mvr
The "mv" coreutil but with regular expressions.

## Usage

```bash
mvr.py match_regex rename_regex files [files ...]
```

## Examples

#### Rename all .zip files to .cbz files
```bash
$ mvr.py '\.zip$' '.cbz' *
```

#### Use anything python's `re` module supports like character classes and backreferences
```bash
$ mvr.py 'img(\d+).png' 'image\1.png' *
```

#### Will warn you if there's a collision in the new names
```shell
$ mvr.py '.+' 'constant_string' *.txt
Collision exists in new file names. Aborting...
```
