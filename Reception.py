from PublicClass import *

class Reception(ttk.Frame):
	def __init__(self,root:tk.Tk):
		super().__init__(root,width=WINDOW_WIDTH,height=WINDOW_HEIGHT,relief="solid")
		
		self.client = ClientInfo()
		self.mem_bool_var = tk.BooleanVar()
		self.mem_num_var = tk.StringVar()
		self.name_var = tk.StringVar()
		self.reservation_var = tk.BooleanVar()
		self.subject_var = tk.StringVar()
		self.staff_var = tk.StringVar()
		self.reception_start()
		
	def client_reset(self):
		self.client.clear()
		self.mem_bool_var.set(False)
		self.mem_num_var.set("")
		self.name_var.set("")
		self.reservation_var.set(False)
		self.subject_var.set("")
		self.staff_var.set("")
	
	###画面1 : 受付開始，メンバーかどうか確認###
	def reception_start(self):
		self.mem_bool_var.set(False)
		put(widget=ttk.Label(self,text="受付開始",anchor=tk.CENTER,font=("Arial",40)),xy=(2,0),w=4,h=2)
		put(widget=ttk.Label(self,text="PCデポのメンバー様ですか?(優先受付いたします)",anchor=tk.CENTER),xy=(0,2),w=8)
		put(widget=SwitchButton(parent=self,function=self.fill_number,text="メンバー"),xy=(0,3),w=2,h=2)
		put(widget=SwitchButton(parent=self,function=self.check_member,text="わからない"),xy=(3,3),w=2,h=2)
		put(widget=SwitchButton(parent=self,function=self.fill_name,text="メンバーでない"),xy=(6,3),w=2,h=2)

	
	###画面1-1 : メンバー番号入力###
	def fill_number(self):
		self.mem_bool_var.set(True)
		put(ttk.Label(self,text="メンバー番号を入力してください(不明な場合はそのままで結構です)",anchor=tk.CENTER),xy=(0,0),w=4)
		put(ttk.Label(self,textvariable=self.mem_num_var),xy=(2,1),w=4)
		put(SwitchButton(parent=self,function=self.fill_name,text="決定"),xy=(5,1))
		put(SwitchButton(parent=self,function=self.reception_start,text="戻る"),xy=(6,1))
		put(NumberKey(parent=self,strvar=self.mem_num_var,maxlen=8),xy=(0,2),w=8,h=3)
	
	###画面1-2 : メンバーかどうかわからない###
	def check_member(self):
		put(ttk.Label(self,text="こちらのカウンターはPCデポという会社が運営しております。",anchor=tk.CENTER),xy=(0,0),w=8)
		put(ttk.Label(self,text="PCデポでは月額のメンバーシップ会員のお客様を優先して受付を行なっております。",anchor=tk.CENTER),xy=(0,1),w=8)
		put(SwitchButton(parent=self,function=self.reception_start,text="戻る"),xy=(0,3),w=2,h=2)
	
	###画面2 : 名前入力###
	def fill_name(self):
		put(ttk.Label(self,text="お名前を入力してください",anchor=tk.CENTER),xy=(0,0),w=8)
		put(ttk.Label(self,textvariable=self.name_var),xy=(0,1),w=4)
		put(ttk.Label(self,text="様"),xy=(4,1))
		put(SwitchButton(parent=self,function=self.select_subject,text="決定"),xy=(6,1))
		put(SwitchButton(parent=self,function=self.reception_start,text="戻る"),xy=(7,1))
		put(Keyboard(parent=self,var=self.name_var),xy=(0,2),w=8,h=3)
	
	###画面3 : 用件確認###
	def select_subject(self):
		put(ttk.Label(self,text="本日はいかがなさいましたか?",anchor=tk.CENTER),xy=(2,0),w=4,h=2)
		put(ttk.Combobox(self,textvariable=self.subject_var,values=ClientInfo.subject_list),xy=(2,3),w=4)
		put(SwitchButton(self,function=self.reservation_check,text="決定"),xy=(6,2),w=2,h=2)
		
	###画面4 : 予約確認###
	def reservation_check(self):
		self.reservation_var.set(False)
		put(ttk.Label(self,text="本日のご来店に際しまして，事前にお時間のご予約はございますか?",anchor=tk.CENTER),xy=(0,0),w=8)
		put(SwitchButton(parent=self,function=self.select_subject,text="戻る"),xy=(0,3),w=2,h=2)
		put(SwitchButton(parent=self,function=self.resevation_set,text="はい"),xy=(3,3),w=2,h=2)
		put(SwitchButton(parent=self,function=self.before_staff,text="いいえ"),xy=(6,3),w=2,h=2)
	
	def resevation_set(self): #予約あったときに記録するだけ
		self.reservation_var.set(True)
		self.before_staff()
	
	def before_staff(self): #担当スタッフ確認はメンバー限定
		if self.mem_bool_var.get(): self.staff_check()
		else: self.data_confirmation() #メンバーじゃなければ画面5とばして画面6へ
	
	###画面5 : 担当スタッフ確認###
	def staff_check(self):
		put(ttk.Label(self,text="当店で担当のスタッフはいらっしゃいますか?",anchor=tk.CENTER),xy=(0,0),w=8)
		put(SwitchButton(parent=self,function=self.reservation_check,text="戻る"),xy=(0,3),w=2,h=2)
		put(SwitchButton(parent=self,function=self.data_confirmation,text="決定"),xy=(6,3),w=2,h=2)

	###画面6 : 入力情報確認###
	def data_confirmation(self,error_massages=[]):
		put(ttk.Label(self,text="入力内容をご確認ください",anchor=tk.CENTER),xy=(0,0),w=8)
		label_text = ""
		label_text += "会員番号    : " + (self.mem_num_var.get() if self.mem_bool_var.get() else "--------") + "\n"
		label_text += "お名前　    : " + self.name_var.get() + "様\n"
		label_text += "内容　　    : " + self.subject_var.get() + "\n"
		label_text += "ご予約　    : " + ("あり" if self.reservation_var.get() else "なし") + "\n"
		label_text += "担当スタッフ : " + (self.staff_var.get()) + "\n"
		for error_massage in error_massages:
			label_text += error_massage + "\n"
		put(ttk.Label(self,text=label_text),xy=(3,1),w=2,h=2)
		put(SwitchButton(parent=self,function=self.staff_check,text="戻る"),xy=(0,3),w=2,h=2)
		put(SwitchButton(parent=self,function=self.data_conversion,text="決定"),xy=(6,3),w=2,h=2)
	
	def data_conversion(self): #入力内容をClientInfo型に変換
		error_messages = []
		client = ClientInfo()
		client.member_num = int(self.mem_num_var.get()) if self.mem_bool_var.get() else 0
		if self.name_var.get() == "": error_messages.append("お名前が入力されていません。")
		else: client.name = self.name_var.get()
		client.reservation = self.reservation_var.get()
		if self.subject_var.get() == "": error_messages.append("ご用件が選択されていません。")
		else: client.subject = self.subject_var.get()
		client.staff = self.staff_var.get()

		if error_messages: #データの不備あり
			self.data_confirmation(error_massages=error_messages)
			return
		
		client.registration()

	
	def clear_frame(self):
		for child in self.winfo_children():
			child.destroy()
		
class SwitchButton(ttk.Button): #画面遷移を行うボタン
	def __init__(self,parent:Reception,function,text:str): #フレームと実行関数を渡す
		self.parent = parent
		self.function = function
		super().__init__(parent,text=text,command=self.pushed)
	
	def pushed(self):
		self.parent.clear_frame()
		self.function()
		del self
	
	#override
	def destroy(self):
		super().destroy()
		del self

CELL_WIDTH = WINDOW_WIDTH//8
CELL_HEIGHT = WINDOW_HEIGHT//5
def put(widget:ttk.Widget,xy:tuple[int,int],w=1,h=1):
	widget.place(x=(xy[0]+w/2)*CELL_WIDTH,y=(xy[1]+h/2)*CELL_HEIGHT,width=w*CELL_WIDTH,height=h*CELL_HEIGHT,anchor=tk.CENTER)