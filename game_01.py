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

status_str.set('Score: '+ str(score) + ' | ' + 'Lives: ' + '♥'*lives)
show_status = Label(window, textvariable=status_str, font=('FC Minimal', 20))
show_status.pack(pady=20)

#สร้าง words category hints
word_dict = {
    'chatipho':
        {'category': 'RJarn',
         'hints': ['ชอบจังคลิปเต้นเนี่ย', 'ปรับปรุงโลจิก', 'คำผวน']
        },
    'sirimongkol':
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

#กล่องให้กรอก guess
textentry = Entry(window, width=10, borderwidth=1, font=('FC Minimal', 28), justify='center')
textentry.pack(pady=15)

#ปุ่มกด submit พร้อมฟังก์ชันที่อัพเดต clue และสถานะของเกม
def update_clue(guess, secret_word, clue):
    for i in range(len(secret_word)):
        if guess == secret_word[i]:
            clue[i] = guess

    clue_str.set(' | '. join(clue))
    win = ''.join(clue) == secret_word
    return win

def update_screen():
    #ประกาศตัวแปรพวกนี้ให้เป็น global เพื่อให้ฟังก์ชันนี้เข้าถึงตัวแปรใน command ได้
    global game_end, score, lives, secret_word, clue, hints
    
    guess = textentry.get().strip() #Strip to remove whitespaces
    guess = guess.lower() #lowercase

    if guess in secret_word:
        win = update_clue(guess, secret_word, clue)
        if win:
            print('เฉลยตึงๆ : ' + secret_word)
            score += 1
            print('Score : ' + str(score))
            clue_str.set('Ahe! Ans : ' + secret_word)
            window.update()
            time.sleep(5) #ทำให้โปรแกรมค้างไว้ 5 วิ
            
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

submit_btn = Button(window, text='Submit', command=update_screen)
submit_btn.pack()

#โปรแกรมหลักที่ check ว่าจบเกมแล้วหรือยัง
def main():
    if not game_end:
        #print('Test Refresh')
        window.after(1000, main)
    else:
        submit_btn['state'] = 'disable'
        print('Quitting...')
        window.quit()

window.after(1000, main)
window.mainloop()

#จบเกม
print('End Game')

