from tkinter import *
import tkinter.messagebox
import customtkinter
import random
import time

#สร้าง app window
# Label = Tk.Label(text='Hello world')
window = Tk()
window.title('Tum Kai')
window.geometry('700x840')

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    
    #App
    def __init__(self):
        super().__init__()
        
        game_end = False #เริ่มต้นเกมยังไม่จบ
        score = 0
        lives = 3
        
        #ชื่อเกมด้านบนสุด
        self.label_1 = customtkinter.CTkLabel(text="What's in the blank?",
                                            text_font=("FC Minimal", 25))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=150)
        
        #แสดงชีวิตและคะแนน
        self.status_str = customtkinter.CTkLabel(text = "Score: " + str(score) + " | " + "Lives: " + "♥"*lives, 
                                            text_font=('FC Minimal', 20))
        self.status_str.grid(row=2, column=0, pady=10, padx=150)
        
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
        
        # แสดง category บน window
        self.category_str = customtkinter.CTkLabel(text = (word_dict[secret_word]['category']),
                                    text_font=('FC Minimal', 20)) 
        self.category_str.grid(row=3, column=0,  sticky="we", pady=10, padx=225)
        
        # แสดง clue
        self.clue_str = customtkinter.CTkLabel(text = ' | '.join(clue),
                                        text_font=('FC Minimal', 35))
        self.clue_str.grid(row=4, column=0, pady=10, padx=225)
        
        # เเสดง hints
        hints = word_dict[secret_word]['hints']
        self.hints = customtkinter.CTkLabel(text = word_dict[secret_word]['hints'],
                                            text_font = ("FC Minimal", 25))
        hints = ('\n'.join(hints))

        self.show_hint_text = customtkinter.CTkLabel(text = hints,
                                            text_font=('FC Minimal', 20))
        self.show_hint_text.grid(row=5, column=0, pady=10, padx=225)
        
        # กล่อง input
        self.entry = customtkinter.CTkEntry(width=200,
                                        placeholder_text="Insert what's on your mind.", 
                                        text_font=("FC Minimal", 10), justify='center')
        self.entry.grid(row=6, column=0, pady=10, padx=225)
        entry = self.entry
        
        #ปุ่มกด submit พร้อมฟังก์ชันที่อัพเดต clue และสถานะของเกม
        def update_clue(guess, secret_word, clue):
            for i in range(len(secret_word)):
                if guess == secret_word[i]:
                    clue[i] = guess

            self.clue_str = customtkinter.CTkLabel(text = ' | '.join(clue),
                                        text_font=('FC Minimal', 35))
            win = ''.join(clue) == secret_word
            return win
        
        def update_screen():
            #ประกาศตัวแปรพวกนี้ให้เป็น global เพื่อให้ฟังก์ชันนี้เข้าถึงตัวแปรใน command ได้
            global game_end, score, lives, secret_word, clue, hints
            
            guess = entry.get().strip() #Strip to remove whitespaces
            guess = guess.lower() #lowercase

            if guess in secret_word:
                win = update_clue(guess, secret_word, clue)
                if win:
                    print('เฉลยตึงๆ : ' + secret_word)
                    score += 1
                    print('Score : ' + str(score))
                    self.entry = customtkinter.CTkEntry(text = 'Ahe! Ans : ' + secret_word)
                    self.update()
                    time.sleep(5) #ทำให้โปรแกรมค้างไว้ 5 วิ
                    
                    if len(words) < 1:
                        game_end = True
                        self.entry = customtkinter.CTkEntry(text='Congrats!')
                    else:
                        secret_word, clue = new_secret_word()
                        category_str = (word_dict[secret_word]['category'])
                        self.category_str = customtkinter.CTkEntry(text = ' | '.join(clue))
                        hints = word_dict[secret_word]['hints']
                        self.hints_str = customtkinter.CTkLabel(text = '\n'.join(hints))
            else:
                print('ผิดแล้ว ไอควาย หน้าโง่')
                lives -= 1
                if lives < 1:
                    self.clue_str = customtkinter.CTkLabel(text = 'Game Over!')
                    game_end = True
                
                self.status_str = customtkinter.CTkLabel(text = 'Score : ' + str(score) + ' | ' + 'Lives: ' + '♥'*lives)
                self.entry.delete(0, 'end')
        
        #ปุ่ม
        self.button = customtkinter.CTkButton(text="Submit",
                                                border_width=2,  # <- custom border_width
                                                fg_color=None,  # <- no fg_color
                                                command=update_screen)
        self.button.grid(row=7, column=0, columnspan=1, pady=20, padx=225, sticky="we")
        
    # def button_event(self, update_screen):
    #     command=update_screen()

    def update_clue(guess, secret_word, clue):
        for i in range(len(secret_word)):
            if guess == secret_word[i]:
                clue[i] = guess

        clue_str = (' | '. join(clue))
        win = ''.join(clue) == secret_word
        return win

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
