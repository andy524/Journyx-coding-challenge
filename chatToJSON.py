import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

def addBlock(feature,data):
  if len(data) == 0 :
    return ""
  out = " \"" + feature + "\": [\n"
  for i in range(0,len(data)):
    if (feature == "links"):    # creating block for links
      #3 space then {
      out = out + "   {\n"
      # 4 space url
      out = out + "    \"url\": " + "\"" + data[0] +"\",\n"
      page = BeautifulSoup(urlopen(data[0]))
      # 4 space title
      out = out + "    \"title\": " + "\"" + page.title.string +"\",\n"
      #3 space then }
      out = out + "   }"
    else:                       # creating block for mentions and emoticons
      out = out + "  " + data[i]
    if i != len(data) - 1:
      out = out + ",\n"
  out = out + "\n ],\n"
  return out
def jsonParse(line):
  ment  = []
  emo   = []
  links  = []
  count = 0
  tokens = line.split(" ")
  
  for each in tokens:
    if each[0] == "@":
      ment.append("\"" + each[1:] + "\"")
    elif each[0] =="(" and each[len(each)-1] == ")":
      emo.append("\"" + each[1:len(each)-1] + "\"")
    elif each[0:4] =="http":
      links.append(each)
    elif re.search('[a-zA-Z]',each):
      count = count + 1
  res =     "{\n"
  res = res + addBlock("emoticons", emo)
  res = res + addBlock("mentions", ment)  
  res = res + addBlock("links",   links)
  res = res + " \"words\": " + str(count) + "\n"
  res = res + "}"
  return res
    
testCases = [ "@john hey, you around?",
              "Good morning! (smile) (coffee)",
              "@mary @john (success) such a cool feature! Check this out: https://journyx.com/features-and-benefits/data-validation-tool",
              "The World Series is starting soon! (cheer) https://www.mlb.com/ and https://espn.com",]

for i in range(0,len(testCases)-1):
  print("######### Test Case "+ str(i)  +" ##############")
  ans = jsonParse(testCases[i])
  print (ans)