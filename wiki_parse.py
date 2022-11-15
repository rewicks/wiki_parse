#!/usr/bin/env python

import sys
import argparse
from lxml import etree
import time
import re

# removes all text that occurs within open_ch close_ch (preserves balances) unless specified for the special case of [ something | something ]
units = {
        '24': 'Y',
        '21': 'Z',
        '18': 'E',
        '15': 'P',
        '12': 'T',
        '9': 'G',
        '6': 'M',
        '5': 'hk',
        '4': 'ma',
        '3': 'k',
        '2': 'h',
        '1': 'da',
        '-1': 'd',
        '-2': 'c',
        '-3': 'm',
        '-4': 'dm',
        '-5': 'cm',
        '-6': 'µ',
        '-9': 'n',
        '-12': 'p',
        '-15': 'f',
        '-18': 'a',
        '-21': 'z',
        '-24': 'y'
}
langs = {
        'ady': 'Adyghe',
        'af': 'Afrikaans',
        'sq': 'Albanian',
        'gsw': 'Alemannic German',
        'gct': 'Colonia Tovar Dialect',
        'swg': 'Swabian German',
        'wae': 'Walser German',
        'am': 'Amharic',
        'ar': 'Arabic',
        'hy': 'Armenian',
        'as': 'Assamese',
        'ast': 'Asturian',
        'ext': 'Extremaduran',
        'le': 'Leonese',
        'mwl': 'Mirandese',
        'aus': 'Australian Aboriginal languages',
        'az': 'Azerbaijani',
        'eu': 'Basque',
        'be': 'Belarusian',
        'bn': 'Bengali',
        'ber': 'Berber',
        'br': 'Breton',
        'bg': 'Bulgarian',
        'my': 'Burmese',
        'yue': 'Cantonese',
        'ca': 'Catalan',
        'va': 'Valencian',
        'ksh': 'Colognian',
        'co': 'Corsican',
        'cs': 'Czech',
        'da': 'Danish',
        'nl': 'Dutch',
        'arz': 'Egyptian Arabic',
        'egl': 'Emilian',
        'rgn': 'Romagnol',
        'en': 'English',
        'eo': 'Esperanto',
        'et': 'Estonian',
        'fj': 'Fijian',
        'fi': 'Finnish',
        'frp': 'Franco-Provençal',
        'fr': 'French',
        'gl': 'Galician',
        'ka': 'Georgian',
        'el': 'Greek',
        'grc': 'Greek',
        'gu': 'Gujarati',
        'ht': 'Haitian Creole',
        'haw': 'Hawaiian',
        'he': 'Hebrew',
        'acw': 'Hejazi Arabic',
        'hns': 'Hindustani',
        'hi': 'Hindi',
        'ur': 'Urdu',
        'hu': 'Hungarian',
        'is': 'Icelandic',
        'iu': 'Inuktitut',
        'ik': 'Inupiaq',
        'ga': 'Irish',
        'it': 'Italian',
        'itdia': 'Italian dialects',
        'ja': 'Japanese',
        'kk': 'Kazakh',
        'km': 'Khmer',
        'ko': 'Korean',
        'ku': 'Kurdish',
        'kmr': 'Kurmanji (Northern Kurdish)',
        'ckb': 'Sorani (Central Kurdish)',
        'sdh': 'Southern Kurdish',
        'ky': 'Kyrgyz',
        'lo': 'Lao',
        'la': 'Latin',
        'lv': 'Latvian',
        'apc': 'Lebanese Arabic',
        'lij': 'Ligurian',
        'lt': 'Lithuanian',
        'lmo': 'Lombard',
        'lb': 'Luxembourgish',
        'mk': 'Macedonian',
        'mg': 'Malagasy',
        'ms': 'Malay',
        'id': 'Indonesian',
        'ml': 'Malayalam',
        'mt': 'Maltese',
        'cmn': 'Standard Chinese',
        'gv': 'Manx',
        'mai': 'Maithili',
        'mi': 'Māori',
        'mr': 'Marathi',
        'mh': 'Marshallese',
        'mfe': 'Mauritian Creole',
        'myn': 'Mayan',
        'mn': 'Mongolian',
        'nah': 'Nahuatl',
        'nv': 'Navajo',
        'nap': 'Neapolitan',
        'ne': 'Nepali',
        'ss': 'Swazi',
        'xh': 'Xhosa',
        'zu': 'Zulu',
        'nod': 'Northern Thai',
        'no': 'Norwegian',
        'oc': 'Occitan',
        'or': 'Odia',
        'ang': 'Old English',
        'fa': 'Persian',
        'pms': 'Piedmontese',
        'pl': 'Polish',
        'pt': 'Portuguese',
        'pa': 'Punjabi',
        'qu': 'Quechua',
        'ro': 'Romanian',
        'rm': 'Romansh',
        'ru': 'Russian',
        'sa': 'Sanskrit',
        'sc': 'Sardinian',
        'gd': 'Scottish Gaelic',
        'sh': 'Serbo-Croatian',
        'hr': 'Croatian',
        'sr': 'Serbian',
        'shn': 'Shan',
        'khb': 'Tai Lue',
        'scn': 'Sicilian',
        'sk': 'Slovak',
        'sl': 'Slovene',
        'es': 'Spanish',
        'de': 'German',
        'sw': 'Swahili',
        'sv': 'Swedish',
        'tl': 'Tagalog',
        'taiwain': 'Taiwanese Hokkien',
        'ta': 'Tamil',
        'tt': 'Tatar',
        'te': 'Telugu',
        'th': 'Thai',
        'bo': 'Tibetan',
        'ti': 'Tigrinya',
        'aeb': 'Tunisian Arabic',
        'tr': 'Turkish',
        'tk': 'Turkmen',
        'uk': 'Ukrainian',
        'uz': 'Uzbek',
        'vec': 'Venetian',
        'vi': 'Vietnamese',
        'wa': 'Walloon',
        'cy': 'Welsh',
        'fy': 'West Frisian',
        'yi': 'Yiddish',
        'ace': 'Acehnese',
        'aec': 'Saidi Arabic',
        'afb': 'Gulf Arabic',
        'ain': 'Ainu',
        'ak': 'Akan (Fante, Twi)',
        'akk': 'Akkadian',
        'alg': 'Algonquian (Micmac, Cree)',
        'als': 'Albanian dialects',
        'an': 'Aragonese',
        'arn': 'Mapuche',
        'art': 'artificial (Ido, Tolkien, etc.)',
        'ath': 'Athabaskan (Dene, Navajo)',
        'ay': 'Aymara',
        'azc': 'Uto-Aztecan (Shoshone, Comanche)',
        'ba': 'Bashkir',
        'bar': 'Bavarian',
        'bm': 'Manding/Bambara',
        'bodia': 'Bodish',
        'cau': '(North) Caucasian',
        'cel': 'Celtic (Brythonic, Gaulish)',
        'ch': 'Chamorro',
        'cop': 'Coptic',
        'csb': 'Kashubian',
        'cv': 'Chuvash',
        'dedia': 'German dialects',
        'dv': 'Dhivehi',
        'dz': 'Dzongkha',
        'ee': 'Gbe (Ewe, Fon)',
        'endia': 'English dialects',
        'enm': 'Middle English',
        'esdia': 'Spanish dialects',
        'fo': 'Faroese',
        'frdia': 'French dialects (Canadian, Metis, Norman)',
        'fur': 'Friulian',
        'gag': 'Gagauz',
        'gez': 'Ge\'ez',
        'gn': 'Guaraní',
        'guc': 'Wayuu',
        'ha': 'Hausa',
        'hak': 'Hakka',
        'hmn': 'Hmong',
        'ig': 'Igbo',
        'iro': 'Iroquoian (Mohawk, Cherokee)',
        'jv': 'Javanese',
        'ki': 'Kikuyu',
        'kjq': 'Western Keres',
        'kl': 'Greenlandic',
        'kn': 'Kannada',
        'kok': 'Konkani',
        'ks': 'Kashmiri',
        'ksw': 'S\'gaw Karen',
        'kw': 'Cornish',
        'lad': 'Ladino',
        'lg': 'Ganda',
        'li': 'Limburgish',
        'lld': 'Ladin',
        'ltc': 'Middle Chinese',
        'lzz': 'Laz',
        'maz': 'Central Mazahua',
        'mga': 'Middle Irish',
        'mid': 'Neo-Mandaic',
        'mnc': 'Manchu',
        'mnw': 'Mon',
        'moh': 'Mohawk',
        'mos': 'Mossi/Gurunsi',
        'mus': 'Muskogean (Chickasaw, Creek)',
        'na': 'Nauruan',
        'nan': 'Minnan/Taiwanese',
        'ncl': 'Classical Nahuatl',
        'nds': 'Low Saxon',
        'non': 'Old Norse',
        'nus': 'Nuer',
        'ny': 'Chewa',
        'oax': 'Oaxaca (Zapotec, Mixe, Otomi)',
        'om': 'Oromo',
        'os': 'Ossetian',
        'pap': 'Papiamento',
        'pdc': 'Pennsylvania German',
        'pi': 'Pali (linked to Sanskrit)',
        'pjt': 'Pitjantjatjara',
        'poly': 'Polynesian',
        'ps': 'Pashto',
        'ptdia': 'Portuguese dialects',
        'qya': 'Quenya',
        'rej': 'Rejang',
        'rw': 'Rwanda-Rundi',
        'ryu': 'Okinawan langs',
        'sal': 'Salish & NW Coast',
        'sco': 'Scots',
        'sd': 'Sindhi',
        'sec': 'Sechelt',
        'sei': 'Seri',
        'sem': '(ancient) Semitic, Egyptian',
        'sga': 'Old Irish',
        'si': 'Sinhala',
        'sio': 'Siouan (Omaha, Lakota)',
        'sjn': 'Sindarin',
        'sla': 'Slavic (old Slavic, Silesian, Sorbian)',
        'sm': 'Samoan',
        'sn': 'Shona',
        'so': 'Somali',
        'sotho': 'Sotho',
        'stq': 'Saterland Frisian',
        'su': 'Sundanese',
        'sux': 'Sumerian',
        'sva': 'Svan',
        'syc': 'Classical Syriac',
        'syr': 'Syriac',
        'tet': 'Tetum',
        'tix': 'Southern Tiwa',
        'tlh': 'Klingon',
        'tn': 'Tswana',
        'to': 'Tongan',
        'tyv': 'Tuvan',
        'tzl': 'Talossan',
        'ug': 'Uyghur',
        'wad': 'Wandamen',
        'wo': 'Wolof',
        'wbp': 'Warlpiri',
        'wuu': 'Wu/Shanghainese',
        'xmf': 'Mingrelian',
        'yo': 'Yoruba',
        'nci': 'Classical Nahuatl'
}

