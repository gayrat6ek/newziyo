# -*- coding: utf-8 -*-
import re
import sys

LATIN_TO_CYRILLIC = {
    'a': 'а', 'A': 'А',
    'b': 'б', 'B': 'Б',
    'd': 'д', 'D': 'Д',
    'e': 'е', 'E': 'Е',
    'f': 'ф', 'F': 'Ф',
    'g': 'г', 'G': 'Г',
    'h': 'ҳ', 'H': 'Ҳ',
    'i': 'и', 'I': 'И',
    'j': 'ж', 'J': 'Ж',
    'k': 'к', 'K': 'К',
    'l': 'л', 'L': 'Л',
    'm': 'м', 'M': 'М',
    'n': 'н', 'N': 'Н',
    'o': 'о', 'O': 'О',
    'p': 'п', 'P': 'П',
    'q': 'қ', 'Q': 'Қ',
    'r': 'р', 'R': 'Р',
    's': 'с', 'S': 'С',
    't': 'т', 'T': 'Т',
    'u': 'у', 'U': 'У',
    'v': 'в', 'V': 'В',
    'x': 'х', 'X': 'Х',
    'y': 'й', 'Y': 'Й',
    'z': 'з', 'Z': 'З',
    'ʼ': 'ъ',  # TODO: case?
}
LATIN_VOWELS = (
    'a', 'A', 'e', 'E', 'i', 'I', 'o', 'O', 'u', 'U', 'o‘', 'O‘'
)

# These words cannot be reliably converted to cyrillic because of the lossy
# nature of the to_latin converter.
TS_WORDS = {
    'aberra(ts)ion': 'аберрацион',
}
# These words cannot be reliably transliterated into cyrillic
E_WORDS = {
    'bel(e)taj': 'бельэтаж',
    'bugun-(e)rta': 'бугун-эрта',
    'diqqat-(e)ʼtibor': 'диққат-эътибор',
    'ich-(e)t': 'ич-эт',
    'karat(e)': 'каратэ',
    'm(e)r': 'мэр',
    'obroʻ-(e)ʼtiborli': 'обрў-эътиборли',
    'omon-(e)son': 'омон-эсон',
    'r(e)ket': 'рэкет',
    'sut(e)mizuvchilar': 'сутэмизувчилар',
    'upa-(e)lik': 'упа-элик',
    'xayr-(e)hson': 'хайр-эҳсон',
    'qayn(e)gachi': 'қайнэгачи',
}
# Not to confuse with ш
SH_WORDS = {
    'a(sh)ob': 'асҳоб',
    'mu(sh)af': 'мусҳаф'
}
# Not to confuse with ё
YO_WORDS = {
    'general-ma(yo)r': 'генерал-майор',
    '(yo)g': 'йог',
    '(yo)ga': 'йога',
    '(yo)gurt': 'йогурт',
    '(yo)d': 'йод',
    '(yo)dlamoq': 'йодламоқ',
    '(yo)dli': 'йодли',
    'ma(yo)nez': 'майонез',
    'mikrorayon': 'микрорайон',
    'ma(yo)r': 'майор',
    'ra(yo)n': 'район',
}
YU_WORDS = {
    'mo(yu)pa': 'мойупа',
    'po(yu)stun': 'пойустун'
}
YA_WORDS = {
    'po(ya)bzal': 'пойабзал',
    'po(ya)ndoz': 'пойандоз',
    'po(ya)fzal': 'пойафзал'
}
YE_WORDS = {
    'i(ye)': 'ийе',
    'konve(ye)r': 'конвейер',
    'ple(ye)r': 'плейер',
    'sta(ye)r': 'стайер',
    'fo(ye)': 'фойе'
}
SOFT_SIGN_WORDS = {
    'aviamodel': 'авиамодель',

}

