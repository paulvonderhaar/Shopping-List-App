import requests
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer

def main():
    LastFlag=False
    Site='https://www.heb.com/category/490113/490542'
    prices=[]
    priceperamount=[]
    names=[]
    amounts=[]
    while(LastFlag==False):
        print(Site)
        a = requests.get(Site)
        soup = BeautifulSoup(a.content, 'html.parser')
        b = soup.find_all("li",{"class":"responsivegriditem product-grid-large-fifth product-grid-small-6"})
        for item in b:
            name=str(item.find('span',{"class":"responsivegriditem__title"}).getText())
            name=name.split(",")
            names.append(name[0].strip())
            amounts.append(name[1].strip())
            price=str(item.find('div',{"class":"cat-price"}).getText())
            price=price.split()
            if(price[1]=='for'):
                pricevalue=float(price[2].replace('$',''))
                pricevalue=pricevalue/float(price[0])
                prices.append("$"+str(pricevalue))
                priceperamount.append(price[3])
            else:
                try:
                    prices.append(price[0].strip())
                    priceperamount.append(price[2])
                except IndexError:
                    priceperamount.append('null')
        c=(soup.find(('a'),{'aria-label':'go to next page'}))
        if(c!=None):
            Site='https://www.heb.com'+c['href']
        else:
            LastFlag=True
    #for i in range (len(prices)):
    #    print (names[i])
    #    print (amounts[i])
    #    print(prices[i])
    #    print(priceperamount[i])
    #    print()

    df=pd.DataFrame(list(zip(names,amounts,prices,priceperamount)), columns = ['Name','Amount','Price','Price per Unit'])
    print(df.head(10))

main()