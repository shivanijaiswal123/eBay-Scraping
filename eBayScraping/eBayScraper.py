import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import Counter
import re
import random
import pprint
import json



data=[]

def productData(url,detail):
    
    html = urlopen(url)
    bsObj = BeautifulSoup(html, "html.parser")
    
    
        
    div=bsObj.find("div",{"class":"si-content"})
    
    if(div):
        seller_name=div.find("span",{"class":"mbg-nw"}).get_text()
        detail["seller_name"]=seller_name

        rating=div.find("span",{"class":"mbg-l"}).a.get_text()
        detail["rating"]=rating

    else:
        div=bsObj.find("div",{"class":"seller-persona "})

        if(div):
            div=bsObj.find("div",{"class":"seller-persona "})

            anch=div.findAll("span",{"class":"no-wrap"})

            for data in anch[1:2]:
                item=data.get_text().split()
                seller_name=item[0]
                detail["seller_name"]=seller_name
                if(len(item)>1):
                    temp = re.findall(r'\d+', item[1])
                
                    rating=temp[0]
                    detail["rating"]=rating

        else:
            
            baseDiv=bsObj.find("div",{"class":"row profileRow"})

            if(baseDiv):
                span=baseDiv.findAll("span")
                
                seller_name=span[1].get_text()
                detail["seller_name"]=seller_name
                
                r=span[2].get_text().split()
                rating=re.findall(r'\d+', r[2])
                detail["rating"]=rating[0]

            else:
                div=bsObj.find("div",{"class":"seller-persona s-logo"})
                print(div)
                anch=div.findAll("span",{"class":"no-wrap"})

                for data in anch[1:2]:
                    item=data.get_text().split()
                    seller_name=item[0]
                    detail["seller_name"]=seller_name

                    temp = re.findall(r'\d+', item[1])
                    if(temp):
                        rating=temp[0]
                    detail["rating"]=rating





def productsLinks(url,detail):
    html = urlopen(url)
    bsObj = BeautifulSoup(html, "html.parser")

    ul=bsObj.find("section",{"class":"b-module b-list b-listing srp-list b-display--landscape"}).find("ul",{"class":"b-list__items_nofooter"})
    li=ul.findAll("li")
    
    count=1
    for product in li:

        productLink=product.find("a",href=True)["href"]
        
        print("     ",count,productLink)#{product link}

        title=product.find("h3",{"class":"s-item__title"}).get_text()
        price=product.find("span",{"class":"s-item__price"}).get_text()
       
        detail["title"]=title
        detail["price"]=price
        detail["position"]=count


        productData(productLink,detail)

        pprint.pprint(detail)

        data.append(detail)
       

        print("---------------------------------------------------------------------------------------------")

        count +=1





def subCategory(categories,li):
    
    for item in li:
        anchorTag=item.find('a',{"class":"b-textlink b-textlink--sibling"},href=True)
        
        
        if(anchorTag):
            
            
            html = urlopen(anchorTag["href"])
            bsObj = BeautifulSoup(html, "html.parser")


            #This is hirerachy. 
            ol=bsObj.find("nav",{"class":"b-breadcrumb"}).ol
            headers=ol.findAll("li")

            
            head=[]
            for h in headers[1:]:
                head.append(h.get_text())
            
            
            ul = bsObj.find("section",{"class":"b-module b-list b-categorynavigations b-display--landscape"}).ul
            liOfSubCat = ul.find_all('li')
            
            
            strongTag=ul.find('strong').get_text()
            anchorTags=ul.findAll('a',{"class":"b-textlink b-textlink--sibling"})


            subCategories=[]
            subCat=[]

            subCategories.append(strongTag)

            for category in anchorTags:
                subCategories.append(category.get_text())
                subCat.append(category.get_text())


            
            if(Counter(categories) == Counter(subCategories)):
                
                hirerachy=""
                sign=""
                

                for item in head:
                    hirerachy = hirerachy+sign+item
                    sign="-->"

                data={}
                data["category"]=head[0]

                indice=1
                for item in head[1:]:
                    data["subcategory"+str(indice)]=item
                    indice += 1

                print("1 "+anchorTag["href"])
                data["page_no"]=1
                productsLinks(anchorTag["href"],data)

                html = urlopen(anchorTag["href"])
                bsObj = BeautifulSoup(html, "html.parser")



                pages=bsObj.find("ol",{"class":"ebayui-pagination__ol"})
                
                if(pages):

                    #for scraping main pages 1-2-3-4--N like this.
                    
                    pageList=pages.findAll("li")
                    
                    if(len(pageList)>5):
                        pageList=random.sample(pageList[1:],k=5)

                    count=2
                    for page in pageList[1:]:
                        detail={}

                        detail["category"]=head[0]
                        
                        index=1
                        for item in head[1:]:
                            detail["subcategory"+str(index)]=item
                            index += 1




                        link=page.find("a",href=True)["href"]
                        pagination=link.split('=')
                        detail["page_no"]=pagination[-1]
                        print(count,link)
 
                        
                        productsLinks(link,detail)
                        # print(detail)
                        count +=1
                        # print(detail)
                    
                
                print("-----------------------------------------------------------------")
                
                

            else:
                
                subCategory(subCat,liOfSubCat)
          

    
        




    
    
def scraper(URL):
    html = urlopen(URL)
    bsObj = BeautifulSoup(html, "html.parser")

    ul = bsObj.find("section",{"class":"b-module b-list b-speciallinks b-display--landscape"}).ul
    li = ul.find_all('li',recursive=False)
    
    return li



url="https://www.ebay.com/b/Musical-Instruments-Gear/619/bn_1865601"
li=scraper(url)



for item in li[:2]:
    
    achr=item.find("a",href=True)["href"] 
    print(achr)
    print("**************************************************************")

    ul=item.find("ul")

    if(ul):
        
        html = urlopen(achr)
        bsObj = BeautifulSoup(html, "html.parser")
    
        ul = bsObj.find("section",{"class":"b-module b-list b-categorynavigations b-display--landscape"}).ul
        li= ul.findAll("li")
        

        # This is only for list
        anchorTags=ul.findAll('a',{"class":"b-textlink b-textlink--sibling"})

        categories=[]
        for category in anchorTags:
            categories.append(category.get_text())
        
        subCategory(categories,li)
        
   
        


file=open("DjEquipment.json","w")  
file.write(str(data))
file.close()       
 






















    
        
        

    
     

        

        

    
    