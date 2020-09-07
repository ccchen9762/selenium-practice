import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext

import requests
from bs4 import BeautifulSoup
import lxml
import os
from urllib.request import urlretrieve
import sys

#main page info
mainpage=tk.Tk()
mainpage.title("DownPic")
mainpage.geometry("800x600")

#===========================================basic layout===========================================
#label url
label_url=tk.Label(mainpage, text="Input target url :", anchor="e")
label_url.place(x=50, y=30, width=140, height=24)
#entry url
url=tk.StringVar()
entry_url=tk.Entry(mainpage, textvariable=url)
entry_url.place(x=200, y=30, width=180, height=24)

#label file location
label_file_location=tk.Label(mainpage, text="Choose save location :", anchor="e")
label_file_location.place(x=50, y=70, width=140, height=24)
#entry file location
file_location=tk.StringVar()
entry_file_location=tk.Entry(mainpage, textvariable=file_location)
entry_file_location.place(x=200, y=70, width=180, height=24)

#lanel result
label_result=tk.Label(mainpage, text="Result :")
label_result.place(x=50, y=150, height=30)
#scrolledtext result
result_st=scrolledtext.ScrolledText(mainpage)
result_st.place(x=50, y=180, width=540, height=360)
#===========================================basic layout===========================================

#========================================button & function========================================
#filedialog
def search_file():
    #global file_name #actually it's unambiguous, so don't need this line
    file_location.set(filedialog.askdirectory())
#filedialog button
buttonGO=tk.Button(mainpage, text="...", relief="raised", command=search_file)
buttonGO.place(x=400, y=70, width=30, height=24)

#download
def start_download():
    #requests
    requests1 = requests.get(url.get())
    result_st.insert('end', "request status code = " + str(requests1.status_code) + "\n")
    if requests1.status_code == 200: #if success
        result_st.insert('end', "request successed\n\n")
        soup=BeautifulSoup(requests1.text,"lxml")
        image=soup.find_all("div")
        links=[]
        for d in image:
            if d.find('img'):        #再從div找img裡面的src  
                result=d.find('img')['src']
                #print(result)
                links.append(result)
        x=1
        for link in links:
            local = os.path.join(file_location.get() + "/" + str(x) + ".jpg")
            result_st.insert('end', "Downloading pic to : \"" + file_location.get() + "/" + str(x) + ".jpg\"\n")
            urlretrieve(link,local) #link是下載的網址 local是儲存圖片的檔案位址
            x+=1
            if x>3:
                break
        result_st.insert('end', "\nsuccessfully download " + str(x-1) + " pictures\n\n")
        result_st.insert('end', "=" * 50 + "\n\n")
    else: #if failed
        result_st.insert('end', "request failed\n\n")
        result_st.insert('end', "=" * 50 + "\n\n")
#download button
button_down=tk.Button(mainpage, text="Start Download", relief="raised", command=start_download)
button_down.place(x=600, y=70, width=100, height=24)
#========================================button & function========================================

mainpage.mainloop()

