# parallel_corpora_cleaning
Abstract:
Kinda rough python script for cleaning parallel corpora from irrelevant to machine translation models entries.

When provided sentence-aligned \n separated parallel corpora, cleaning is two steps for now:
1. Delete all the lines, which contain words, ocurring in the whole corpus only once (variable internally changeable).
2. Delete all the lines, consisting of more then 20% (internally changeable) special characters (any apart from alphabet and spaces).