x_sampa = {
        'a' : 'a',
        'b' : 'b',
        'b_<' : 'ɓ',
        'c' : 'c',
        'd' : 'd',
        'd`' : 'ɖ',
        'd_<' : 'ɗ',
        'e' : 'e',
        'f' : 'f',
        'g' : 'g',
        'g_<' : 'ɠ',
        'h' : 'h',
        'h\\' : 'ɦ',
        'i' : 'i',
        'j' : 'j',
        'j\\' : 'ʝ',
        'k': 'k',
        'l': 'l',
        'l`' : 'ɭ',
        'l\\' : 'ɺ',
        'm' : 'm',
        'n' : 'n',
        'n`' : 'ɳ',
        'o' : 'o',
        'p' : 'p',
        'p\\' : 'ɸ',
        'q' : 'q',
        'r' : 'r',
        'r`' : 'ɽ',
        'r\\' : 'ɹ',
        'r\\`' : 'ɻ',
        's' : 's',
        's`' : 'ʂ',
        's\\' : 'ɕ',
        't' : 't',
        't`' : 'ʈ',
        'u' : 'u',
        'v' : 'v',
        'v\\' : 'ʋ',
        'w' : 'w',
        'x' : 'x',
        'x\\' : 'ɧ',
        'y' : 'y',
        'z' : 'z',
        'z`' : 'ʐ',
        'z\\': 'ʑ',
        'A' : 'ɑ',
        'B' : 'β',
        'B\\' : 'ʙ',
        'C' : 'ç',
        'D' : 'ð',
        'E' : 'ɛ',
        'F' : 'ɱ',
        'G' : 'ɣ',
        'G\\' : 'ɢ',
        'G\\_<' : 'ʛ',
        'H' : 'ɥ',
        'H\\' : 'ʜ',
        'I' : 'ɪ',
        'I\\' : 'ᵻ',
        'J' : 'ɲ',
        'J\\' : 'ɟ',
        'J\\_<' : 'ʄ',
        'K' : 'ɬ',
        'K\\' : 'ɮ',
        'L' : 'ʎ',
        'L\\' : 'ʟ',
        'M' : 'ɯ',
        'M\\' : 'ɯ',
        'N' : 'ŋ',
        'N\\' : 'ɴ',
        'O' : 'ɔ',
        'O\\' : 'ʘ',
        'P' : 'ʋ',
        'v\\' : 'ʋ',
        'Q' : 'ɒ',
        'R' : 'ʁ',
        'R\\' : 'ʀ',
        'S' : 'ʃ',
        'T' : 'θ',
        'U' : 'ʊ',
        'U\\' : 'ᵿ',
        'V' : 'ʌ',
        'W' : 'ʍ',
        'X' : 'χ',
        'X\\' : 'ħ',
        'Y' : 'ʏ',
        'Z' : 'ʒ',
        '.' : '.',
        '"' : 'ˈ',
        '%' : 'ˌ',
        '\'' : 'ʲ',
        '_j' : 'ʲ',
        ':' : 'ː',
        ':\\' : 'ˑ',
        '-' : '',
        '@' : 'ə',
        '@\\' : 'ɘ',
        '@`' : 'ɚ',
        '{' : 'æ',
        '}' : 'ʉ',
        '1' : 'ɨ',
        '2' : 'ø',
        '3' : 'ɜ',
        '3\\' : 'ɞ',
        '4' : 'ɾ',
        '5' : 'ɫ',
        '6' : 'ɐ',
        '7' : 'ɤ',
        '8' : 'ɵ',
        '9' : 'œ',
        '&' : 'ɶ',
        '?' : 'ʔ',
        '?\\' : 'ʕ',
        '<\\' : 'ʢ',
        '>\\' : 'ʡ',
        '^' : 'ꜛ',
        '!' : 'ꜜ',
        '!\\' : 'ǃ',
        '|' : '|',
        '|\\' : 'ǀ',
        '||' : '‖',
        '|\\|\\' : 'ǁ',
        '=\\' : 'ǂ',
        '-\\' : '‿',
        '_"' : ' ̈',
        '_+' : ' ̟',
        '_-' : ' ̠',
        '_/' : ' ̌',
        '_0' : ' ̥',
        '=' : ' ̩',
        '_=' : ' ̩',
        '_>' : 'ʼ',
        '_?\\' : 'ˤ',
        '_\\' : ' ̂',
        '_^' : ' ̯',
        '_}' : ' ̚',
        '`' : '˞',
        '~' : ' ̃',
        '_~' : ' ̃',
        '_A' : ' ̘',
        '_a' : ' ̺',
        '_B' : ' ̏',
        '_B_L' : ' ᷅',
        '_c' : ' ̜',
        '_d' : ' ̪',
        '_e' : ' ̴',
        '<F>' : '↘',
        '_F' : ' ̂',
        '_G' : 'ˠ',
        '_H' : ' ́',
        '_H_T' : ' ᷄',
        '_h' : 'ʰ',
        'ʲ' : '_j',
        '_k' : ' ̰',
        '_L' : ' ̀',
        '_l' : 'ˡ',
        '_M' : ' ̄',
        '_m' : ' ̻',
        '_N' : ' ̼',
        '_n' : 'ⁿ',
        '_O' : ' ̹',
        '_o' : ' ̞',
        '_q' : ' ̙',
        '<R>' : '↗',
        '_R' : ' ̌',
        '_R_F' : ' ᷈',
        '_r' : ' ̝',
        '_T' : ' ̋',
        '_t' : ' ̤',
        '_v' : ' ̬',
        '_w' : 'ʷ',
        '_X' : ' ̆',
        '_x' : ' ̽',
        '_' : ' ',
        ',_' : ', '
}


