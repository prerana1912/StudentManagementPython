from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import pandas as pd #python library to analyze data
import matplotlib.pyplot as plt
import requests #to make HTTP requests to any API in the world
import json #sorting and transfering data between browser and the server 
import bs4


##################################### create database and table #####################################
con = None
try:
	con = connect("StudentDataBase.db")
	#print("connected")
	sql="create table if not exists SMS(rno int primary key,name text,marks int)"
	cursor = con.cursor()
	cursor.execute(sql)
	#print("Table created")
except Exception as e:
	print("Issue ",e)
finally:
	if con is not None:
		con.close()
		#print("Disconnected")

############################################ Functions ############################################

######################### add ######################### 
def add(): 
	root.withdraw()        # hide root 
	add_st.deiconify()     # visible add_st
			
def addback():
	add_st.withdraw()      # hide add_st
	root.deiconify()       # visible root

def addsave():
	con=None
	try:
		con = connect("StudentDataBase.db")
		rno = int(add_st_entrno.get())
		name=add_st_entrname.get()
		marks=int(add_st_entrmarks.get())

		cursor=con.cursor()
		if rno <= 0:
			showerror('Invalid','Please enter valid roll number')
			con.rollback()
		elif rno == "" :
			showerror('Invalid','rno cannot be empty')
			con.rollback()	
		elif name == ""  :
			showerror('Invalid','Please enter valid Name')
			con.rollback()
		elif (not name.strip().isalpha()):
			showerror('Invalid','Please enter valid Name')
			con.rollback()
		elif len(name) <2 :
			showerror('Invalid','Please enter valid name')
			con.rollback()
		elif marks== '' :
			showerror('Invalid','Please enter valid marks')
			con.rollback()
		elif (marks<0 or marks > 100) :
			showerror('Invalid','Please enter valid marks')
			con.rollback()
		else:

			sql="insert into SMS values('%d','%s','%d')"
			values=(rno,name,marks)
			cursor.execute(sql % values)
			con.commit()
			msg=str(cursor.rowcount)+ " record inserted "
			showinfo("Added ",msg)
			add_st_entrno.delete(0,END) # delete all text in widget
			add_st_entrname.delete(0,END)
			add_st_entrmarks.delete(0,END)
			add_st_entrno.focus()
	
	except IntegrityError:
		con.rollback()
		showerror("Invalid ","No duplicate data")
	
	except ValueError as e :
		con.rollback() 
		showerror("Invalid ","Enter all the valid details and then click save")

	except Error as error:
        	showerror("Failed to add reocord in sqlite table", e)
	finally:
		if con is not None:
			con.close()

######################### view ######################### 

def view():
	root.withdraw()        # hide root
	view_st.deiconify()    # visible view_st
	view_st_data.delete(1.0,END) 
	con=None
	try:
		con = connect("StudentDataBase.db")
		sql = "select * from SMS"
		cursor = con.cursor()
		cursor.execute(sql)
		data = cursor.fetchall()
		info=""
		for d in data:
			info = info +"rno=" +str(d[0])+",Name="+str(d[1]) + ",Marks="+str(d[2])+"\n"
		view_st_data.insert(INSERT,info)
	except Exception as e :
		showerror("issue ")
	except Error as e:
        	showerror("Failed to view reocord from a sqlite table", e)
	finally:
		if con is not None:
			con.close()

def viewback():   
	view_st.withdraw()    # hide view_st
	root.deiconify()      # visible root

######################### update ######################### 
def up():  
	root.withdraw()
	Update_st.deiconify()
	
def upsave():
	con=None
	try:
		con = connect("StudentDataBase.db")
		rno = int(Update_st_entrno.get())
		name=Update_st_entrname.get()
		marks=int(Update_st_entrmarks.get())

		cursor=con.cursor()
		if (rno <= 0):
			showerror('Invalid','Please enter valid roll number')
			con.rollback()
		
		elif rno == '' :
			showerror('Invalid','Please enter valid roll number')
			con.rollback()	
		elif name == ""  :
			showerror('Invalid','Please enter valid Name')
			con.rollback()
		elif (not name.strip().isalpha()):
			showerror('Invalid','Please enter valid Name')
			con.rollback()
				
		elif len(name) <2 :
			showerror('Invalid','Please enter valid name')
			con.rollback()
		elif marks== '' :
			showerror('Invalid','Please enter valid marks')
			con.rollback()
		
		elif (marks<0 or marks > 100) :
			showerror('Invalid','Please enter valid marks')
			con.rollback()
		else:

			sql="update SMS set name='%s',marks='%d' where rno='%d'"
			args=(name,marks,rno)
			cursor.execute(sql % args)
			con.commit()
			if (cursor.rowcount==0):
				showerror('Invalid','Roll number not found for update , please check roll number..')
				con.rollback()
			else:
				msg=str(cursor.rowcount)+ " record updated "
				showinfo("Successful ",msg)
				Update_st_entrno.delete(0,END)
				Update_st_entrname.delete(0,END)
				Update_st_entrmarks.delete(0,END)
				

	
	except IntegrityError:
		con.rollback()
		showerror("Invalid ","No duplicate data")
	
	except ValueError as e :
		con.rollback() 
		showerror("Invalid ","Enter all the valid details and then click save")

	except Error as e:
        	showerror("Failed to view reocord from a sqlite table", e)
	finally:
		if con is not None:
			con.close()


