# wiki_parse
parses wikipedia xml dumps mediocrally. Storing here for ease of pointing. I think most people use cirrus extractor instead.

## USE

```cat swwiki-20200120-pages-articles-multistream.xml | python wiki_parse.py```
or
```python wiki_parse.py --input swwiki-20200120-pages-articles-multistream.xml```

I do not believe any of the other parameters are super functional.

## Example output

```
Sheria Unbalanced tags!
Mwanzo Unbalanced tags!
Akiolojia	Intro	Akiolojia (kutoka Kiyunani αρχαίος = zamani na λόγος = neno, usemi) ni somo linalohusu mabaki ya tamaduni za watu wa nyakati zilizopita. Wanaakiolojia wanatafuta vitu vilivyobaki, kwa mfano kwa kuchimba ardhi na kutafuta mabaki ya majengo, makaburi, silaha, vifaa, vyombo na mifupa ya watu.
Akiolojia	Akiolojia na historia	Tofauti na somo la Historia, akiolojia haichunguzi sana maandishi hasa ili kupata ufafanuzi wa mambo ya kale. Historia inatazama zaidi habari zilizoandikwa lakini akiolojia inatazama vitu vilivyobaki kutoka zamani. Wanaakiolojia wanaweza kutumia maandishi na habari za historia wakiamua jinsi gani waendelee na utafiti wao, kwa mfano wachimbe wapi. Lakini hutumia mitindo ya sayansi mbalimbali kuchunguza vitu vinavyopatikana kwa njia ya akiolojia.
Akiolojia	Akiolojia na historia	Kinyume chake, matokeo ya akiolojia ni chanzo muhimu kwa wachunguzi wa historia. Mara nyingi matokeo ya akiolojia yanaweza kupinga au kuthibitisha habari zilizoandikwa au kufungua macho kwa kuzielewa tofauti.
Akiolojia	Mfano wa Pompei	Mfano bora wa akiolojia ni utafiti wa mji wa Pompei huko Italia. Habari za Pompei zimepatikana katika maandishi mbalimbali ya Kiroma, lakini mji uliharibika kabisa na kufunikwa na majivu ya volkeno Vesuvio mwaka 79 B.K. 
```

## Known problems

1. Unbalanced tags. I think to some extent this was problems with the xml but it happens often enough that there is probably also a bug in the script. If a balance error is caught, it prints "Unbalanced tags!" instead of the content and skips.
2. IPA/other special symbol rendering. If I recall correctly, I think there's also an issue with some footnote/citation/links because of the way wikipedia handles them.
