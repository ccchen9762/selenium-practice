import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import time

#main page info
mainpage=tk.Tk()
mainpage.title("DownPic")
mainpage.geometry("800x600")

webdriver_path = 'D:\\Drivers\\chromedriver.exe'

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
result_st=scrolledtext.ScrolledText(mainpage, state='disabled')
result_st.place(x=50, y=180, width=700, height=360)
#===========================================basic layout===========================================

#========================================button & function========================================
#filedialog
def search_file():
    #global file_name #actually it's unambiguous, so don't need this line
    file_location.set(filedialog.askdirectory())
#filedialog button
button_file=tk.Button(mainpage, text="...", relief="raised", command=search_file)
button_file.place(x=400, y=70, width=30, height=24)

#request
def request_html():
    #open driver
    driver1 = webdriver.Chrome(executable_path=webdriver_path)
    driver1.get(url.get())
    #time.sleep(5)
    #driver1.find_element_by_xpath("//*[@id=\"content\"]/div/button").click()

#request button
button_request=tk.Button(mainpage, text="request", relief="raised", command=request_html)
button_request.place(x=480, y=30, width=100, height=24)
"""
#download
def start_download():
    result_st.configure(state='normal')
    result_st.insert('end', "finding img\n...\n")
    soup=BeautifulSoup(requests1.text,"lxml") #html.parser, html5lib, lxml, lxml is faster
    image=soup.find_all("div")
    img_url = [] #download url list
    img_url_dic = {} #prevent download twice
    for d in image:
        if d.find('img'):        #再從div找img裡面的src  
            result=d.find('img')['src']
            if not result in img_url_dic:
                result_st.insert('end', "find img : " + result + "\n")
                img_url.append(result)
                img_url_dic[result]=1
    x=1
    for link in img_url:
        local = os.path.join(file_location.get() + "/" + str(x) + ".jpg")
        result_st.insert('end', "Downloading pic to : \"" + file_location.get() + "/" + str(x) + ".jpg\"\n")
        urlretrieve(link,local) #link是下載的網址 local是儲存圖片的檔案位址
        x+=1
        #if x>3:
        #    break
    result_st.insert('end', "\nsuccessfully download " + str(x-1) + " pictures\n...\n")
    result_st.insert('end', "=" * 50 + "\n\n")
    result_st.configure(state='disabled')
#download button
button_down=tk.Button(mainpage, text="Start Download", relief="raised", command=start_download)
button_down.place(x=480, y=70, width=100, height=24)
"""
#========================================button & function========================================

#mainpage.mainloop()

