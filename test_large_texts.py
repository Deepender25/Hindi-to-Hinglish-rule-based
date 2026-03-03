"""
Comprehensive Test Suite for Hindi to Hinglish Converter
Tests large paragraphs with expected outputs - EXTENDED VERSION
"""

import sys
import io
from hinglish_converter import HinglishConverter

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# Comprehensive test cases with expected outputs
TEST_CASES = [
    {
        "name": "Daily Conversation - Greeting",
        "hindi": "नमस्ते दोस्तों! आप सब कैसे हैं? मुझे उम्मीद है आप सब ठीक होंगे। आज का दिन बहुत सुहाना है।",
        "expected": "namaste doston! aap sab kaise hain? mujhe umeed hai aap sab theek honge. aaj ka din bahut suhaana hai.",
    },
    {
        "name": "Family Scene - Dinner Time",
        "hindi": "मेरी माँ ने आज बहुत स्वादिष्ट खाना बनाया है। पूरी, सब्जी, दाल और चावल सब कुछ बहुत अच्छा लग रहा है। हम सब परिवार के साथ बैठकर खाना खाएंगे।",
        "expected": "meri maa ne aaj bahut swaadisht khana banaaya hai. poori, sabzi, daal aur chawal sab kuchh bahut achha lag raha hai. hum sab parivaar ke saath baithkar khana khaaenge.",
    },
    {
        "name": "School/College Scene",
        "hindi": "मुझे सुबह स्कूल जाना है। मेरे सभी दोस्त वहाँ मिलेंगे। हमें पढ़ाई करनी है और फिर खेल खेलना है। शिक्षक आज एक नया पाठ पढ़ाएंगे।",
        "expected": "mujhe subah school jaana hai. mere sabhi dost vahaan milenge. hamein padhaai karni hai aur phir khel khelna hai. shikshak aaj ek naya paath padhaaenge.",
    },
    {
        "name": "Shopping - Market Visit",
        "hindi": "मैं बाजार जा रहा हूं। मुझे सब्जियां और फल खरीदने हैं। टमाटर, आलू, प्याज, गोभी सब लेना है। क्या आपको भी कुछ चाहिए?",
        "expected": "main bazaar ja raha hoon. mujhe sabziyaan aur phal khareedne hain. tamaatar, aaloo, pyaaz, gobhi sab lena hai. kya aapko bhi kuchh chahiye?",
    },
    {
        "name": "Weather - Rainy Day",
        "hindi": "आज बहुत गर्मी है। धूप बहुत तेज है। मुझे पानी पीना है। शाम को शायद बारिश होगी। मौसम बदल रहा है।",
        "expected": "aaj bahut garmi hai. dhoop bahut tez hai. mujhe paani peena hai. shaam ko shaayad baarish hogi. mausam badal raha hai.",
    },
    {
        "name": "Emotions - Happiness",
        "hindi": "मैं आज बहुत खुश हूं। मुझे अपने दोस्तों के साथ समय बिताना पसंद है। हम हंसते हैं और मज़ा करते हैं। जिंदगी अच्छी है।",
        "expected": "main aaj bahut khush hoon. mujhe apne doston ke saath samay bitaana pasand hai. hum hansate hain aur maza karte hain. zindagi achhi hai.",
    },
    {
        "name": "Technology - Phone Issue",
        "hindi": "मेरा मोबाइल फोन खराब हो गया। स्क्रीन टूट गई है। मुझे नया फोन खरीदना है। मैं इंटरनेट से ऑर्डर करूंगा। डिलीवरी कल तक आ जाएगी।",
        "expected": "mera mobile phone kharaab ho gaya. screen toot gayi hai. mujhe naya phone khareedna hai. main internet se order karunga. delivery kal tak aa jaayegi.",
    },
    {
        "name": "Health - Doctor Visit",
        "hindi": "मुझे सिरदर्द हो रहा है। बुखार भी है। मुझे दवा लेनी होगी। कल मैं डॉक्टर से मिलूंगा। उम्मीद है जल्दी ठीक हो जाऊंगा।",
        "expected": "mujhe sirdard ho raha hai. bukhaar bhi hai. mujhe dawa leni hogi. kal main doctor se milunga. umeed hai jaldi theek ho jaoonga.",
    },
    {
        "name": "Travel - Train Journey",
        "hindi": "हम कल शहर जा रहे हैं। हम ट्रेन से जाएंगे। स्टेशन पर सुबह सात बजे पहुंचेंगे। वहाँ हम अपने रिश्तेदारों से मिलेंगे।",
        "expected": "hum kal shehar ja rahe hain. hum train se jaaenge. station par subah saat baje pahunchenge. vahaan hum apne rishtedaaron se milenge.",
    },
    {
        "name": "Food - Cooking",
        "hindi": "मुझे खाना पकाना पसंद है। मैं आलू की सब्जी और दाल चावल बनाऊंगा। घी और मसाले डालकर स्वादिष्ट बनाऊंगा। यह बहुत स्वादिष्ट होगा।",
        "expected": "mujhe khana pakaana pasand hai. main aaloo ki sabzi aur daal chawal banaunga. ghee aur masaale daalkar swaadisht banaunga. yah bahut swaadisht hoga.",
    },
    {
        "name": "Movie Experience",
        "hindi": "कल मैं अपने दोस्तों के साथ सिनेमा गया। हमने एक नई फिल्म देखी जो बहुत अच्छी थी। फिल्म में एक लड़का और लड़की की कहानी दिखाई गई थी। उनकी दोस्ती बहुत प्यारी थी। हम सबने बहुत एंजॉय किया।",
        "expected": "kal main apne doston ke saath cinema gaya. hamne ek nayi film dekhi jo bahut achhi thi. film mein ek ladka aur ladki ki kahaani dikhaayi gayi thi. unki dostee bahut pyaari thi. hum sabne bahut enjoy kiya.",
    },
    {
        "name": "Moral Story - Honesty",
        "hindi": "एक समय की बात है। एक गांव में एक बूढ़ा आदमी रहता था। उसके पास एक बेटा और एक बेटी थी। वह बहुत गरीब था लेकिन बहुत ईमानदार था। वह हर रोज़ जंगल से लकड़ियां इकट्ठी करके बेचता था।",
        "expected": "ek samay ki baat hai. ek gaanv mein ek boodha aadmi rehta tha. uske paas ek beta aur ek beti thi. vah bahut gareeb tha lekin bahut imaandaar tha. vah har roz jungle se lakdiyan ikatthi karke bechta tha.",
    },
    {
        "name": "Question Answer Format",
        "hindi": "तुम कहाँ जा रहे हो? मैं बाजार जा रहा हूं। तुम क्या खरीदोगे? मुझे कुछ सब्जियां चाहिए। क्या तुम मेरे साथ चलोगे? हां, ज़रूर।",
        "expected": "tum kahaan ja rahe ho? main bazaar ja raha hoon. tum kya khareedoge? mujhe kuchh sabziyaan chahiye. kya tum mere saath chaloge? haan, zaroor.",
    },
    {
        "name": "Childhood Memories",
        "hindi": "जब मैं छोटा था तो मैं अपनी दादी के साथ रहता था। वह मुझे हर रात कहानियां सुनाती थीं। मुझे उनकी कहानियां बहुत पसंद थीं। वह मुझे अच्छे संस्कार सिखाती थीं।",
        "expected": "jab main chhota tha toh main apni dadi ke saath rehta tha. vah mujhe har raat kahaaniyaan sunaati thiin. mujhe unki kahaaniyaan bahut pasand thiin. vah mujhe achchhe sanskaar sikhaati thiin.",
    },
    {
        "name": "WhatsApp Chat Style",
        "hindi": "हेलो भाई! क्या हाल है? सब ठीक है ना? कल पार्टी में आ रहे हो ना? टाइम से पहुंचना। बहुत मज़ा करेंगे।",
        "expected": "hello bhai! kya haal hai? sab theek hai naa? kal party mein aa rahe ho naa? time se pahunchna. bahut maza karenge.",
    },
    {
        "name": "Formal Invitation",
        "hindi": "प्रिय मित्र, आशा है आप कुशल मंगल होंगे। आपको यह पत्र लिखते हुए मुझे बहुत खुशी हो रही है। मैं आपको अपने नए घर में आमंत्रित करना चाहता हूं। कृप्या इस रविवार आएं।",
        "expected": "priya mitr, aasha hai aap kushal mangal honge. aapko yah patra likhte hue mujhe bahut khushi ho rahi hai. main aapko apne naye ghar mein aamantrit karna chahta hoon. kripya is ravivaar aayen.",
    },
    {
        "name": "Festival - Diwali",
        "hindi": "दीवाली का त्योहार आ रहा है। हम अपने घर को साफ कर रहे हैं। नए कपड़े खरीदेंगे। मिठाइयां बनाएंगे। पटाखे जलाएंगे। सबको बधाई देंगे।",
        "expected": "diwali ka tyohaar aa raha hai. hum apne ghar ko saaf kar rahe hain. naye kapde khareedenge. mithaiyaan banaaenge. pataakhe jalaayenge. sabko badhaai denge.",
    },
    {
        "name": "Religious Context",
        "hindi": "भगवान राम एक अच्छे राजा थे। उन्होंने अयोध्या में बहुत अच्छा शासन किया। लोग उन्हें प्यार करते थे। उनकी कहानी रामायण में लिखी है। हमें उनसे बहुत कुछ सीखना चाहिए।",
        "expected": "bhagwan raam ek achchhe raja the. unhone ayodhya mein bahut achha shaasan kiya. log unhein pyaar karte the. unki kahaani raamayan mein likhi hai. hamein unse bahut kuchh seekhna chahiye.",
    },
    {
        "name": "Love Story - Romantic",
        "hindi": "राहुल और प्रिया एक दूसरे से बहुत प्यार करते थे। वे हर रोज़ मिलते थे। एक दूसरे को तोहफे देते थे। उनकी शादी बहुत धूमधाम से हुई। वे खुशी से रहने लगे।",
        "expected": "rahul aur priya ek dusre se bahut pyaar karte the. ve har roz milte the. ek dusre ko tohfe dete the. unki shaadi bahut dhoomdhaam se hui. ve khushi se rehne lage.",
    },
    {
        "name": "Sad Emotional",
        "hindi": "आज मैं बहुत उदास हूं। मेरा दिल टूट गया है। मुझे किसी से बात नहीं करनी है। मैं अकेला रहना चाहता हूं। दुख की घड़ी है यह।",
        "expected": "aaj main bahut udaas hoon. mera dil toot gaya hai. mujhe kisi se baat nahi karni hai. main akela rehna chahta hoon. dukh ki ghadi hai yah.",
    },
    {
        "name": "Angry Conversation",
        "hindi": "तुमने यह क्या किया? मुझे बहुत गुस्सा आ रहा है। तुम मेरी बात नहीं सुनते हो। अब और नहीं। मैं तुमसे बात नहीं करूंगा।",
        "expected": "tumne yah kya kiya? mujhe bahut gussa aa raha hai. tum meri baat nahi sunte ho. ab aur nahi. main tumse baat nahi karoonga.",
    },
    {
        "name": "News Report Style",
        "hindi": "आज सुबह एक बड़ी दुर्घटना हुई। एक बस और ट्रक में टक्कर हो गई। दस लोग घायल हुए हैं। पुलिस मौके पर पहुंच गई है। जांच जारी है।",
        "expected": "aaj subah ek badi durghatna hui. ek bus aur truck mein takkar ho gayi. das log ghaayal hue hain. police mauke par pahunch gayi hai. jaanch jaari hai.",
    },
    {
        "name": "Office/Workplace",
        "hindi": "सर, मुझे कल छुट्टी चाहिए। मेरे घर में एक प्रोग्राम है। मैं अपना काम पहले ही पूरा कर लूंगा। कृप्या मंजूर करें। मैं आभारी रहूंगा।",
        "expected": "sir, mujhe kal chhutti chahiye. mere ghar mein ek program hai. main apna kaam pahle hi poora kar loonga. kripya manzoor karen. main aabhaari rahunga.",
    },
    {
        "name": "Bank Transaction",
        "hindi": "मुझे अपने खाते से पैसे निकालने हैं। एटीएम कार्ड से निकालूंगा। पिन नंबर डालूंगा। रसीद लूंगा। धन्यवाद।",
        "expected": "mujhe apne khaate se paise nikaalne hain. atm card se nikaaloonga. pin number daaloonga. raseed loonga. dhanyavaad.",
    },
    {
        "name": "Restaurant Order",
        "hindi": "भैया, एक प्लेट चोले भटूरे लाओ। साथ में लस्सी भी लाना। बिल कितना हुआ? यह लो पैसे। बाकी रख लो।",
        "expected": "bhaiya, ek plate chole bhature laao. saath mein lassi bhi laana. bill kitna hua? yah lo paise. baaki rakho lo.",
    },
    {
        "name": "Hospital Scene",
        "hindi": "डॉक्टर साहब, मेरी तबीयत ठीक नहीं है। सीने में दर्द हो रहा है। सांस फूल रही है। जांच करवानी है। दवा दे दीजिए।",
        "expected": "doctor sahab, meri tabiyat theek nahi hai. seene mein dard ho raha hai. saans phool rahi hai. jaanch karwaani hai. dawa de dijiye.",
    },
    {
        "name": "Railway Station",
        "hindi": "किस प्लेटफॉर्म पर गाड़ी आएगी? समय क्या हुआ है? टिकट कहाँ से कटेगा? कुल्लड़ वाली चाय मिलेगी क्या?",
        "expected": "kis platform par gaadi aayegi? samay kya hua hai? ticket kahaan se katega? kullad vaali chai milegi kya?",
    },
    {
        "name": "Wedding Ceremony",
        "hindi": "आज मेरे भाई की शादी है। बारात आ गई है। डीजे बज रहा है। सब नाच रहे हैं। दुल्हन बहुत सुंदर लग रही है। खाना बहुत अच्छा है।",
        "expected": "aaj mere bhai ki shaadi hai. baaraat aa gayi hai. dj baj raha hai. sab naach rahe hain. dulhan bahut sundar lag rahi hai. khana bahut achha hai.",
    },
    {
        "name": "Birthday Celebration",
        "hindi": "जन्मदिन मुबारक हो! केक काटो। मोमबत्ती बुझाओ। खुशियां मनाओ। उपहार खोलो। तस्वीरें खींचो। यादगार पल हैं।",
        "expected": "janamdin mubaarak ho! kaek kaato. mombatti bujhaao. khushiyaan manaao. uphaar kholo. tasveeren kheencho. yaadgaar pal hain.",
    },
    {
        "name": "Shayari/Poetry",
        "hindi": "दिल से दिल की बात करते हैं। खामोश रातों में साथ रहते हैं। दर्द भी अपना अपना है। फिर भी एक दूसरे का साथ नहीं छोड़ते।",
        "expected": "dil se dil ki baat karte hain. khaamosh raaton mein saath rehte hain. dard bhi apna apna hai. phir bhi ek dusre ka saath nahi chhodte.",
    },
    {
        "name": "Motivational Speech",
        "hindi": "कभी हार मत मानो। संघर्ष जारी रखो। सफलता जरूर मिलेगी। महान लोग गिरकर उठे हैं। तुम भी कर सकते हो। विश्वास रखो।",
        "expected": "kabhi haara mat maano. sangharsh jaari rakho. safalata zaroor milegi. mahaan log girkar uthe hain. tum bhi kar sakte ho. vishwaas rakho.",
    },
    {
        "name": "Job Interview",
        "hindi": "सर, मेरा नाम अमित है। मैंने बीटेक किया है। मुझे कंप्यूटर का अच्छा ज्ञान है। मैं मेहनती हूं। मुझे नौकरी चाहिए।",
        "expected": "sir, mera naam amit hai. maine btech kiya hai. mujhe computer ka achha gyaan hai. main mehnati hoon. mujhe naukri chahiye.",
    },
    {
        "name": "Police Station",
        "hindi": "साहब, मेरा पर्स चोरी हो गया। गली में दो बदमाश थे। उन्होंने धमकाया। पैसे और फोन ले लिए। एफआईआर लिखवानी है।",
        "expected": "saahab, mera purse chori ho gaya. gali mein do badmaash the. unhone dhamkaaya. paise aur phone le liye. fir likhwaani hai.",
    },
    {
        "name": "Temple Visit",
        "hindi": "हम सुबह मंदिर गए। भगवान का आशीर्वाद लिया। प्रसाद चढ़ाया। आरती की। मन शांत हुआ। भक्ति का अनुभव हुआ।",
        "expected": "hum subah mandir gaye. bhagwan ka aashirvaad liya. prasaad chadhaaya. aarti ki. man shaant hua. bhakti ka anubhav hua.",
    },
    {
        "name": "Flight Journey",
        "hindi": "मैं हवाई जहाज से दिल्ली जा रहा हूं। एयरपोर्ट पर जल्दी पहुंचना होगा। बोर्डिंग पास लेना है। सामान चेक इन करना है।",
        "expected": "main hawaai jahaaz se dilli ja raha hoon. airport par jaldi pahunchna hoga. boarding paas lena hai. saamaan check in karna hai.",
    },
    {
        "name": "Hotel Check-in",
        "hindi": "मुझे एक कमरा चाहिए। दो दिन ठहरना है। बिल भुगतान करूंगा। वाईफाई मिलेगा क्या? नाशता शामिल है ना?",
        "expected": "mujhe ek kamra chahiye. do din theherna hai. bill bhugataan karoonga. wifi milega kya? naashta shaamil hai naa?",
    },
    {
        "name": "Shopping Mall",
        "hindi": "मॉल बहुत बड़ा है। ब्रांडेड दुकानें हैं। छूट पर खरीदारी करेंगे। फूड कोर्ट में खाएंगे। मूवी भी देखेंगे। मज़ा आएगा।",
        "expected": "mall bahut bada hai. branded dukaanen hain. chhoot par khareedaari karenge. food court mein khaaenge. movie bhi dekhenge. maza aayega.",
    },
    {
        "name": "Rainy Day Memory",
        "hindi": "बारिश हो रही थी। मैं छत पर खड़ा था। ठंडी हवा चल रही थी। पकोड़े खाए। चाय पी। बहुत मज़ा आया। यादें ताज़ा हो गईं।",
        "expected": "baarish ho rahi thi. main chhat par khada tha. thandi hava chal rahi thi. pakode khaaye. chai pi. bahut maza aaya. yaaden taaza ho gayi.",
    },
    {
        "name": "Old Age Wisdom",
        "hindi": "बुजुर्ग लोग अनुभवी होते हैं। उनकी बातें सुनो। जीवन के रहस्य समझ में आएंगे। सम्मान करो। आशीर्वाद लो। जीवन सफल होगा।",
        "expected": "bujurg log anubhavi hote hain. unki baaten suno. jeevan ke rahasya samajh mein aayenge. sammaan karo. aashirvaad lo. jeevan safal hoga.",
    },
    {
        "name": "Farmer's Life",
        "hindi": "किसान सुबह खेत में जाता है। खाद डालता है। पानी देता है। फसल उगाता है। महनत से काम करता है। हमें खाना देता है।",
        "expected": "kisaan subah khet mein jaata hai. khaad daalta hai. paani deta hai. fasal ugaata hai. mehnat se kaam karta hai. hamein khana deta hai.",
    },
    {
        "name": "Student Life",
        "hindi": "परीक्षा आ रही है। रात भर पढ़ाई करनी है। नोट्स बनाने हैं। याद करना है। अच्छे नंबर लाने हैं। माता पिता को खुश करना है।",
        "expected": "parikshaa aa rahi hai. raat bhar padhaai karni hai. notes banaane hain. yaad karna hai. achchhe number laane hain. maata pita ko khush karna hai.",
    },
    {
        "name": "Mother's Love",
        "hindi": "माँ सबसे प्यारी होती है। वह बच्चों की देखभाल करती है। रात भर जगती है। खाना बनाती है। स्नेह से पालती है। माँ जैसा कोई नहीं।",
        "expected": "maa sabse pyaari hoti hai. vah bachchon ki dekhbaal karti hai. raat bhar jagti hai. khana banaati hai. sneh se paalti hai. maa jaisa koi nahi.",
    },
    {
        "name": "Father's Hard Work",
        "hindi": "पापा सुबह काम पर जाते हैं। शाम को थककर आते हैं। परिवार का खर्च चलाते हैं। बच्चों को पढ़ाते हैं। बहुत मेहनत करते हैं।",
        "expected": "papa subah kaam par jaate hain. shaam ko thakkar aate hain. parivaar ka kharch chalaate hain. bachchon ko padhaate hain. bahut mehnat karte hain.",
    },
    {
        "name": "Friendship Bond",
        "hindi": "दोस्ती एक अनमोल रिश्ता है। सच्चे दोस्त कम मिलते हैं। समय पर काम आते हैं। सुख दुख में साथ देते हैं। दोस्ती निभानी चाहिए।",
        "expected": "dostee ek anmol rishta hai. sachche dost kam milte hain. samay par kaam aate hain. sukh dukh mein saath dete hain. dostee nibhaani chahiye.",
    },
    {
        "name": "Village Life",
        "hindi": "गांव का जीवन शांत है। हरियाली है। पशु पाले जाते हैं। दूध निकाला जाता है। खेती की जाती है। लोग सरल हैं।",
        "expected": "gaanv ka jeevan shaant hai. hariyaali hai. pashu paale jaate hain. doodh nikaala jaata hai. kheti ki jaati hai. log saral hain.",
    },
    {
        "name": "City Life",
        "hindi": "शहर में भीड़ है। ट्रैफिक जाम होता है। लोग भागते रहते हैं। समय की कमी है। सुविधाएं ज्यादा हैं। जीवन तेज है।",
        "expected": "shehar mein bheed hai. traffic jam hota hai. log bhaagte rehte hain. samay ki kami hai. suvidhaaein zyaada hain. jeevan tez hai.",
    },
    {
        "name": "Sports - Cricket Match",
        "hindi": "भारत और पाकिस्तान का मैच है। स्टेडियम भरा है। लोग झंडे लहरा रहे हैं। चीयर लीडर्स नाच रहे हैं। छक्का लगा। जश्न मनाओ।",
        "expected": "bharat aur pakistan ka match hai. stadium bhara hai. log jhande lehra rahe hain. cheer leaders naach rahe hain. chakka laga. jashn manaao.",
    },
    {
        "name": "Pet Animal",
        "hindi": "मेरे पास एक कुत्ता है। उसका नाम टाइगर है। वह बहुत प्यारा है। मेरे साथ खेलता है। भौंकता है। दरवाजे पर रखवाली करता है।",
        "expected": "mere paas ek kutta hai. uska naam tiger hai. vah bahut pyaara hai. mere saath khelta hai. bhaunkta hai. darvaaze par rakhwali karta hai.",
    },
    {
        "name": "Music and Songs",
        "hindi": "मुझे संगीत सुनना पसंद है। मीठे गाने लगते हैं। गाना गाता हूं। ताली बजाता हूं। नाचता हूं। मन प्रसन्न हो जाता है।",
        "expected": "mujhe sangeet sunna pasand hai. meethe gaane lagte hain. gaana gaata hoon. taali bajaata hoon. naachta hoon. man prasann ho jaata hai.",
    },
    {
        "name": "Reading Books",
        "hindi": "पढ़ने की आदत अच्छी होती है। किताबें ज्ञान देती हैं। रोज़ पढ़ता हूं। उपन्यास पसंद हैं। पुस्तकालय जाता हूं। नई किताबें खरीदता हूं।",
        "expected": "padhne ki aadat achhi hoti hai. kitaaben gyaan deti hain. roz padhta hoon. upanyaas pasand hain. pustakaalaya jaata hoon. nayi kitaaben khareedta hoon.",
    },
    {
        "name": "Exercise and Health",
        "hindi": "सुबह उठकर व्यायाम करो। दौड़ लगाओ। योग करो। सेहत अच्छी रहेगी। ताकत बढ़ेगी। बीमारियां दूर रहेंगी। जीवन स्वस्थ होगा।",
        "expected": "subah uthkar vyaayaam karo. daud lagaao. yog karo. sehat achhi rahegi. taakat badhegi. beemariyaan door rahengi. jeevan svasth hoga.",
    },
    {
        "name": "Dream and Ambition",
        "hindi": "मैं एक डॉक्टर बनना चाहता हूं। लोगों की सेवा करूंगा। गरीबों का इलाज करूंगा। नाम कमाऊंगा। माता पिता का सपना पूरा करूंगा।",
        "expected": "main ek doctor banna chahta hoon. logon ki seva karoonga. gareebon ka ilaaj karoonga. naam kamaaoonga. maata pita ka sapna poora karoonga.",
    },
    {
        "name": "Nature Beauty",
        "hindi": "प्रकृति बहुत सुंदर है। पहाड़ देखो। झरने सुनो। पक्षी देखो। फूल सुंगो। हरियाली में खो जाओ। मन शांत होगा।",
        "expected": "prakriti bahut sundar hai. pahaad dekho. jharne suno. pakshi dekho. phool sungo. hariyaali mein kho jaao. man shaant hoga.",
    },
    {
        "name": "Patriotic Speech",
        "hindi": "भारत माता की जय। हम भारतीय हैं। हमारी संस्कृति महान है। झंडा लहराओ। राष्ट्र गान गाओ। देश की सेवा करो। गर्व महसूस करो।",
        "expected": "bharat maata ki jay. hum bhaaratee hain. hamaari sanskriti mahaan hai. jhanda lehraao. rashtra gaan gaao. desh ki seva karo. garv mehsoos karo.",
    },
    {
        "name": "Season Change",
        "hindi": "मौसम बदल रहा है। गर्मी जा रही है। बारिश आ रही है। फिर सर्दी आएगी। हर मौसम का अपना मज़ा है। प्रकृति का चक्र है।",
        "expected": "mausam badal raha hai. garmi ja rahi hai. baarish aa rahi hai. phir sardi aayegi. har mausam ka apna maza hai. prakriti ka chakra hai.",
    },
    {
        "name": "New Year Resolution",
        "hindi": "नया साल आ गया है। नई शुरुआत करो। बुरी आदतें छोड़ो। अच्छे काम करो। मेहनत से पढ़ो। सफलता पाओ। खुश रहो।",
        "expected": "naya saal aa gaya hai. nayi shuruaat karo. buri aadaten chhodo. achchhe kaam karo. mehnat se padho. safalata paao. khush raho.",
    },
    {
        "name": "Grandma's Recipe",
        "hindi": "दादी के हाथ का खाना अच्छा लगता है। हलवा बनाती हैं। दाल बाफले बनाती हैं। मिठाइयां बनाती हैं। सबको खिलाती हैं। प्यार से बनाती हैं।",
        "expected": "dadi ke haath ka khana achha lagta hai. halwa banaati hain. daal baafle banaati hain. mithaiyaan banaati hain. sabko khilaati hain. pyaar se banaati hain.",
    },
    {
        "name": "Brother-Sister Bond",
        "hindi": "भाई बहन का रिश्ता अनोखा है। लड़ते हैं। मगर प्यार भी करते हैं। रक्षाबंधन पर बहन राखी बांधती है। भाई उपहार देता है। साथ में खुशी मनाते हैं।",
        "expected": "bhai behen ka rishta anokha hai. ladate hain. magar pyaar bhi karte hain. rakshabandhan par behen raakhi baandhti hai. bhai uphaar deta hai. saath mein khushi manaate hain.",
    },
    {
        "name": "College Friends",
        "hindi": "कॉलेज के दिन यादगार होते हैं। दोस्ती गहरी होती है। कैंपस में घूमते हैं। कैंटीन में बैठते हैं। एग्जाम की तैयारी करते हैं। जीवन भर याद रहता है।",
        "expected": "college ke din yaadgaar hote hain. dostee gehri hoti hai. campus mein ghoomte hain. canteen mein baithte hain. exam ki taiyaari karte hain. jeevan bhar yaad rehta hai.",
    },
    {
        "name": "Morning Routine",
        "hindi": "सुबह जल्दी उठो। नहाओ धो। प्रार्थना करो। नाश्ता करो। स्कूल जाओ। पढ़ाई करो। खेलो कूदो। घर आओ। होमवर्क करो। सो जाओ।",
        "expected": "subah jaldi utho. nahaao dho. praarthana karo. naashta karo. school jaao. padhaai karo. khelo koodo. ghar aao. homework karo. so jaao.",
    },
    {
        "name": "Marriage Proposal",
        "hindi": "मुझे एक अच्छी लड़की से शादी करनी है। वह पढ़ी लिखी हो। समझदार हो। घर संभाल सके। माता पिता का सम्मान करे। साथ में खुश रहें।",
        "expected": "mujhe ek achchi ladki se shaadi karni hai. vah padhi likhi ho. samajhdar ho. ghar sambhal sake. maata pita ka sammaan kare. saath mein khush rahen.",
    },
    {
        "name": "Old Friends Meet",
        "hindi": "पुराने दोस्त मिले। बहुत खुशी हुई। पुरानी यादें ताज़ा हुईं। हंसी मज़ाक हुआ। खाना खाया। फोटो खींची। वादा किया फिर मिलेंगे।",
        "expected": "puraane dost mile. bahut khushi hui. puraanee yaaden taaza huin. hansi mazaak hua. khana khaya. photo kheenchi. vaada kiya phir milenge.",
    },
    {
        "name": "First Day at Work",
        "hindi": "आज पहला दिन है। नर्वस हूं। नए लोग मिलेंगे। बॉस से बात करूंगा। काम सीखूंगा। मेहनत करूंगा। अच्छा इंप्रेशन डालूंगा।",
        "expected": "aaj pehla din hai. nervous hoon. naye log milenge. boss se baat karoonga. kaam seekhunga. mehnat karoonga. achha impression daaloonga.",
    },
    {
        "name": "Lost Child",
        "hindi": "बच्चा खो गया है। मां रो रही है। पुलिस को बुलाओ। ऐलान करो। भीड़ में ढूंढो। सूचना दो। उम्मीद है मिल जाएगा।",
        "expected": "bachcha kho gaya hai. maa ro rahi hai. police ko bulaao. elaan karo. bheed mein dhoondho. soochna do. umeed hai mil jaayega.",
    },
    {
        "name": "House Warming",
        "hindi": "नया घर बन गया है। गृह प्रवेश का कार्यक्रम है। रिश्तेदार आ रहे हैं। पूजा होगी। भोजन कराया जाएगा। खुशियां मनाएंगे। नई शुरुआत होगी।",
        "expected": "naya ghar ban gaya hai. grih pravesh ka karyakram hai. rishtedaar aa rahe hain. pooja hogi. bhojan karaaya jaayega. khushiyaan manaayenge. nayi shuruaat hogi.",
    },
    {
        "name": "Final Exam Preparation",
        "hindi": "परीक्षा कल है। डर लग रहा है। सारी रात पढ़ाई करनी है। सभी विषय देखने हैं। नोट्स याद करने हैं। पानी पीते रहो। आराम भी करो। सफल होना है।",
        "expected": "parikshaa kal hai. dar lag raha hai. saari raat padhaai karni hai. sabhi vishay dekhne hain. notes yaad karne hain. paani peete raho. aaraam bhi karo. safal hona hai.",
    },
]