CYRILLIC_TO_LATIN = {
    'а': 'a', 'А': 'A',
    'б': 'b', 'Б': 'B',
    'в': 'v', 'В': 'V',
    'г': 'g', 'Г': 'G',
    'д': 'd', 'Д': 'D',
    'е': 'e', 'Е': 'E',
    'ё': 'yo', 'Ё': 'Yo',
    'ж': 'j', 'Ж': 'J',
    'з': 'z', 'З': 'Z',
    'и': 'i', 'И': 'I',
    'й': 'y', 'Й': 'Y',
    'к': 'k', 'К': 'K',
    'л': 'l', 'Л': 'L',
    'м': 'm', 'М': 'M',
    'н': 'n', 'Н': 'N',
    'о': 'o', 'О': 'O',
    'п': 'p', 'П': 'P',
    'р': 'r', 'Р': 'R',
    'с': 's', 'С': 'S',
    'т': 't', 'Т': 'T',
    'у': 'u', 'У': 'U',
    'ф': 'f', 'Ф': 'F',
    'х': 'x', 'Х': 'X',
    'ц': 's', 'Ц': 'S',
    'ч': 'ch', 'Ч': 'Ch',
    'ш': 'sh', 'Ш': 'Sh',
    'ъ': 'ʼ', 'Ъ': 'ʼ',
    'ь': '', 'Ь': '',
    'э': 'e', 'Э': 'E',
    'ю': 'yu', 'Ю': 'Yu',
    'я': 'ya', 'Я': 'Ya',
    'ў': 'oʻ', 'Ў': 'Oʻ',
    'қ': 'q', 'Қ': 'Q',
    'ғ': 'gʻ', 'Ғ': 'Gʻ',
    'ҳ': 'h', 'Ҳ': 'H',
}
CYRILLIC_VOWELS = (
    'а', 'А', 'е', 'Е', 'ё', 'Ё', 'и', 'И', 'о', 'О', 'у', 'У', 'э', 'Э',
    'ю', 'Ю', 'я', 'Я', 'ў', 'Ў'
)


def to_cyrillic(text):
    """Transliterate latin text to cyrillic  using the following rules:
    1. ye = е in the beginning of a word or after a vowel
    2. e = э in the beginning of a word or after a vowel
    3. ц exception words
    4. э exception words
    """
    # These compounds must be converted before other letters
    compounds_first = {
        'ch': 'ч', 'Ch': 'Ч', 'CH': 'Ч',
        # this line must come before 's' because it has an 'h'
        'sh': 'ш', 'Sh': 'Ш', 'SH': 'Ш',
        # This line must come before 'yo' because of it's apostrophe
        'yo‘': 'йў', 'Yo‘': 'Йў', 'YO‘': 'ЙЎ',
    }
    compounds_second = {
        'yo': 'ё', 'Yo': 'Ё', 'YO': 'Ё',
        # 'ts': 'ц', 'Ts': 'Ц', 'TS': 'Ц',  # No need for this, see TS_WORDS
        'yu': 'ю', 'Yu': 'Ю', 'YU': 'Ю',
        'ya': 'я', 'Ya': 'Я', 'YA': 'Я',
        'ye': 'е', 'Ye': 'Е', 'YE': 'Е',
        # different kinds of apostrophes
        'o‘': 'ў', 'O‘': 'Ў', 'oʻ': 'ў', 'Oʻ': 'Ў',
        'g‘': 'ғ', 'G‘': 'Ғ', 'gʻ': 'ғ', 'Gʻ': 'Ғ',
    }
    beginning_rules = {
        'ye': 'е', 'Ye': 'Е', 'YE': 'Е',
        'e': 'э', 'E': 'Э',
    }
    after_vowel_rules = {
        'ye': 'е', 'Ye': 'Е', 'YE': 'Е',
        'e': 'э', 'E': 'Э',
    }
    exception_words_rules = {
        's': 'ц', 'S': 'Ц',
        'ts': 'ц', 'Ts': 'Ц', 'TS': 'Ц',  # but not tS
        'e': 'э', 'E': 'э',
        'sh': 'сҳ', 'Sh': 'Сҳ', 'SH': 'СҲ',
        'yo': 'йо', 'Yo': 'Йо', 'YO': 'ЙО',
        'yu': 'йу', 'Yu': 'Йу', 'YU': 'ЙУ',
        'ya': 'йа', 'Ya': 'Йа', 'YA': 'ЙА',
    }

    # standardize some characters
    # the first one is the windows string, the second one is the mac string
    text = text.replace('ʻ', '‘')

    def replace_soft_sign_words(m):
        word = m.group(1)
        if word.isupper():
            result = SOFT_SIGN_WORDS[word.lower()].upper()
        elif word[0].isupper():
            result = SOFT_SIGN_WORDS[word.lower()]
            result = result[0].upper() + result[1:]
        else:
            result = SOFT_SIGN_WORDS[word.lower()]
        return result

    for word in SOFT_SIGN_WORDS:
        text = re.sub(
            r'\b(%s)' % word,
            replace_soft_sign_words,
            text,
            flags=re.U
        )

    def replace_exception_words(m):
        """Replace ц (or э) only leaving other characters unchanged"""
        return '%s%s%s' % (
            m.group(1)[:m.start(2)],
            exception_words_rules[m.group(2)],
            m.group(1)[m.end(2):]
        )
    # loop because of python's limit of 100 named groups
    for word in list(TS_WORDS.keys()) + list(E_WORDS.keys()):
        text = re.sub(
            r'\b(%s)' % word,
            replace_exception_words,
            text,
            flags=re.U
        )

    # compounds
    text = re.sub(
        r'(%s)' % '|'.join(compounds_first.keys()),
        lambda x: compounds_first[x.group(1)],
        text,
        flags=re.U
    )

    text = re.sub(
        r'(%s)' % '|'.join(compounds_second.keys()),
        lambda x: compounds_second[x.group(1)],
        text,
        flags=re.U
    )

    text = re.sub(
        r'\b(%s)' % '|'.join(beginning_rules.keys()),
        lambda x: beginning_rules[x.group(1)],
        text,
        flags=re.U
    )

    text = re.sub(
        r'(%s)(%s)' % ('|'.join(LATIN_VOWELS),
                       '|'.join(after_vowel_rules.keys())),
        lambda x: '%s%s' % (x.group(1), after_vowel_rules[x.group(2)]),
        text,
        flags=re.U
    )

    text = re.sub(
        r'(%s)' % '|'.join(LATIN_TO_CYRILLIC.keys()),
        lambda x: LATIN_TO_CYRILLIC[x.group(1)],
        text,
        flags=re.U
    )

    return text