# adds the prefix to scientific notation xml values
def fix_units(content):
    try:
        value = content.split('|')[1]
        if 'e' in content.split('|')[2]:
            try:
                prefix = units[content.split('|')[2][2:]]
            except:
                return ''
        else:
            prefix = ''
        value += f' {prefix}{content.split("|")[-1][2:]}'
        return value
    except:
        return '' 


def clean_ipa(content):
    content = content.split('|')
    lang_id = content[0].split('-')[-1]
    language = langs[lang_id]
    content.remove(content[0])
    prefix = ''
    if 'pron' in content:
        prefix = 'pronounced'
        content.remove('pron')
    elif 'lang' in content:
        prefix = language
        content.remove('lang')
    else:
        prefix = lang_id + " Pronunciation:"
    things_to_remove = []
    for c in content:
        if ".wav" in c or ".ogg" in c or ".oga" in c or ".flac" in c or "audio=" in c or ".mp3" in c:
            this_to_remove.append(c)
    for r in things_to_remove:
        content.remove(r)
    ipa_output = '/'
    for c in content:
        if c not in x_sampa and (c == content[0] or c == content[1]):
            prefix = c
        if c not in x_sampa:
            ipa_output += c
        else:
            ipa_output += x_sampa[c]
    ipa_output += '/'
    return prefix + ' ' + ipa_output

