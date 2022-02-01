import os
import lxml.html as lh
import requests as rq
import csv
import time



session = 81
chmbrs = ["H", "S"]
path = os.environ["USERPROFILE"] + "/Desktop/amendments"                                                                                                              
if not os.path.exists(path):
    os.mkdir(path)
os.chdir(path)
while(session <= 87):                                                                                                                                               
    with open("amendments" + str(session) + ".csv", "w", newline="") as file:                                                                                        
        writer = csv.writer(file, dialect="excel", delimiter = ",")
        writer.writerow(("Bill", "Amendments"))
        for chmbr in chmbrs:
            n = 0
            if(chmbr == "H"):
                url = "https://capitol.texas.gov/Reports/Report.aspx?LegSess=" + str(session) + "R&ID=housefiled"
            else:
                url = "https://capitol.texas.gov/Reports/Report.aspx?LegSess=" + str(session) + "R&ID=senatefiled"
            u = rq.get(url, timeout=75)
            doc = lh.fromstring(u.content)
            size = len(doc.xpath("//table"))
            for num in range(1, size):
                while(True):
                    try:
                        bill_n = doc.xpath("//table[" + str(num) + "]//a")[0].text_content().split(" ")   
                        bill = bill_n[0]
                        n = int(bill_n[1])
                        if(bill != "HB" and bill != "SB"):
                            print("Waiting...")
                            break
                        a_url = "https://capitol.texas.gov/BillLookup/Amendments.aspx?LegSess=" + str(session) + "R&Bill=" + bill + str(n)
                        a_u = rq.get(a_url, timeout=75)
                        a_doc = lh.fromstring(a_u.content)
                        amendment = a_doc.xpath('//html//body//div[1]//div[4]//form//span')
                        print("Working on " + bill + " " + str(n) + "...")
                        if (len(amendment) > 0):
                            writer.writerow((bill + " " + str(n),
                                             amendment[0].text_content().split(" ")[3]))  
                        else:
                            writer.writerow((bill + " " + str(n), "0"))   

                    except:
                        time.sleep(20)   
                        continue
                    break


                                                                                                                                           



    session += 1