def normalize_text(text):
    """Normalize text for comparison."""
    return " ".join(text.lower().split())


def calculate_accuracy(result, expected):
    """Calculate word-level accuracy."""
    result_words = normalize_text(result).split()
    expected_words = normalize_text(expected).split()

    total = max(len(result_words), len(expected_words))
    if total == 0:
        return 100.0, 100.0

    matches = sum(1 for r, e in zip(result_words, expected_words) if r == e)
    expected_set = set(expected_words)
    matches_loose = sum(1 for r in result_words if r in expected_set)

    strict_acc = (matches / total) * 100
    loose_acc = (matches_loose / total) * 100

    return strict_acc, loose_acc


def run_tests():
    """Run all test cases."""
    converter = HinglishConverter()

    print("=" * 90)
    print(" " * 20 + "HINDI TO HINGLISH - COMPREHENSIVE TEST SUITE")
    print(" " * 25 + f"Total Test Cases: {len(TEST_CASES)}")
    print("=" * 90)

    results = []
    total_strict_acc = 0
    total_loose_acc = 0

    for i, test in enumerate(TEST_CASES, 1):
        print(f"\n{'─' * 90}")
        print(f"Test #{i:02d}: {test['name']}")
        print(f"{'─' * 90}")

        result = converter.convert(test["hindi"])

        print(f"\n📝 HINDI TEXT:")
        print(f"   {test['hindi']}")
        print(f"\n✅ EXPECTED:")
        print(f"   {test['expected']}")
        print(f"\n🎯 GOT:")
        print(f"   {result}")

        strict_acc, loose_acc = calculate_accuracy(result, test["expected"])
        total_strict_acc += strict_acc
        total_loose_acc += loose_acc

        if strict_acc >= 90:
            status = "✅ EXCELLENT"
            emoji = "🌟"
        elif strict_acc >= 75:
            status = "✅ GOOD"
            emoji = "👍"
        elif strict_acc >= 60:
            status = "⚠️ FAIR"
            emoji = "😐"
        else:
            status = "❌ NEEDS WORK"
            emoji = "🔧"

        print(
            f"\n{emoji} ACCURACY: {strict_acc:.1f}% (strict) / {loose_acc:.1f}% (loose) - {status}"
        )

        results.append(
            {
                "num": i,
                "name": test["name"],
                "strict_acc": strict_acc,
                "loose_acc": loose_acc,
                "status": status,
            }
        )

    # Summary
    print("\n" + "=" * 90)
    print(" " * 35 + "FINAL SUMMARY")
    print("=" * 90)

    avg_strict = total_strict_acc / len(TEST_CASES)
    avg_loose = total_loose_acc / len(TEST_CASES)

    print(f"\n📊 OVERALL ACCURACY:")
    print(f"   Strict: {avg_strict:.1f}%")
    print(f"   Loose:  {avg_loose:.1f}%")

    excellent = sum(1 for r in results if "EXCELLENT" in r["status"])
    good = sum(1 for r in results if "GOOD" in r["status"])
    fair = sum(1 for r in results if "FAIR" in r["status"])
    needs_work = sum(1 for r in results if "NEEDS" in r["status"])

    print(f"\n📈 BREAKDOWN:")
    print(f"   🌟 EXCELLENT (≥90%): {excellent:2d}/{len(TEST_CASES)}")
    print(f"   👍 GOOD (75-89%):     {good:2d}/{len(TEST_CASES)}")
    print(f"   😐 FAIR (60-74%):     {fair:2d}/{len(TEST_CASES)}")
    print(f"   🔧 NEEDS WORK (<60%): {needs_work:2d}/{len(TEST_CASES)}")

    # Show all results in table
    print(f"\n📋 DETAILED RESULTS:")
    print(f"{'─' * 90}")
    print(f"{'#':<4} {'Test Name':<45} {'Accuracy':<12} {'Status':<15}")
    print(f"{'─' * 90}")
    for r in results:
        print(
            f"{r['num']:<4} {r['name']:<45} {r['strict_acc']:>6.1f}%      {r['status']:<15}"
        )

    # Cache stats
    print(f"\n{'=' * 90}")
    print(" " * 35 + "PERFORMANCE METRICS")
    print(f"{'=' * 90}")
    cache_info = converter.get_cache_info()
    print(f"📦 Cache Hits:     {cache_info.hits}")
    print(f"📦 Cache Misses:   {cache_info.misses}")
    print(f"📦 Cache Size:     {cache_info.currsize}/{cache_info.maxsize}")

    if cache_info.hits + cache_info.misses > 0:
        hit_rate = (cache_info.hits / (cache_info.hits + cache_info.misses)) * 100
        print(f"📊 Cache Hit Rate: {hit_rate:.1f}%")

    print(f"\n{'=' * 90}")

    return avg_strict, avg_loose


if __name__ == "__main__":
    avg_strict, avg_loose = run_tests()

    print("\n" + "=" * 90)
    if avg_strict >= 80:
        print("🎉 OVERALL RESULT: PASSED (≥ 80% accuracy)")
        sys.exit(0)
    elif avg_strict >= 60:
        print("⚠️  OVERALL RESULT: FAIR (60-79% accuracy)")
        sys.exit(0)
    else:
        print("❌ OVERALL RESULT: NEEDS IMPROVEMENT (< 60% accuracy)")
        sys.exit(1)
