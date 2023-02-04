import tkinter as tk
from tkinter import ttk
import unicodedata

from PublicClass import *

def adjast(text,width:int,pos:str = "^")->str: #全角文字入りテキストの幅調整
	#f文字列で長さ指定した時，全角文字は実際には長さ2にも関わらず1でカウントされるため，長くなってしまう
	#全角文字の数だけ指定の長さを短くする
	text = str(text)
	for moji in text:
		if unicodedata.east_asian_width(moji) in "FWA": #文字が全角の時
			width -= 1 
	if width<0: print("OverFlow!")
	return f"{text: {pos}{width}}"

class Staff(ttk.Frame):
	table_top_text = "|".join(list(map(lambda text_width: adjast(text_width[0],text_width[1]),
			[("待ち番号",10),("会員番号",10),("お名前",25),("内容",40),("予約",6),("担当",10),("来店時刻",10)])))
	header_list = ["待ち番号",	"会員番号",	"お名前",	"内容",	"予約",	"担当",	"来店時刻"]
	col_width = [ 	2,			2,			4,		6,		2,		2,		2]
	row_max = 8 #表示可能な人数

	def __init__(self,subroot:tk.Toplevel):
		super().__init__(subroot,width=WINDOW_WIDTH,height=WINDOW_HEIGHT)
		self.clients:int = 0 #現在の人数
		self.row_start:int = 0 #表示している最初の待ち番号

		self.renew()

	def renew(self,row_start=0): #最新情報読み込んで表示更新
		ChildDelete(self)

		self.add_header()

		client_list = ClientInfo.query_all()
		self.clients = len(client_list)
		
		for (index,client) in enumerate(client_list):
			#self.make_label(client).pack()
			self.add_row(client=client,row=index+2)
	
	def make_label(self,client:ClientInfo)->ttk.Label:
		format_info = [(client.waiting_num,10),(client.member_num,10),(client.name+" 様",25),(client.subject,40),
						("あり"if client.reservation else "なし",6),(client.staff,10),(client.timestamp,10)]
		text = "|".join(list(map(lambda text_width: adjast(text_width[0],text_width[1]),format_info)))
		print(text)

		return ttk.Label(self,text=text,font=("Arial",20),foreground=("blue"if client.member_num>0 else "blue"),anchor=tk.W)

	def add_header(self):
		col = 0
		for index in range(len(Staff.col_width)):
			put(ttk.Label(self,text=Staff.header_list[index],font=("Arial",10),background="gray",anchor=tk.CENTER),xy=(col,1),w=Staff.col_width[index])
			col += Staff.col_width[index]
	
	def add_row(self,client:ClientInfo,row:int):
		data = [client.waiting_num,client.member_num,client.name+" 様",client.subject,"あり"if client.reservation else "なし",client.staff,client.timestamp]
		col = 0
		for index in range(len(data)):
			put(ttk.Label(self,text=data[index],font=("Arial",12),foreground=("blue" if client.member_num>0 else "black"),anchor=tk.CENTER),xy=(col,row),w=Staff.col_width[index])
			col += Staff.col_width[index]
			status_box = ttk.Combobox(self,values=ClientInfo.status_list,state="readonly")
			status_box.set(client.status)
			status_box.bind('<<ComboboxSelected>>',lambda _:self.status_changed(client,status_box))
			put(status_box,xy=(col,row),w=24-col)
	
	def status_changed(self,client:ClientInfo,statusbox:ttk.Combobox):
		client.status_update(statusbox.get())
		print_all()


CELL_WIDTH = WINDOW_WIDTH//24
CELL_HEIGHT = WINDOW_HEIGHT//10
def put(widget:ttk.Widget,xy:tuple[int,int],w=1,h=1):
	widget.place(x=(xy[0]+w/2)*CELL_WIDTH,y=(xy[1]+h/2)*CELL_HEIGHT,width=w*CELL_WIDTH,height=h*CELL_HEIGHT,anchor=tk.CENTER)