# deletes text within {} and []
# optionally keeps the last option in []
# or converts certain types of {} to a printable format (ie quotes or values)
def clean_brackets(content, open_ch, close_ch, title, keep_inside=False):
    stack = []
    output = ''
    inside = ''
    for s in content:
        
        # when the stack is empty, we are not within a bracketed text
        if s == open_ch:
            stack.append(s)
        elif s == close_ch:

            # a non-zero number of wikipedia articles have malformatted brackets
            # or peculiar edge cases. In this case, it will simply ignore these,
            # so they will be in the resulting text
            try:
                stack.pop(0)
            except:
                print(f'{title} Exception found with unbalanced parentheses!')
            
            # wikipedia uses [] for links with various information inside
            # the last section appears to be the one that actually shows up in text
            if keep_inside and open_ch == '[' and len(stack) == 0:
                if ':' not in inside:
                    output += inside.split('|')[-1]
                elif 'http' in inside:
                    # this handles the edge case with urls within the links (instead of other articles)
                    output += ' '.join(inside.split(' ')[1:])
                inside = ''
            
            # {} mostly contains irrelevant xml information, but it also contains formatting for a few cases that we want to remain in text
            # the first is values in scientific notation
            # the second is quotes (which is not always used either)
            elif keep_inside and open_ch == '{' and len(stack) == 0:
                if 'val' == inside.split('|')[0].strip():
                    output += fix_units(inside)
                elif '|quote=' in inside:
                    inside = clean_brackets(inside.split('|quote=')[-1], '{', '}', title, keep_inside=True)
                    inside = clean_brackets(inside, '[', ']', title, keep_inside=True)
                    inside = inside.split('|')[0]
                    output += inside
                output += inside
                inside = ''
        elif len(stack) == 0:
            output += s
        else:
            inside += s
    return output


