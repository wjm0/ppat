"""
Transliterate in CLI mode
"""
import sys

from translators.translator import IndexTranslator, RuleTranslator


index_translator = IndexTranslator()

rule_translator = RuleTranslator()

if __name__ == '__main__':
    words = sys.argv[1]

    lang_codes = []

    for l in sys.argv[2: ]:
        lang_codes.append(l)

    print('Result:')
    print('From dictionary:')
    print(index_translator.search(words))
    print('From rule:')
    print(rule_translator.translate(words, lang_codes))
