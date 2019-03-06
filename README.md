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
 of it. When the web server starts, it should only read the Transliterature Table **once** for the best performance.

## Translator Layer

The core and most complicated layer of PPAT.

### Index Translator Method Solutions

Because of some translations are conventional, though some are not very standardized, we use those translations in order
 to make it easier to search those names in search engines and reference articles.


We have download and formatted the _Place Names Of The World_ and _Names Of The World People_ data into json files,
 which contain an array of objects that have _english_, _culture_ and _chinese_ attributes. We can load the file into
 Python objects when the engine starts. The typical class is shown below:

```python
class IndexTranslator:
    def __init__(self):
        pass

    def search(self, keyword):
        pass
```

### Algorithm Translator Method Solutions

When we translate the names that cannot find in the reference articles and search engines, manually we use the
 Transliteration Table to match each vowels and consonants to get a standardized translation. But the table is 
 **not** a simple Finite Automata as it contains a lot of transaction rules. We will analysis those rules from
 common cases to complicated ones.

#### Common Cases Solution

See this part of Germany transliteration table:


| ------- | Consonants | b bb | p pp |
| ------- | ---------- | ---- | ---- |
| Vowels  | ---------- | 布   | 普    |
| a aa ah | 阿         | 巴   | 帕    |


1. If no charactors need to be scanned, program over. Scan the consonants row for a **longest** match. This can
 determine the column we choose, jump to 3. If cannot find any match, jump to 2.
2. Scan the vowels column for a **longest** match. If find one, the cross cell of consonants column and the vowel row
 you match is the output. Drop what have been transliterated, jump to 1. Otherwise, raise an error.
3. Scan the next few words to the matched consonant in the vowel column for a **longest** match. If find one, the cross
 cell of consonants column and the vowel row you match is the output. Drop what have been transliterated, jump to 1.
 Otherwise, raise an error.


This algorithm can be simply implemented by a finite automata. But there are more rules you should follow
 **in and out of** the table.

### Solutions of Table Rules

Those rules are always marked in the tables so we call them _Table Rules_. Usually they can be marked out with special
 symbols so we can load them when our `AlgorithmTranslator` initialized. For example in the Germany Transliteration
 Table, some vowels only can be matched after a vowel, like `y`. And another example is that the same name can be
 translated for men and women, like `代` and `戴`.


Out of loading process, we shall record the states such as "just match a consonant" or "at the end of the word" and
 so on. When `match` process are executed, we will check those conditions to determine which row/column to be matched
 or just raised an error.

### Solutions of More Rules out of Tables

There are more complicated and tricky rules out of the table, which are at the end of the Transliteration Table PDF.
 They are described by natural language so we can't simply make a special mark or make the `match` function more
 complicated. So we should write a another `lang_code.py` file contains `match` `before_match` `after_match` processes
 for each specialized language.


In fact, some rules out of tables can be transmitted into the table. You should only write necessary rules in this file.

### Rule Storage

In order to manage the rules in a readable way, we store the data of rules into two separated files:

- lang_code.csv: Store structured data of rules in a comma separated values file. So the rules can be read by machine
 and people
- lang_code.py: Describe special rules that can't be stored in the csv file.
