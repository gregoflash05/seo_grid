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