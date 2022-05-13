import spacy
import re
from bs4 import BeautifulSoup

nlp = spacy.load("en_core_web_sm")

html_content = """gem-icon-half-1" style="color: #5B6770;"><span class="back-angle">&#xf1f3;</span></span><span class="gem-icon-half-2" style="color: #5B6770;"><span class="back-angle">&#xf1f3;</span></span></div></div> </div> </div> </div> <div class="quickfinder-item-info-wrapper"> <div class="quickfinder-item-info " > <div class="quickfinder-item-title" style="color: #5B6770;">Contact</div> <div class="quickfinder-item-text" style="color: #333;">Marion Frankiel<br />
marion.frankiel@xroad-formation.com<br />
06 64 41 46 72<br />
<br />
Xavier Schoenlaub<br />
xavier.schoenlaub@xroad-formation.com<br />
06 29 85 46 19</div> </div> </div> </div> </div> </div> </div></div></div></div></div><div class="vc_row-full-width vc_clearfix"></div><div id="vc_row-627e68f57339f" class="vc_row wpb_row vc_row-fluid vc_custom_1461336070525 thegem-custom-627e68f5733949516"><div class="wpb_column vc_column_container vc_col-sm-12 thegem-custom-627e68f5734de9811"><div class="vc_column-inner thegem-custom-inner-627e68f5734e0 vc_custom
"""

soup = BeautifulSoup(html_content, "lxml")
body = soup.body.text
print(body)
doc = nlp(body)

print("Output :")
for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)


