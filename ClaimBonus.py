import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog
from tkinter import scrolledtext
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import os
import re #regular expression

#color info
bg_deep = "#4F4F4F"
bg_middle = "#6C6C6C"
bg_light = "#7B7B7B"
bg_highlight = "#C4E1FF"
fg_deep = "#FCFCFC"

#main page info
mainpage=tk.Tk()
mainpage.title("claim script")
mainpage.geometry("800x600+640+160")
mainpage.configure(bg=bg_deep)
mainpage.resizable(False, False)

webdriver_path = 'D:\\Drivers\\chromedriver.exe'

#url info
first_page = "https://www.twitch.tv/"
second_page = "https://www.twitch.tv/franchiseglobalart"

#pos info
position_x = 50
position_y = 20
space_x = 150
space_y = 40

label_font_config = tkFont.Font(family="Arial", size=10, weight="bold")
word_font_config = tkFont.Font(family="Arial", size=10)

#global variable
claiming = False

#========================================event & function========================================
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

#login
def login_func(elementA, elementP, acc, pas, target_page):
    elementA.send_keys(acc.get())  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    elementP.send_keys(pas.get())  #use send_keys instead of sendkey for webelements
    result_st.configure(state='normal')
    result_st.insert('end', "username/password sent\n\n")
    result_st.configure(state='disabled')
    driver1.find_element_by_xpath("/html/body/div[3]/div/div/div/div/div/div[1]/div/div/div[3]/form/div/div[3]/button").click()
    target_page.destroy()

#open driver
def open_driver():
    if re.match("http[s]?://([a-zA-Z]|[0-9]|[$-_@.&+]|[!*,]|(%[0-9a-fA-F][0-9a-fA-F]))+", url.get()): #best url re?
        #open driver
        global driver1
        driver1 = webdriver.Chrome(executable_path=webdriver_path)
        driver1.get(url.get())
        result_st.configure(state='normal')
        result_st.insert('end', "open web driver\n\n")
        result_st.insert('end', "connect to"+url.get()+"\n\n")
        result_st.configure(state='disabled')
        WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"root\"]/div/div[2]/nav/div/div[3]/div[3]/div/div[1]/div[1]/button")))
        #click login button
        driver1.find_element_by_xpath("//*[@id=\"root\"]/div/div[2]/nav/div/div[3]/div[3]/div/div[1]/div[1]/button").click()
        WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"login-username\"]")))
        account_element = driver1.find_element_by_xpath("//*[@id=\"login-username\"]")
        password_element = driver1.find_element_by_xpath("//*[@id=\"password-input\"]")
        #================================================start of login page================================================
        #config
        login_page=tk.Toplevel(mainpage)
        login_page.title("Login")
        login_page.geometry("360x160+900+400")
        login_page.configure(bg=bg_deep)
        login_page.resizable(False, False)
        #parameter
        login_pos_x=20
        login_pos_y=20
        #label account
        label_account=tk.Label(login_page, text="Account  ", anchor="e", bg=bg_deep, fg=fg_deep, font=label_font_config)
        label_account.place(x=login_pos_x, y=login_pos_y, width=100, height=24)
        #entry account
        account=tk.StringVar()
        entry_account=tk.Entry(login_page, textvariable=account, bg=bg_light, fg=fg_deep, font=word_font_config)
        entry_account.place(x=login_pos_x+120, y=login_pos_y, width=180, height=24)
        #label password
        label_password=tk.Label(login_page, text="Password  ", anchor="e", bg=bg_deep, fg=fg_deep, font=label_font_config)
        label_password.place(x=login_pos_x, y=login_pos_y+space_y, width=100, height=24)
        #entry password
        password=tk.StringVar()
        entry_password=tk.Entry(login_page, show="*", textvariable=password, bg=bg_light, fg=fg_deep, font=word_font_config)
        entry_password.place(x=login_pos_x+120, y=login_pos_y+space_y, width=180, height=24)
        #=================================================button=================================================
        #login button
        button_file=tk.Button(login_page, text="Login", command=lambda:login_func(account_element, password_element, account, password, login_page), bg=bg_middle, fg=fg_deep, font=label_font_config)
        button_file.bind("<Enter>", lambda event: on_enter(event, button_file))
        button_file.bind("<Leave>", lambda event: on_leave(event, button_file))
        button_file.place(x=login_pos_x+140, y=login_pos_y+space_y*2+10, width=60, height=24)
        #================================================end of login page================================================
    else:
        result_st.configure(state='normal')
        result_st.insert('end', "Invalid url, remember to include http(s)\n\n")
        result_st.configure(state='disabled')

