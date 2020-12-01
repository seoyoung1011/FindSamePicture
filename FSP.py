from tkinter import *
import tkinter.filedialog
import os, random, time
from tkinter import messagebox
from PIL import Image
import mouse

select_theme = '기본 테마'

class FindSamePicture(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.frame = None
        self.geometry("600x400")
        self.resizable(0, 0)
        self.switch_frame(main)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.frame.pack()
        self.propagate(0)

class main(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, width=600, height=400)
        Label(self, text="같은 그림 찾기", font=('맑은 고딕', 28)).place(x="180", y="80")
        Button(self, text="게임 시작", font=('맑은 고딕', 17), command=lambda: master.switch_frame(startgame)).place(x="240", y="180")
        Button(self, text="테마 설정", font=('맑은 고딕', 17), command=lambda: master.switch_frame(setting_theme)).place(x="240", y="240")
        self.propagate(0)

class startgame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, width=600, height=400)
        back = Button(self, text="뒤로 가기", command=lambda: master.switch_frame(main))
        back.place(x='0', y='0')
        how_play_game = Label(self, text="게임 방법\n\n"
                                         "-원하는 테마를 클릭하고 선택\n 버튼을 누릅니다.\n"
                                         "-게임 시작 버튼을 누릅니다.\n"
                                         "-게임창 우측 상단에 있는 시작을\n 누르면 이미지가 잠깐 보여집니다.\n"
                                         "-그 밑에 비어있는 텍스트 상자에\n 동일한 이미지의 칸의 번호를 각각\n 입력한 뒤 선택 버튼을 누릅니다.", justify='left', font=("맑은 고딕", 12))
        how_play_game.place(x='50', y='50')
        self.listbox = Listbox(self, height=7)
        files = os.listdir('./themes/')
        for (i, file) in enumerate(files):
            self.listbox.insert(i + 1, file)
        Label(self, text="테마 선택", font=('맑은 고딕', 16)).place(x="350", y="40")
        self.listbox.place(x="350", y="80")
        Button(self, text="선택", command=self.ins).place(x='360', y='220')
        Button(self, text="게임 시작", command=lambda: master.switch_frame(game_start)).place(x='400', y='220')
        self.propagate(0)

    def ins(self):
        global select_theme
        theme = str(self.listbox.get(self.listbox.curselection()))
        print(self.listbox.curselection())
        print(theme)
        select_theme = theme


class setting_theme(Frame):
    pic_list = []
    def __init__(self, master):
        Frame.__init__(self, master, width=600, height=400)
        back = Button(self, text="뒤로 가기", command=lambda: master.switch_frame(main))
        back.pack(side="left", anchor="n")
        how_add_theme = Label(self, text="테마 추가 방법\n\n"
                                         "-이미지 선택을 눌러 8개의\n 사진을 가져옵니다.\n"
                                         "-게임 시작 버튼을 누릅니다\n"
                                         "-사진 파일 png, jpg만 가능하며\n 되도록이면 1:1 비율의\n 사진을 권장합니다.\n"
                                         "-8개를 추가한 후 테마 저장을\n 누른 뒤 게임시작으로 들어가\n 테마가 추가 된 것을 확인합니다.", justify='left', font=("맑은 고딕", 12))
        how_add_theme.place(x='50', y='50')
        self.listbox = Listbox(self, height=9)
        self.listbox.place(x="350", y="80")
        Button(self, text="이미지 선택", command=self.select_pic).place(x='415', y='235')
        Button(self, text="테마 저장", command=self.theme_add).place(x='500', y='330')
        self.propagate(0)

    def select_pic(self):
        root = tkinter.filedialog.askopenfilename(title="Select image", filetype=(('PNG 파일', '*.png'), ('JGP 파일', '*.jpg')))
        dir_name = os.path.basename(root)
        if root in self.pic_list:
            messagebox.showinfo("!!!!!", "이미지가 중복됩니다!!!")
            return 0
        self.listbox.insert(1, dir_name)
        self.pic_list.append(root)
        print(root)
        print(dir_name)
        print(self.pic_list)

    def theme_add(self):
        j = 0
        try:
            for i in range(1, 100):
                if not(os.path.exists(f'./themes/테마{i}')):
                    os.mkdir(os.path.join(f'./themes/테마{i}'))
                    j = i
                    break
        except OSError:
            print('Error: 파일을 생성하지 못했습니다')
        for i, file in enumerate(self.pic_list):
            img = Image.open(file)
            img_size = img.resize((95, 95))
            img_size.save(f'./themes/테마{j}/pic{i+1}.png')
        messagebox.showinfo("!!!!!", "테마가 추가 되었습니다! 게임 시작으로 들어가 확인해주세요!")

