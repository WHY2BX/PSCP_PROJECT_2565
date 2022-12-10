#import package
from tkinter import *
import random
import time
import customtkinter

#สร้าง app window
# Label = Tk.Label(text='Hello world')
window = Tk()
window.title('Tum Kai')
window.geometry('700x840')

#สถานะเกม
game_end = False #เริ่มต้นเกมยังไม่จบ
score = 0
lives = 3

#เเสดง score กับ lives บน window

status_str = StringVar() #มาจาก Tkinter

# status_str = customtkinter.CTkLabel(text = "Score: " + "%d" %score + " | " + "Lives: " + "♥"*lives, 
#                                             text_font=('FC Minimal', 20))
# status_str.pack(pady=10, padx=150)

status_str.set('Score: '+ str(score) + ' | ' + 'Lives: ' + '♥'*lives)
show_status = Label(window, textvariable=status_str, font=('FC Minimal', 20))
show_status.pack(pady=20)

#สร้าง words category hints
word_dict = {
    'x':
        {'category': 'RJarn',
         'hints': ['ชอบจังคลิปเต้นเนี่ย', 'ปรับปรุงโลจิก', 'คำผวน']
        },
    'y':
        {'category': 'Friend',
         'hints': ['ตะหลุ่ม', 'ตุ่มมง', 'พอเถอะสแว้ก']
        }
    }

words = list(word_dict.keys())
#functionสุ่มคำ(random)เเละสร้างclue ['?',...,'?']
def new_secret_word():
    random.shuffle(words)
    secret_word = words.pop()
    clue = list('?'*len(secret_word))
    return secret_word, clue

secret_word, clue = new_secret_word()

#แสดง category, clue บน window
category_str = StringVar()
category_str.set(word_dict[secret_word]['category'])
show_category = Label(window, textvariable=category_str, font=('FC Minimal', 20)) 
show_category.pack(pady=10)

clue_str = StringVar()
clue_str.set(' | '.join(clue))
show_clue = Label(window, textvariable=clue_str, font=('FC Minimal', 35))
show_clue.pack(padx=10, pady=10)

#เเสดง hints
hints = word_dict[secret_word]['hints']
hints_text = StringVar()
hints_text.set('hints')
hints_str = StringVar()
hints_str.set('\n'.join(hints))

show_hint_text = Label(window, textvariable=hints_text, font=('FC Minimal', 20))
show_hint_text.pack()
show_hint_text = Label(window, textvariable=hints_str, font=('FC Minimal', 28))
show_hint_text.pack(pady=10)

#ปุ่มกด submit พร้อมฟังก์ชันที่อัพเดต clue และสถานะของเกม
def update_clue(guess, secret_word, clue):
    for i in range(len(secret_word)):
        if guess == secret_word[i]:
            clue[i] = guess

    clue_str.set(' | '. join(clue))
    win = ''.join(clue) == secret_word
    return win

#กด return ด้วย enter + ลบข้อความเก่าออก
def onReturn(event):
    print('Return Pressed')
    textentry_first.delete(0, 'end')
    

#กล่องให้กรอก guess ยังไม่ได้
textentry_first = customtkinter.CTkEntry(width=200,
                    text_font=("FC Minimal", 20), justify='center')
textentry_first.bind("<Return>", onReturn)
textentry_first.pack(pady=10, padx=225)

def update_screen():
    #ประกาศตัวแปรพวกนี้ให้เป็น global เพื่อให้ฟังก์ชันนี้เข้าถึงตัวแปรใน command ได้
    global game_end, score, lives, secret_word, clue, hints, textentry

    guess = textentry_first.get().strip() #Strip to remove whitespaces
    guess = guess.lower() #lowercase

    if guess in secret_word:
        win = update_clue(guess, secret_word, clue)
        if win:
            print('เฉลยตึงๆ : ' + secret_word)
            score += 1
            print('Score : ' + str(score))
            clue_str.set('Ahe! Ans : ' + secret_word)
            window.update()
            time.sleep(1) #ทำให้โปรแกรมค้างไว้ 5 วิ
            status_str.set('Score : ' + str(score) + ' | ' + 'Lives: ' + '♥'*lives)
            
            if len(words) < 1:
                game_end = True
                clue_str.set('Congrats!')
            else:
                secret_word, clue = new_secret_word()
                category_str.set(word_dict[secret_word]['category'])
                clue_str.set(' | '.join(clue))
                hints = word_dict[secret_word]['hints']
                hints_str.set('\n'.join(hints))
    else:
        print('ผิดแล้ว ไอควาย หน้าโง่')
        lives -= 1
        if lives < 1:
            clue_str.set('Game Over!')
            game_end = True
        
        status_str.set('Score : ' + str(score) + ' | ' + 'Lives: ' + '♥'*lives)
        textentry.delete(0, 'end')

button = customtkinter.CTkButton(text="Submit",
                                    border_width=2,  # <- custom border_width
                                    fg_color=None,  # <- no fg_color
                                    command=update_screen)
button.pack(pady=20, padx=225)

#โปรแกรมหลักที่ check ว่าจบเกมแล้วหรือยัง
def main():
    if not game_end:
        #print('Test Refresh')
        window.after(1000, main)

    else:
        button['state'] = 'disable'
        print('Quitting...')
        window.quit()

window.after(1000, main)
window.mainloop()

#จบเกม
print('End Game')
