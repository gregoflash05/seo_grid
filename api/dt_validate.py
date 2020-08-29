def campaign_test(link, campaign_name, user_campaign_details):
            for i in user_campaign_details:
                if i['link'] == link:
                    return 'TrueL'
                    break
                elif i['campaign_name'] == campaign_name:
                    return 'TrueC'
                    break

def keyword_test(keyword, campaign_keyword_details):
            for i in campaign_keyword_details:
                if i['keyword'] == keyword:
                    return 'TrueK'
                    break

def edit_campaign_test(pk, link, campaign_name, user_campaign_details):
            for i in user_campaign_details:
                if i['id'] == pk:
                    continue
                else:
                    if i['link'] == link:
                        return 'TrueL'
                        break
                    elif i['campaign_name'] == campaign_name:
                        return 'TrueC'
                        break

# def edit_keyword_test(pk, keyword, campaign_keyword_details):
#             for i in campaign_keyword_details:
#                 if i['keyword'] == keyword:
#                     return 'TrueK'
#                     break

def data_output(data):
    if data == None:
        return "Pending"
    else:
        return data

def validate_language(language):
    languages = {"Afrikaans" :"AF","Albanian" : "SQ","Arabic" : "AR","Armenian" : "HY","Basque" : "EU","Bengali" : "BN","Bulgarian" : "BG","Catalan" : "CA","Cambodian" : "KM","Chinese (Mandarin)" : "ZH","Croatian" : "HR","Czech" : "CS","Danish" : "DA","Dutch" : "NL","English" : "EN","Estonian" : "ET","Fiji" : "FJ","Finnish" : "FI",
    "French" : "FR","Georgian" : "KA","German" : "DE","Greek" : "EL","Gujarati" : "GU","Hebrew" : "HE","Hindi" : "HI",
    "Hungarian" : "HU","Icelandic" : "IS","Indonesian" : "ID","Irish" : "GA","Italian" : "IT","Japanese" : "JA",
    "Javanese" : "JW","Korean" : "KO","Latin" : "LA","Latvian" : "LV","Lithuanian" : "LT","Macedonian" : "MK",
    "Malay" : "MS","Malayalam" : "ML","Maltese" : "MT","Maori" : "MI","Marathi" : "MR","Mongolian" : "MN",
    "Nepali" : "NE","Norwegian" : "NO","Persian" : "FA","Polish" : "PL","Portuguese" : "PT","Punjabi" : "PA",
    "Quechua" : "QU","Romanian" : "RO","Russian" : "RU","Samoan" : "SM","Serbian" : "SR","Slovak" : "SK",
    "Slovenian" : "SL","Spanish" : "ES","Swahili" : "SW","Swedish " : "SV","Swedish" : "SV","Tamil" : "TA",
    "Tatar" : "TT","Telugu" : "TE","Thai" : "TH","Tibetan" : "BO","Tonga" : "TO","Turkish" : "TR","Ukrainian" : "UK",
    "Urdu" : "UR","Uzbek" : "UZ","Vietnamese" : "VI","Welsh" : "CY","Xhosa" : "XH",}
    language_list = language.split(' ')
    print(language_list)
    print(len(language_list))
    if len(language_list) > 1:
        language = ''
        for i in language_list:
            if i != '':
                if language != '':
                    language = "{} {}".format(language, i)
                else:
                    language = "{}".format(i)
            else:
                continue
    else:
        language = language_list[0]
    try:
        abv = languages[language].lower()
    except:
        abv = ''
    return abv