def upback():
	Update_st.withdraw()
	root.deiconify()

######################### delete ######################### 
def dele():   
	root.withdraw()
	delete_st.deiconify()

def deleback():
	delete_st.withdraw()
	root.deiconify()

def delesave():
	con=None
	try:
		con = connect("StudentDataBase.db")
		cursor=con.cursor()	
		drno=int(delete_st_entrno.get())
		if drno < 0:
			showerror('Invalid','Please enter Valid Roll Number ')
			con.rollback()
		else :
			sql = """DELETE FROM SMS WHERE rno = ?"""
			cursor.execute(sql,(drno,))
			con.commit()
			if (cursor.rowcount==0):
				showerror('Invalid','Roll Number not found')
				con.rollback()
			else:
				msg=str(cursor.rowcount)+ " record deleted "
				showinfo("Deleted","Record deleted successfully")
				delete_st_entrno.delete(0,END)
				
			cursor.close()
	except ValueError as e :
		con.rollback() 
		showerror('Invalid ','Enter all the valid details and then click save')

	except Error as e:
        	showerror("Failed to delete reocord from a sqlite table", e)
	finally:
		if con is not None:
			con.close()	

######################### chart ######################### 
def chart():
	 
	connection=connect("StudentDataBase.db")

	df=pd.read_sql(sql="select * from SMS",con=connection)
	df.to_csv("stu_details.csv",index=False)



	########## Chart #############
	data = pd.read_csv("stu_details.csv")# making data frame from csv file
	name=data['name'].tolist()#array into list
	marks=data['marks'].tolist()
	plt.bar(name,marks,width=0.25,color='skyblue',label='marks')

	plt.xlabel("Name of Students")
	plt.ylabel("Marks of Students")
	plt.title("Progress Report")
	#plt.grid()
	plt.legend(shadow=True)
	#plt.savefig("Progress_report_in_pdf.pdf")
	#plt.savefig("Progress_report_in_PNG.png")

	plt.show()



############################################ root ############################################
root = Tk()
root.title(" S.M.S. ")
root.geometry("1080x600+150+50") #(widthxheight+x+y)
root.configure(bg='RosyBrown1')


btnAdd = Button(root,text="ADD",width=10,font=('arial',18,'bold'), command = add)
btnView = Button(root,text="VIEW",width=10,font=('arial',18,'bold'), command = view)
btnUpdate = Button(root,text="UPDATE",width=10,font=('arial',18,'bold'), command = up)
btnDelete = Button(root,text="DELETE",width=10,font=('arial',18,'bold'), command = dele)
btnCharts = Button(root,text="CHARTS",width=10,font=('arial',18,'bold'),command = chart)

######## Location ###########

try:
	web_address1 = "https://ipinfo.io/"
	res = requests.get(web_address1)
	data = res.json()
	city_name = data['city']
	

# for temperature

	a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
	a2 = "&q=" + city_name
	a3 = "&appid=c6e315d09197cec231495138183954bd"
	web_address = a1 + a2 + a3
	res = requests.get(web_address)
	
	datatemp = res.json()
	
	m=datatemp['main']
	t=round(m['temp'])
	

except Exception as e:
	showerror("issue ",e)

####Location Label
degree_sign = u"\N{DEGREE SIGN}"
lblLocation=Label(root,text=" Location : "+city_name+"\t\t\t\t\t\t"+"Temperature : "+str(t)+degree_sign+" C",font=('arial',18,'bold'),bg='RosyBrown1')

##### for Quote of the day

try: 
	# get the html
	get_html="https://www.brainyquote.com/quote_of_the_day"
	res = requests.get(get_html)
	
	# parse the HTML
	data = bs4.BeautifulSoup(res.text, "html.parser")
	##print(data)

	#html tree traversal
	info = data.find('img',{"class":"p-qotd"})
	##print(info)
	quote = info['alt']
	
except Exception as e:
	showerror("Issue  ",e)

##### QOD label

lblQOD=Label(root,text="QOD : "+quote,font=('arial',18,'bold'),bg='RosyBrown1')


