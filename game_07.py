#import package
from tkinter import *
import random
import time
import customtkinter
import pygame
import sys
import os
from PIL import Image, ImageTk

pygame.mixer.init()

customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("blue")



#instrumentals
bg_music = pygame.mixer.music.load('bg.mp3')
correct_sound = pygame.mixer.Sound('correct.wav')
wrong_sound = pygame.mixer.Sound('buzzer.wav')

pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1) #<-----ปรับเสียงbg(เป็นfloat) ปรับได้ตั้งเเต่0.0ถึง1.0
correct_sound.set_volume(0.1) #<-----ปรับเสียงeffect ถูก
wrong_sound.set_volume(0.1) #<-----ปรับเสียงeffcet ผิด

#สร้าง app window
window = Tk()
window.title('<e> Quiz')
window.geometry('700x840')

window.maxsize(700, 840)
window.minsize(700, 840)

#icon
icon = PhotoImage(file = 'icon.jpg')
window.iconphoto(False, icon)

#bg
# window.config(bg = '#add123')
# image = Image.open("test_bg_01.png")
# photo = ImageTk.PhotoImage(image)
# window.wm_attributes('-transparentcolor','#add123')
# label1 = Label( window, image = photo)
# label1.place(x = 0, y = 0)

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
    'append()':
        {'category': 'list method',
         'hints': ['สามารถเพิ่มค่าเข้าไปใน list ได้']
        },
    'insert()':
        {'category': 'list method',
         'hints': ['สามารถเเทรกค่าเข้าไปใน list\nตามตำเเหน่งที่ต้องการได้']
        },
    'sort()':
        {'category': 'list method',
         'hints': ['สามารถเรียงลำดับค่าใน list ได้']
        },
    'index()':
        {'category': 'list method',
         'hints': ['สามารถระบุตำเเหน่งของค่าที่ต้องการใน list ได้']
        },
    'capitalize()':
        {'category': 'string method',
         'hints': ['สามารถเปลี่ยนตัวอักษรตัวเเรก\nเป็นตัวพิมพ์ใหญ่ได้']
        },
    'find()':
        {'category': 'string method',
         'hints': ['สามารถระบุตำเเหน่งของค่าที่ต้องการได้']
        },
    'isnumeric()':
        {'category': 'string method',
         'hints': ['จะคืนค่า True ถ้าหากอักขระทุกตัว\nบนstringเป็นตัวเลข']
        },
    'lower()':
        {'category': 'string method',
         'hints': ['เปลี่ยน string ทุกตัวเป็นตัวพิมพ์เล็ก']
        },
    'upper()':
        {'category': 'string method',
         'hints': ['เปลี่ยน string ทุกตัวเป็นตัวพิมพ์ใหญ่']
        },
    'swapcase()':
        {'category': 'string method',
         'hints': ['เปลี่ยน string ที่เป็นตัวพิมพ์เล็กเป็นตัวพิมพ์ใหญ่\nเเละเปลี่ยนตัวพิมพ์ใหญ่เป็นตัวพิมพ์เล็ก']
        },
    'get()':
        {'category': 'dict method',
         'hints': ['คืนค่า value ของ key ที่ระบุ']
        },
    'items()':
        {'category': 'dict method',
         'hints': ['คืนค่าออกมาเป็น list ที่ประกอบไปด้วย\n tuple ที่มี key เเละ value อยู่กันเป็นคู่']
        },
    'keys()':
        {'category': 'dict method',
         'hints': ['คืนค่าออกมาเป็น keys ของ dictionary\nที่ระบุโดยออกมาในรูปเเบบ list']
        },
    'pop()':
        {'category': 'dict method',
         'hints': ['ลบ key เเละ value ของมันตามที่ระบุ']
        },
    'update()':
        {'category': 'dict method',
         'hints': ['เพิ่มค่าใน dictionary\nตาม key เเละ values ที่ระบุ']
        },
    'values()':
        {'category': 'dict method',
         'hints': ['คืนค่าออกมาเป็น values ทุกตัวที่อยู่ใน dict']
        },
    'operator': 
        {'category': 'basic programming',
         'hints': ['ตัวดำเนินการ เรียกว่า\n*ตอบเป็นเอกพจน์*']
        },
    'operand':
        {'category': 'basic programming',
         'hints': ['ตัวถูกกระทำ เรียกว่า\n*ตอบเป็นเอกพจน์*']
        },
    'builtins':
        {'category': 'basic programming',
         'hints': ['Function print() เป็น Built-in function\nที่อยู่ใน Module ชื่อว่าอะไร']
        },
    'pemdas':
        {'category': 'basic programming',
         'hints': ['ลำดับการทำงานของเครื่องหมายทางคณิตศาสตร์\nโดยจะเรียงลำดับการทำงานจากซ้ายไปขวา']
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
            textentry.delete(0, 'end')

    clue_str.set(' | '. join(clue))
    win = ''.join(clue) == secret_word
    return win

#กล่องให้กรอก guess 
textentry = customtkinter.CTkEntry(master=window ,width=200,
                font=customtkinter.CTkFont("FC Minimal", size=20), justify='center', corner_radius=15)

def update_screen(event):
    #ประกาศตัวแปรพวกนี้ให้เป็น global เพื่อให้ฟังก์ชันนี้เข้าถึงตัวแปรใน command ได้
    global game_end, score, lives, secret_word, clue, hints

    guess = textentry.get().strip() #Strip to remove whitespaces
    guess = guess.lower() #lowercase

    if guess in secret_word:
        
        win = update_clue(guess, secret_word, clue)
        if win:
            #print('เฉลยตึงๆ : ' + secret_word)
            score += 1
            print('Score : ' + str(score))
            correct_sound.play()
            clue_str.set('Ahe! Ans : ' + secret_word)
            window.update()
            time.sleep(1) #ทำให้โปรแกรมค้างไว้ 1 วิ
            status_str.set('Score : ' + str(score) + ' | ' + 'Lives: ' + '♥'*lives)
            textentry.delete(0, 'end')
            
            
            if len(words) < 1:
                game_end = True
                clue_str.set('Congrats!')
            else:
                secret_word, clue = new_secret_word()
                category_str.set(word_dict[secret_word]['category'])
                clue_str.set(' | '.join(clue))
                hints = word_dict[secret_word]['hints']
                hints_str.set('\n'.join(hints))
                textentry.delete(0, 'end')
    else:
        print('ผิดแล้ว ไอควาย หน้าโง่')
        lives -= 1
        wrong_sound.play()
        textentry.delete(0, 'end')
        if lives < 1:
            clue_str.set('Game Over!')
            game_end = True

        status_str.set('Score : ' + str(score) + ' | ' + 'Lives: ' + '♥'*lives)
        textentry.delete(0, 'end')

def update_screen_2():
    #ประกาศตัวแปรพวกนี้ให้เป็น global เพื่อให้ฟังก์ชันนี้เข้าถึงตัวแปรใน command ได้
    global game_end, score, lives, secret_word, clue, hints

    guess = textentry.get().strip() #Strip to remove whitespaces
    guess = guess.lower() #lowercase

    if guess in secret_word:
        
        win = update_clue(guess, secret_word, clue)
        if win:
            #print('เฉลยตึงๆ : ' + secret_word)
            score += 1
            print('Score : ' + str(score))
            correct_sound.play()
            clue_str.set('Ahe! Ans : ' + secret_word)
            window.update()
            time.sleep(1) #ทำให้โปรแกรมค้างไว้ 1 วิ
            status_str.set('Score : ' + str(score) + ' | ' + 'Lives: ' + '♥'*lives)
            textentry.delete(0, 'end')
            
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
        wrong_sound.play()
        textentry.delete(0, 'end')
        if lives < 1:
            clue_str.set('Game Over!')
            game_end = True

        status_str.set('Score : ' + str(score) + ' | ' + 'Lives: ' + '♥'*lives)
        textentry.delete(0, 'end')

textentry.bind('<Return>', update_screen)
textentry.pack(pady=10, padx=225)
    
button = customtkinter.CTkButton(master=window, text="Submit",
                                bg_color = 'transparent',
                                border_width=2,  # <- custom border_width
                                border_spacing=0,
                                fg_color=None,  # <- no fg_color
                                corner_radius=10,
                                command=update_screen_2)
button.pack(pady=20, padx=225)

#โปรแกรมหลักที่ check ว่าจบเกมแล้วหรือยัง
def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)

def Close():
    window.destroy()

def main():
    if not game_end:
        #print('Test Refresh')
        window.after(1000, main)

    else:
        button.configure(state="disabled")
        print('Quitting...')
        exit_button = customtkinter.CTkButton(master=window, text="Exit",
                                bg_color = 'transparent',
                                border_width=2,  # <- custom border_width
                                border_spacing=0,
                                fg_color=None,  # <- no fg_color
                                corner_radius=10,
                                command= Close)
        exit_button.pack(pady=20)
        restart_button = customtkinter.CTkButton(master=window, text="Play again?",
                                bg_color = 'transparent',
                                border_width=2,  # <- custom border_width
                                border_spacing=0,
                                fg_color=None,  # <- no fg_color
                                corner_radius=10,
                                command= restart_program)
        restart_button.pack(pady=20)
window.after(1000, main)
window.mainloop()

#จบเกม
print('End Game')