# paragraph boundaries are determined by where there are two new lines in the text
# there are a couple of edge cases where this is not the case (lists and headers) so 
# it is reformated so two new lines become one and one becomes zero
def reformat_lines(content):
    content = content.replace('=\n', '=\n\n')
    content = content.replace('\n=', '\n\n=')
    content = content.replace('\n*', '\n\n*')
    content = content.replace('\n#', '\n\n#')
    content = content.replace('\n:', '\n\n:')
    content = content.replace('\n', '\u2581')
    content = content.replace('\u2581\u2581', '\n')
    content = content.replace('\u2581', ' ')
    return content

# formats each paragraph by prefixing headers (delineated by tabs)
# in order to limit the number of lists, we regulate that we only
# include a section if at least punc_percent of lines do not end in a a-z character
def format(content,title, punc_percent=0.66):
    output = ''
    header_prefix = 'Intro'
    count = 0
    num_punc = 0
    
    content = reformat_lines(content)
    content = clean_text(content, title)
    section = ''
    
    for line in content.split('\n'):
        if line.strip() != '':
            
            # wikipedia starts section headers with = where the number denotes the level
            if '=' == line.strip()[0]:
                header_prefix = line.replace('=', '')
                # ensure there are a sufficient number of lines that end in punctuation
                if len(section.strip().split()) > 1:
                    if num_punc / len(section.split('\n')[:-1]) >= punc_percent:
                        output += section
                section = ''
                num_punc = 0
            else:
                # handles malformatting when a article has a phonetic description in its intro
                line = line.replace('(; ', '(')
                
                # skips empty lines, math equations, and some citations (:)
                if line.strip() != '' and line.strip()[0] != ':':
                    
                    # makes sure this is not a redirect
                    # I believe this will take care of redirects regardless of language
                    # but it will remove any element of a list that happens to be malformatted
                    # and is only one word
                    # the '#' is xml for a numbered list, so the numbers are restored
                    if len(line) > 0:
                        if '#' in line and line.strip()[0] == '#' and '#redirect' not in line.lower():
                            line = line.replace('#', str(count+1) + '.')
                            count += 1
                        else:
                            count = 0                    

                    # '*' is sometimes followed by only xml text (ie brackets or something), so
                    # we only include if it has content
                    if len(line.split()) > 2: 
                        section += f'{title.strip()}\t{header_prefix.strip()}\t{line.strip()}\n'
                        if line.strip()[-1] in [';', ':', '\'', '"', ',', '.', '?', '!', '$', '%']:
                            num_punc += 1
    return output  


