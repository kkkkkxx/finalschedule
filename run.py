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
    BIOS 11128 1 LEC Introduction to Human Genetics Christianson 10:30 AM 12:30 PM W 6/8/2016 BSLC 205
    BIOS 11132 1 LEC Genes, Evolution, and Society Lahn 1:30 PM 3:30 PM R 6/9/2016 BSLC 205
    BIOS 11133 1 LEC Human Variation, Race, and Genomics Lindo 4:00 PM 6:00 PM W 6/8/2016 BSLC 205
    BIOS 11140 1 LEC Biotechnology for the 21st Century Bhasin 10:30 AM 12:30 PM T 6/7/2016 BSLC 218
    BIOS 12115 1 LEC Responses of Cardiopulmonary System to Stress Gupta 8:00 AM 10:00 AM T 6/7/2016 BSLC 205
    BIOS 12117 1 LEC The 3.5 Billion Year History of the Human Body Shubin 1:30 PM 3:30 PM R 6/9/2016 BSLC 008
    BIOS 12120 1 LEC Pheromones: The Chemical Signals Around You. Ruvinsky 10:30 AM 12:30 PM T 6/7/2016 BSLC 001
    BIOS 13111 1 LEC Natural History of North American Deserts Larsen 1:30 PM 3:30 PM F 6/10/2016 BSLC 109
    BIOS 13112 0 LEC Natural History of North American Deserts; Field School Larsen 1:30 PM 3:30 PM F 6/10/2016 Classroom not yet listed
    BIOS 14114 0 LEC Drugs Galore: What They Are and What They Do To You Zaragoza 10:30 AM 12:30 PM R 6/9/2016 BSLC 218
    BIOS 14115 1 LEC From Social Neuroscience to Medical Neuroscience and Back Cacioppo 10:30 AM 12:30 PM R 6/9/2016 BSLC 008
    BIOS 15115 1 LEC Cancer Biology: How Good Cells Go Bad Villereal 10:30 AM 12:30 PM T 6/7/2016 BSLC 008
    BIOS 15123 1 LEC The Microbiome in Human and Environmental Health Gilbert 10:30 AM 12:30 PM T 6/7/2016 BSLC 205
    BIOS 20150 0 LEC How Can We Understand the Biosphere? Allesina 10:30 AM 12:30 PM T 6/7/2016 BSLC 109
    BIOS 20151 0 LEC Introduction to Quantitative Modeling in Biology Basic Kondrashov 8:00 AM 10:00 AM T 6/7/2016 BSLC 109
    BIOS 20152 0 LEC Introduction to Quantitative Modeling in Biology Advanced Kondrashov 1:30 PM 3:30 PM T 6/7/2016 BSLC 205
    BIOS 20171 0 LEC Human Genetics and Developmental Biology Christianson 10:30 AM 12:30 PM F 6/10/2016 BSLC 205
    BIOS 20172 0 LEC Mathematical Modeling for Pre-Med Students I. Jafari Haddadian 10:30 AM 12:30 PM W 6/8/2016 BSLC 109
    BIOS 20188 AA LEC Fundamentals of Physiology Mcgehee 10:30 AM 12:30 PM F 6/10/2016 BSLC 109
    BIOS 20189 BB LEC Fundamentals of Developmental Biology Ho 10:30 AM 12:30 PM M 6/6/2016 BSLC 109
    BIOS 20200 0 LEC Introduction To Biochemistry Makinen 4:00 PM 6:00 PM R 6/9/2016 BSLC 109
    BIOS 21207 1 LEC Cell Biology Lamppa 10:30 AM 12:30 PM M 6/6/2016 BSLC 240
    BIOS 21249 1 LEC Organization, Expression, and Transmission of Genome Information. Shapiro 10:30 AM 12:30 PM R 6/9/2016 BSLC 240
    BIOS 21317 1 LEC Topics in Biological Chemistry Rice 10:30 AM 12:30 PM W 6/8/2016 BSLC 218
    BIOS 21328 1 LEC Biophysics of Biomolecules Sosnick 4:00 PM 6:00 PM T 6/7/2016 KCBD 3200
    BIOS 21349 0 LEC Protein Structure and Functions in Medicine Tang 8:00 AM 10:00 AM T 6/7/2016 BSLC 313
    BIOS 21356 1 LEC Vertebrate Development Prince 10:30 AM 12:30 PM T 6/7/2016 BSLC 202
    BIOS 21407 1 LEC Image Processing In Biology Josephs 1:30 PM 3:30 PM M 6/6/2016 CLSC 119
    BIOS 21417 1 LEC Systems Biology: Molecular Regulatory Logic of Networks Aprison 10:30 AM 12:30 PM F 6/10/2016 BSLC 305
    BIOS 22236 1 LEC Reproductive Biology of Primates Martin 10:30 AM 12:30 PM W 6/8/2016 BSLC 305
    BIOS 22250 1 LEC Chordates: Evolution and Comparative Anatomy Coates 1:30 PM 3:30 PM T 6/7/2016 BSLC 305
    BIOS 22260 1 LEC Vertebrate Structure and Function Sereno 10:30 AM 12:30 PM T 6/7/2016 ACC F150
    BIOS 23100 1 LEC Dinosaur Science Sereno 8:00 AM 10:00 AM T 6/7/2016 ACC F150
    BIOS 23232 0 LEC Ecology & Evolution in the Southwest Larsen 1:30 PM 3:30 PM F 6/10/2016 Classroom not yet listed
    BIOS 23233 0 LEC Ecology & Evolution in the Southwest:Field School Larsen 1:30 PM 3:30 PM F 6/10/2016 Classroom not yet listed
    BIOS 23254 1 LEC Mammalian Ecology Larsen 10:30 AM 12:30 PM T 6/7/2016 BSLC 313
    BIOS 23299 1 LEC Plant Development/Molecular Genetics Greenberg 8:00 AM 10:00 AM T 6/7/2016 BSLC 305
    BIOS 23409 1 LEC The Ecology and Evolution of Infectious Diseases Dwyer 8:00 AM 10:00 AM T 6/7/2016 BSLC 240
    BIOS 23410 1 LEC Complex Interactions: Coevolution, Parasites, Mutualists, and Cheaters Lumbsch 4:00 PM 6:00 PM M 6/6/2016 BSLC 324
    BIOS 24205 1 LEC Systems Neuroscience Hale 1:30 PM 3:30 PM T 6/7/2016 BSLC 008
    BIOS 24218 1 LEC Molecular Neurobiology Sisodia 10:30 AM 12:30 PM R 6/9/2016 BSLC 313
    BIOS 24232 1 LEC Computational Approaches to Cogintive Neuroscience Hatsopoulos 1:30 PM 3:30 PM R 6/9/2016 BSLC 240
    BIOS 24408 1 LEC Modeling and Signal Analysis for Neuroscientists Van Drongelen 1:30 PM 3:30 PM F 6/10/2016 BSLC 401
    BIOS 25109 1 LEC Tpcs: Reproductive Bio/Cancer Greene 10:30 AM 12:30 PM T 6/7/2016 BSLC 240
    BIOS 25126 1 LEC Animal Models of Human Disease Niekrasz 4:00 PM 6:00 PM W 6/8/2016 BSLC 001
    BIOS 25228 1 LEC Endocrinology III: Human Disease Musch 4:00 PM 6:00 PM R 6/9/2016 BSLC 001
    BIOS 25287 1 LEC Introduction to Virology Manicassamy 1:30 PM 3:30 PM F 6/10/2016 BSLC 001
    BIOS 25308 1 LEC Heterogeneity in Human Cancer: Etiology and Treatment Macleod 1:30 PM 3:30 PM R 6/9/2016 BSLC 202
    BIOS 28407 1 LEC Genomics and Systems Biology Gilad 1:30 PM 3:30 PM T 6/7/2016 BSLC 218
    BIOS 29326 1 LEC Intro: Medical Physics Armato III 1:30 PM 3:30 PM T 6/7/2016 BSLC 240
    CABI 32000 1 LEC Translational Approaches in Cancer Biology Macleod 1:30 PM 3:30 PM T 6/7/2016 BSLC 202
    CAPP 30123 1 LEC Computer Science with Applications-3 Wachs 10:30 AM 12:30 PM F 6/10/2016 RY 276
    CAPP 30235 1 LEC Databases for Public Policy Elmore 8:00 AM 10:00 AM T 6/7/2016 RY 277
    CAPP 30254 1 LEC Machine Learning for Public Policy Ghani 10:30 AM 12:30 PM T 6/7/2016 RY 276
    CATA 11100 1 LEC Accelerated Catalan I Girons Masot 10:30 AM 12:30 PM M 6/6/2016 C 210
    CATA 21600 1 LEC Catalan Culture and Society: Art, Music, and Cinema Girons Masot 10:30 AM 12:30 PM W 6/8/2016 C 210
    CCTS 40006 1 CRS Pharmacogenomics: Discovery and Implementation Huang 10:30 AM 12:30 PM M 6/6/2016 BSLC 305
    CHDV 20890 1 SEM Mental Health: International and Social Perspectives Sandhya 1:30 PM 3:30 PM F 6/10/2016 RO 329
    CHDV 20890 2 SEM Mental Health: International and Social Perspectives Sandhya 4:00 PM 6:00 PM M 6/6/2016 RO 432
    CHDV 21901 1 CRS Language, Culture, and Thought Lucy 1:30 PM 3:30 PM T 6/7/2016 HM 130
    CHEM 11300 1 LEC Comprehensive General Chemistry-III Lee 10:30 AM 12:30 PM M 6/6/2016 K 107
    CHEM 11300 2 LEC Comprehensive General Chemistry-III Roux 10:30 AM 12:30 PM M 6/6/2016 K 120
    CHEM 12300 0 LEC Honors General Chemistry-3 Voth 8:00 AM 10:00 AM W 6/8/2016 K 120
    CHEM 20200 1 LEC Inorganic Chemistry-2 Jordan 10:30 AM 12:30 PM M 6/6/2016 K 102
    CHEM 22200 0 LEC Organic Chemistry-3 Snyder 10:30 AM 12:30 PM T 6/7/2016 K 107
    CHEM 23200 0 LEC Honors Organic Chemistry-3 Rawal 10:30 AM 12:30 PM T 6/7/2016 K 120
    CHEM 26300 1 LEC Chem Kinetic/Dynamics Butler 10:30 AM 12:30 PM F 6/10/2016 K 102
    CHEM 26800 1 LEC Computational Chemistry and Biology Dinner 8:00 AM 10:00 AM T 6/7/2016 K 120
    CHEM 30900 1 LEC Bioinorganic Chemistry He 8:00 AM 10:00 AM T 6/7/2016 K 102
    CHEM 36500 1 LEC Chemical Dynamics Sibener 10:30 AM 12:30 PM T 6/7/2016 K 102
    CHEM 36700 1 LEC Experimental Physical Chemistry Special Topics Scherer 10:30 AM 12:30 PM T 6/7/2016 K 101
    CHEM 38700 1 LEC Biophysical Chemistry Tokmakoff 8:00 AM 10:00 AM T 6/7/2016 K 101
    CHIN 10300 ALL CRS Elementary Modern Chinese-3 Staff 8:00 AM 10:00 AM W 6/8/2016 C 319
    CHIN 10300 ALL CRS Elementary Modern Chinese-3 Staff 10:30 AM 12:30 PM M 6/6/2016 C202
    CHIN 11300 1 CRS First -Yr. Chinese for Bilinqual Speakers-3 Yang 10:00 AM 12:00PM M 6/6/2016 C 304
    CHIN 20300 ALL CRS Intermediate Modern Chinese-3 Staff 8:00 AM 10:00 AM R 6/9/2016 STU 104
    CHIN 21300 1 CRS Accelerated Chinese for Bilingual Speakers-3 Xu 8:00 AM 10:00 AM M 6/6/2016 C 430
    CHIN 30300 1 CRS Advanced Modern Chinese-3 Yang 10:00 AM 12:00PM W 6/8/2016 C 304
    CHIN 30300 2 CRS Advanced Modern Chinese-3 Xu 8:00 AM 10:00 AM R 6/8/2016 C 213
    CHIN 41300 1 CRS Fourth-Year Modern Chinese-3 Kuo 8:00 AM 10:00 AM R 6/9/2016 C 103
    CHIN 51300 1 CRS Fifth-Year Modern Chinese-3 Wang 8:00 AM 10:00 AM R 6/9/2016 C 104
    CLAS 34515 1 CRS Money and the Ancient Greek World Bresson 1:30 PM 3:30 PM F 6/10/2016 C 409
    CLAS 35415 1 CRS Text into Data: Digital Philology Dik 1:30 PM 3:30 PM T 6/7/2016 CL 021
    CLAS 45716 1 SEM Sem: Ghosts, Demons & Supernatural Danger in the Anc. World Lincoln 1:30 PM 3:30 PM F 6/10/2016 CL 021
    CLCV 25808 1 CRS Roman Law Ando 10:30 AM 12:30 PM R 6/9/2016 HM 140
    CLCV 28315 1 SEM Ephron Seminar Gouvea 10:30 AM 12:30 PM R 6/9/2016 HM 150
    CLCV 29000 1 CRS Myth Course Shandruk 1:30 PM 3:30 PM T 6/7/2016 HM 150
    CMSC 11000 1 LEC Multimed Prog: Interdisc Art-1 Sterner 1:30 PM 3:30 PM R 6/9/2016 RY 277
    CMSC 12300 1 LEC Computer Science with Applications-3 Wachs 10:30 AM 12:30 PM F 6/10/2016 RY 277
    CMSC 15200 1 LEC Intro To Computer Science-2 Franklin 1:30 PM 3:30 PM F 6/10/2016 STU 101
    CMSC 15400 1 LEC Intro To Computer Systems Hoffmann 10:30 AM 12:30 PM M 6/6/2016 RY 251
    CMSC 15400 2 LEC Intro To Computer Systems Gunawi 10:30 AM 12:30 PM W 6/8/2016 RY 251
    CMSC 15400 3 LEC Intro To Computer Systems Wachs 1:30 PM 3:30 PM F 6/10/2016 RY 251
    CMSC 22001 1 LEC Software Construction Lu 1:30 PM 3:30 PM R 6/9/2016 RY 276
    CMSC 22010 1 LEC Digital Fabrication Stevens 1:30 PM 3:30 PM F 6/10/2016 SCL 240
    CMSC 22100 1 LEC Programming Languages Shaw 10:30 AM 12:30 PM R 6/9/2016 RY 251
    CMSC 23310 1 LEC Advanced Distributed Systems Sotomayor Basilio 4:00 PM 6:00 PM W 6/8/2016 C 112
    CMSC 23310 2 LEC Advanced Distributed Systems Sotomayor Basilio 4:00 PM 6:00 PM M 6/6/2016 C 112
    CMSC 23900 1 LEC Data Visualization Kindlmann 10:30 AM 12:30 PM T 6/7/2016 RY 251
    CMSC 25020 1 LEC Computational Linguistics Goldsmith 10:30 AM 12:30 PM M 6/6/2016 K 101
    CMSC 27200 1 LEC Theory of Algorithms Simon 10:30 AM 12:30 PM F 6/10/2016 RY 251
    CMSC 27230 1 LEC Honors Theory of Algorithms Drucker 10:30 AM 12:30 PM W 6/8/2016 RY 276
    CMSC 27410 1 LEC Honors Combinatorics Babai 10:30 AM 12:30 PM R 6/9/2016 RY 276
    CMSC 27500 1 LEC Graph Theory Mulmuley 8:00 AM 10:00 AM T 6/7/2016 RY 251
    CMSC 27610 1 LEC Digital Biology Scott 8:00 AM 10:00 AM T 6/7/2016 RY 276
    CMSC 28100 1 LEC Intro Complexity Theory Mulmuley 1:30 PM 3:30 PM T 6/7/2016
    CMSC 32001 1 LEC Topics: Programming Langs. Chugh 1:30 PM 3:30 PM R 6/9/2016 P 022
    CMSC 33001 1 LEC Topics in Systems Chong 1:30 PM 3:30 PM T 6/7/2016 RY 277
    CMSC 33251 1 LEC Topics in Computer Security Feldman 1:30 PM 3:30 PM F 6/10/2016 RY 277
    CMSC 34900 1 LEC Topics In Scientific Computing Scott 10:30 AM 12:30 PM R 6/9/2016 RY 277
    CMSC 35050 1 LEC Computational Linguistics Goldsmith 10:30 AM 12:30 PM M 6/6/2016 K 101
    CMSC 37120 1 LEC Topics in Discrete Mathematics Razborov 10:30 AM 12:30 PM T 6/7/2016 RY 277
    CMSC 37200 1 LEC Combinatorics Babai 10:30 AM 12:30 PM R 6/9/2016 Classroom not yet listed
    CMSC 38100 1 CRS Computability Theory-2 Hirschfeldt 1:30 PM 3:30 PM T 6/7/2016 Classroom not yet listed
    CRWR 12013 1 SEM Special Topics in Fiction: Genre Rules and Rebels DeWoskin 10:30 AM 12:30 PM T 6/7/2016 M 102
    CRWR 22115 1 SEM Advanced Fiction Workshop: Characters in Conflict DeWoskin 1:30 PM 3:30 PM F 6/10/2016 M 102
    CRWR 27103 1 CRS Advanced Screenwriting Petrakis 1:30 PM 3:30 PM R 6/9/2016 LC 802
    EALC 19900 1 CRS Early Modern Japanese History Toyosawa 4:00 PM 6:00 PM W 6/8/2016 C 303
    ECON 19800 1 LEC Introduction To Microeconomics Sanderson 1:30 PM 3:30 PM M 6/6/2016 SS 122
    ECON 19800 2 CRS Introduction To Microeconomics List 1:30 PM 3:30 PM R 6/9/2016 SS 122
    ECON 20000 ALL LEC Elements of Economic Analysis-1 Tsiang 6:30 PM 8:30 PM M 6/6/2016 SHFE 146
    ECON 20010 1 LEC Elements of Economics Analysis 1: Honors Cuesta Rodriguez 1:30 PM 3:30 PM T 6/7/2016 STU 102
    ECON 20200 1 LEC Elements of Economic Analysis-3 Tartari 8:00 AM 10:00 AM W 6/8/2016 STU 104
    ECON 20200 2 LEC Elements of Economic Analysis-3 Tartari 10:30 AM 12:30 PM M 6/6/2016 STU 104
    ECON 20200 3 LEC Elements of Economic Analysis-3 Lopes de Melo 6:30 PM 8:30 PM M 6/6/2016 Classroom not yet listed
    ECON 20200 4 LEC Elements of Economic Analysis-3 Lopes de Melo 6:30 PM 8:30 PM M 6/6/2016 Classroom not yet listed
    ECON 20200 5 LEC Elements of Economic Analysis-3 Lopes de Melo 6:30 PM 8:30 PM M 6/6/2016 Classroom not yet listed
    ECON 20210 1 LEC Elements of Economics Analysis 3-HONORS van Vliet 1:30 PM 3:30 PM T 6/7/2016 RO 015
    ECON 20300 1 CRS Elements of Economic Analysis-4 Wang 10:30 AM 12:30 PM M 6/6/2016 SHFE 146
    ECON 20300 2 LEC Elements of Economic Analysis-4 Hughes 10:30 AM 12:30 PM R 6/9/2016 SHFE 146
    ECON 20310 1 LEC Elements of Economics Analysis 4:HONORS Yoshida 1:30 PM 3:30 PM T 6/7/2016 SHFE 203
    ECON 20700 1 LEC Game Theory and Economic Applications Myerson 10:30 AM 12:30 PM M 6/6/2016 SHFE 021
    ECON 20740 1 LEC Analysis of Collective Decision-Making van Weelden 8:00 AM 10:00 AM W 6/8/2016 SHFE 146
    ECON 20900 1 LEC Intro To Econometrics: Honors Gay 4:00 PM 6:00 PM W 6/8/2016 SHFE 203
    ECON 21000 1 LEC Econometrics A Hickman 4:00 PM 6:00 PM W 6/8/2016 SHFE 146
    ECON 21000 2 LEC Econometrics A Hickman 4:00 PM 6:00 PM M 6/6/2016 SHFE 203
    ECON 21000 3 LEC Econometrics A PENDING 10:30 AM 12:30 PM R 6/9/2016 SHFE 203
    ECON 21000 4 LEC Econometrics A Bittmann 8:00 AM 10:00 AM T 6/7/2016 RO 011
    ECON 21150 1 LEC Topics in Applied Econometrics Tartari 1:30 PM 3:30 PM F 6/10/2016 SHFE 203
    ECON 21200 1 LEC Time Series Econometrics Marrone 10:30 AM 12:30 PM R 6/9/2016 STU 104
    ECON 21410 1 LEC Computational Methods in Economics Browne 8:00 AM 10:00 AM T 6/7/2016 SHFE 203
    ECON 23000 1 LEC Money and Banking Yoshida 8:00 AM 10:00 AM T 6/7/2016 SHFE 021
    ECON 25000 1 LEC Introduction To Finance Choi 4:00 PM 6:00 PM W 6/8/2016 RO 011
    ECON 25100 1 LEC Financial Economics B: Speculative Markets Alvarez 10:30 AM 12:30 PM T 6/7/2016 STU 105
    ECON 26600 1 LEC Urban Economics Tolley 10:30 AM 12:30 PM W 6/8/2016 SHFE 203
    ECON 30300 1 LEC Price Theory-3 Reny 1:30 PM 3:30 PM T 6/7/2016 SHFE 146
    ECON 30701 1 LEC Evolutionary Game Theory Szentes 8:00 AM 10:00 AM T 6/7/2016 SHFE 103
    ECON 31200 1 LEC Empirical Analysis-3 Bonhomme 10:30 AM 12:30 PM T 6/7/2016 STU 101
    ECON 31710 1 LEC Identification in Nonlinear Econometric Models Torgovitsky 1:30 PM 3:30 PM F 6/10/2016 P 222
    ECON 33200 1 LEC Theory of Income-3 Mulligan 8:00 AM 10:00 AM W 6/8/2016 SHFE 203
    ECON 34901 1 LEC Social Interactions and Inequality Durlauf 10:30 AM 12:30 PM M 6/6/2016 SHFE 103
    ECON 35003 1 LEC Human Capital, Markets, and the Family Heckman 4:00 PM 6:00 PM M 6/6/2016 SHFE 141
    ECON 35301 1 LEC International Trade & Growth Lucas Jr 10:30 AM 12:30 PM T 6/7/2016 SHFE 103
    ECON 40104 1 LEC Advanced Industrial Organization IV Hickman 6:00 PM 8:00 PM T 6/7/2016 SHFE 103
    ECON 50300 1 SEM Becker Applied Economics Workshop List 1:30 PM 3:30 PM R 6/9/2016 SHFE 146
    EGPT 10103 1 LEC Middle Egyptian Texts-1 Singer 10:30 AM 12:30 PM F 6/10/2016 C 102
    EGPT 20110 1 LEC Introduction to Old Egyptian Hainline 10:30 AM 12:30 PM M 6/6/2016 OR 208
    EGPT 20210 1 LEC Introduction to Late Egyptian Johnson 10:30 AM 12:30 PM F 6/10/2016 OR 208
    ENGL 20222 1 CRS Introduction to British Romantic Literature Hansen 10:30 AM 12:30 PM R 6/9/2016 SHFE 103
    ENST 24102 1 CRS Environmental Politics Lodato 4:00 PM 6:00 PM T 6/7/2016 HM 130
    ENST 27120 1 SEM Historical Ecology of the Calumet Region Lycett 10:30 AM 12:30 PM F 6/10/2016 WB 102
    ENST 27220 1 SEM Environmental Management and Planning in the Calumet Region Shaikh 10:30 AM 12:30 PM T 6/7/2016 SHFE 242
    ENST 27320 1 SEM Topics in the Ecology of the Calumet Region Anastasio 10:30 AM 12:30 PM M 6/6/2016 CL 313
    FINM 32400 1 LEC Computing for Finance-3 Liyanaarachchi 6:00 PM 8:00 PM T 6/7/2016 MS 112
    FINM 33150 1 LEC Regression Analysis and Quantitative Trading Strategies Boonstra 6:00 PM 8:00 PM W 6/8/2016 MS 112
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