def to_latin(text):
    """Transliterate cyrillic text to latin using the following rules:
    1. ц = s at the beginning of a word.
    ц = ts in the middle of a word after a vowel.
    ц = s in the middle of a word after consonant (DEFAULT in CYRILLIC_TO_LATIN)
        цирк = sirk
        цех = sex
        федерация = federatsiya
        функция = funksiya
    2. е = ye at the beginning of a word or after a vowel.
    е = e in the middle of a word after a consonant (DEFAULT).
    3. Сентябр = Sentabr, Октябр = Oktabr
    """
    beginning_rules = {
        'ц': 's', 'Ц': 'S',
        'е': 'ye', 'Е': 'Ye'
    }
    after_vowel_rules = {
        'ц': 'ts', 'Ц': 'Ts',
        'е': 'ye', 'Е': 'Ye'
    }

    text = re.sub(
        r'(сент|окт)([яЯ])(бр)',
        lambda x: '%s%s%s' % (x.group(1),
                              'a' if x.group(2) == 'я' else 'A', x.group(3)),
        text,
        flags=re.IGNORECASE | re.U
    )

    text = re.sub(
        r'\b(%s)' % '|'.join(beginning_rules.keys()),
        lambda x: beginning_rules[x.group(1)],
        text,
        flags=re.U
    )

    text = re.sub(
        r'(%s)(%s)' % ('|'.join(CYRILLIC_VOWELS),
                       '|'.join(after_vowel_rules.keys())),
        lambda x: '%s%s' % (x.group(1), after_vowel_rules[x.group(2)]),
        text,
        flags=re.U
    )

    text = re.sub(
        r'(%s)' % '|'.join(CYRILLIC_TO_LATIN.keys()),
        lambda x: CYRILLIC_TO_LATIN[x.group(1)],
        text,
        flags=re.U
    )

    return text


def transliterate(text, to_variant):
    if to_variant == 'cyrillic':
        text = to_cyrillic(text)
    elif to_variant == 'latin':
        text = to_latin(text)

    return text

if __name__ == "__main__":
    """cat input_in_lat.txt | python transliterate.py > output_in_cyr.txt"""
    for line in sys.stdin:
        sys.stdout.write(transliterate(line, 'cyrillic'))
