# wiki_parse
parses wikipedia xml dumps mediocrally. Storing here for ease of pointing. I think most people use cirrus extractor instead.

## USE

```cat swwiki-20200120-pages-articles-multistream.xml | python wiki_parse.py```
or
```python wiki_parse.py --input swwiki-20200120-pages-articles-multistream.xml```

I do not believe any of the other parameters are super functional.

## Known problems

1. Unbalanced tags. I think to some extent this was problems with the xml but it happens often enough that there is probably also a bug in the script. If a balance error is caught, it prints "Unbalanced tags!" instead of the content and skips.
2. IPA/other special symbol rendering. If I recall correctly, I think there's also an issue with some footnote/citation/links because of the way wikipedia handles them.
