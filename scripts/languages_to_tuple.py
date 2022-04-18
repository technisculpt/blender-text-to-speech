#!"/usr/bin/python3"

import sys
import os 
with open(os.path.join(sys.path[0], r"./languages")) as f:
    file = (f.read())

langs = file.split('<')
langs = langs[1:len(langs)]

 # ('0',"Male",""),
for index, lang in enumerate(langs):
    l = lang.split('\n')[0].split('=')[1]
    print(f"('{index}', '{l}', ''),")

'''
    language_enumerator : bpy.props.EnumProperty(
                name = "",
                description = "gender options",
                items=[('0', 'afrikaans', ''),
                    ('1', 'aragonese', ''),
                    ('2', 'bulgarian', ''),
                    ('3', 'bosnian', ''),
                    ('4', 'catalan', ''),
                    ('5', 'czech', ''),
                    ('6', 'welsh', ''),
                    ('7', 'danish', ''),
                    ('8', 'german', ''),
                    ('9', 'greek', ''),
                    ('10', 'default', ''),
                    ('11', 'english', ''),
                    ('12', 'en-scottish', ''),
                    ('13', 'english-north', ''),
                    ('14', 'english_rp', ''),
                    ('15', 'english_wmids', ''),
                    ('16', 'english-us', ''),
                    ('17', 'en-westindies', ''),
                    ('18', 'esperanto', ''),
                    ('19', 'spanish', ''),
                    ('20', 'spanish-latin-am', ''),
                    ('21', 'estonian', ''),
                    ('22', 'persian', ''),
                    ('23', 'persian-pinglish', ''),
                    ('24', 'finnish', ''),
                    ('25', 'french-Belgium', ''),
                    ('26', 'french', ''),
                    ('27', 'irish-gaeilge', ''),
                    ('28', 'greek-ancient', ''),
                    ('29', 'hindi', ''),
                    ('30', 'croatian', ''),
                    ('31', 'hungarian', ''),
                    ('32', 'armenian', ''),
                    ('33', 'armenian-west', ''),
                    ('34', 'indonesian', ''),
                    ('35', 'icelandic', ''),
                    ('36', 'italian', ''),
                    ('37', 'lojban', ''),
                    ('38', 'georgian', ''),
                    ('39', 'kannada', ''),
                    ('40', 'kurdish', ''),
                    ('41', 'latin', ''),
                    ('42', 'lingua_franca_nova', ''),
                    ('43', 'lithuanian', ''),
                    ('44', 'latvian', ''),
                    ('45', 'macedonian', ''),
                    ('46', 'malayalam', ''),
                    ('47', 'malay', ''),
                    ('48', 'nepali', ''),
                    ('49', 'dutch', ''),
                    ('50', 'norwegian', ''),
                    ('51', 'punjabi', ''),
                    ('52', 'polish', ''),
                    ('53', 'brazil', ''),
                    ('54', 'portugal', ''),
                    ('55', 'romanian', ''),
                    ('56', 'russian', ''),
                    ('57', 'slovak', ''),
                    ('58', 'albanian', ''),
                    ('59', 'serbian', ''),
                    ('60', 'swedish', ''),
                    ('61', 'swahili-test', ''),
                    ('62', 'tamil', ''),
                    ('63', 'turkish', ''),
                    ('64', 'vietnam', ''),
                    ('65', 'vietnam_hue', ''),
                    ('66', 'vietnam_sgn', ''),
                    ('67', 'Mandarin', ''),
                    ('68', 'cantonese', ''),])
'''