# cleans html tags in the xml. They tend to be quite messy because of all the refs
def clean_tags(content, title):
    
    # while paused, we stop adding the character stream to output
    PAUSE = False
    output = ''

    # stack works the same as the bracket cleaner to keep track of balance
    stack = []
        
    # comment is if the last tag was a comment--< but not closing tag
    COMMENT = False
    for i, c in enumerate(content):
        if c == '<' and not COMMENT:
            try:
                if content[i+1] == '/':
                    if len(stack) == 0:
                        print(f"{title} Unbalanced tags!")
                    else:
                        stack.pop(0)
                elif content[i+1] == '!':
                    COMMENT = True
                    stack.append('<')
                    PAUSE = True
                else:
                    stack.append('<')
                    PAUSE = True
            except:
                pass
        elif c == '>':
            if not COMMENT:
                try:
                    if content[i-1] == '/' and len(stack) > 0:
                        stack.pop(0)
                    if len(stack) == 0:
                        PAUSE = False
                except:
                    pass
            else:
                if len(stack) == 0:
                    print(f"{title} Unbalanced tags!")
                stack.pop(0)
                COMMENT = False
        elif not PAUSE:
            output += c
    return output
        
# gets rid of extra html nonsense
def clean_text(content, title, citations=False):
    content = content.replace('&lt', '<')
    content = content.replace('&gt', '>')
    content = content.replace('<br>', '')
    content = clean_brackets(content, '{', '}', title, keep_inside=True)
    
    content = clean_tags(content, title)

    content = clean_brackets(content, '[',']', title, keep_inside=True)
    content = content.replace("\'\'\'", '')
    content = content.replace("\'\'", "")
    content = content.replace('&nbsp;', '')
    
    content = content.replace('* ', '*')
    content = content.replace('*', '* ')
    
    # this should also theoretically prevent most redirects
    if len(content.split()) > 5:
        return content
    return ''


