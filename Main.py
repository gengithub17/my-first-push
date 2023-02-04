from PublicClass import *
from Reception import Reception
from Staff import Staff

class Root(tk.Tk):
	def __init__(self):
		super().__init__()
		self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
		self.title("タッチで操作してください")

		Reception(self).pack()

class SubRoot(tk.Toplevel):
	def __init__(self):
		super().__init__()
		self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
		self.title("スタッフ管理画面")
		Staff(self).pack()

test_client = ClientInfo(member_num=0,name="ハマダ",subject="操作説明，ご相談")
test2_client = ClientInfo(member_num=16002222,name="ニシノ",subject="定期点検(プレミアムメンバー様限定)")

if __name__ == "__main__":
	try:
		create_table()
		root = Root()
		test_client.registration()
		test2_client.registration()

		subroot = SubRoot()
		root.mainloop()
	finally:
		remove_table()

