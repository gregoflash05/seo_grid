res = requests.get(url)
# soup = bs4(res.text, "html.parser")
# soup1 = soup.find("script")
# soup1 = str(soup1)
# soup2 = soup1.replace("dataLayer = window.dataLayer || [];", "")
# soup3 = soup2.split("{")
# water = []
# water.append("siteinfo")
# for data in soup3:
#     if "rank" in data:
#         water.append(data)
#     if "global" in data:
#         water.append(data)

# oo = "".join(water)
# oo = oo.split("}")
# oo = oo[:1]
# haa = "".join(oo)
# haa = haa.replace(" ","").replace("siteinfo", "").replace("\"rank\":", "").strip()
# haa = "{"+ haa+"}"
# print(haa)