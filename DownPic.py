import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog
from tkinter import scrolledtext
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import time
import re #regular expression

#color info
bg_deep = "#4F4F4F"
bg_middle = "#6C6C6C"
bg_light = "#8E8E8E"
bg_highlight = "#C4E1FF"
fg_deep = "#FCFCFC"

#main page info
mainpage=tk.Tk()
mainpage.title("DownPic")
mainpage.geometry("800x600+640+160")
mainpage.configure(bg=bg_deep)
mainpage.resizable(False, False)

webdriver_path = 'D:\\Drivers\\chromedriver.exe'

#pos info
position_x = 50
position_y = 20
space_x = 150
space_y = 40

label_font_config = tkFont.Font(family="Arial", size=10, weight="bold")
word_font_config = tkFont.Font(family="Arial", size=10)
#===========================================basic layout===========================================
#label url
label_url=tk.Label(mainpage, text="Target url  ", anchor="e", bg=bg_deep, fg=fg_deep, font=label_font_config)
label_url.place(x=position_x, y=position_y, width=150, height=24)
#entry url
url=tk.StringVar()
entry_url=tk.Entry(mainpage, textvariable=url, bg=bg_light, fg=fg_deep, font=word_font_config)
entry_url.place(x=position_x+space_x, y=position_y, width=180, height=24)

#label file location
label_file_location=tk.Label(mainpage, text="Choose save location  ", anchor="e", bg=bg_deep, fg=fg_deep, font=label_font_config)
label_file_location.place(x=position_x, y=position_y+space_y, width=150, height=24)
#entry file location
file_location=tk.StringVar()
entry_file_location=tk.Entry(mainpage, textvariable=file_location, bg=bg_light, fg=fg_deep, font=word_font_config)
entry_file_location.place(x=position_x+space_x, y=position_y+space_y, width=150, height=24)

#label account
label_account=tk.Label(mainpage, text="Account  ", anchor="e", bg=bg_deep, fg=fg_deep, font=label_font_config)
label_account.place(x=position_x, y=position_y+space_y*2, width=150, height=24)
#entry account
account=tk.StringVar()
entry_account=tk.Entry(mainpage, textvariable=account, bg=bg_light, fg=fg_deep, font=word_font_config)
entry_account.place(x=position_x+space_x, y=position_y+space_y*2, width=180, height=24)

#label password
label_password=tk.Label(mainpage, text="Password  ", anchor="e", bg=bg_deep, fg=fg_deep, font=label_font_config)
label_password.place(x=position_x, y=position_y+space_y*3, width=150, height=24)
#entry password
password=tk.StringVar()
entry_password=tk.Entry(mainpage, show="*", textvariable=password, bg=bg_light, fg=fg_deep, font=word_font_config)
entry_password.place(x=position_x+space_x, y=position_y+space_y*3, width=180, height=24)

#lanel result
label_result=tk.Label(mainpage, text="Log :", bg=bg_deep, fg=fg_deep, font=label_font_config)
label_result.place(x=position_x, y=position_y+space_y*4, height=30)
#scrolledtext result
result_st=scrolledtext.ScrolledText(mainpage, padx=12, pady=10, bg=bg_light, fg=fg_deep, font=word_font_config)
result_st.place(x=position_x, y=position_y+space_y*4+30, width=700, height=360)
result_st.insert('end', "Hello!\n\n")
result_st.configure(state='disabled')
#===========================================basic layout===========================================

#========================================button & function========================================
#button event
def on_enter(event, event_button):
    event_button["background"] = bg_highlight
    event_button["foreground"] = bg_deep
def on_leave(event, event_button):
    event_button['background'] = bg_middle
    event_button["foreground"] = fg_deep

#filedialog
def search_file():
    file_location.set(filedialog.askdirectory())
#filedialog button
button_file=tk.Button(mainpage, text="...", relief="flat", command=search_file, bg=bg_middle, fg=fg_deep, font=label_font_config)
button_file.bind("<Enter>", lambda event: on_enter(event, button_file))
button_file.bind("<Leave>", lambda event: on_leave(event, button_file))
button_file.place(x=position_x+space_x*2, y=position_y+space_y, width=30, height=24)

#open driver
def open_driver():
    if re.match("http[s]?://([a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(%[0-9a-fA-F][0-9a-fA-F]))+", url.get()):
        result_st.configure(state='normal')
        result_st.insert('end', "Connecting "+url.get()+"\n\n")
        #open driver
        driver1 = webdriver.Chrome(executable_path=webdriver_path)
        driver1.get(url.get())
        result_st.insert('end', "\nsuccessfully open web driver\n\n")
        result_st.configure(state='disabled')
        time.sleep(5)
        #do something like below
        driver1.find_element_by_xpath("//*[@id=\"content\"]/div/button").click()
        time.sleep(5)
        driver1.close()
    else:
        result_st.configure(state='normal')
        result_st.insert('end', "Invalid url, remember to include http(s)\n\n")
        result_st.configure(state='disabled')
#open driver button
button_open_driver=tk.Button(mainpage, text="open driver", relief="flat", command=open_driver, bg=bg_middle, fg=fg_deep, font=label_font_config)
button_open_driver.bind("<Enter>", lambda event: on_enter(event, button_open_driver))
button_open_driver.bind("<Leave>", lambda event: on_leave(event, button_open_driver))
button_open_driver.place(x=540, y=30, width=120, height=50)

#download
def start_download():
    result_st.configure(state='normal')
    #result_st.insert('end', "\nsuccessfully download " + str(x-1) + " pictures\n...\n")
    result_st.insert('end', "=" * 50 + "\n\n")
    result_st.configure(state='disabled')
#download button
button_down=tk.Button(mainpage, text="Start Download", relief="flat", command=start_download, bg=bg_middle, fg=fg_deep, font=label_font_config)
button_down.bind("<Enter>", lambda event: on_enter(event, button_down))
button_down.bind("<Leave>", lambda event: on_leave(event, button_down))
button_down.place(x=540, y=100, width=120, height=50)

#========================================button & function========================================

mainpage.mainloop()