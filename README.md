# People & Places Automated Translator

When translating games such as Crusader Kings 2 and Europa Universals 4, there are many names of places and people for
 translators to search in search engines and dictionaries, which will slow down their efficiency and enthusiasm. 
This project is aimed to translate the names automatedly but accurately. CLI mode can read a file to be translated for
 best efficiency and the Web Server can let more translators use it in handle.

## Getting Started

This project runs in Python 3.6/7 and the required packages are listed in `src/requirements.txt`.

## Usage

### Web Service

```sh
# With requirements already installed
> cd src/
> flask run
```

Check our demo website at <https://ppat.enderqiu.cn>.

### CLI mode

```sh
# With requirements already installed
> cd src/
> python cli.py
...
```

## Authors

- [EnderQIU](https://github.com/EnderQIU)

## License

This project is open-sourced under the GPL v3 License.

## About Copyright

1. No copyright infringement intended.
2. If there is a copyright violation content, please e-mail <a934560824@163.com> to delete.
3. No money is being made of this project.

## Structure

```ascii
+--------------------------+--------------------------+
|                          |                          |
| Keyword&Parameter Input  |      Result Displayer    |
|                          |                          |
+--------------------------+--------------------------+
|                                                     |
|                    Web Frontend                     |
|                                                     |
+-----------------+----------------^------------------+
                  |                |
+-----------------v----------------+------------------+
|                                                     |
|       Parameter Resolver & Result Formatter         |
|                                                     |
+--------------------------+--------------------------+  Backend
|                          |                          |  Service
|                          |                          |
|                          |                          |
|    Index Transalator     |   Algorithm Translator   |
|                          |                          | <-- Could be a standalone CLI program
|                          |                          |     with another initializer, parameter
|                          |                          |     resolver and result displayer.
+-----^-----------+--------+-------^------------+-----+
      |           |                |            |
+-----+-----------v-------+ +------+------------v-----+
|                         | |                         |
|    Index Data Reader    | |     Algorithm Loader    | Index & Rules
|                         | |                         |   Loader
+-----^-------------------+ +-------------------^-----+
      |                                         |
+-----+------------------------------+ +--------+-----+ Rule & Index
| people.data.json & place.data.json | | t.csv & t.py |  Storage
+------------------------------------+ +--------------+
```

## Translating Process


```
+----------------------+
|                      |
| Raw Input (UTF-8)    |
|                      |
+-----------+----------+  +------------+
            |             |            |
            +<------------+ big_phoney |
            |             |            |
+-----------v----------+  +------------+
|                      |
| Phonetics (Optional) |
|                      |
+-----------+----------+  +-----------+
            |             |           |
            +<------------+ By rules  |
            |             |           |
+-----------v----------+  +-----------+
|                      |
|  Chinese Characters  +--> Post Processes ...
|                      |
+----------------------+
```

According to transliteration tables, some languages have phonetics system. For them we need to translate raw names
 input to phonetic at first and then translate phonetics to Chinese characters. See process details in 
 [Transliteration Rules](src/translators/data/README). And some processes that structured rules can't described are
 listed in `.py` files.