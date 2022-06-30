
from soynlp.hangle import jamo_levenshtein

s1 = '안녕핳시오'
s2 = '안녛 하시오'
s1 = str(s1.replace(" ", ""))
s2 = str(s2.replace(" ", ""))

print(jamo_levenshtein(s1, s2)) # 0.3333333333333333