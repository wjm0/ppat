# TEXT TO CHINESE TRANSLITERATION

This approach was inspired by a TTS project called _eSpeak_ so we use many thoughts and expression in it. In a
 transliteration table we will see many **vowels** and **consonants** pairs and a few extra rules in natural language.
 Most of these can be translate into structured descriptions, with witch we use for processing words of names.

## To Phonetic Rules

The rules in the <lang_code>.tp file specify the Chinese characters which are used to transliterate each letter to
 phonetics. In some languages such as English, they have a very complex transformation rule. But most of languages' 
 rules are as simply as an one-shot reflection. This file is unnecessary when a language has no special phonetic system.

> book ===> bUk (English, with special phonetic system)
> gü   ===> gü (Spanish, simply copy them)


## Transliteration Rules

The rules in the <lang_code>.tl file specify the Chinese characters which are used to transliterate each letter
 (or phonetic), or sequence of letters (or phonetics). Some rules only apply when the letter or letters are preceded by,
 or followed by, other specified letters.
 
With so many rules, we still cannot get rid of those two bad situations:

1. Plural rules are matched: At first we should try our best to avoid these rules. However, when it happens we choose
 the first rules matched to process the word.
 
2. No matches found: This situation is not usually happens. You should check the rules' integrity at first, or raise an
 error.

### Rule Groups

The rules are organized in groups, each starting with a ".group" line:

- .group <character>

A group for each letter or character.

- .group <2 characters>

Optional groups for some common 2 letter combinations. This is only needed, for efficiency, in cases where there are
 many rules for a particular letter. They would not be needed for a language which has regular spelling rules. Any of
 them can be a non-ascii character.

- .group

A group for other characters which don't have their own group.

- .L<nn>

Defines a group of leter sequences, any of which can match with Lnn in a pre or post rule (see below). nn is a 2 digit
 decimal number in the range 01 to 25. eg:

> .L01 b bl br pl pr

- .replace

See section 4.7 Character Substitution, below.


When matching a word, firstly the 2-letter group for the two letters at the current position in the word
 (if such a group exists) is searched, and then the single-letter group. The highest scoring rule in either of those two
 groups is used.

### Rules

Each rule is on separate line, and has the syntax:

```
[<pre>)] <match> [(<post>] <Chinese Characters>
```

Alphabetic characters in the <pre>, <match>, and <post> parts are case-insensitive. Some upper case English letters are
 used in <pre> and <post> with special meanings.
 
 ### Special Characters in both <pre> and <post>

```
_	Beginning or end of a word
\A	Any vowel (the set of vowel characters may be defined for a particular language).
\C	Any consonant.
\B \H \F \G \Y 	These may indicate other sets of characters (defined for a particular language).
\L<nn>	Any of the sequence of characters defined as a letter group (see above chapter).
\K	Not a vowel (i.e. a consonant or word boundary or non-alphabetic character).
\X	There is no vowel until the word boundary.
\%	Doubled (placed before a character in <pre> and after it in <post>.
```

### Special Characters in <pre>

```
```

### Special Characters in <post>

```
```

### <Chinese Characters> section

```
甲/乙  Both "甲" and "乙" are OK
丙(丁) Use "丙" when translate a name of men, use "丁" for wemen
```

## Post Process Rules