#reads in and separates out just the pages
def batch_pages(input_file, batch_size):
    pages = []
    for line in input_file:
        if line.strip() == '<page>':
            pages.append(line)
        elif len(pages) > 0 and pages[-1][-8:] != '</page>\n':
            pages[-1] += line
        if line.strip() == '</page>' and len(pages) == batch_size:
            yield pages
            pages = []
    if len(pages) > 0:
        if pages[-1][-8:] != '</page>\n':
            yield pages[:-1]
        else:
            yield pages

def title_check(title):
    if ':' in title:
        if len(title.split(':')[1]) > 0:
            if title.split(':')[1][0] != ' ':
                return False
    return True

def process_batch(pages, output_file):
    restricted_formats = ['text/css', 'text/javascript']
    output = []
    for page in pages:
        xml = etree.fromstring(page)
        page_dict = {}
        page_dict['title'] = xml.find('title').text
        if title_check(page_dict['title']):
            revision = xml.find("revision")
            if revision.find("format").text not in restricted_formats:
                try:
                    text = revision.find("text").text
                    page_dict['text'] = format(text, page_dict['title'])
                except Exception as e:
                    page_dict['text'] = ""
            if page_dict['text'].strip() != '' and '#REDIRECT' not in page_dict['text'].upper():
                output.append(page_dict)
    for page in output:
        print(f'{page["text"]}'.strip(), file=output_file)

def fine_get_pages(input_file):
    last_page = ''
    page = []
    for line in input_file:
        if line.split('\t')[0] != last_page:
            if len(page) > 0:
                yield page
            page = [line]
        else:
            page.append(line)
        last_page = line.split('\t')[0]
    if len(page) > 0:
        yield page

def fine_process_page(page, output_file):
    disallowed_sections = ['See also', 'Bibliography', 'References', 'Footnotes', 'Further reading', 'Etymological bibliography', 'Sources', 'External links', 'Selected works']
    disallowed_titles = ['disambiguation']
    for line in page:
        if line.split('\t')[0].strip() not in disallowed_titles:
            if line.split('\t')[1].strip() not in disallowed_sections:
                print("\t".join(line.split("\t")[2:]).strip(),file=output_file)
    print('', file=output_file)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default=None)
    parser.add_argument('--output', default=None)
    parser.add_argument('--titles', action='store_true')
    parser.add_argument('--tags', default=None)
    parser.add_argument('--batch_size', type=int, default=100)
    parser.add_argument('--fine', action='store_true')

    args = parser.parse_args()

    if args.input is not None:
        input_file = open(args.input, 'r')
    else:
        input_file = sys.stdin

    if args.output is not None:
        output_file = open(args.output, 'w')
    else:
        output_file = sys.stdout

    if args.tags is None:
        args.tags = []
    else:
        args.tags = args.tags.split(',')
    accepted_tags = args.tags + ['text']

    if args.fine:
        for page in fine_get_pages(input_file):
            fine_process_page(page, output_file)    

    else:
        #start = time.time()
        for batch in batch_pages(input_file, args.batch_size):
            process_batch(batch, output_file)
        #end = time.time()
        #print(end-start)
