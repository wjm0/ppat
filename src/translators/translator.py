import os
import json
import re
import sys


class IndexTranslator:
    """
    Transliterating by dictionary
    """

    def __init__(self):
        with open(os.path.join(sys.path[0], 'translators', 'data', 'index', 'people.json'), 'r') as people_json:
            with open(os.path.join(sys.path[0], 'translators', 'data', 'index', 'places.json'), 'r') as place_json:
                try:
                    print('Loading file "data/index/places.json" ... ', end='')
                    people_data = json.loads(people_json.read())
                    print('loaded.')
                    print('Loading file "data/index/people.json" ... ', end='')
                    place_data = json.loads(place_json.read())
                    print('loaded.')
                except json.JSONDecodeError as e:
                    print(str(e))
                    exit(1)
                else:
                    self.people_index = {}
                    self.places_index = {}

                    # build indexes
                    for m in people_data:
                        self.people_index[m['name']] = m
                    print('Places names data indexed!')
                    for n in place_data:
                        self.places_index[n['name']] = n
                    print('People names data indexed!')
                    print('Index Translator initialized successfully!')

    def search(self, keyword):
        """
        param: keyword 
        Must be a name of a place or a person.
        If contains backspace(s), it will output multiple results.
        
        return: [<dict>...]
        """
        assert isinstance(keyword, str)

        names = keyword.split(' ')  # e.g. names = "adam James"

        i = 0
        for name in names:
            names[i] = name.capitalize()
            i += 1

        results = {'people': {}, 'places': {}}

        # people names
        for name in names:
            people_index_item = self.people_index.get(name, -1)
            places_index_item = self.places_index.get(name, -1)
            if people_index_item != -1:
                results['people'][name] = people_index_item
            if places_index_item != -1:
                results['places'][name] = places_index_item

        return results


class NoRuleMatched(Exception):
    def __str__(self):
        return 'NO RULE MATCHED. CHECK YOUR RULE FILES'



