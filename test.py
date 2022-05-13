import nltk
from nameparser.parser import HumanName
from bs4 import BeautifulSoup


def get_human_names(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary=False)
    person_list = []
    person = []
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1:  # avoid grabbing lone surnames
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
            name = ''
        person = []
    return person_list


text = """"gem-icon-half-1" style="color: #5B6770;"><span class="back-angle">&#xf1f3;</span></span><span class="gem-icon-half-2" style="color: #5B6770;"><span class="back-angle">&#xf1f3;</span></span></div></div> </div> </div> </div> <div class="quickfinder-item-info-wrapper"> <div class="quickfinder-item-info " > <div class="quickfinder-item-title" style="color: #5B6770;">Contact</div> <div class="quickfinder-item-text" style="color: #333;">Marion Frankiel<br />
marion.frankiel@xroad-formation.com<br />
06 64 41 46 72<br />
<br />
Xavier Schoenlaub<br />
xavier.schoenlaub@xroad-formation.com<br />
06 29 85 46 19</div> </div> </div> </div> </div> </div> </div></div></div></div></div><div class="vc_row-full-width vc_clearfix"></div><div id="vc_row-627e68f57339f" class="vc_row wpb_row vc_row-fluid vc_custom_1461336070525 thegem-custom-627e68f5733949516"><div class="wpb_column vc_column_container vc_col-sm-12 thegem-custom-627e68f5734de9811"><div class="vc_column-inner thegem-custom-inner-627e68f5734e0 vc_custom
"""

"""soup = BeautifulSoup(text, "lxml")
body = soup.body.text
print(body)"""

names = get_human_names(text)

print("LAST, FIRST")
for name in names:
    last_first = HumanName(name).last + ', ' + HumanName(name).first
    print(last_first)

# Xavier pas compris