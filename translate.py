import re

# defined longest to shortest
# src: https://www.dyslexia-reading-well.com/44-phonemes-in-english.html
# there are many grapheme duplicates, re-order or edit the lists as needed to prioritize/limit certain replacements

# [graphemes], replacement. if None, don't replace
VOWELS = [
    [["eigh", "aigh", r"a\we", "ea", "ey", "ai", "ay", "er", "et", "ei", "au", "a"], None],  # 0 eɪ bay, maid, weigh, straight, pay, foyer, filet, eight, gauge, mate, break, they
    [["augh", "ough", "oor", "oar", "ore", "our", "aw", "ar", "au", "or", "a"], None],  # 1 ɔ: paw, ball, fork, poor, fore, board, four, taught, war, bought, sauce
    [["ayer", "air", "are", "ear", "ere", "eir"], None],  # 2 eəʳ chair, dare, pear, where, their, prayer
    [["ough", "oew", r"u\we", "oo", "ew", "ue", "oe", "ui", "ou", "o"], None],  # 3 u: who, loon, dew, blue, flute, shoe, through, fruit, manoeuvre, group
    [["eigh", "igh", r"i\we", "ye", "uy", "ai", "is", "ie", "i", "y"], None],  # 4 aɪ spider, sky, night, pie, guy, stye, aisle, island, height, kite
    [["ough", "eau", r"o\we", "oa", "oe", "ow", "oo", "ew", "o"], None],  # 5 oʊ open, moat, bone, toe, sow, dough, beau, brooch, sew
    [["ough", "aw", "au", "ho", "a"], None],  # 6 ɒ swan, honest, maul, slaw, fought
    [["ough", "ow", "ou"], None],  # 7 aʊ now, shout, bough
    [["ear", "eer", "ere", "ier"], None],  # 8 ɪəʳ ear, steer, here, tier
    [["ear", "our", "ir", "er", "ur", "or", "yr"], None],  # 9 ɜ:ʳ bird, term, burn, pearl, word, journey, myrtle
    [["ure", "our"], None],  # 10 ʊəʳ cure, tourist
    [["our", "er", "ur", "ar", "a", "i"], None],  # 11 ə about, ladder, pencil, dollar, honour, augur
    [["uoy", "oy", "oi"], None],  # 12 ɔɪ join, boy, buoy
    [["ee", "ea", "ey", "oe", "ie", "ei", "eo", "ay", "e", "y", "i"], None],  # 13 i: be, bee, meat, lady, key, phoenix, grief, ski, deceive, people, quay
    [["ea", "ie", "ai", "eo", "ei", "ae", "e", "u", "a"], None],  # 14 e end, bread, bury, friend, said, many, leopard, heifer, aesthetic
    [["au", "ai", "a"], None],  # 15 æ cat, plaid, laugh
    [["ui", "ie", "i", "e", "o", "u", "y"], None],  # 16 ɪ it, england, women, busy, guild, gym, sieve
    [["ou", "oo", "o", "u"], None],  # 17 ʊ and ʌ wolf, look, bush, would + lug, monkey, blood, double
    [["a"], None],  # 18 ɑ: arm
]

# [graphemes], replacement. if None, don't replace
CONSONANTS = [
    [["ngue", "ng", "n"], None],  # 0 ŋ ring, pink, tongue
    [["gue", "gu", "gh", "gg", "g"], None],  # 1 g gun, egg, ghost, guest, prologue
    [["dge", "di", "gg", "ge", "j"], None],  # 2 dʒ jam, wage, giraffe, edge, soldier, exaggerate
    [["tch", "ch", "tu", "ti", "te"], None],  # 3 tʃ chip, watch, future, action, righteous
    [["sci", "ti", "sh", "ce", "ci", "si", "ch", "s"], None],  # 4 ʃ sham, ocean, sure, special, pension, machine, conscience, station
    [["bb", "b"], None],  # 5 b bug, bubble
    [["dd", "ed", "d"], None],  # 6 d dad, add, milled
    [["ff", "ph", "gh", "lf", "ft", "f"], None],  # 7 f fat, cliff, phone, enough, half, often
    [["wh", "h"], None],  # 8 h hop, who
    [["qu", "ck", "ch", "cc", "lk", "q", "x", "k", "c"], None],  # 9 k kit, cat, chris, accent, folk, bouquet, queen, rack, box
    [["ll", "l"], None],  # 10 l live, well
    [["mm", "mb", "mn", "lm", "m"], None],  # 11 m man, summer, comb, column, palm
    [["nn", "kn", "gn", "pn", "mn", "n"], None],  # 12 n net, funny, know, gnat, pneumonic, mneumonic
    [["pp", "p"], None],  # 13 p pin, dippy
    [["rr", "wr", "rh", "r"], None],  # 14 r run, carrot, wrench, rhyme
    [["ss", "sc", "ps", "st", "ce", "se", "s"], None],  # 15 s sit, less, circle, scene, psycho, listen, pace, course
    [["tt", "th", "ed", "t"], None],  # 16 t tip, matter, thomas, ripped
    [["ph", "ve", "v", "f"], None],  # 17 v vine, of, stephen, five
    [["wh", "w", "u", "o"], None],  # 18 w wit, why, quick, choir
    [["zz", "ss", "ze", "se", "x", "s", "z"], None],  # 19 z zed, buzz, his, scissors, xylophone, craze
    [["si", "z", "s"], None],  # 20 ʒ treasure, division, azure
    [["th"], None],  # 21 θ and ð thongs + leather
    [["y", "i", "j"], None],  # 22 j you, onion, hallelujah
]

class Example:
    def __init__(self) -> None:
        v = VOWELS.copy()
        v[1][1] = "ay"
        v[3][1] = "aw"
        v[4][1] = "oo"
        v[8][1] = "o"
        v[9][1] = "o"
        v[10][1] = "an"
        v[12][1] = "ek"
        v[13][1] = "oo"
        v[17][1] = "u"
        self.vowels = v
        c = CONSONANTS.copy()
        c[1][1] = "k"
        c[9][1] = "g"
        c[10][1] = "k"
        c[15][1] = "zz"
        self.consonants = c
        
    def translate(self, value: str) -> str:
        # upper case is untouched, change that if ya want
        result = value
        for v in self.vowels:
            if v[1]:
                for x in v[0]:
                    result = re.sub(x, v[1], result)
        for c in self.consonants:
            if c[1]:
                for x in c[0]:
                    result = result.replace(x, c[1])
        return result
    
e = Example()
sample1 = "Everyone has the right to freedom of thought, conscience and religion; this right includes freedom to change his religion or belief, and freedom, either alone or in community with others and in public or private, to manifest his religion or belief in teaching, practice, worship and observance."
sample2 = "The quick brown fox jumps over the lazy dog"
test1 = e.translate(sample1)
test2 = e.translate(sample2)
print(f"{sample1} = {test1}")
print(f"{sample2} = {test2}")