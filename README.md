# People & Place Automated Translator

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
> python src/translators/translator.py
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
|                          |                          |   Layer
|                          |                          |
|    Index Transalator     |   Algorithm Translator   |
|                          |                          | <-- Could be a standalone CLI program
|                          |                          |     with another initializer, parameter
|                          |                          |     resolver and result displayer.
+-----^-----------+--------+-------^------------+-----+
      |           |                |            |
+-----+-----------v-------+ +------+------------v-----+
|                         | |                         |
|    Index Data Reader    | |     Algorithm Loader    | Translate
|                         | |                         |   Layer
+-----^-------------------+ +-------------------^-----+
      |                                         |
+-----+------------------------------+ +--------+-----+   Rule
| people.data.json & place.data.json | | t.csv & t.py |  Storage
+------------------------------------+ +--------------+   Layer
```

We will analysis this structure following a Top-Down level method.

## Frontend

We give two ways to use PPAT: Web and CLI. The web server also calls the PPAT_CLI for result and displays it to the
 frontend. Both Web and CLI accept the following parameters:

1. Keyword: The name you want to translate.
2. Language or Culture: The culture that the keyword belongs.
3. Place or People: Optional. Whether the name is a place or a person.

The frontend also receive a response from the PPAT web server, witch contains a JSON object described below:

```json
{
    "index": [
        {
            "keyword": "Keyword you search",
            "culture": "The culture that the translation belongs",
            "chinese": "The translation of the keyword"
        }
    ],
    "algorithm": [
        {
            "keyword": "Keyword you search",
            "culture": "The table that the translation uses",
            "chinese": "The translation of the keyword",
            "category": "woman/man/place"
        }
    ],
    "meta": {
        "elapsed_time": 328
    }
}
```

The frontend also needs a API to get all available cultures.

## Web Service Layer

This layer resolve parameters from frontend and also format results from `Translator`s. Be aware of the initialization
 of it. When the web server starts, it should only read the Transliteration Table **once** for the best performance.

## Translator Layer

```
+----------------------+
|                      |
| Raw Input (UTF-8)    |
|                      |
+-----------+----------+  +-----------+
            |             |           |
            +<------------+ By eSpeak |
            |             |           |
+-----------v----------+  +-----------+
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

According to transliteration tables, some languages have its phonetics system. We need to translate raw names input to
 phonetic first and then translate phonetics to Chinese characters. See details in 
 [Transliteration Rules](docs/transliteration_rules.md). And some processes that structured rules can't described are
 listed in `.py` files.