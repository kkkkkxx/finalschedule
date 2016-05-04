from flask import Flask, request, redirect
import twilio.twiml

app = Flask(__name__)

# Try adding your own number to this list!
callers = {
    "+14124179805": "George",
    "+19542269211": "Philip",
}

finals = {
    "AANL 10103 1": ["LEC", "Elementary Hittite (3)", "Goedegebuure", "8:00 AM", "10:00 AM", "W", "6/8/2016", "OR 315"],
    "AKKD 10103 1": ["LEC", "Elementary Akkadian (3)", "Reculeau", "10:30 AM", "12:30 PM", "M", "6/6/2016", "OR 210"],
    "ANTH 21420 1": ["SEM", "Ethnographic Methods", "Jenkins", "1:30 PM", "3:30 PM", "R", "6/9/2016", "HM 104"],
    "ARAB 10103 1": ["LEC", "Elementary Arabic (3)", "abu-Eledam", "10:30 AM", "12:30 PM", "F", "6/10/2016", "HM 145"],
    "ARAB 10103 2": ["LEC", "Elementary Arabic (3)", "abu-Eledam", "10:30 AM", "12:30 PM", "M", "6/6/2016," "HM 145"],
    "ARAB 10103 3": ["LEC", "Elementary Arabic (3)", "Choudar", "1:30 PM", "3:30 PM", "F", "6/10/2016", "C 201A-B"],
    "ARAB 10251 1": ["LEC", "Colloquial Egyptian Arabic (1)", "Abdel Mobdy", "1:30 PM", "3:30 PM", "R", "6/9/2016", "C 210"],
    "ARAB 20103 2": ["LEC", "Intermediate Arabic (3)", "Heikkinen", "1:30 PM", "3:30 PM", "F", "6/10/2016", "C 104"],
    "ARAB 20103 3": ["LEC", "Intermediate Arabic (3)", "Abdel Mobdy", "4:00 PM", "6:00 PM", "R", "6/9/2016", "WB 230"],
    "ARAB 29001 1": ["LEC", "Arabic Through Film", "Forster", "1:30 PM", "3:30 PM", "T", "6/7/2016", "C 403"],
    "ARAB 30203 1": ["LEC", "High Intermediate Modern Standard Arabic (3)", "Forster", "10:30 AM", "12:30 PM", "W", "6/8/2016", "HM 104"],
    "ARAB 30303 1": ["LEC", "High Intermediate Classical Arabic (3)", "Heikkinen", "10:30 AM", "12:30 PM", "W", "6/8/2016", "C 104"],
    "ARAB 30352 1": ["LEC", "Arabic Through Maghribi Literature", "Choudar", "4:00 PM", "6:00 PM", "W", "6/8/2016", "C 430"],
    "ARAB 40102 1": ["LEC", "Advanced Arabic Syntax (2)", "Qutbuddin", "10:30 AM", "12:30 PM", "T", "6/7/2016", "P 218"],
    "ARAB 40392 1": ["SEM", "Readings: The Sira Literature", "Donner", "1:30 PM", "3:30 PM", "F", "6/10/2016", "OR 210"],
    "ARAM 10403 1": ["LEC", "Elementary Syriac (3)", "Creason", "10:30 AM", "12:30 PM", "R", "6/9/2016", "OR 208"],
    "ARTH 15707 1": ["CRS", "American Art since the Great War", "English", "1:30 PM", "3:30 PM", "T", "6/7/2016", "CWAC 157"],
    "ARTV 10100 1": ["CRS", "Visual Language: On Images", "Beck", "1:30 PM", "3:30 PM", "F", "6/10/2016", "LC 601"],
    "ARTV 10100 2": ["CRS", "Visual Language: On Images", "Mauser", "6:00 PM", "8:00 PM", "T", "6/7/2016", "LC 401"],
    "ARTV 10100 3": ["CRS", "Visual Language: On Images", "Adams", "10:30 AM", "12:30 PM", "T", "6/7/2016", "LC 401"],
    "ARTV 10100 4": ["CRS", "Visual Language: On Images", "Lloyd", "1:30 PM", "3:30 PM", "T", "6/7/2016", "LC 601"],
    "ARTV 10100 5": ["CRS", "Visual Language: On Images", "Williamson", "4:00 PM", "6:00 PM", "T", "6/7/2016", "LC 601"],
    "ARTV 10200 1": ["CRS", "Visual Language: On Objects", "Jackson", "10:30 AM", "12:30 PM", "M", "6/6/2016", "LC 110"],
    "ARTV 10200 2": ["CRS", "Visual Language: On Objects", "Rouse", "10:30 AM", "12:30 PM", "M", "6/6/2016", "Classroom not yet listed"],
    "ARTV 21501 1": ["CRS", "Introduction to Printmaking", "Desjardins", "1:30 PM", "3:30 PM", "T", "6/7/2016", "LC 109"],
    "ARTV 22310 1": ["CRS", "Art of Engagement", "Ginsburg", "10:30 AM", "12:30 PM", "T", "6/7/2016", "LC 108"],
    "ARTV 22500 1": ["CRS", "Digital Imaging", "Salavon", "10:30 AM", "12:30 PM", "M", "6/6/2016", "LC 028"],
    "ARTV 22502 1": ["CRS", "Data and Algorithm in Art", "Salavon", "1:30 PM", "3:30 PM", "F", "6/10/2016", "LC 028"],
    "ARTV 23804 1": ["CRS", "Experimental Animation", "Wolniak", "10:30 AM", "12:30 PM", "T", "6/7/2016", "LC 014"],
    "ARTV 23805 1": ["CRS", "Minimalist Experiment in Film and Video", "Rodowick", "1:30 PM", "3:30 PM", "T", "6/7/2016", "LC 014"],
    "ARTV 24121 1": ["CRS", "Adopted Strategies", "Jackson", "1:30 PM", "3:30 PM", "F", "6/10/2016", "LC 110"],
    "ARTV 24201 1": ["CRS", "Collage", "Wolniak", "1:30 PM", "3:30 PM", "T", "6/7/2016", "LC 401"],
    "ARTV 24401 1": ["CRS", "Photography (1)", "Letinsky", "1:30 PM", "3:30 PM", "F", "6/10/2016", "ED B 045 D"],
    "ARTV 24402 1": ["CRS", "Photography (2)", "Letinsky", "1:30 PM", "3:30 PM", "F", "6/10/2016", "Classroom not yet listed"],
    "ARTV 27210 1": ["CRS", "Intermediate/Advanced Painting", "Desjardins", "8:00 AM", "10:00 AM", "T", "6/7/2016", "LC 203"],
    "ARTV 29600 1": ["CRS", "Junior Seminar", "Ginsburg", "1:30 PM", "3:30 PM", "T", "6/7/2016", "LC 802"],
    "ARTV 39901 1": ["CRS", "21st Century Art", "Jackson", "8:00 AM", "10:00 AM", "W", "6/8/2016", "LC 802"],
    "ARTV 44319 1": ["CRS", "Writing Images/Picturing Words", "Stockholder", "1:30 PM", "3:30 PM", "F", "6/10/2016" "LC 109"],
    "ASLG 10300 1": ["CRS", "American Sign Language (3)", "Ronchen", "10:30 AM", "12:30 PM", "W", "6/8/2016", "C 115"],
    "ASLG 10300 2": ["CRS", "American Sign Language (3)", "Ronchen", "4:00 PM", "6:00 PM", "R", "6/9/2016", "C 115"],
    "ASLG 10600 1": ["CRS", "Intermediate ASL (3)", "Ronchen", "10:30 AM", "12:30 PM", "R", "6/9/2016", "C 115"],
    "BANG 10300 1": ["CRS", "First-Year Bangla (3)", "Bhaduri", "8:00 AM", "10:00 AM", "W", "6/8/2016", "C 210"],
    "BANG 20300 1": ["CRS", "Second-Year Bangla (3)", "Bhaduri", "10:30 AM", "12:30 PM", "F", "6/10/2016", "C 228"],
    "BASQ 12200 1": ["CRS", "Elementary Basque (3)", "Palenzuela Rodrigo", "10:30 AM", "12:30 PM", "R", "6/9/2016", "C 430"],
    "BCSN 10303 1": ["CRS", "First-Year Bosnian/Croatian/Serbian (3)", "Petkovic", "1:30 PM", "3:30 PM", "F", "6/10/2016", "C 205"],
    "BCSN 20303 1": ["CRS", "Second-Year Bosnian/Croatian/Serbian (3)", "Petkovic", "10:30 AM", "12:30 PM", "M", "6/6/2016", "F 408"],
    "BCSN 21300 1": ["CRS", "(Re)Branding the Balkan City: Comtemp Belgrade/Sarajevo/Zagreb", "Petkovic", "10:30 AM", "12:30 PM", "R", "6/9/2016", "F 408"]
    "BIOS 11128 1": ["LEC Introduction to Human Genetics Christianson 10:30 AM 12:30 PM W 6/8/2016 BSLC 205
    "BIOS 11132 1": ["LEC Genes, Evolution, and Society Lahn 1:30 PM 3:30 PM R 6/9/2016 BSLC 205
    "BIOS 11133 1": ["LEC Human Variation, Race, and Genomics Lindo 4:00 PM 6:00 PM W 6/8/2016 BSLC 205
    "BIOS 11140 1": ["LEC Biotechnology for the 21st Century Bhasin 10:30 AM 12:30 PM T 6/7/2016 BSLC 218
    "BIOS 12115 1": ["LEC Responses of Cardiopulmonary System to Stress Gupta 8:00 AM 10:00 AM T 6/7/2016 BSLC 205
    "BIOS 12117 1": ["LEC The 3.5 Billion Year History of the Human Body Shubin 1:30 PM 3:30 PM R 6/9/2016 BSLC 008
    "BIOS 12120 1": ["LEC Pheromones: The Chemical Signals Around You. Ruvinsky 10:30 AM 12:30 PM T 6/7/2016 BSLC 001
    "BIOS 13111 1": ["LEC Natural History of North American Deserts Larsen 1:30 PM 3:30 PM F 6/10/2016 BSLC 109
    "BIOS 13112 0": ["LEC Natural History of North American Deserts; Field School Larsen 1:30 PM 3:30 PM F 6/10/2016 Classroom not yet listed
    "BIOS 14114 0": ["LEC Drugs Galore: What They Are and What They Do To You Zaragoza 10:30 AM 12:30 PM R 6/9/2016 BSLC 218
    "BIOS 14115 1": ["LEC From Social Neuroscience to Medical Neuroscience and Back Cacioppo 10:30 AM 12:30 PM R 6/9/2016 BSLC 008
    "BIOS 15115 1": ["LEC Cancer Biology: How Good Cells Go Bad Villereal 10:30 AM 12:30 PM T 6/7/2016 BSLC 008
    "BIOS 15123 1": ["LEC The Microbiome in Human and Environmental Health Gilbert 10:30 AM 12:30 PM T 6/7/2016 BSLC 205
    "BIOS 20150 0": ["LEC How Can We Understand the Biosphere? Allesina 10:30 AM 12:30 PM T 6/7/2016 BSLC 109
    "BIOS 20151 0": ["LEC Introduction to Quantitative Modeling in Biology Basic Kondrashov 8:00 AM 10:00 AM T 6/7/2016 BSLC 109
    "BIOS 20152 0": ["LEC Introduction to Quantitative Modeling in Biology Advanced Kondrashov 1:30 PM 3:30 PM T 6/7/2016 BSLC 205
    "BIOS 20171 0": ["LEC Human Genetics and Developmental Biology Christianson 10:30 AM 12:30 PM F 6/10/2016 BSLC 205
    "BIOS 20172 0": ["LEC Mathematical Modeling for Pre-Med Students I. Jafari Haddadian 10:30 AM 12:30 PM W 6/8/2016 BSLC 109
    "BIOS 20188 AA": ["LEC Fundamentals of Physiology Mcgehee 10:30 AM 12:30 PM F 6/10/2016 BSLC 109
    "BIOS 20189 BB": ["LEC Fundamentals of Developmental Biology Ho 10:30 AM 12:30 PM M 6/6/2016 BSLC 109
    "BIOS 20200 0": ["LEC Introduction To Biochemistry Makinen 4:00 PM 6:00 PM R 6/9/2016 BSLC 109
    "BIOS 21207 1": ["LEC Cell Biology Lamppa 10:30 AM 12:30 PM M 6/6/2016 BSLC 240
    "BIOS 21249 1": ["LEC Organization, Expression, and Transmission of Genome Information. Shapiro 10:30 AM 12:30 PM R 6/9/2016 BSLC 240
    "BIOS 21317 1": ["LEC Topics in Biological Chemistry Rice 10:30 AM 12:30 PM W 6/8/2016 BSLC 218
    "BIOS 21328 1": ["LEC Biophysics of Biomolecules Sosnick 4:00 PM 6:00 PM T 6/7/2016 KCBD 3200
    "BIOS 21349 0": ["LEC Protein Structure and Functions in Medicine Tang 8:00 AM 10:00 AM T 6/7/2016 BSLC 313
    "BIOS 21356 1": ["LEC Vertebrate Development Prince 10:30 AM 12:30 PM T 6/7/2016 BSLC 202
    "BIOS 21407 1": ["LEC Image Processing In Biology Josephs 1:30 PM 3:30 PM M 6/6/2016 CLSC 119
    "BIOS 21417 1": ["LEC Systems Biology: Molecular Regulatory Logic of Networks Aprison 10:30 AM 12:30 PM F 6/10/2016 BSLC 305
    "BIOS 22236 1": ["LEC Reproductive Biology of Primates Martin 10:30 AM 12:30 PM W 6/8/2016 BSLC 305
    "BIOS 22250 1": ["LEC Chordates: Evolution and Comparative Anatomy Coates 1:30 PM 3:30 PM T 6/7/2016 BSLC 305
    "BIOS 22260 1": ["LEC Vertebrate Structure and Function Sereno 10:30 AM 12:30 PM T 6/7/2016 ACC F150
    "BIOS 23100 1": ["LEC Dinosaur Science Sereno 8:00 AM 10:00 AM T 6/7/2016 ACC F150
    "BIOS 23232 0": ["LEC Ecology & Evolution in the Southwest Larsen 1:30 PM 3:30 PM F 6/10/2016 Classroom not yet listed
    "BIOS 23233 0": ["LEC Ecology & Evolution in the Southwest:Field School Larsen 1:30 PM 3:30 PM F 6/10/2016 Classroom not yet listed
    "BIOS 23254 1": ["LEC Mammalian Ecology Larsen 10:30 AM 12:30 PM T 6/7/2016 BSLC 313
    "BIOS 23299 1": ["LEC Plant Development/Molecular Genetics Greenberg 8:00 AM 10:00 AM T 6/7/2016 BSLC 305
    "BIOS 23409 1": ["LEC The Ecology and Evolution of Infectious Diseases Dwyer 8:00 AM 10:00 AM T 6/7/2016 BSLC 240
    "BIOS 23410 1": ["LEC Complex Interactions: Coevolution, Parasites, Mutualists, and Cheaters Lumbsch 4:00 PM 6:00 PM M 6/6/2016 BSLC 324
    "BIOS 24205 1": ["LEC Systems Neuroscience Hale 1:30 PM 3:30 PM T 6/7/2016 BSLC 008
    "BIOS 24218 1": ["LEC Molecular Neurobiology Sisodia 10:30 AM 12:30 PM R 6/9/2016 BSLC 313
    "BIOS 24232 1": ["LEC Computational Approaches to Cogintive Neuroscience Hatsopoulos 1:30 PM 3:30 PM R 6/9/2016 BSLC 240
    "BIOS 24408 1": ["LEC Modeling and Signal Analysis for Neuroscientists Van Drongelen 1:30 PM 3:30 PM F 6/10/2016 BSLC 401
    "BIOS 25109 1": ["LEC Tpcs: Reproductive Bio/Cancer Greene 10:30 AM 12:30 PM T 6/7/2016 BSLC 240
    "BIOS 25126 1": ["LEC Animal Models of Human Disease Niekrasz 4:00 PM 6:00 PM W 6/8/2016 BSLC 001
    "BIOS 25228 1": ["LEC Endocrinology III: Human Disease Musch 4:00 PM 6:00 PM R 6/9/2016 BSLC 001
    "BIOS 25287 1": ["LEC Introduction to Virology Manicassamy 1:30 PM 3:30 PM F 6/10/2016 BSLC 001
    "BIOS 25308 1": ["LEC Heterogeneity in Human Cancer: Etiology and Treatment Macleod 1:30 PM 3:30 PM R 6/9/2016 BSLC 202
    "BIOS 28407 1": ["LEC Genomics and Systems Biology Gilad 1:30 PM 3:30 PM T 6/7/2016 BSLC 218
    "BIOS 29326 1": ["LEC Intro: Medical Physics Armato III 1:30 PM 3:30 PM T 6/7/2016 BSLC 240
    "CABI 32000 1": ["LEC Translational Approaches in Cancer Biology Macleod 1:30 PM 3:30 PM T 6/7/2016 BSLC 202
    "CAPP 30123 1": ["LEC Computer Science with Applications-3 Wachs 10:30 AM 12:30 PM F 6/10/2016 RY 276
    "CAPP 30235 1": ["LEC Databases for Public Policy Elmore 8:00 AM 10:00 AM T 6/7/2016 RY 277
    "CAPP 30254 1": ["LEC Machine Learning for Public Policy Ghani 10:30 AM 12:30 PM T 6/7/2016 RY 276
    "CATA 11100 1": ["LEC Accelerated Catalan I Girons Masot 10:30 AM 12:30 PM M 6/6/2016 C 210
    "CATA 21600 1": ["LEC Catalan Culture and Society: Art, Music, and Cinema Girons Masot 10:30 AM 12:30 PM W 6/8/2016 C 210
    "CCTS 40006 1": ["CRS Pharmacogenomics: Discovery and Implementation Huang 10:30 AM 12:30 PM M 6/6/2016 BSLC 305
    "CHDV 20890 1": ["SEM Mental Health: International and Social Perspectives Sandhya 1:30 PM 3:30 PM F 6/10/2016 RO 329
    "CHDV 20890 2": ["SEM Mental Health: International and Social Perspectives Sandhya 4:00 PM 6:00 PM M 6/6/2016 RO 432
    "CHDV 21901 1": ["CRS Language, Culture, and Thought Lucy 1:30 PM 3:30 PM T 6/7/2016 HM 130
    "CHEM 11300 1": ["LEC Comprehensive General Chemistry-III Lee 10:30 AM 12:30 PM M 6/6/2016 K 107
    "CHEM 11300 2": ["LEC Comprehensive General Chemistry-III Roux 10:30 AM 12:30 PM M 6/6/2016 K 120
    "CHEM 12300 0": ["LEC Honors General Chemistry-3 Voth 8:00 AM 10:00 AM W 6/8/2016 K 120
    "CHEM 20200 1": ["LEC Inorganic Chemistry-2 Jordan 10:30 AM 12:30 PM M 6/6/2016 K 102
    "CHEM 22200 0": ["LEC Organic Chemistry-3 Snyder 10:30 AM 12:30 PM T 6/7/2016 K 107
    "CHEM 23200 0": ["LEC Honors Organic Chemistry-3 Rawal 10:30 AM 12:30 PM T 6/7/2016 K 120
    "CHEM 26300 1": ["LEC Chem Kinetic/Dynamics Butler 10:30 AM 12:30 PM F 6/10/2016 K 102
    "CHEM 26800 1": ["LEC Computational Chemistry and Biology Dinner 8:00 AM 10:00 AM T 6/7/2016 K 120
    "CHEM 30900 1": ["LEC Bioinorganic Chemistry He 8:00 AM 10:00 AM T 6/7/2016 K 102
    "CHEM 36500 1": ["LEC Chemical Dynamics Sibener 10:30 AM 12:30 PM T 6/7/2016 K 102
    "CHEM 36700 1": ["LEC Experimental Physical Chemistry Special Topics Scherer 10:30 AM 12:30 PM T 6/7/2016 K 101
    "CHEM 38700 1": ["LEC Biophysical Chemistry Tokmakoff 8:00 AM 10:00 AM T 6/7/2016 K 101
    "CHIN 10300 1": ["CRS Elementary Modern Chinese-3 Cai, Xiang, or Kuo 8:00 AM 10:00 AM W 6/8/2016 C 319
    "CHIN 10300 2": ["CRS Elementary Modern Chinese-3 Cai, Xiang, or Kuo 8:00 AM 10:00 AM W 6/8/2016 C 319
    "CHIN 10300 3": ["CRS Elementary Modern Chinese-3 Cai, Xiang, or Kuo 8:00 AM 10:00 AM W 6/8/2016 C 319
    "CHIN 10300 4": ["CRS Elementary Modern Chinese-3 Cai, Xiang, or Kuo 10:30 AM 12:30 PM M 6/6/2016 C 202
    "CHIN 10300 5": ["CRS Elementary Modern Chinese-3 Cai, Xiang, or Kuo 10:30 AM 12:30 PM M 6/6/2016 C 202
    "CHIN 11300 1": ["CRS First -Yr. Chinese for Bilinqual Speakers-3 Yang 10:00 AM 12:00PM M 6/6/2016 C 304
    "CHIN 20300 1": ["CRS Intermediate Modern Chinese-3 Li 8:00 AM 10:00 AM R 6/9/2016 STU 104
    "CHIN 20300 2": ["CRS Intermediate Modern Chinese-3 Li 8:00 AM 10:00 AM R 6/9/2016 STU 104
    "CHIN 21300 1": ["CRS Accelerated Chinese for Bilingual Speakers-3 Xu 8:00 AM 10:00 AM M 6/6/2016 C 430
    "CHIN 30300 1": ["CRS Advanced Modern Chinese-3 Yang 10:00 AM 12:00PM W 6/8/2016 C 304
    "CHIN 30300 2": ["CRS Advanced Modern Chinese-3 Xu 8:00 AM 10:00 AM R 6/8/2016 C 213
    "CHIN 41300 1": ["CRS Fourth-Year Modern Chinese-3 Kuo 8:00 AM 10:00 AM R 6/9/2016 C 103
    "CHIN 51300 1": ["CRS Fifth-Year Modern Chinese-3 Wang 8:00 AM 10:00 AM R 6/9/2016 C 104
    "CLAS 34515 1": ["CRS Money and the Ancient Greek World Bresson 1:30 PM 3:30 PM F 6/10/2016 C 409
    "CLAS 35415 1": ["CRS Text into Data: Digital Philology Dik 1:30 PM 3:30 PM T 6/7/2016 CL 021
    "CLAS 45716 1": ["SEM Sem: Ghosts, Demons & Supernatural Danger in the Anc. World Lincoln 1:30 PM 3:30 PM F 6/10/2016 CL 021
    "CLCV 25808 1": ["CRS Roman Law Ando 10:30 AM 12:30 PM R 6/9/2016 HM 140
    "CLCV 28315 1": ["SEM Ephron Seminar Gouvea 10:30 AM 12:30 PM R 6/9/2016 HM 150
    "CLCV 29000 1": ["CRS Myth Course Shandruk 1:30 PM 3:30 PM T 6/7/2016 HM 150
    "CMSC 11000 1": ["LEC Multimed Prog: Interdisc Art-1 Sterner 1:30 PM 3:30 PM R 6/9/2016 RY 277
    "CMSC 12300 1": ["LEC Computer Science with Applications-3 Wachs 10:30 AM 12:30 PM F 6/10/2016 RY 277
    "CMSC 15200 1": ["LEC Intro To Computer Science-2 Franklin 1:30 PM 3:30 PM F 6/10/2016 STU 101
    "CMSC 15400 1": ["LEC Intro To Computer Systems Hoffmann 10:30 AM 12:30 PM M 6/6/2016 RY 251
    "CMSC 15400 2": ["LEC Intro To Computer Systems Gunawi 10:30 AM 12:30 PM W 6/8/2016 RY 251
    "CMSC 15400 3": ["LEC Intro To Computer Systems Wachs 1:30 PM 3:30 PM F 6/10/2016 RY 251
    "CMSC 22001 1": ["LEC Software Construction Lu 1:30 PM 3:30 PM R 6/9/2016 RY 276
    "CMSC 22010 1": ["LEC Digital Fabrication Stevens 1:30 PM 3:30 PM F 6/10/2016 SCL 240
    "CMSC 22100 1": ["LEC Programming Languages Shaw 10:30 AM 12:30 PM R 6/9/2016 RY 251
    "CMSC 23310 1": ["LEC Advanced Distributed Systems Sotomayor Basilio 4:00 PM 6:00 PM W 6/8/2016 C 112
    "CMSC 23310 2": ["LEC Advanced Distributed Systems Sotomayor Basilio 4:00 PM 6:00 PM M 6/6/2016 C 112
    "CMSC 23900 1": ["LEC Data Visualization Kindlmann 10:30 AM 12:30 PM T 6/7/2016 RY 251
    "CMSC 25020 1": ["LEC Computational Linguistics Goldsmith 10:30 AM 12:30 PM M 6/6/2016 K 101
    "CMSC 27200 1": ["LEC Theory of Algorithms Simon 10:30 AM 12:30 PM F 6/10/2016 RY 251
    "CMSC 27230 1": ["LEC Honors Theory of Algorithms Drucker 10:30 AM 12:30 PM W 6/8/2016 RY 276
    "CMSC 27410 1": ["LEC Honors Combinatorics Babai 10:30 AM 12:30 PM R 6/9/2016 RY 276
    "CMSC 27500 1": ["LEC Graph Theory Mulmuley 8:00 AM 10:00 AM T 6/7/2016 RY 251
    "CMSC 27610 1": ["LEC Digital Biology Scott 8:00 AM 10:00 AM T 6/7/2016 RY 276
    "CMSC 28100 1": ["LEC Intro Complexity Theory Mulmuley 1:30 PM 3:30 PM T 6/7/2016
    "CMSC 32001 1": ["LEC Topics: Programming Langs. Chugh 1:30 PM 3:30 PM R 6/9/2016 P 022
    "CMSC 33001 1": ["LEC Topics in Systems Chong 1:30 PM 3:30 PM T 6/7/2016 RY 277
    "CMSC 33251 1": ["LEC Topics in Computer Security Feldman 1:30 PM 3:30 PM F 6/10/2016 RY 277
    "CMSC 34900 1": ["LEC Topics In Scientific Computing Scott 10:30 AM 12:30 PM R 6/9/2016 RY 277
    "CMSC 35050 1": ["LEC Computational Linguistics Goldsmith 10:30 AM 12:30 PM M 6/6/2016 K 101
    "CMSC 37120 1": ["LEC Topics in Discrete Mathematics Razborov 10:30 AM 12:30 PM T 6/7/2016 RY 277
    "CMSC 37200 1": ["LEC Combinatorics Babai 10:30 AM 12:30 PM R 6/9/2016 Classroom not yet listed
    "CMSC 38100 1": ["CRS Computability Theory-2 Hirschfeldt 1:30 PM 3:30 PM T 6/7/2016 Classroom not yet listed
    "CRWR 12013 1": ["SEM Special Topics in Fiction: Genre Rules and Rebels DeWoskin 10:30 AM 12:30 PM T 6/7/2016 M 102
    "CRWR 22115 1": ["SEM Advanced Fiction Workshop: Characters in Conflict DeWoskin 1:30 PM 3:30 PM F 6/10/2016 M 102
    "CRWR 27103 1": ["CRS Advanced Screenwriting Petrakis 1:30 PM 3:30 PM R 6/9/2016 LC 802
    "EALC 19900 1": ["CRS Early Modern Japanese History Toyosawa 4:00 PM 6:00 PM W 6/8/2016 C 303
    "ECON 19800 1": ["LEC Introduction To Microeconomics Sanderson 1:30 PM 3:30 PM M 6/6/2016 SS 122
    "ECON 19800 2": ["CRS Introduction To Microeconomics List 1:30 PM 3:30 PM R 6/9/2016 SS 122
    "ECON 20000 1": ["LEC Elements of Economic Analysis-1 Tsiang 6:30 PM 8:30 PM M 6/6/2016 SHFE 146
    "ECON 20000 2": ["LEC Elements of Economic Analysis-1 Tsiang 6:30 PM 8:30 PM M 6/6/2016 SHFE 146
    "ECON 20010 1": ["LEC Elements of Economics Analysis 1: Honors Cuesta Rodriguez 1:30 PM 3:30 PM T 6/7/2016 STU 102
    "ECON 20200 1": ["LEC Elements of Economic Analysis-3 Tartari 8:00 AM 10:00 AM W 6/8/2016 STU 104
    "ECON 20200 2": ["LEC Elements of Economic Analysis-3 Tartari 10:30 AM 12:30 PM M 6/6/2016 STU 104
    "ECON 20200 3": ["LEC Elements of Economic Analysis-3 Lopes de Melo 6:30 PM 8:30 PM M 6/6/2016 Classroom not yet listed
    "ECON 20200 4": ["LEC Elements of Economic Analysis-3 Lopes de Melo 6:30 PM 8:30 PM M 6/6/2016 Classroom not yet listed
    "ECON 20200 5": ["LEC Elements of Economic Analysis-3 Lopes de Melo 6:30 PM 8:30 PM M 6/6/2016 Classroom not yet listed
    "ECON 20210 1": ["LEC Elements of Economics Analysis 3-HONORS van Vliet 1:30 PM 3:30 PM T 6/7/2016 RO 015
    "ECON 20300 1": ["CRS Elements of Economic Analysis-4 Wang 10:30 AM 12:30 PM M 6/6/2016 SHFE 146
    "ECON 20300 2": ["LEC Elements of Economic Analysis-4 Hughes 10:30 AM 12:30 PM R 6/9/2016 SHFE 146
    "ECON 20310 1": ["LEC Elements of Economics Analysis 4:HONORS Yoshida 1:30 PM 3:30 PM T 6/7/2016 SHFE 203
    "ECON 20700 1": ["LEC Game Theory and Economic Applications Myerson 10:30 AM 12:30 PM M 6/6/2016 SHFE 021
    "ECON 20740 1": ["LEC Analysis of Collective Decision-Making van Weelden 8:00 AM 10:00 AM W 6/8/2016 SHFE 146
    "ECON 20900 1": ["LEC Intro To Econometrics: Honors Gay 4:00 PM 6:00 PM W 6/8/2016 SHFE 203
    "ECON 21000 1": ["LEC Econometrics A Hickman 4:00 PM 6:00 PM W 6/8/2016 SHFE 146
    "ECON 21000 2": ["LEC Econometrics A Hickman 4:00 PM 6:00 PM M 6/6/2016 SHFE 203
    "ECON 21000 3": ["LEC Econometrics A PENDING 10:30 AM 12:30 PM R 6/9/2016 SHFE 203
    "ECON 21000 4": ["LEC Econometrics A Bittmann 8:00 AM 10:00 AM T 6/7/2016 RO 011
    "ECON 21150 1": ["LEC Topics in Applied Econometrics Tartari 1:30 PM 3:30 PM F 6/10/2016 SHFE 203
    "ECON 21200 1": ["LEC Time Series Econometrics Marrone 10:30 AM 12:30 PM R 6/9/2016 STU 104
    "ECON 21410 1": ["LEC Computational Methods in Economics Browne 8:00 AM 10:00 AM T 6/7/2016 SHFE 203
    "ECON 23000 1": ["LEC Money and Banking Yoshida 8:00 AM 10:00 AM T 6/7/2016 SHFE 021
    "ECON 25000 1": ["LEC Introduction To Finance Choi 4:00 PM 6:00 PM W 6/8/2016 RO 011
    "ECON 25100 1": ["LEC Financial Economics B: Speculative Markets Alvarez 10:30 AM 12:30 PM T 6/7/2016 STU 105
    "ECON 26600 1": ["LEC Urban Economics Tolley 10:30 AM 12:30 PM W 6/8/2016 SHFE 203
    "ECON 30300 1": ["LEC Price Theory-3 Reny 1:30 PM 3:30 PM T 6/7/2016 SHFE 146
    "ECON 30701 1": ["LEC Evolutionary Game Theory Szentes 8:00 AM 10:00 AM T 6/7/2016 SHFE 103
    "ECON 31200 1": ["LEC Empirical Analysis-3 Bonhomme 10:30 AM 12:30 PM T 6/7/2016 STU 101
    "ECON 31710 1": ["LEC Identification in Nonlinear Econometric Models Torgovitsky 1:30 PM 3:30 PM F 6/10/2016 P 222
    "ECON 33200 1": ["LEC Theory of Income-3 Mulligan 8:00 AM 10:00 AM W 6/8/2016 SHFE 203
    "ECON 34901 1": ["LEC Social Interactions and Inequality Durlauf 10:30 AM 12:30 PM M 6/6/2016 SHFE 103
    "ECON 35003 1": ["LEC Human Capital, Markets, and the Family Heckman 4:00 PM 6:00 PM M 6/6/2016 SHFE 141
    "ECON 35301 1": ["LEC International Trade & Growth Lucas Jr 10:30 AM 12:30 PM T 6/7/2016 SHFE 103
    "ECON 40104 1": ["LEC Advanced Industrial Organization IV Hickman 6:00 PM 8:00 PM T 6/7/2016 SHFE 103
    "ECON 50300 1": ["SEM Becker Applied Economics Workshop List 1:30 PM 3:30 PM R 6/9/2016 SHFE 146
    "EGPT 10103 1": ["LEC Middle Egyptian Texts-1 Singer 10:30 AM 12:30 PM F 6/10/2016 C 102
    "EGPT 20110 1": ["LEC Introduction to Old Egyptian Hainline 10:30 AM 12:30 PM M 6/6/2016 OR 208
    "EGPT 20210 1": ["LEC Introduction to Late Egyptian Johnson 10:30 AM 12:30 PM F 6/10/2016 OR 208
    "ENGL 20222 1": ["CRS Introduction to British Romantic Literature Hansen 10:30 AM 12:30 PM R 6/9/2016 SHFE 103
    "ENST 24102 1": ["CRS Environmental Politics Lodato 4:00 PM 6:00 PM T 6/7/2016 HM 130
    "ENST 27120 1": ["SEM Historical Ecology of the Calumet Region Lycett 10:30 AM 12:30 PM F 6/10/2016 WB 102
    "ENST 27220 1": ["SEM Environmental Management and Planning in the Calumet Region Shaikh 10:30 AM 12:30 PM T 6/7/2016 SHFE 242
    "ENST 27320 1": ["SEM Topics in the Ecology of the Calumet Region Anastasio 10:30 AM 12:30 PM M 6/6/2016 CL 313
    "FINM 32400 1": ["LEC Computing for Finance-3 Liyanaarachchi 6:00 PM 8:00 PM T 6/7/2016 MS 112
    "FINM 33150 1": ["LEC Regression Analysis and Quantitative Trading Strategies Boonstra 6:00 PM 8:00 PM W 6/8/2016 MS 112
    "FREN 10100 1": ["LEC Beginning Elementary French-1 Grangier 8:00 AM 10:00 AM R 6/9/2016 C 106
    "FREN 10200 2": ["LEC Beginning Elementary French-2 Liu 8:00 AM 10:00 AM R 6/9/2016 C 110
    "FREN 10300 1": ["LEC Beginning Elementary French-3 Legrand 8:00 AM 10:00 AM R 6/9/2016 K 120
    "FREN 10300 2": ["LEC Beginning Elementary French-3 Di Vito 8:00 AM 10:00 AM R 6/9/2016 K 120
    "FREN 10300 3": ["LEC Beginning Elementary French-3 Liu 8:00 AM 10:00 AM R 6/9/2016 K 120
    "FREN 10300 4": ["LEC Beginning Elementary French-3 Faton 8:00 AM 10:00 AM R 6/9/2016 K 120
    "FREN 10300 5": ["LEC Beginning Elementary French-3 Delgado-Norris 8:00 AM 10:00 AM R 6/9/2016 K 120
    "FREN 20100 1": ["LEC Language History Culture-1 Legrand 8:00 AM 10:00 AM R 6/9/2016 C 402
    "FREN 20200 1": ["LEC Language History Culture-2 Petrush 8:00 AM 10:00 AM R 6/9/2016 C 107
    "FREN 20200 2": ["LEC Language History Culture-2 Petrush 8:00 AM 10:00 AM R 6/9/2016 C 107
    "FREN 20300 1": ["LEC Language History Culture-3 Faton 8:00 AM 10:00 AM R 6/9/2016 STU 102
    "FREN 20300 2 LEC Language History Culture-3 Bordeaux 8:00 AM 10:00 AM R 6/9/2016 STU 102
    "FREN 20300 3 LEC Language History Culture-3 Bordeaux 8:00 AM 10:00 AM R 6/9/2016 STU 102
    "FREN 20500 1 LEC Ecrire En Francais Berg 8:00 AM 10:00 AM R 6/9/2016 C 302
    "FREN 20500 2 LEC Ecrire En Francais Gao 8:00 AM 10:00 AM R 6/9/2016 C 302
    "FREN 20601 1 LEC Expression orale et phonetique Berg 10:30 AM 12:30 PM W 6/8/2016 C 302
    "FREN 21810 1 CRS Introduction à la littérature française du XVIIIe siècle Morrissey 10:30 AM 12:30 PM M 6/6/2016 C 103
    "GEOG 28600 1 SEM Advanced GIS Analysis Schuble 4:00 PM 6:00 PM W 6/8/2016 BSLC 018
    "GEOS 13300 1 LEC The Atmosphere Abbot 1:30 PM 3:30 PM F 6/10/2016
    "GEOS 21100 1 LEC Introduction to Petrology Dauphas 10:30 AM 12:30 PM M 6/6/2016 HGS 313
    "GEOS 21200 1 LEC Physics Of The Earth Heinz 1:30 PM 3:30 PM R 6/9/2016 HGS 184
    "GEOS 21205 1 LEC Intro: Seismology, Earthquakes, Near Surface Earth Seismicity MacAyeal 1:30 PM 3:30 PM R 6/9/2016 WB 310C
    "GEOS 23400 0 LEC Global Warming for Science Majors Archer 10:30 AM 12:30 PM F 6/10/2016 Classroom not yet listed
    "GEOS 24250 1 LEC Geophysical Fluid Dynamics: Understanding the Motions of the Atmosphere and Oceans Nakamura 1:30 PM 3:30 PM F 6/10/2016 HGS 180
    "GEOS 24705 1 LEC Energy: Science, Technology and Human Usage Moyer 1:30 PM 3:30 PM R 6/9/2016 SS 401
    "GLST 24102 1 SEM Entertainment Industrial: Presents, Pasts, and Futures of Fun Kohl 1:30 PM 3:30 PM R 6/9/2016 C 319
    "GLST 24103 1 SEM Paradise and Parks: Art, Science, Politics O'Connell 1:30 PM 3:30 PM T 6/7/2016 HM 102
    "GREK 10300 1 CRS Introduction To Attic Greek-3 Darden 10:30 AM 12:30 PM W 6/8/2016 HM 150
    "GREK 11300 1 CRS Accel Intro To Attic Greek-3 Wash 10:30 AM 12:30 PM W 6/8/2016 HM 135
    "GREK 20300 1 CRS Intermediate Greek-3 Faraone 10:30 AM 12:30 PM W 6/8/2016 CL 021
    "GREK 21800 1 CRS Greek Epic Faraone 10:30 AM 12:30 PM F 6/10/2016 CL 021
    "GREK 32800 1 CRS Survey Of Greek Lit-2: Prose Dik 10:30 AM 12:30 PM T 6/7/2016 CL 021
    "GRMN 10300 1 SEM Elementary German For Beginners-3 Haydt 8:00 AM 10:00 AM R 6/9/2016 SS 122
    "GRMN 10300 2 SEM Elementary German For Beginners-3 Friedland 8:00 AM 10:00 AM R 6/9/2016 SS 122
    "GRMN 10300 3 SEM Elementary German For Beginners-3 Flannery 8:00 AM 10:00 AM R 6/9/2016 SS 122
    "GRMN 10300 4 SEM Elementary German For Beginners-3 Hooper 8:00 AM 10:00 AM R 6/9/2016 SS 122
    "GRMN 20300 1 SEM Kurzprosa 20. Jahrhundert Resvick 8:00 AM 10:00 AM R 6/9/2016 C 102
    "GRMN 20300 2 SEM Kurzprosa 20. Jahrhundert Benert 8:00 AM 10:00 AM R 6/9/2016 C 102
    "GRMN 33300 1 SEM German For Research Purposes Haswell Todd 10:30 AM 12:30 PM R 6/9/2016 C 319
    "HEBR 10103 1 LEC Elementary Classical Hebrew-3 10:30 AM 12:30 PM F 6/10/2016 WB 130
    "HEBR 10503 1 CRS Introductory Modern Hebrew-3 Almog 10:30 AM 12:30 PM R 6/9/2016 C 201A-B
    "HEBR 10503 1 CRS Introductory Modern Hebrew-3 Almog 10:30 AM 12:30 PM W 6/8/2016 C 201A-B
    "HEBR 20003 1 LEC Punic Inscriptions Pardee 10:30 AM 12:30 PM F 6/10/2016 OR 210
    "HEBR 20106 1 LEC Intermed Classical Hebrew-3 Pardee 8:00 AM 10:00 AM W 6/8/2016 OR 208
    "HEBR 30503 1 CRS Advanced Modern Hebrew-3 Loewy Shacham 1:30 PM 3:30 PM T 6/7/2016 C 201C
    "HIND 10300 1 CRS First-Year Hindi-3 Grunebaum 1:30 PM 3:30 PM F 6/10/2016 C 210
    "HIND 20300 1 CRS Second-Year Hindi-3 Grunebaum 1:30 PM 3:30 PM M 6/6/2016 C 213
    "HIND 30300 1 CRS Third-Year Hindi-3 Williams 10:30 AM 12:30 PM T 6/7/2016 HM 135
    "HIND 40300 1 CRS Fourth-Year Hindi-3 Williams 10:30 AM 12:30 PM T 6/7/2016 HM 135
    "HIND 47902 1 CRS Readings: Advanced Hindi -3 Williams 10:30 AM 12:30 PM T 6/7/2016 HM 135
    "HIST 13002 8 CRS History of European Civilization-2 Phillips 10:30 AM 12:30 PM M 6/6/2016 C 107
    "HIST 13002 10 CRS History of European Civilization-2 Craig 10:30 AM 12:30 PM T 6/7/2016 C 107
    "HIST 13003 7 CRS History of European Civilization-3 Leuchter 1:30 PM 3:30 PM T 6/7/2016 C 107
    "HIST 13300 1 CRS Western Civilization-3 Weintraub 10:30 AM 12:30 PM F 6/10/2016 C 107
    "HIST 13700 2 CRS America in World Civilization-3 Flores 8:00 AM 10:00 AM T 6/7/2016 RO 301
    "HIST 13700 3 CRS America in World Civilization-3 Parker 1:30 PM 3:30 PM F 6/10/2016 SHFE 141
    "HIST 13700 4 CRS America in World Civilization-3 Sparrow 1:30 PM 3:30 PM T 6/7/2016 WB 102
    "HIST 15300 0 LEC Intro to East Asian Civilization-3 Hwang 10:30 AM 12:30 PM M 6/6/2016 CLSC 101
    "HIST 16900 1 CRS Anc Mediterr World-3 Kaegi 10:30 AM 12:30 PM T 6/7/2016 C 203
    "HIST 22505 1 CRS Modern Britain 1688-1901 Abritton Jonsson 1:30 PM 3:30 PM R 6/9/2016 SS 302
    "HIST 23706 1 LEC The Soviet Union Gilburd 1:30 PM 3:30 PM F 6/10/2016 HM 140
    "HIST 24608 1 CRS Frontiers and Expansion in Modern China Pomeranz 10:30 AM 12:30 PM T 6/7/2016 HM 140
    "HIST 25309 1 CRS History of Perception Rossi 1:30 PM 3:30 PM R 6/9/2016 WB 106
    "HIST 25415 1 CRS History of Information Johns 10:30 AM 12:30 PM M 6/6/2016 SS 401
    "HIST 29514 1 CRS Rise of the Modern Corporation Levy 1:30 PM 3:30 PM F 6/10/2016 C 319
    "HIST 29632 1 SEM Hist Colloq: The CIA and American Democracy Cumings 1:30 PM 3:30 PM T 6/7/2016 RO 432
    "HCHR 32106 1 CRS Introduction ot the Study of Iconography Krause 1:30 PM 3:30 PM T 6/7/2016 CWAC 153
    "HMRT 20100 0 LEC Human Rights-1 Laurence 1:30 PM 3:30 PM F 6/10/2016 MS 112
    "ITAL 10300 1 LEC Elementary Italian-3 Masciello 8:00 AM 10:00 AM R 6/9/2016 HGS 101
    "ITAL 10300 2 LEC Elementary Italian-3 Guslandi 8:00 AM 10:00 AM R 6/9/2016 HGS 101
    "ITAL 10300 3 LEC Elementary Italian-3 Porretto 8:00 AM 10:00 AM R 6/9/2016 HGS 101
    "ITAL 10300 4 LEC Elementary Italian-3 Moslemani 8:00 AM 10:00 AM R 6/9/2016 HGS 101
    "ITAL 12200 1 LEC Italian for Speakers of Romance Languages Porretto 8:00 AM 10:00 AM R 6/9/2016 C 112
    "ITAL 20300 1 LEC Language History Culture-3 Vegna 8:00 AM 10:00 AM R 6/9/2016 C 409
    "ITAL 20300 2 LEC Language History Culture-3 Vegna 8:00 AM 10:00 AM R 6/9/2016 C 409
    "JAPN 10300 1 CRS Elementary Modern Japanese-3 Miyachi 8:00 AM 10:00 AM T 6/7/2016 C 402
    "JAPN 10300 2 CRS Elementary Modern Japanese-3 Katagiri 8:00 AM 10:00 AM T 6/7/2016 C 203
    "JAPN 10300 3 CRS Elementary Modern Japanese-3 Lory 8:00 AM 10:00 AM M 6/6/2016 C 403
    "JAPN 20300 1 CRS Intermediate Modern Japanese-3 Katagiri 8:00 AM 10:00 AM M 6/6/2016 C 203
    "JAPN 21300 1 CRS Intrmdte Japn Thru Japnmtn-2 Miyachi 8:00 AM 10:00 AM M 6/6/2016 C 402
    "JAPN 30300 1 CRS Advanced Modern Japanese-3 Lory 10:30 AM 12:30 PM M 6/6/2016 C 403
    "JWSC 20121 1 SEM The Bible and Archaeology Schloen 1:30 PM 3:30 PM R 6/9/2016 C 110
    "KORE 10300 1 LEC Intro To Korean Language-3 Kim 10:30 AM 12:30 PM F 6/10/2016 C 219
    "KORE 10300 2 LEC Intro To Korean Language-3 Kim 10:30 AM 12:30 PM M 6/6/2016 C 219
    "KORE 20300 1 LEC Intermediate Korean-3 Kang 10:30 AM 12:30 PM F 6/10/2016 C 115
    "KORE 30300 1 CRS Advanced Korean-3 Kim 10:30 AM 12:30 PM R 6/9/2016 C 201C
    "KORE 42300 1 CRS Changing Identity of Contemporary Korea thru Film & Literature Kim 10:30 AM 12:30 PM R 6/9/2016 C 213
    "LACS 16300 1 LEC Intro to Latin American Civ-3 Fischer 1:30 PM 3:30 PM F 6/10/2016 STU 102
    "LATN 10300 1 CRS Introduction To Latin-3 Radding 10:30 AM 12:30 PM F 6/10/2016 CL 405
    "LATN 10300 2 CRS Introduction To Latin-3 Thangada 10:30 AM 12:30 PM M 6/6/2016 HM 150
    "LATN 11300 1 CRS Accel Intro To Latin-3 Weeda 10:30 AM 12:30 PM M 6/6/2016 WB 103
    "LATN 20300 1 CRS Intermediate Latin-3 Allen 10:30 AM 12:30 PM M 6/6/2016 WB 130
    "LATN 21900 1 CRS Roman Comedy White 10:30 AM 12:30 PM M 6/6/2016 CL 021
    "LATN 24615 1 SEM Augustine: Early Philosophical Works Ando 1:30 PM 3:30 PM F 6/10/2016 CL 405
    "LING 20001 0 LEC Intro to Linguistics Flinn 10:30 AM 12:30 PM M 6/6/2016 HM 130
    "LING 20202 1 CRS Advanced Syntax Pietraszko 1:30 PM 3:30 PM F 6/10/2016 Y 106
    "LING 20301 0 CRS Intro to Semantics & Pragmatics Francez 10:30 AM 12:30 PM T 6/7/2016 RO 011
    "LING 21300 0 CRS Historical Linguistics Gorbachov 10:30 AM 12:30 PM T 6/7/2016 CLSC 101
    "LING 27910 1 CRS Sign Language Linguistics Fenlon 8:00 AM 10:00 AM T 6/7/2016 WB 408
    "LING 31000 1 CRS Morphology Arregui 10:30 AM 12:30 PM R 6/9/2016 P 319
    "LING 33920 1 CRS The Language of Deception and Humor Riggle 1:30 PM 3:30 PM F 6/10/2016 P 016
    "MAPS 36900 1 SEM Anthropology of Disability Fred 1:30 PM 3:30 PM R 6/9/2016 SHFE 141
    "MARA 10300 1 CRS First Year Marathi-3 Engblom 1:30 PM 3:30 PM F 6/10/2016 C 224
    "MARA 20300 1 CRS Second-Year Marathi-3 Engblom 1:30 PM 3:30 PM T 6/7/2016 C 224
    "MATH 13200 58 LEC Elem Functions And Calculus-2 Chonoles 4:00 PM 6:00 PM R 6/9/2016 SS 107
    "MATH 13300 10 LEC Elem Functions And Calculus-3 Moore 8:00 AM 10:00 AM W 6/8/2016 E 202
    "MATH 13300 20 LEC Elem Functions And Calculus-3 Banerjee 10:30 AM 12:30 PM F 6/10/2016 E 202
    "MATH 13300 22 LEC Elem Functions And Calculus-3 Chowdhury 10:30 AM 12:30 PM F 6/10/2016 E 203
    "MATH 13300 40 LEC Elem Functions And Calculus-3 Pham 10:30 AM 12:30 PM W 6/8/2016 SS 105
    "MATH 13300 42 LEC Elem Functions And Calculus-3 Cheng 10:30 AM 12:30 PM W 6/8/2016 SS 107
    "MATH 13300 44 LEC Elem Functions And Calculus-3 Howe 10:30 AM 12:30 PM W 6/8/2016 SS 108
    "MATH 13300 48 LEC Elem Functions And Calculus-3 Tran 10:30 AM 12:30 PM W 6/8/2016 P 016
    "MATH 13300 50 LEC Elem Functions And Calculus-3 Zhou 4:00 PM 6:00 PM R 6/9/2016 P 022
    "MATH 15300 11 LEC Calculus-3 Nagpal 8:00 AM 10:00 AM W 6/8/2016 RY 358
    "MATH 15300 20 LEC Calculus-3 di Fiore 8:00 AM 10:00 AM T 6/7/2016 HGS 184
    "MATH 15300 21 LEC Calculus-3 Nagpal 10:30 AM 12:30 PM F 6/10/2016 E 207
    "MATH 15300 22 LEC Calculus-3 Ding 8:00 AM 10:00 AM T 6/7/2016 E 312
    "MATH 15300 30 LEC Calculus-3 Rubin 10:30 AM 12:30 PM T 6/7/2016 SS 107
    "MATH 15300 31 LEC Calculus-3 Campos Salas 10:30 AM 12:30 PM M 6/6/2016 SS 105
    "MATH 15300 32 LEC Calculus-3 Chen 10:30 AM 12:30 PM T 6/7/2016 SS 105
    "MATH 15300 41 LEC Calculus-3 Chen 10:30 AM 12:30 PM W 6/8/2016 KPTC 101
    "MATH 15300 45 LEC Calculus-3 Chen 10:30 AM 12:30 PM W 6/8/2016 RO 011
    "MATH 15300 50 LEC Calculus-3 Leal 10:30 AM 12:30 PM R 6/9/2016 HGS 184
    "MATH 15300 51 LEC Calculus-3 Casto 4:00 PM 6:00 PM R 6/9/2016 P 016
    "MATH 15900 41 LEC Intro to Proof in Analysis & Lin. Alg. Shotton 10:30 AM 12:30 PM W 6/8/2016 RO 015
    "MATH 15900 45 LEC Intro to Proof in Analysis & Lin. Alg. Bate 10:30 AM 12:30 PM W 6/8/2016 E 312
    "MATH 15900 55 LEC Intro to Proof in Analysis & Lin. Alg. Bate 4:00 PM 6:00 PM R 6/9/2016 E 312
    "MATH 15900 57 LEC Intro to Proof in Analysis & Lin. Alg. Shotton 4:00 PM 6:00 PM R 6/9/2016 SS 108
    "MATH 16300 20 LEC Honors Calculus-3 Beaudry 8:00 AM 10:00 AM T 6/7/2016 RY 358
    "MATH 16300 21 LEC Honors Calculus-3 Zimmermann 10:30 AM 12:30 PM F 6/10/2016 RY 358
    "MATH 16300 30 LEC Honors Calculus-3 Creek 10:30 AM 12:30 PM T 6/7/2016 RY 358
    "MATH 16300 31 LEC Honors Calculus-3 Stehnova 10:30 AM 12:30 PM M 6/6/2016 RY 358
    "MATH 16300 32 LEC Honors Calculus-3 Levin 10:30 AM 12:30 PM T 6/7/2016 E 207
    "MATH 16300 33 LEC Honors Calculus-3 Hickman 10:30 AM 12:30 PM M 6/6/2016 SS 107
    "MATH 16300 41 LEC Honors Calculus-3 Brown 10:30 AM 12:30 PM W 6/8/2016 RY 358
    "MATH 16300 50 LEC Honors Calculus-3 Grigoriev 10:30 AM 12:30 PM R 6/9/2016 RY 358
    "MATH 16300 51 LEC Honors Calculus-3 Hurtado-Salazar 4:00 PM 6:00 PM R 6/9/2016 RY 358
    "MATH 19520 41 LEC Math Methods for Soc. Sci Chi 10:30 AM 12:30 PM W 6/8/2016 P 022
    "MATH 19520 49 LEC Math Methods for Soc. Sci Wu 10:30 AM 12:30 PM W 6/8/2016 HGS 184
    "MATH 19520 55 LEC Math Methods for Soc. Sci Ho 4:00 PM 6:00 PM R 6/9/2016 HGS 184
    "MATH 19520 59 LEC Math Methods for Soc. Sci Manning 4:00 PM 6:00 PM R 6/9/2016 K 102
    "MATH 19620 30 LEC Linear Algebra Filip 10:30 AM 12:30 PM T 6/7/2016 E 202
    "MATH 19620 32 LEC Linear Algebra Gadish 10:30 AM 12:30 PM T 6/7/2016 P 016
    "MATH 19620 50 LEC Linear Algebra Chai 10:30 AM 12:30 PM R 6/9/2016 E 202
    "MATH 19620 52 LEC Linear Algebra Frankel 10:30 AM 12:30 PM R 6/9/2016 E 207
    "MATH 19620 54 LEC Linear Algebra Apisa 10:30 AM 12:30 PM R 6/9/2016 E 308
    "MATH 20100 53 LEC Math Methods For Phy Sci-2 Jia 4:00 PM 6:00 PM R 6/9/2016 E 207
    "MATH 20100 55 LEC Math Methods For Phy Sci-2 Xue 4:00 PM 6:00 PM R 6/9/2016 E 202
    "MATH 20300 47 LEC Analysis In Rn-1 Lindsey 10:30 AM 12:30 PM W 6/8/2016 E 203
    "MATH 20300 49 LEC Analysis In Rn-1 Xue 10:30 AM 12:30 PM W 6/8/2016 E 202
    "MATH 20400 45 LEC Analysis In Rn-2 Snelson 10:30 AM 12:30 PM W 6/8/2016 E 207
    "MATH 20400 55 LEC Analysis In Rn-2 Haberman 4:00 PM 6:00 PM R 6/9/2016 RO 011
    "MATH 20500 31 LEC Analysis In Rn-3 Jing 10:30 AM 12:30 PM M 6/6/2016 E 308
    "MATH 20500 33 LEC Analysis In Rn-3 Snelson 10:30 AM 12:30 PM M 6/6/2016 E 207
    "MATH 20500 35 LEC Analysis In Rn-3 Ziesler 10:30 AM 12:30 PM M 6/6/2016 SS 108
    "MATH 20500 41 LEC Analysis In Rn-3 Jing 10:30 AM 12:30 PM W 6/8/2016 E 308
    "MATH 20500 51 LEC Analysis In Rn-3 Voda 4:00 PM 6:00 PM R 6/9/2016 E 308
    "MATH 20900 31 LEC Honors Analysis In Rn-3 Csornyei 10:30 AM 12:30 PM M 6/6/2016 E 206
    "MATH 21100 61 LEC Basic Numerical Analysis Demanet 1:30 PM 3:30 PM F 6/10/2016 E 203
    "MATH 23500 20 LEC Markov Chains, Martingales, and Brownian Motion Lawler 8:00 AM 10:00 AM T 6/7/2016 E 206
    "MATH 24100 50 LEC Topics In Geometry Chambers 10:30 AM 12:30 PM R 6/9/2016 E 206
    "MATH 24200 51 LEC Algebraic Number Theory Corlette 4:00 PM 6:00 PM R 6/9/2016 E 203
    "MATH 25500 51 LEC Basic Algebra-2 Le 4:00 PM 6:00 PM R 6/9/2016 E 206
    "MATH 25600 11 LEC Basic Algebra-3 Hickman 8:00 AM 10:00 AM W 6/8/2016 E 308
    "MATH 25600 31 LEC Basic Algebra-3 Le 10:30 AM 12:30 PM M 6/6/2016 E 312
    "MATH 25600 33 LEC Basic Algebra-3 Le Hung 10:30 AM 12:30 PM M 6/6/2016 P 016
    "MATH 25900 31 LEC Basic Algebra-3 (honors) Corlette 10:30 AM 12:30 PM M 6/6/2016 E 202
    "MATH 25900 33 LEC Basic Algebra-3 (honors) Emerton 10:30 AM 12:30 PM M 6/6/2016 E 203
    "MATH 26300 50 LEC Elem Algebraic Topology Zakharevich 10:30 AM 12:30 PM R 6/9/2016 E 203
    "MATH 27000 32 LEC Basic Complex Variables Smart 10:30 AM 12:30 PM T 6/7/2016 E 206
    "MATH 27400 20 LEC Diff Manifolds And Integration Dottener 8:00 AM 10:00 AM T 6/7/2016 E 203
    "MATH 27500 30 LEC Basic Thry Partial Diff Equ Feldman 10:30 AM 12:30 PM T 6/7/2016 E 203
    "MENG 20100 1 SEM Turning Science & Innovation into Impactful Technologies Guha 4:00 PM 6:00 PM M 6/6/2016 BSLC 305
    "MENG 24300 1 LEC The Engineering and Biology of Tissue Repair Hubbell 1:30 PM 3:30 PM F 6/10/2016 BSLC 240
    "MENG 26010 1 LEC Engineering Principles of Conservation Swartz 10:30 AM 12:30 PM R 6/9/2016 BSLC 305
    "MENG 26020 1 LEC Engineering Electrodynamics Cleland 8:00 AM 10:00 AM T 6/7/2016 P 022
    "MENG 29600 1 LEC Practice of Research Awschalom 1:30 PM 3:30 PM R 6/9/2016 RO 011
    "MENG 33400 1 CRS Applied Probability For Engineers Ghosh 10:30 AM 12:30 PM T 6/7/2016 C 112
    "MENG 34200 1 LEC Selec Tpcs Molec Engineering: Molecular/Materials Modelling II Galli 10:30 AM 12:30 PM T 6/7/2016 C 119
    "MICR 33000 1 CRS Bacteria/Bacteriophage Genetics and Cell Biology Crosson 1:30 PM 3:30 PM T 6/7/2016 Classroom not yet listed
    "MOGK 20300 1 CRS Intermediate Modern Greek-3 Koutsiviti 10:30 AM 12:30 PM W 6/8/2016 RO 432
    "MSBI 31100 1 CRS Introduction to Clinical Research Informatics McClintock 6:00 PM 8:00 PM T 6/7/2016 GC ARR
    "MSBI 31200 1 CRS Leadership and Management for Informaticians Baltasi 6:00 PM 8:00 PM T 6/7/2016 Classroom not yet listed
    "MUSI 10100 1 LEC Intro: Western Art Music Brodsky 8:00 AM 10:00 AM T 6/7/2016 LC 802
    "MUSI 10100 2 LEC Intro: Western Art Music Gordon 10:30 AM 12:30 PM R 6/9/2016 LC 901
    "MUSI 10100 3 LEC Intro: Western Art Music Hopkins 4:00 PM 6:00 PM R 6/9/2016 GO H 402
    "MUSI 10200 1 LEC Introduction To World Music Dempsey 1:30 PM 3:30 PM F 6/10/2016
    "MUSI 10200 3 CRS Introduction To World Music Gough 1:30 PM 3:30 PM T 6/7/2016 LC 901
    "MUSI 10200 4 LEC Introduction To World Music Nimjee 4:00 PM 6:00 PM W 6/8/2016 GO H 402
    "MUSI 10300 1 LEC Intro: Music Materials/Design Cheung 10:30 AM 12:30 PM T 6/7/2016 GO H 402
    "MUSI 10300 2 LEC Intro: Music Materials/Design Pukinskis 1:30 PM 3:30 PM R 6/9/2016 GO H 402
    "MUSI 10400 1 LEC Intro: Music Analysis/Criticism Loeffler 8:00 AM 10:00 AM T 6/7/2016 GO H 402
    "MUSI 12200 1 LEC Music In Western Civ-2 Kendrick 10:30 AM 12:30 PM M 6/6/2016 C 307
    "MUSI 15300 1 LEC Harmony and Voice Leading-3 Murphy 10:30 AM 12:30 PM M 6/6/2016 GO H 402
    "MUSI 15300 2 LEC Harmony and Voice Leading-3 Murphy 10:30 AM 12:30 PM W 6/8/2016 GO H 402
    "MUSI 23716 1 SEM Music of the Latin American Outlaws Sanchez Rojo 1:30 PM 3:30 PM T 6/7/2016 GO H 402
    "MUSI 24316 1 SEM Music and Melancholy Brodsky 10:30 AM 12:30 PM T 6/7/2016 LC 802
    "MUSI 25600 1 CRS Jazz Theory And Improvisation Bowden 4:00 PM 6:00 PM W 6/8/2016 Classroom not yet listed
    "MUSI 28116 1 CRS Piano Repertoire of the Twentieth Century Briggs 1:30 PM 3:30 PM F 6/10/2016 LC 703
    "MUSI 30716 1 CRS Opera as Idea and Performance Nussbaum 1:30 PM 3:30 PM R 6/9/2016 LBQ V
    "MUSI 34100 1 SEM Seminar: Composition Thomas 4:00 PM 6:00 PM T 6/7/2016 LC 901
    "NEAA 20003 1 LEC Art & Archaeology Near East -3: Levant Schloen 1:30 PM 3:30 PM T 6/7/2016 C 110
    "NEAA 20040 1 SEM Monuments and Monumentality in the Past and Present Osborne 8:00 AM 10:00 AM T 6/7/2016 C 106
    "NEAA 30080 1 SEM Migrations and Population Movements of the Ancient Near East Osborne 1:30 PM 3:30 PM F 6/10/2016 OR 208
    "NEHC 10101 1 LEC Intro To The Middle East Donner 10:30 AM 12:30 PM M 6/6/2016 RO 015
    "NEHC 20003 1 CRS History & Society of Ancient Near East-3 Goedegebuure 10:30 AM 12:30 PM W 6/8/2016 HM 130
    "NEHC 20013 1 LEC Ancient Empires-3 Siegel 1:30 PM 3:30 PM R 6/9/2016 HGS 101
    "NEHC 20503 1 LEC Islamic History & Society-3:The Modern Middle East Shissler 10:30 AM 12:30 PM T 6/7/2016 STU 104
    "NEHC 20603 1 LEC Islamic Thought and Literature-3 El Shamsy 10:30 AM 12:30 PM M 6/6/2016 HM 140
    "NEHC 20658 1 LEC Narrating Conflict in Modern Arabic Literature Hayek 1:30 PM 3:30 PM R 6/9/2016 WB 103
    "NEHC 20766 1 CRS Shamans & Oral Poets of Central Asia Arik 4:00 PM 6:00 PM R 6/9/2016 C 107
    "NEHC 30325 1 SEM The Medieval Muslim Curriculum El Shamsy 4:00 PM 6:00 PM W 6/8/2016 SS 106
    "NEHC 30722 1 SEM Iranian Political Culture II Payne 1:30 PM 3:30 PM R 6/9/2016 WB 130
    "NEHC 30833 1 SEM Late Ottoman History-2 Shissler 10:30 AM 12:30 PM R 6/9/2016 C 228
    "NEHC 30937 1 SEM Nationalism & Colonialism in the Middle East Bashkin 10:30 AM 12:30 PM M 6/6/2016 P 218
    "NELG 20901 1 SEM Adv Sem: Comparative Semitic Linguistics Hasselbach 1:30 PM 3:30 PM T 6/7/2016 OR 208
    "PBHS 35100 1 CRS Health Services Research Methods Sanghavi 1:30 PM 3:30 PM F 6/10/2016 BSLC 202
    "PBPL 24751 1 Dis The Business of Nonprofits and the Evolving Social Sector Velasquez 4:00 PM 6:00 PM W 6/8/2016 C 110
    "PBPL 25120 1 Dis Child Development and Public Policy Kalil 1:30 PM 3:30 PM M 6/6/2016 PBPL 289B
    "PBPL 25370 1 Dis Social Justice and Social Policy Marinescu 4:00 PM 6:00 PM W 6/8/2016 PBPL 289A
    "PBPL 26400 1 Dis Quantitative Methods in Public Policy Fowler 1:30 PM 3:30 PM R 6/9/2016 CLSC 101
    "PBPL 28805 1 Dis Behavioral Economics and Policy Leitzel 10:30 AM 12:30 PM R 6/9/2016 C 104
    "PERS 10103 1 LEC Elementary Persian-3 Ghahremani 10:30 AM 12:30 PM W 6/8/2016 C 102
    "PERS 20103 1 LEC Intermediate Persian-3 Ghahremani 1:30 PM 3:30 PM F 6/10/2016 CL 313
    "PHIL 23205 0 CRS Intro to Phenomenology Moati 4:00 PM 6:00 PM W 6/8/2016 STU 102
    "PHIL 27000 0 CRS Hist Phil-3: Kant And 19th C Conant 10:30 AM 12:30 PM R 6/9/2016 SS 122
    "PHIL 29200 1 CRS Junior Tutorial Amit 1:30 PM 3:30 PM F 6/10/2016 WB 106
    "PHIL 29300 1 CRS Senior Tutorial Amit 1:30 PM 3:30 PM F 6/10/2016 WB 103
    "PHSC 11000 0 LEC Sci/Earth: Envir Hist/Earth Webster 10:30 AM 12:30 PM W 6/8/2016 HGS 101
    "PHSC 13400 0 LEC Global Warming Archer 10:30 AM 12:30 PM F 6/10/2016 K 107
    "PHYS 12300 0 LEC General Physics-3 Grandi 10:30 AM 12:30 PM R 6/9/2016 KPTC 106
    "PHYS 13300 AA LEC Waves, Optics, & Heat Collar 10:30 AM 12:30 PM F 6/10/2016 KPTC 106
    "PHYS 13300 BB LEC Waves, Optics, & Heat Wakely 8:00 AM 10:00 AM T 6/7/2016 KPTC 106
    "PHYS 14300 AA LEC Honors Waves, Optics, & Heat Oreglia 10:30 AM 12:30 PM F 6/10/2016 KPTC 120
    "PHYS 14300 BB LEC Honors Waves, Optics, & Heat Schmitz 10:30 AM 12:30 PM T 6/7/2016 KPTC 120
    "PHYS 21103 1 LEC Experimental Physics-3 Simon 4:00 PM 6:00 PM M 6/6/2016 KPTC 120
    "PHYS 22000 1 LEC Introductory Math Methods of Physics Reid 10:30 AM 12:30 PM M 6/6/2016 KPTC 120
    "PHYS 22600 1 LEC Electronics Chin 10:30 AM 12:30 PM T 6/7/2016 KPTC 105
    "PHYS 22700 1 LEC Intermed Electr/Magnet-2 Levin 10:30 AM 12:30 PM F 6/10/2016 HGS 101
    "PHYS 23400 1 LEC Quantum Mechanics-1 Levin 10:30 AM 12:30 PM W 6/8/2016 KPTC 106
    "PHYS 23700 1 LEC Nuclei & Elementary Particles Kim 10:30 AM 12:30 PM M 6/6/2016 KPTC 103
    "PHYS 32300 1 LEC Advanced Electrodynamics-2 Savard 10:30 AM 12:30 PM W 6/8/2016 KPTC 105
    "PHYS 35200 1 LEC Statistical Mechanics Son 10:30 AM 12:30 PM T 6/7/2016 KPTC 103
    "PHYS 36300 1 LEC Particle Physics Wang 10:30 AM 12:30 PM M 6/6/2016 KPTC 105
    "PHYS 36700 1 LEC Soft Condensed Matter Phys Nagel 8:00 AM 10:00 AM T 6/7/2016 KPTC 105
    "PHYS 37100 1 LEC Introduction To Cosmology Wald 8:00 AM 10:00 AM W 6/8/2016 KPTC 105
    "PHYS 44500 1 LEC Quantum Field Theory-3 Carena 10:30 AM 12:30 PM F 6/10/2016 KPTC 101
    "PHYS 48400 1 LEC String Theory-2 Harvey 8:00 AM 10:00 AM T 6/7/2016 KPTC 103
    "PLSC 22913 1 LEC The Practice of Social Science Research Conley 10:30 AM 12:30 PM R 6/9/2016 STU 101
    "PLSC 25303 1 SEM Evaluating the Candidates in the 2016 Presidential Election Conley 8:00 AM 10:00 AM T 6/7/2016 SS 108
    "PLSC 25402 1 LEC Fragmented Politics and Global Markets Gulotty 8:00 AM 10:00 AM T 6/7/2016 HM 130
    "PLSC 28701 1 LEC Introduction to Political Theory Wilson 4:00 PM 6:00 PM W 6/8/2016 K 107
    "PLSC 28900 1 LEC Strategy Pape Jr 1:30 PM 3:30 PM F 6/10/2016 K 107
    "POLI 10303 1 CRS First Year Polish-3 Kosmala 10:30 AM 12:30 PM M 6/6/2016 C 201C
    "POLI 20303 1 CRS Second-Year Polish-3 Houle 10:30 AM 12:30 PM M 6/6/2016 C 224
    "PPHA 50600 1 CRS Urban Revitalization Project: Gary, Indiana Brown 8:00 AM 10:00 AM W 6/8/2016 PBPL 224
    "PSYC 20400 0 LEC Cognitive Psychology Berman 10:30 AM 12:30 PM T 6/7/2016 SS 122
    "PSYC 20700 1 LEC Sensation and Perception Le Doux 8:00 AM 10:00 AM T 6/7/2016 CLSC 101
    "PSYC 22500 1 SEM Cognitive Development O'Doherty 10:30 AM 12:30 PM M 6/6/2016 STU 101
    "PSYC 37900 1 LEC Experimental Design-2 Shevell 10:30 AM 12:30 PM T 6/7/2016 SS 401
    "REES 23137 1 CRS Narratives Suspense in European/Russian Lit/Film Peters 10:30 AM 12:30 PM W 6/8/2016 SS 106
    "REES 24401 1 CRS Vampires, Villains, & Magic: The Supernatural in Eastern Euro Franklin 10:30 AM 12:30 PM M 6/6/2016 HM 102
    "REES 25700 1 CRS Russian Lit from Modernism to Postmodernism King 1:30 PM 3:30 PM R 6/9/2016 F 408
    "RLST 10100 1 SEM Intro To Religious Studies Rosengarten 4:00 PM 6:00 PM W 6/8/2016 SS 107
    "RUSS 10303 1 CRS First-Year Russian-3 Houle 8:00 AM 10:00 AM R 6/9/2016 P 016
    "RUSS 10303 2 CRS First-Year Russian-3 Koehl 8:00 AM 10:00 AM R 6/9/2016 P 016
    "RUSS 10303 3 CRS First-Year Russian-3 Postema 8:00 AM 10:00 AM R 6/9/2016 P 016
    "RUSS 20303 1 CRS Second-Year Russian-3 Mandusic 4:00 PM 6:00 PM R 6/9/2016 C 205
    "RUSS 20902 1 CRS Third-Year Russ: Culture-3 Pichugin 10:30 AM 12:30 PM W 6/8/2016 C 201C
    "RUSS 21502 1 CRS Adv Russian Through Media-3 Pichugin 4:00 PM 6:00 PM R 6/9/2016 C 218
    "RUSS 29912 1 CRS Special Topics in Advanced Russian Pichugin 4:00 PM 6:00 PM W 6/8/2016 F 408
    "SALC 20200 1 CRS Intro To South Asian Civ-2 Majumdar 1:30 PM 3:30 PM F 6/10/2016 C 303
    "SALC 47302 1 CRS Transmission of Islamic Knowledge in South Asia since 1800 Robinson 1:30 PM 3:30 PM R 6/9/2016 F 209
    "SALC 49300 1 CRS South Asian Aesthetics: Rasa to Rap, Kamasutra to Kant Williams 1:30 PM 3:30 PM T 6/7/2016 C 115
    "SOCI 20106 1 CRS Political Sociology Clark 4:00 PM 6:00 PM M 6/6/2016 KPTC 106
    "SOCI 20112 1 CRS Appl Hierarchical Linear Model Raudenbush 10:30 AM 12:30 PM F 6/10/2016 SS 401
    "SOCI 20140 1 CRS Qualitative Field Methods McRoberts 10:30 AM 12:30 PM T 6/7/2016 SS 404
    "SOCI 20191 1 CRS Social Change in the United States Stolzenberg 10:30 AM 12:30 PM R 6/9/2016 HM 130
    "SOCI 20192 1 CRS The Effects of Schooling Stolzenberg 10:30 AM 12:30 PM T 6/7/2016 HM 130
    "SOCI 20204 1 CRS Sociology of Civil Society Lee 1:30 PM 3:30 PM T 6/7/2016 SS 404
    "SOCI 20233 1 CRS Race in Contemporary American Society Hicks-Bartlett 1:30 PM 3:30 PM F 6/10/2016 ED 151
    "SOCI 20236 1 CRS Political Modernization Garrido 1:30 PM 3:30 PM F 6/10/2016 SHFE 103
    "SOCI 20244 1 CRS Political Theology II Glaeser 4:00 PM 6:00 PM M 6/6/2016 SS 404
    "SOCI 28069 1 CRS Computing and Society Castelle 10:30 AM 12:30 PM R 6/9/2016 SS 404
    "SOSC 15300 2 DIS Classics Soc/Polit Thought-3 Ferreira 8:00 AM 10:00 AM M 6/6/2016 SHFE 141
    "SOSC 15300 4 DIS Classics Soc/Polit Thought-3 Lyons 8:00 AM 10:00 AM M 6/6/2016 C 102
    "SOSC 15300 6 DIS Classics Soc/Polit Thought-3 Little 8:00 AM 10:00 AM M 6/6/2016 HM 104
    "SOSC 15300 11 DIS Classics Soc/Polit Thought-3 Zaffini 8:00 AM 10:00 AM W 6/8/2016 HM 148
    "SOSC 15300 12 DIS Classics Soc/Polit Thought-3 Arlen 8:00 AM 10:00 AM M 6/6/2016 C 107
    "SOSC 15300 14 DIS Classics Soc/Polit Thought-3 Valiquette Moreau 8:00 AM 10:00 AM M 6/6/2016 HM 145
    "SOSC 15300 15 DIS Classics Soc/Polit Thought-3 Galloway 8:00 AM 10:00 AM M 6/6/2016 WB 103
    "SOSC 15300 16 DIS Classics Soc/Polit Thought-3 Arlen 8:00 AM 10:00 AM M 6/6/2016 C 107
    "SPAN 10200 1 LEC Beginning Elementary Spanish-2 Cajkova 8:00 AM 10:00 AM R 6/9/2016 C 116
    "SPAN 10300 1 LEC Beginning Elementary Spanish-3 Lear 8:00 AM 10:00 AM R 6/9/2016 K 107
    "SPAN 10300 2 LEC Beginning Elementary Spanish-3 Moraga Guerra 8:00 AM 10:00 AM R 6/9/2016 K 107
    "SPAN 10300 3 LEC Beginning Elementary Spanish-3 Lear 8:00 AM 10:00 AM R 6/9/2016 K 107
    "SPAN 10300 4 LEC Beginning Elementary Spanish-3 Rojas 8:00 AM 10:00 AM R 6/9/2016 K 107
    "SPAN 10300 5 LEC Beginning Elementary Spanish-3 Powers 8:00 AM 10:00 AM R 6/9/2016 K 107
    "SPAN 10300 6 LEC Beginning Elementary Spanish-3 Mateos Fernandez 8:00 AM 10:00 AM R 6/9/2016 K 107
    "SPAN 10300 7 LEC Beginning Elementary Spanish-3 Rojas 8:00 AM 10:00 AM R 6/9/2016 K 107
    "SPAN 20100 1 LEC Language History Culture-1 Indacoechea 8:00 AM 10:00 AM R 6/9/2016 C 115
    "SPAN 20100 2 LEC Language History Culture-1 Gutierrez Bascon 8:00 AM 10:00 AM R 6/9/2016 C 115
    "SPAN 20200 1 LEC Language History Culture-2 Van Den Hout 8:00 AM 10:00 AM R 6/9/2016 C 301
    "SPAN 20200 2 LEC Language History Culture-2 Tain Gutierrez 8:00 AM 10:00 AM R 6/9/2016 C 301
    "SPAN 20300 1 LEC Language History Culture-3 McCarron 8:00 AM 10:00 AM R 6/9/2016 CLSC 101
    "SPAN 20300 2 LEC Language History Culture-3 Hong 8:00 AM 10:00 AM R 6/9/2016 CLSC 101
    "SPAN 20300 3 LEC Language History Culture-3 Acevedo Moreno 8:00 AM 10:00 AM R 6/9/2016 CLSC 101
    "SPAN 20300 4 LEC Language History Culture-3 Sedlar 8:00 AM 10:00 AM R 6/9/2016 CLSC 101
    "SPAN 20400 1 LEC Composicion y conversacion avanzada I Mateos Fernandez 10:30 AM 12:30 PM W 6/8/2016 C 203
    "SPAN 20500 1 LEC Composicion y conversacion avanzada II Indacoechea 1:30 PM 3:30 PM F 6/10/2016 C 110
    "SPAN 20602 1 LEC Discurso Academico para Hablantes Nativos Van Den Hout 10:30 AM 12:30 PM M 6/6/2016 C 104
    "SPAN 21100 1 LEC Las Regiones Del Espanol Lozada Cerna 10:30 AM 12:30 PM M 6/6/2016 C 116
    "STAT 20000 1 CRS Elementary Statistics Burbank 10:30 AM 12:30 PM W 6/8/2016 E 133
    "STAT 22000 1 CRS Stat Meth And Applications Huang 10:30 AM 12:30 PM M 6/6/2016 SS 122
    "STAT 22000 2 CRS Stat Meth And Applications Huang 1:30 PM 3:30 PM M 6/6/2016 E 133
    "STAT 22200 1 CRS Linear Models And Exper Design Huang 10:30 AM 12:30 PM M 6/6/2016 SS 122
    "STAT 22400 1 CRS Applied Regression Analysis Burbank 4:00 PM 6:00 PM R 6/9/2016 SS 122
    "STAT 23400 1 CRS Statistical Models/Method-1 Dey 8:00 AM 10:00 AM T 6/7/2016 RO 015
    "STAT 23400 2 CRS Statistical Models/Method-1 Collins 10:30 AM 12:30 PM T 6/7/2016 HGS 101
    "STAT 23400 3 CRS Statistical Models/Method-1 Jahangoshahi 10:30 AM 12:30 PM R 6/9/2016 RO 015
    "STAT 24500 1 CRS Statistical Theory/Method-2 Chatterjee 8:00 AM 10:00 AM T 6/7/2016 E 133
    "STAT 24610 1 CRS Pattern Recognition Ke 10:30 AM 12:30 PM T 6/7/2016 E 133
    "STAT 25100 1 CRS Intro To Math Probability Weare 1:30 PM 3:30 PM T 6/7/2016 HGS 101
    "STAT 25150 1 CRS Intro to Math Probability - A Fefferman 10:30 AM 12:30 PM M 6/6/2016 E 133
    "STAT 26700 1 CRS History of Statistics Stigler 10:30 AM 12:30 PM F 6/10/2016 E 133
    "STAT 30210 1 CRS Bayesian Analysis and Principles of Statistics Stephens 1:30 PM 3:30 PM M 6/6/2016 GHJ 226
    "STAT 31100 1 CRS Mathematical Computation III: Numerical Methods for PDE's Demanet 4:00 PM 6:00 PM W 6/8/2016 HM 145
    "STAT 34700 1 CRS Generalized Linear Models Amit 1:30 PM 3:30 PM T 6/7/2016 E 133
    "STAT 35400 1 CRS Gene Regulation Reinitz 1:30 PM 3:30 PM T 6/7/2016 GHJ 226
    "STAT 37710 1 CRS Machine Learning Kondor 1:30 PM 3:30 PM R 6/9/2016 STU 101
    "STAT 37790 1 CRS Topics in Statistical Machine Learning Lafferty 4:00 PM 6:00 PM R 6/9/2016 GHJ 226
    "STAT 38300 1 CRS Measure-Theoretic Probability-III Ding 10:30 AM 12:30 PM M 6/6/2016 GHJ 226
    "STAT 48100 1 CRS High-Dimensional Statistics II Barber 10:30 AM 12:30 PM T 6/7/2016 GHJ 226
    "SWAH 25400 1 CRS Swahili-3 Mpiranya 10:30 AM 12:30 PM T 6/7/2016 C 218
    "TAML 10300 1 CRS First-Year Tamil-3 Annamalai 1:30 PM 3:30 PM T 6/7/2016 C 218
    "TAML 20300 1 CRS Second-Year Tamil-3 Annamalai 1:30 PM 3:30 PM R 6/9/2016 C 208
    "TBTN 10300 1 CRS First-Year Tibetan-3 Ngodup 10:30 AM 12:30 PM M 6/6/2016 C 208
    "TBTN 20300 1 CRS Second-Year Tibetan-3 Staff 4:00 PM 6:00 PM R 6/9/2016 C 224
    "TURK 10103 1 LEC Elementary Turkish-3 Arik 10:30 AM 12:30 PM F 6/10/2016 C 201A-B
    "TURK 10106 1 LEC Introduction to Old Turkic 2 Arik 1:30 PM 3:30 PM T 6/7/2016 C 207
    "TURK 30503 1 LEC Ottoman Turkish-3 Anetshofer-Karateke 8:00 AM 10:00 AM T 6/7/2016 C 210
}




@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond and greet the caller by name."""

    message_body = request.values.get('Body', None)
    if message_body in finals:
        classname = finals[message_body][1] + ""
        classprofessor = finals[message_body][2] + ""
        classweekday = finals[message_body][5] + ""
        classdate = finals[message_body][6] + ""
        finalbegin = finals[message_body][3] + ""
        finalend = finals[message_body][4] + ""
        finalroom = finals[message_body][7] + ""
        yourfinal = "Class Name: " + classname + "\nProfessor: " + classprofessor + "\nDate: " + classweekday + ", " + classdate + "\n" + "Location: " + finalroom + "\nTime: " + finalbegin + " - " + finalend + ""
        message = yourfinal
    else:
        message = "Class not found!\nMake sure you have the correct format of [Dept. Code] [Class Code] [Section Number].\nNote: you can find what section of a class is yours by going to http://classes.uchicago.edu.\nLastly, if you are sure you are sending the correct class, your class is not listed on the school's final exam schedule (you may have a seperate department exam schedule)."

    resp = twilio.twiml.Response()
    resp.message(message)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