class RuleTranslator:
    """
    Transliterating by rules
    """
    def __init__(self):
        self.rules = {}
        for file_path in os.listdir(os.path.join('.', 'data', 'rule')):
            if os.path.splitext(file_path)[1] == '.rule':
                print('Found rule file: {}...'.format(file_path), end='')
                with open(file_path, 'r') as rule_file:
                    print('loading...', end='')
                    self._load_rule(file_path, rule_file)
                    print('loaded!')
        print('All "*.rule" files in data/rule are loaded!')

    def _get_kv(self, line, line_number, lang_code):
        """
        Get a k, v pair from a line likes 'key   =  value'.
         Key and value could contains spaces but useless spaces between '=' will be removed
        :param line:
        :return: (k, v)
        """
        items = re.split(r'[\s]*=[\s]*]', line, lang_code)

        assert len(items) == 2, "Invalid key/value pair at line: {} \n in file: {}.rule".format(line_number, lang_code)

        return items[0], items[1]

    def _load_kv(self, line, current_section, line_number, lang_code):
        def parse_k_cv(k):  # Parse Key in Consonants/Vowels section: Get possible <pre> and <post>
            pre, match, post = '', '', ''
            for i in range(len(k)):
                if k[i] == ')':
                    pre = k[0: i]
                elif k[i] == '(':
                    post = k[i + 1:]
            match = k.lstrip(pre + ')').rstrip(post + '(')
            assert match is not '', \
                'Invalid key (<match> not found): {} in "{}" section at line {} in file {}.py'\
                    .format(current_section, k, line_number, lang_code)

            matches = re.split(r'\s*[|]\s*', match)

            try:
                pre.replace('\\C', self.rules[lang_code]['phonetics']['consonants'])   # replace \C to any consonants
                post.replace('\\C', self.rules[lang_code]['phonetics']['consonants'])  # replace \C to any consonants
                pre.replace('\\V', self.rules[lang_code]['phonetics']['consonants'])   # replace \V to any vowels
                post.replace('\\V', self.rules[lang_code]['phonetics']['consonants'])  # replace \V to any vowels
            except KeyError as e:
                print(str(e))
                print('.phonetics section should be ahead of .consonants and .vowels sections')
                print('at line {} in file {}.rule'.format(line_number, lang_code))
                exit(1)

            return pre, matches, post  # (<pre>, [<match1>, <match2>, ...], <post>)

        def parse_k_t(k):  # Parse Key in Transliteration section: 'm, n' --> (m, n)
            m, n = 0, 0
            for i in range(k):
                if k[i] == ',':
                    m = int(k[0, i])
                    n = int(k[i + 1:].lstrip(' '))
                    break
            assert m != 0 and n != 0, \
                'Invalid key (not a <x, y> pair): {} in ".transliteration" section at line {} in file {}.py'\
                    .format(k, line_number, lang_code)
            return m, n

        try:
            if current_section not in self.rules[lang_code].keys():
                self.rules[lang_code][current_section] = {}  # init 'current_section' as a dict
            k, v = self._get_kv(line, line_number, lang_code)

            # validate k/v
            if current_section == 'phonetics':
                assert k in ('consonants', 'vowels'), \
                    'Invalid key (should be "consonants" or "vowels"): "{}" ' \
                    'in ".phonetics" section at line {} in file {}.py' \
                        .format(k, line_number, lang_code)
                self.rules[lang_code][current_section][k] = '[' + v + ']+'
            elif current_section.startswith('consonants') or current_section.startswith('vowels'):
                # v should be a digit
                assert v.isdigit(), 'Value should be a digit in section "{}": line {} in file: {}.rule'\
                    .format(current_section, line_number, lang_code)
                self.rules[lang_code][current_section][parse_k_cv(k)] = int(v)
            elif current_section.startswith('transliteration'):
                # k should be a digit
                assert k.isdigit(), 'Key should be a digit in section "{}": line {} in file: {}.rule'\
                    .format(current_section, line_number, lang_code)
                self.rules[lang_code][current_section][parse_k_t(k)] = v
        except Exception as e:
            print('Error {} while loading k/v in "{}" section at line {} in file: {}.rule' \
                  .format(str(e), current_section, line_number, lang_code))
            exit(1)

    def _check_meta_k(self, k, line_number, lang_code):
        """
        Check whether the key in meta section is available.
        :param k:
        :param line_number:
        :param lang_code:
        :return:
        """
        self.available_meta_keys = ('language_name',)
        assert k in self.available_meta_keys, \
            'Invalid key in ".meta" section at line {} in file: {}.rule'.format(line_number, lang_code)

    def _load_rule(self, file_path, rule_file):
        """
        Load rules in "*.rule" file. Store it into self.rules
        :param file_path:
        :param rule_file:
        """
        current_section = ''
        line_number = 0
        lang_code = os.path.split(os.path.splitext(file_path)[0])[1]  # Get 'a' from '/c/d/a.rule'
        self.rules[lang_code] = {}
        available_sections = ('.phonetics',  # consonants + vowels
                              '.consonants people',
                              '.vowels people',
                              '.transliteration people'
                              '.consonants places',
                              '.vowels places',
                              '.transliteration places',
                              )
        for line in rule_file.readlines():  # this will **preserve** the \n at end of lines
            line_number += 1
            if line.startswith('//') or line.startswith('\n'):  # line of comment
                continue
            if line.startswith('.'):  # line of section header
                current_section = line.rstrip('\n').lstrip('.')  # current_section = 'XX XX'
                continue

            # If this line is not continued by starting with dot,
            # treat the line as a key/value pair section content
            if current_section == 'meta':  # meta information
                k, v = self._get_kv(line, line_number, lang_code)
                self._check_meta_k(k, line_number, lang_code)
                self.rules[lang_code]['meta'][k] = v
            elif current_section == 'to_phonetics':  # translate words to phonetics
                if '.to_phonetics' not in self.rules[lang_code].keys():  # init 'to_phonetics' as a list
                    self.rules[lang_code]['to_phonetics'] = []
                k, v = self._get_kv(line, line_number, lang_code)  # lines here will be 'out = in' or 'out = fun(in)'
                if k == 'out' and v == 'in':  # just copy words
                    self.rules[lang_code]['to_phonetics'].append(lambda x: x)
                elif re.match(r'\w+\(in\)', v) is not None:
                    function_name = v.split('(')[0]  # Get the function name and import it dynamically

                    assert os.path.exists(os.path.join('.', 'data', 'rule', lang_code + '.py')), \
                        'No such file: {}.py in "data/rule/" for {} in ".to_phonetic" section' \
                        ' at line {} in file: {}.rule'.format(lang_code, function_name, line_number, lang_code)

                    self.rules[lang_code]['.to_phonetics'].append(
                        __import__('data.rule.{}.{}'.format(lang_code, function_name)))
                else:
                    print('Error in ".to_phonetics" section at line {} in rule file: {}'.format(line_number, rule_file))
                    exit(1)
            elif current_section in available_sections:
                self._load_kv(line, current_section, line_number, lang_code)
            else:
                print('Invalid section name "{}" at line {} in rule file: {}'.format(current_section,
                                                                                     line_number, rule_file))
                exit(1)

    def _check_pre(self, pre_phonetic, pre):
        """
        Check whether pre_phonetic matches pre
        :param pre_phonetic:
        :param pre:
        :return: True if matched, else False
        """
        assert isinstance(pre_phonetic, str)
        assert isinstance(pre, str)

        if re.match(pre, pre_phonetic):
            return True
        else:
            return False

    def _check_post(self, post_phonetic, post):
        """
        Check whether post_phonetic matches post
        :param post_phonetic:
        :param post:
        :return:
        """
        assert isinstance(post_phonetic, str)
        assert isinstance(post, str)

        if re.match(post, post_phonetic):
            return True
        else:
            return False

    def _match(self, phonetic, start_index, rule):
        """
        Match a longest pattern in rule at the start index of phonetic
        If matched, return >=1.
        Else, return 0.
        :param phonetic: a complete phonetic of a word
        :param start_index: int: start index of the phonetic that need to match
        :param rule: self.rule[lang_code + category]
        :return: (<value of the matched rule>, <length of pattern>)
        """
        assert isinstance(rule, dict)
        assert isinstance(start_index, int)
        assert isinstance(phonetic, str)

        match_pattern = ''
        match_index = 0

        for k in rule.keys():  # k = ('<pre>', [<match1>, <match2>, ...], '<post>'), v = 'str(int)'
            pre = k[0]
            post = k[1]

            for match in k[1]:
                if phonetic[start_index:].startswith(match):
                    if k[0]:  # Have <pre>
                        if not self._check_pre(phonetic[0:start_index], pre):
                            break  # invalid match, check next
                    if k[2]:  # Have <post>
                        if not self._check_post(phonetic[start_index + 1:], post):
                            break  # invalid match, check next
                    # <pre> and <post> are both satisfied, compare the match length
                    if len(match) > len(match_pattern):
                        match_pattern = match
                        match_index = rule[k]

        assert match_index != 0, 'No match pattern: check your .rule file'

        return match_index, len(match_pattern)

    def _find(self, coord_c, coord_v, l_rule_t):
        """
        Find chinese transliteration at (coord_c, coord_v) of l_rule_t
        :param coord_c: coordinate of consonants row
        :param coord_v: coordinate of vowels column
        :param l_rule_t:
        :return:
        """
        assert isinstance(coord_c, int)
        assert isinstance(coord_v, int)

        try:
            r = l_rule_t[(coord_c, coord_v)]
        except KeyError:
            raise NoRuleMatched()
        return r

    def __phonetics2chinese(self, _phonetics, category):
        """
        Phonetic to chinese in the l_rule's category
        :param _phonetics: a 1-layer list ['word1's phonetics', 'word2's phonetics', ...]
        :param category:
        :return:
        """
        l_rule_c = self.l_rule['.consonants ' + category]       # .consonants      section's rules
        l_rule_v = self.l_rule['.vowels ' + category]           # .vowels          section's rules
        l_rule_t = self.l_rule['.transliteration ' + category]  # .transliteration section's rules

        r = ''

        start_index = 0
        for _phonetic in _phonetics:  # for 'phonetic (of one word)' in ['pho1', 'pho2', ...] (of words)
            coord_v, p_len = self._match(_phonetic, start_index, l_rule_v)          # Match longest pattern in vowels column.
            if coord_v:                                                             # If matched,
                r += self._find(1, coord_v, l_rule_t)                               # find chinese at (1, coord_v).
                start_index += p_len                                                # start index ++
            else:                                                                   # Else,
                coord_c, p_len = self._match(_phonetic, start_index, l_rule_c)      # Match longest pattern in consonants row.
                if coord_c:                                                         # If matched,
                    start_index += p_len                                            # Excepted the matched consonant
                    coord_v, p_len = self._match(_phonetic, start_index, l_rule_v)  # Match longest pattern in vowels column.
                    if coord_v:
                        r += self._find(coord_c, coord_v, l_rule_t)                 # find chinese at (coord_c, coord_v)
                        start_index += p_len
                    else:
                        r += self._find(coord_c, 1, l_rule_t)
                else:
                    raise NoRuleMatched()
        return r

    def _phonetics2chinese(self, phonetics):
        """
        Translate phonetics to chinese in rule

        self.rule Example:

        {'.meta':
            {'language_name':''},
         '.to_phonetic': [fun1, fun2, ...],
         '.consonants people': [rule1, rule2, ...],
         '.vowels people': [rule1, rule2, ...],
         '.transliteration people': [rule1, rule2, ...],
         '.consonants places': [rule1, rule2, ...],
         '.vowels places': [rule1, rule2, ...],
         '.transliteration places': [rule1, rule2, ...],
        }
        :param phonetics: list of phonetics -- [[], [], ...]
        :return:

        [                         <-- r
            {                     <-- r[0]
                'people': 'XXX',  <----from phonetics[0]
                'places': 'XXX',  <----from phonetics[0]
            },
            {                     <-- r[1]
                'people': 'XXX',  <----from phonetics[1]
                'places': 'XXX',  <----from phonetics[1]
            },
            ...
        ]

        """

        r = []
        for _phonetics in phonetics:
            r.append({
                'phonetics': ''.join(_phonetics),  # Full phonetics display
                'people': self.__phonetics2chinese(_phonetics, 'people'),
                'places': self.__phonetics2chinese(_phonetics, 'places'),
            })
        return r

    def _words2phonetics(self, funcs, words):
        """

        :param funcs: translation function
        :param words: list
        :return:

        r1 ---> [
        r2 --->     ['pho1', 'pho2', ...],  # gen by func1
        r2 --->     ['pho3', 'pho4', ...],  # gen by func2
                    ...
                ]
        """
        r1 = []
        for func in funcs:
            r2 = []
            for word in words:
                r2.append(func(word))
            r1.append(r2)
        return r1

    def translate(self, words, lang_codes):
        """
        Outer interface, translate words into chinese characters in selected cultures.
        :param words:
        :param lang_code: list: if empty, select all lang_codes.
        :return:
        """
        assert isinstance(words, str) and isinstance(lang_codes, list)

        _words = words.split(' ')
        # Combine lang_codes
        _lang_codes = []
        if len(lang_codes) == 0:
            _lang_codes = self.rules.keys()
        else:
            for m in self.rules.keys():
                for n in lang_codes:
                    if m == n:
                        _lang_codes.append(m)
                        break

        results = []  # store results for every lang_code [<lang_code1>, <lang_code2>, ...]

        for _lang_code in _lang_codes:
            # Select rule for lang_code
            self.l_rule = self.rules[_lang_code]  # lang_code specified rule
            result = {'lang_code': _lang_code, 'transliterations': {}}  # store result for lang_code

            # to phonetics
            phonetics = self._words2phonetics(self.l_rule['.to_phonetics'], words)  # 2-layer list

            result['transliterations'] = self._phonetics2chinese(phonetics)
            results.append(result)

        return results