class game_start(Frame):
    pics = ["pic1A", "pic1B", "pic2A", "pic2B", "pic3A", "pic3B", "pic4A", "pic4B",
            "pic5A", "pic5B", "pic6A", "pic6B", "pic7A", "pic7B", "pic8A", "pic8B"]
    pictures = []
    canvas = Canvas
    canvas2 = Canvas
    def __init__(self, master):
        Frame.__init__(self, master, width=600, height=400)
        Button(self, text='시작', command=self.show_image).pack(side="right", anchor="n")
        Entry(self, width=5).place(x='510', y='30')
        Entry(self, width=5).place(x='510', y='50')
        Button(self, text='선택', command=self.show_image).place(x='555', y='50')
        self.canvas = Canvas(self, width=380, height=380, bg='white')
        self.canvas.place(x='110', y='0')
        self.board()
        self.propagate(0)

    def board(self):
        random.shuffle(self.pics)
        for pic in self.pics:
            if pic in "pic1A" or pic in "pic1B":
                self.pictures.append(PhotoImage(file=f'./themes/{select_theme}/pic1.png'))
            elif pic in "pic2A" or pic in "pic2B":
                self.pictures.append(PhotoImage(file=f'./themes/{select_theme}/pic2.png'))
            elif pic in "pic3A" or pic in "pic3B":
                self.pictures.append(PhotoImage(file=f'./themes/{select_theme}/pic3.png'))
            elif pic in "pic4A" or pic in "pic4B":
                self.pictures.append(PhotoImage(file=f'./themes/{select_theme}/pic4.png'))
            elif pic in "pic5A" or pic in "pic5B":
                self.pictures.append(PhotoImage(file=f'./themes/{select_theme}/pic5.png'))
            elif pic in "pic6A" or pic in "pic6B":
                self.pictures.append(PhotoImage(file=f'./themes/{select_theme}/pic6.png'))
            elif pic in "pic7A" or pic in "pic7B":
                self.pictures.append(PhotoImage(file=f'./themes/{select_theme}/pic7.png'))
            elif pic in "pic8A" or pic in "pic8B":
                self.pictures.append(PhotoImage(file=f'./themes/{select_theme}/pic8.png'))

    def show_image(self):
        for pic in self.pictures:
            if pic == self.pictures[0]: Label(self.canvas, image=pic).place(x='0', y='0')
            elif pic == self.pictures[1]: Label(self.canvas, image=pic).place(x='95', y='0')
            elif pic == self.pictures[2]: Label(self.canvas, image=pic).place(x='190', y='0')
            elif pic == self.pictures[3]: Label(self.canvas, image=pic).place(x='285', y='0')
            elif pic == self.pictures[4]: Label(self.canvas, image=pic).place(x='0', y='95')
            elif pic == self.pictures[5]: Label(self.canvas, image=pic).place(x='95', y='95')
            elif pic == self.pictures[6]: Label(self.canvas, image=pic).place(x='190', y='95')
            elif pic == self.pictures[7]: Label(self.canvas, image=pic).place(x='285', y='95')
            elif pic == self.pictures[8]: Label(self.canvas, image=pic).place(x='0', y='190')
            elif pic == self.pictures[9]: Label(self.canvas, image=pic).place(x='95', y='190')
            elif pic == self.pictures[10]: Label(self.canvas, image=pic).place(x='190', y='190')
            elif pic == self.pictures[11]: Label(self.canvas, image=pic).place(x='285', y='190')
            elif pic == self.pictures[12]: Label(self.canvas, image=pic).place(x='0', y='285')
            elif pic == self.pictures[13]: Label(self.canvas, image=pic).place(x='95', y='285')
            elif pic == self.pictures[14]: Label(self.canvas, image=pic).place(x='190', y='285')
            elif pic == self.pictures[15]: Label(self.canvas, image=pic).place(x='285', y='285')
        self.game()

    def game(self):
        self.update()
        time.sleep(1)
        self.canvas2 = Canvas(self, width=380, height=380, bg='white')
        self.canvas2.place(x='110', y='0')
        print("test")

    def draw_board(self, x, y):
        x = 0
        y = 0
        for pic in self.pictures:
            if pic == self.pictures[0]: Label(self.canvas2, image=pic).place(x=(x-1) * 95, y=(y-1) * 95)
            elif pic == self.pictures[1]: Label(self.canvas2, image=pic).place(x=(x-1) * 95, y=(y-1) * 95)
            elif pic == self.pictures[2]: Label(self.canvas2, image=pic).place(x=(x-1) * 95, y=(y-1) * 95)
            elif pic == self.pictures[3]: Label(self.canvas2, image=pic).place(x=(x-1) * 95, y=(y-1) * 95)
            elif pic == self.pictures[4]: Label(self.canvas2, image=pic).place(x=(x-1) * 95, y=(y-1) * 95)
            elif pic == self.pictures[5]: Label(self.canvas2, image=pic).place(x=(x-1) * 95, y=(y-1) * 95)
            elif pic == self.pictures[6]: Label(self.canvas2, image=pic).place(x=(x-1) * 95, y=(y-1) * 95)
            elif pic == self.pictures[7]: Label(self.canvas2, image=pic).place(x=(x-1) * 95, y=(y-1) * 95)
            elif pic == self.pictures[8]: Label(self.canvas2, image=pic).place(x=(x-1) * 95, y=(y-1) * 95)
            elif pic == self.pictures[9]: Label(self.canvas2, image=pic).place(x=(x-1) * 95, y=(y-1) * 95)
            elif pic == self.pictures[10]: Label(self.canvas2, image=pic).place(x=(x-1) * 95, y=(y-1) * 95)
            elif pic == self.pictures[11]: Label(self.canvas2, image=pic).place(x=(x-1) * 95, y=(y-1) * 95)
            elif pic == self.pictures[12]: Label(self.canvas2, image=pic).place(x=(x-1) * 95, y=(y-1) * 95)
            elif pic == self.pictures[13]: Label(self.canvas2, image=pic).place(x=(x-1) * 95, y=(y-1) * 95)
            elif pic == self.pictures[14]: Label(self.canvas2, image=pic).place(x=(x-1) * 95, y=(y-1) * 95)
            elif pic == self.pictures[15]: Label(self.canvas2, image=pic).place(x=(x-1) * 95, y=(y-1) * 95)

if __name__ == "__main__":
    FSP = FindSamePicture()
    FSP.mainloop()