btnAdd.pack(pady=20)
btnView.pack(pady=20)
btnUpdate.pack(pady=20)
btnDelete.pack(pady=20)
btnCharts.pack(pady=20)
lblLocation.pack(side="left")
lblQOD.place(relx = 0.0,rely = 1.0,anchor ='sw')
#lblQOD.place(x=0,y=600)

############################################ add_st ############################################
add_st = Toplevel(root)
add_st.title(" Add Stu. ")
add_st.geometry("500x600+400+50")
add_st.configure(bg='light blue')

add_st_lblrno = Label(add_st,text="Enter rno",width=10,font=('arial',18,'bold'), bg="light blue")
add_st_entrno = Entry(add_st,bd=5,width=10,font=('arial',18,'bold'))

add_st_lblname = Label(add_st,text="Enter name",width=10,font=('arial',18,'bold'), bg = "light blue")
add_st_entrname = Entry(add_st,bd=5,width=10,font=('arial',18,'bold'))

add_st_lblmarks = Label(add_st,text="Enter marks",width=10,font=('arial',18,'bold'), bg = "light blue")
add_st_entrmarks = Entry(add_st,bd=5,width=10,font=('arial',18,'bold'))

add_st_btnsave =Button(add_st,text="SAVE",width=10,font=('arial',18,'bold'),command=addsave)
add_st_btnback = Button(add_st,text="BACK",width=10,font=('arial',18,'bold'),command=addback)


add_st_lblrno.pack(pady=10)
add_st_entrno.pack(pady=10)

add_st_lblname.pack(pady=10)
add_st_entrname.pack(pady=10)

add_st_lblmarks.pack(pady=10)
add_st_entrmarks.pack(pady=10)

add_st_btnsave.pack(pady=10)
add_st_btnback.pack(pady=10)

add_st.withdraw()                 # hide add_st

############################################ view_st ############################################
view_st = Toplevel(root)
view_st.title(" View Stu. ")
view_st.geometry("500x600+400+50")
view_st.configure(bg='light goldenrod')

view_st_data = ScrolledText(view_st,width=28,height=10,font=('arial',18,'bold'),bg='light goldenrod')
view_st_btnback=Button(view_st,text="BACK",font=('arial',18,'bold'),command = viewback)
view_st_data.pack(pady=10)
view_st_btnback.pack(pady=10)

view_st.withdraw()                   # hide view_st

############################################ Update_st ############################################

Update_st = Toplevel(root)
Update_st.title(" Update Stu. ")
Update_st.geometry("500x600+400+50")
Update_st.configure(bg='peach puff')

Update_st_lblrno = Label(Update_st,text="Enter rno",width=10,font=('arial',18,'bold'), bg = "peach puff")
Update_st_entrno = Entry(Update_st,bd=5,width=20,font=('arial',18,'bold'))

Update_st_lblname = Label(Update_st,text="Enter name",width=10,font=('arial',18,'bold'), bg = "peach puff")
Update_st_entrname = Entry(Update_st,bd=5,width=20,font=('arial',18,'bold'))

Update_st_lblmarks = Label(Update_st,text="Enter marks",width=10,font=('arial',18,'bold'), bg = "peach puff")
Update_st_entrmarks = Entry(Update_st,bd=5,width=20,font=('arial',18,'bold'))
Update_st_btnsave =Button(Update_st,text="SAVE",width=10,font=('arial',18,'bold'),command=upsave)
Update_st_btnback = Button(Update_st,text="BACK",width=10,font=('arial',18,'bold'),command=upback)


Update_st_lblrno.pack(pady=10)
Update_st_entrno.pack(pady=10)
Update_st_lblname.pack(pady=10)
Update_st_entrname.pack(pady=10)
Update_st_lblmarks.pack(pady=10)
Update_st_entrmarks.pack(pady=10)
Update_st_btnsave.pack(pady=10)
Update_st_btnback.pack(pady=10)

Update_st.withdraw()

############################################ delete_st ############################################
		
delete_st = Toplevel(root)
delete_st.title("Delete Stu. ")
delete_st.geometry("500x600+400+50")
delete_st.configure(bg='cornflower blue')

delete_st_lblrno = Label(delete_st,text="Enter rno",width=10,font=('arial',18,'bold'), bg = "cornflower blue")
delete_st_entrno = Entry(delete_st,bd=5,width=20,font=('arial',18,'bold'))

delete_st_btnsave =Button(delete_st,text="SAVE",width=10,font=('arial',18,'bold'),command=delesave)
delete_st_btnback = Button(delete_st,text="BACK",width=10,font=('arial',18,'bold'),command=deleback)

delete_st_lblrno.pack(pady=10)
delete_st_entrno.pack(pady=10)

delete_st_btnsave.pack(pady=40)
delete_st_btnback.pack(pady=10)

delete_st.withdraw()


root.mainloop()

############################################ End ############################################