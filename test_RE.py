import re

s = '''00:41:35 (+14) tiger_mafia_zulu: OMEGALUL
00:41:36 (+1) speakingfox: млж
00:41:38 (+2) avtomaton: SeemsGood SeemsGood SeemsGood SeemsGood SeemsGood
00:41:39 (+1) Daredo_: OMEGALUL
00:41:45 (+6) XsizR: KEKW
00:41:46 (+1) J_Bandit: WutFace LUL
00:41:47 (+1) Cyrpedon: OMEGALUL
00:41:47 (+1) Cyrpedon: ахаххахахаха))
00:41:56 (+9) Andrewhous: :D'''

re_smiles = r'^\d{2}:\d{2}:\d{2}\s\(\+\d*\)\s\S*\s(.*)'  # re.IGNORECASE
l = s.split('\n')
for i in range(8):
    l2 = l[i]
    # print(l2)
    m = re.search(re_smiles, l2)
    msg = m.group(1).upper()
    print(msg)
    m2 = re.search(r'LUL|LAUGH|:D|KEKW|BSUTROLLED|^[ах]{3,}\)*|^хд*\)*[\s]*', msg, re.IGNORECASE)
    if m2:
        print(True)


def find_all(finding_str, s):
    occurences_count = 0
    k = -1
    while True:  # if s.find(finding_str, k) == -1:
        k = s.find(finding_str, k+1)
        if k != -1:
            occurences_count += 1
        else:
            break
    return occurences_count

print()
s = 'RAGE'
s2 = 'BSURAGE BSURAGE BSURAGE BSURAGE'

k = find_all(s, s2)
print(k)
