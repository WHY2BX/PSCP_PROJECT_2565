#import package
from tkinter import *
import random
import time
import customtkinter
import pygame
from PIL import Image, ImageTk

pygame.mixer.init()

customtkinter.set_appearance_mode("System")
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


#bg
# window.config(bg = '#add123')

# image = Image.open("bgzaza.jpg")
# photo = ImageTk.PhotoImage(image)
# window.wm_attributes('-transparentcolor','#add123')
  
# Show image using label
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

#กล่องให้กรอก guess 
class App(customtkinter.CTk):
    window.title('Tum Kai')
    window.geometry('700x840')
    def __init__(self):
        super().__init__()
        self.textentry = customtkinter.CTkEntry(self ,width=200,
                        font=customtkinter.CTkFont("FC Minimal", size=20), justify='center', corner_radius=15)

        def update_screen(event):
            #ประกาศตัวแปรพวกนี้ให้เป็น global เพื่อให้ฟังก์ชันนี้เข้าถึงตัวแปรใน command ได้
            global game_end, score, lives, secret_word, clue, hints

            guess = self.self.textentry.get().strip() #Strip to remove whitespaces
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
                    self.textentry.delete(0, 'end')
                    
                    
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
                self.textentry.delete(0, 'end')
                if lives < 1:
                    clue_str.set('Game Over!')
                    game_end = True

                status_str.set('Score : ' + str(score) + ' | ' + 'Lives: ' + '♥'*lives)
                self.textentry.delete(0, 'end')

        def update_screen_2():
            #ประกาศตัวแปรพวกนี้ให้เป็น global เพื่อให้ฟังก์ชันนี้เข้าถึงตัวแปรใน command ได้
            global game_end, score, lives, secret_word, clue, hints

            guess = self.textentry.get().strip() #Strip to remove whitespaces
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
                    self.textentry.delete(0, 'end')
                    
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
                self.textentry.delete(0, 'end')
                if lives < 1:
                    clue_str.set('Game Over!')
                    game_end = True

                status_str.set('Score : ' + str(score) + ' | ' + 'Lives: ' + '♥'*lives)
                self.textentry.delete(0, 'end')

        self.textentry.bind('<Return>', update_screen)
        self.textentry.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
    
        self.button = customtkinter.CTkButton(self, text="Submit",
                                            border_width=2,  # <- custom border_width
                                            background_corner_colors=None,
                                            fg_color=None,  # <- no fg_color
                                            corner_radius=10,
                                            command=update_screen_2)
        self.button.grid(padx=(20, 0), pady=(20, 20))

#โปรแกรมหลักที่ check ว่าจบเกมแล้วหรือยัง
def main():
    if __name__ == "__main__":
            app = App()
            app.mainloop()
            
    if not game_end:
        #print('Test Refresh')
        window.after(1000, main)
            
    else:
        # self.button['state'] = 'disable'
        print('Quitting...')
        window.quit()


window.after(1000, main)
window.mainloop()

#จบเกม
print('End Game')
