import tkinter as tk
from tkinter import ttk
from functools import partial
import datetime
import os

import DataBase as db

#共通定数
WINDOW_HEIGHT = 500
WINDOW_WIDTH = 1000

NAME_MAX = 20 #名前の最大長

create_command = f"""
	CREATE TABLE {db.TABLE_NAME} (
		waiting_num INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
		member_num int NOT NULL,
		name varchar({NAME_MAX}) NOT NULL,
		reservation int NOT NULL,
		subject varchar(40) NOT NULL,
		staff varchar(10),
		timestamp int NOT NULL,
		status varchar(10)
		);
	"""
def create_table():
	db.execute(create_command) #テーブル作成 #アプリ起動時にMainで実行
def remove_table(): #ファイル削除 #こちらもMainで実行
	os.remove(db.FILENAME)
def print_all():
	print(db.print_all()) #テスト用

class ClientInfo:
	subject_list = ["パソコン，プリンタ等の不具合点検","お預け品の受け取り","パソコンの初期設定案内","操作説明，ご相談","定期点検(プレミアムメンバー様限定)","プレミアムメンバーのご契約に関して","その他"]
	staff_list = ["特になし","有澤","西野","濱田"] #担当
	status_list = ["未対応","対応済み","担当スタッフ待ち","キャンセル"]

	def __init__(self, waiting_num=None, member_num=0, name=None, reservation=False, subject=None, staff="--",timestamp=None,status="未対応"):
		self.waiting_num:int = waiting_num #待ち番号
		self.member_num:int = member_num #会員番号 #一般は0?
		self.name:str = name
		self.reservation:bool = reservation
		self.subject:str = subject #内容
		self.staff:str = staff #担当者
		self.timestamp:int = timestamp
		#self.guide_staff:str = guide_staff #受付したスタッフ
		self.status:str = status
	
	def clear(self):
		self.__init__()

	def registration(self): #顧客情報をdatabaseに登録(挿入)
		self.timestamp = datetime.datetime.now().strftime("%H:%M")

		command = "INSERT INTO"
		columns = " " + db.TABLE_NAME + "("
		values = " VALUES ("
		try:
			pair = (
				("member_num",self.member_num),
				("name",self.name),
				("reservation",self.reservation),
				("subject",self.subject),
				("staff",self.staff),
				("timestamp",self.timestamp),
				("status",self.status)
			)

			for column,value in pair:
				if type(value) is str: value = "\'" + value + "\'"
				columns += column + ", "
				values += str(value) + ", "
			
			columns, values = columns[:-2]+")",values[:-2]+")" #末尾の", "を")"に変換
			command += columns + values + ";"
			waiting_num = db.execute(command)
			if waiting_num==-1:raise ValueError #挿入失敗

		except ValueError:
			print("valueerror")
		
		self.waiting_num = waiting_num
		return waiting_num
	
	def status_update(self,value:str):
		try:
			result = db.execute(f"UPDATE {db.TABLE_NAME} SET status=\'{value}\' WHERE waiting_num={self.waiting_num};")
			if result==-1: raise ValueError
		except ValueError: print("valueerror")


	@classmethod
	def read_DBlist(cls,data:str): #データベースから顧客情報に変換
		client_list = []
		for row in data: #(waiting_num,member_num,name,reservation,subject,staff,timestamp,status)
			client_list.append(ClientInfo(waiting_num=int(row[0]),member_num=int(row[1]),name=row[2],reservation=row[3],subject=row[4],staff=row[5],timestamp=row[6],status=row[7]))
		return client_list
	
	@classmethod
	def query_all(cls):
		return ClientInfo.read_DBlist(db.query(f"SELECT * FROM {db.TABLE_NAME}"))