def handler_claim_func():
    global driver1
    driver1.get(channel.get())
    while claiming:
        WebDriverWait(driver1, 600).until(EC.presence_of_element_located((By.XPATH, "//*[@style=\"width: fit-content;\"]/div/div[1]/div/div/div/div/div/section/div/div[5]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div/div/button")))
        driver1.find_element_by_xpath("//*[@style=\"width: fit-content;\"]/div/div[1]/div/div/div/div/div/section/div/div[5]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div/div/button").click()

def claim_bonus():
    global claiming
    claiming = True
    button_claim.configure(text="stop!", command=stop_claiming)
    handler_thread = threading.Thread(target = handler_claim_func, daemon=True)
    handler_thread.start()

def stop_claiming():
    global claiming
    claiming = False
    button_claim.configure(text="claim bonus!", command=claim_bonus)

"""
#download
def start_download():
    result_st.configure(state='normal')
    #result_st.insert('end', "\nsuccessfully download " + str(x-1) + " pictures\n...\n")
    result_st.insert('end', "=" * 50 + "\n\n")
    result_st.configure(state='disabled')
#download button
button_down=tk.Button(mainpage, text="Start Download", command=start_download, bg=bg_middle, fg=fg_deep, font=label_font_config)
button_down.bind("<Enter>", lambda event: on_enter(event, button_down))
button_down.bind("<Leave>", lambda event: on_leave(event, button_down))
button_down.place(x=540, y=100, width=120, height=50)
"""
#========================================button & function========================================

#===========================================basic layout===========================================
#label url
label_url=tk.Label(mainpage, text="Target url  ", anchor="e", bg=bg_deep, fg=fg_deep, font=label_font_config)
label_url.place(x=position_x, y=position_y, width=150, height=24)
#entry url
url=tk.StringVar()
entry_url=tk.Entry(mainpage, textvariable=url, bg=bg_light, fg=fg_deep, font=word_font_config)
entry_url.place(x=position_x+space_x, y=position_y, width=180, height=24)
entry_url.insert(0, first_page)
#label channel
label_channel=tk.Label(mainpage, text="Target url  ", anchor="e", bg=bg_deep, fg=fg_deep, font=label_font_config)
label_channel.place(x=position_x, y=position_y+space_y, width=150, height=24)
#entry channel
channel=tk.StringVar()
entry_channel=tk.Entry(mainpage, textvariable=channel, bg=bg_light, fg=fg_deep, font=word_font_config)
entry_channel.place(x=position_x+space_x, y=position_y+space_y, width=180, height=24)
entry_channel.insert(0, second_page)


#label file location
label_file_location=tk.Label(mainpage, text="Choose save location  ", anchor="e", bg=bg_deep, fg=fg_deep, font=label_font_config)
label_file_location.place(x=position_x, y=position_y+space_y*2, width=150, height=24)
#entry file location
file_location=tk.StringVar()
entry_file_location=tk.Entry(mainpage, textvariable=file_location, bg=bg_light, fg=fg_deep, font=word_font_config)
entry_file_location.place(x=position_x+space_x, y=position_y+space_y*2, width=180, height=24)
#filedialog button
#relief="flat"
button_file=tk.Button(mainpage, text="...", command=search_file, bg=bg_middle, fg=fg_deep, font=label_font_config)
button_file.bind("<Enter>", lambda event: on_enter(event, button_file))
button_file.bind("<Leave>", lambda event: on_leave(event, button_file))
button_file.place(x=position_x+space_x*2.25, y=position_y+space_y*2, width=30, height=24)


#label result
label_result=tk.Label(mainpage, text="Log :", bg=bg_deep, fg=fg_deep, font=label_font_config)
label_result.place(x=position_x, y=position_y+space_y*4, height=30)
#scrolledtext result
result_st=scrolledtext.ScrolledText(mainpage, padx=12, pady=10, bg=bg_light, fg=fg_deep, font=word_font_config)
result_st.place(x=position_x, y=position_y+space_y*4+30, width=700, height=360)
result_st.insert('end', "Hello!\n\n")
result_st.configure(state='disabled')


#open driver button
button_open_driver=tk.Button(mainpage, text="open driver", command=open_driver, bg=bg_middle, fg=fg_deep, font=label_font_config)
button_open_driver.bind("<Enter>", lambda event: on_enter(event, button_open_driver))
button_open_driver.bind("<Leave>", lambda event: on_leave(event, button_open_driver))
button_open_driver.place(x=position_x+space_x*3, y=position_y, width=120, height=50)
#claim bonus button
button_claim=tk.Button(mainpage, text="claim bonus!", command=claim_bonus, bg=bg_middle, fg=fg_deep, font=label_font_config)
button_claim.bind("<Enter>", lambda event: on_enter(event, button_claim))
button_claim.bind("<Leave>", lambda event: on_leave(event, button_claim))
button_claim.place(x=position_x+space_x*3, y=position_y+space_y*2, width=120, height=50)
#===========================================basic layout===========================================

mainpage.mainloop()