class NumberKey(ttk.Frame):
	key_size = 5
	def __init__(self,parent:ttk.Frame,strvar:tk.StringVar,maxlen=0):
		super().__init__(parent,relief="raised")
		self.var = strvar
		self.maxlen = maxlen #桁数制限 #0なら制限なし
		self.key_create()
	
	def key_create(self):
		for num in range(10):
			key_num = (num+1)%10 #1..9,0の順
			key = ttk.Button(self,text=key_num,command=partial(self.key_pushed,key_num),width=NumberKey.key_size)
			key.grid(column=num%5,row=num//5)
		
		key = ttk.Button(self,text="X",command=self.delkey_pushed)
		key.grid(column=6,row=2)

		key = ttk.Button(self,text="クリア",command=self.clearkey_pushed)
		key.grid(column=6,row=1)

	def key_pushed(self,num):
		if self.maxlen and len(self.var.get())>=self.maxlen: return
		self.var.set(self.var.get()+str(num))
	
	def delkey_pushed(self):
		self.var.set(self.var.get()[:-1])

	def clearkey_pushed(self):
		self.var.set("")
	
	#override
	def destroy(self):
		super().destroy()
		del self

class Keyboard(ttk.Frame):
	chr_list = [] #class_initで生成
	#[[ア行],[カ行],...]という形式

	key_width = 5
	key_height = 10

	@classmethod #クラス変数を定義するため，最初に実行
	def class_init(cls):
		dummy = "#"
		column = [] #各行の文字を格納 #[カタカナ],[濁点],[半濁点],[小文字]の構成
		katakana,dakuten,handakuten,komoji = Keyboard.list_reset()
		
		pos = 0x30a2 #アのunicode
		for num in range(5): #ア行
			char_num = pos+num*2
			katakana[num] = chr(char_num)
			komoji[num] = chr(char_num-1)
		Keyboard.chr_list.append([katakana,dakuten,handakuten,komoji])
		katakana,dakuten,handakuten,komoji = Keyboard.list_reset()

		pos = 0x30ab #カ
		for col in range(2): #カサ行
			for num in range(5):
				char_num = pos+(col*5+num)*2
				katakana[num] = chr(char_num)
				dakuten[num] = chr(char_num+1)
			Keyboard.chr_list.append([katakana,dakuten,handakuten,komoji])
			katakana,dakuten,handakuten,komoji = Keyboard.list_reset()
		
		pos = 0x30bf #タ
		for num in range(2): #タチ
			char_num = pos+num*2
			katakana[num] = chr(char_num)
			dakuten[num] = chr(char_num+1)
		pos = 0x30c4 #ツ
		num = 2
		katakana[num] = chr(pos)
		dakuten[num] = chr(pos+1)
		komoji[num] = chr(pos-1)
		pos=0x30c0 #ダ #ッの分ずれる
		for num in range(3,5): #テト
			char_num = pos+num*2
			katakana[num] = chr(char_num)
			dakuten[num] = chr(char_num+1)
		Keyboard.chr_list.append([katakana,dakuten,handakuten,komoji])
		katakana,dakuten,handakuten,komoji = Keyboard.list_reset()

		pos = 0x30ca #ナ
		for num in range(5): #ナ行
			char_num = pos+num
			katakana[num] = chr(char_num)
		Keyboard.chr_list.append([katakana,dakuten,handakuten,komoji])
		katakana,dakuten,handakuten,komoji = Keyboard.list_reset()

		pos = 0x30cf #ハ
		for num in range(5): #ハ行
			char_num = pos+3*num
			katakana[num] = chr(char_num)
			dakuten[num] = chr(char_num+1)
			handakuten[num] = chr(char_num+2)
		Keyboard.chr_list.append([katakana,dakuten,handakuten,komoji])
		katakana,dakuten,handakuten,komoji = Keyboard.list_reset()

		pos = 0x30de #マ
		for num in range(5): #マ行
			char_num = pos+num
			katakana[num] = chr(char_num)
		Keyboard.chr_list.append([katakana,dakuten,handakuten,komoji])
		katakana,dakuten,handakuten,komoji = Keyboard.list_reset()

		pos = 0x30e4 #ヤ
		for num in range(3): #ヤ行
			char_num = pos+num*2
			katakana[num*2] = chr(char_num)
			komoji[num*2] = chr(char_num-1)
		Keyboard.chr_list.append([katakana,dakuten,handakuten,komoji])
		katakana,dakuten,handakuten,komoji = Keyboard.list_reset()

		pos = 0x30e9 #ラ
		for num in range(5): #ラ行
			char_num = pos+num
			katakana[num] = chr(char_num)
		Keyboard.chr_list.append([katakana,dakuten,handakuten,komoji])
		katakana,dakuten,handakuten,komoji = Keyboard.list_reset()

		#その他
		katakana = ["ワ","ン","ー",dummy,dummy]
		Keyboard.chr_list.append([katakana,dakuten,handakuten,komoji])
		katakana,dakuten,handakuten,komoji = Keyboard.list_reset()
	
	@classmethod
	def list_reset(cls): #katakana,dakuten,handakuten,komojiに対して，すべてdummyで埋めて返す
		return ["#"]*5, ["#"]*5, ["#"]*5, ["#"]*5

	def __init__(self,parent:ttk.Frame,var:tk.StringVar):
		super().__init__(parent)
		self.var = var
		self.key_create()

	def key_create(self):
		for col in range(7): #ア〜マ行
			for row in range(5):
				char = Keyboard.chr_list[col][0][row]
				key = ttk.Button(self,text=char,command=partial(self.key_pushed,char))
				key.grid(column=col,row=row,ipady=Keyboard.key_height)
		col = 7 #ヤ行
		for row in range(3):
			char = Keyboard.chr_list[col][0][row*2]
			key = ttk.Button(self,text=char,command=partial(self.key_pushed,char))
			key.grid(column=col,row=row*2,ipady=Keyboard.key_height)
		col = 8 #ラ行
		for row in range(5):
			char = Keyboard.chr_list[col][0][row]
			key = ttk.Button(self,text=char,command=partial(self.key_pushed,char))
			key.grid(column=col,row=row,ipady=Keyboard.key_height)
		col = 9 #ワ,ン,ー
		for row in range(3):
			char = Keyboard.chr_list[col][0][row]
			key = ttk.Button(self,text=char,command=partial(self.key_pushed,char))
			key.grid(column=col,row=row,ipady=Keyboard.key_height)
		
		key = ttk.Button(self,text="X",command=self.delkey_pushed) #1文字削除
		key.grid(column=10,row=0,ipady=Keyboard.key_height)
		key = ttk.Button(self,text="クリア",command=self.clearkey_pushed) #全削除
		key.grid(column=10,row=1,ipady=Keyboard.key_height)

		key = ttk.Button(self,text="゛",command=self.type_change)
		key.grid(column=10,row=2,ipady=Keyboard.key_height)
		key = ttk.Button(self, text="゜",command=partial(self.type_change,2))
		key.grid(column=10,row=3,ipady=Keyboard.key_height)
		key = ttk.Button(self,text="小文字",command=partial(self.type_change,3))
		key.grid(column=10,row=4,ipady=Keyboard.key_height)
	
	def key_pushed(self,char):
		self.var.set(self.var.get()+char)
	
	def delkey_pushed(self):
		self.var.set(self.var.get()[:-1])
	
	def clearkey_pushed(self):
		self.var.set("")

	def type_change(self, char_type=1): #半濁点時はchar_type=2,小文字は3
		try:
			col_num,type_num,row_num = Keyboard.char2index(self.var.get()[-1])
			if type_num == char_type: #すでに最後が(半)濁音,または小文字
				target = Keyboard.chr_list[col_num][0][row_num]
				self.var.set(self.var.get()[:-1]+target)
			else: #それ以外
				target = Keyboard.chr_list[col_num][char_type][row_num]
				if target != "#":
					self.var.set(self.var.get()[:-1]+target)
		except IndexError: #0文字の時エラー発生
			pass
	
	#override
	def destroy(self):
		super().destroy()
		del self
	
	@classmethod
	def char2index(cls,char_search):
		for col_num, col in enumerate(Keyboard.chr_list):
			for type_num, char_type in enumerate(col):
				for row_num, char in enumerate(char_type):
					if char_search == char:
						return col_num,type_num,row_num
		raise IndexError() #基本的にはないはず

Keyboard.class_init()

def ChildDelete(frame:ttk.Frame):
	for child in frame.winfo_children():
		child.destroy()

def FramesDelete(frames:list[ttk.Frame]):
	for frame in frames:
		ChildDelete(frame)
		frame.destroy()