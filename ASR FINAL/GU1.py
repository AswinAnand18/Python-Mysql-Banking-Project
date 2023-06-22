import qrcode
import pymysql
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from time import gmtime, strftime
from PIL import ImageTk,Image
con=pymysql.connect(host="localhost", user="root",password="#sankar@2005",database="sr")

def connect(name,pin,oc,admn):
   
    mycursor=con.cursor()
    mycursor.execute("use sr ")
    query="insert into FINAL2 (NAME1,PASSWORD1,CREDIT,ADNUM) values (%s,%s,%s,%s)"
    mycursor.execute(query,(name,pin,oc,admn))
    con.commit()
    con.close()
    
def is_number(s):
    try:
        float(s)
        return 1
    except ValueError:
        return 0

def check_acc_nmb(num):
	try:
		fpin=open(num+".txt",'r')
	except FileNotFoundError:
		messagebox.showinfo("Error","Invalid Credentials!\nTry Again!")
		return 0
	fpin.close()
	return 
def home_return(master):
	master.destroy()
	Main_Menu()

def write(master,name,oc,pin,admn,clas):
	
	if( (is_number(name)) or (is_number(oc)==0) or (is_number(pin)==0)or name==""):
		messagebox.showinfo("Error","Invalid Credentials\nPlease try again.")
		master.destroy()
		return 

	f1=open("Accnt_Record.txt",'r')
	accnt_no=int(f1.readline())
	accnt_no+=1
	f1.close()

	f1=open("Accnt_Record.txt",'w')
	f1.write(str(accnt_no))
	f1.close()
	connect(name,pin,oc,admn)
	fdet=open(str(accnt_no)+".txt","w")
	fdet.write(pin+"\n")
	fdet.write(oc+"\n")
	fdet.write(str(accnt_no)+"\n")
	fdet.write(name+"\n")
	fdet.write(admn+"\n")
	fdet.write(clas+"\n")
	fdet.close()
	data = open(str(accnt_no)+".txt","r+")
	a=data.readlines()
	b=a[0:3:2]
	qr = qrcode.QRCode(version = 2,box_size = 5,border = 1)
	qr.add_data(b)
	qr.make(fit = True)
	img = qr.make_image(fill_color = 'black',back_color = 'red')
	img.save(str(accnt_no)+'.png')


	frec=open(str(accnt_no)+"-Transaction History.txt",'w')
	frec.write("Date                             Credit                     Debit                        Balance\n")
	frec.write(str(strftime("[%Y-%m-%d]",gmtime()))+"                            "+oc+"                                                        "+oc+"\n")
	frec.close()
	
	messagebox.showinfo("Details","Your Account Number is:"+str(accnt_no))
	master.destroy()
	return

def crdt_write(master,amt,accnt,name):

	if(is_number(amt)==0):
		messagebox.showinfo("Error","Invalid Credentials\nPlease try again.")
		master.destroy()
		return 

	fdet=open(accnt+".txt",'r')
	pin=fdet.readline()
	camt=int(fdet.readline())
	fdet.close()
	amti=int(amt)
	cb=amti+camt
	fdet=open(accnt+".txt",'w')
	fdet.write(pin)
	fdet.write(str(cb)+"\n")
	fdet.write(accnt+"\n")
	fdet.write(name+"\n")
	fdet.close()
	frec=open(str(accnt)+"-Transaction History.txt",'a+')
	frec.write(str(strftime("[%Y-%m-%d] ",gmtime()))+"                           "+str(amti)+"                                                        "+str(cb)+"\n")
	frec.close()
	messagebox.showinfo("Operation Successfull!!","Amount Credited Successfully!!")
	master.destroy()
	return

def debit_write(master,amt,accnt,name):

	if(is_number(amt)==0):
		messagebox.showinfo("Error","Invalid Credentials\nPlease try again.")
		master.destroy()
		return 
			
	fdet=open(accnt+".txt",'r')
	pin=fdet.readline()
	camt=int(fdet.readline())
	fdet.close()
	if(int(amt)>camt):
		messagebox.showinfo("Error!!","You dont have that amount left in your account\nPlease try again.")
	else:
		amti=int(amt)
		cb=camt-amti
		fdet=open(accnt+".txt",'w')
		fdet.write(pin)
		fdet.write(str(cb)+"\n")
		fdet.write(accnt+"\n")
		fdet.write(name+"\n")
		fdet.close()
		frec=open(str(accnt)+"-Transaction History.txt",'a+')
		frec.write(str(strftime("[%Y-%m-%d]",gmtime()))+"     "+"                                                  "+str(amti)+"                             "+str(cb)+"\n")
		frec.close()
		messagebox.showinfo("Operation Successfull!!","Amount Debited Successfully!!")
		master.destroy()
		return

def Cr_Amt(accnt,name):
	creditwn=tk.Tk()
	creditwn.geometry("600x300")
	creditwn.title("Credit Amount")
	creditwn.configure(bg="blue")
	fr1=tk.Frame(creditwn,bg="blue")
	l_title=tk.Message(creditwn,text="Credit",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="black",justify="center",anchor="center")
	l_title.config(font=("Plagaurd","50","bold"))
	l_title.pack(side="top")
	l1=tk.Label(creditwn,relief="raised",text="Enter Amount to be credited: ")
	e1=tk.Entry(creditwn,relief="raised")
	l1.pack(side="top")
	e1.pack(side="top")
	b=tk.Button(creditwn,text="Credit",relief="raised",command=lambda:crdt_write(creditwn,e1.get(),accnt,name))
	b.pack(side="top")
	creditwn.bind("<Return>",lambda x:crdt_write(creditwn,e1.get(),accnt,name))


def De_Amt(accnt,name):
	debitwn=tk.Tk()
	debitwn.geometry("600x300")
	debitwn.title("Debit Amount")	
	debitwn.configure(bg="blue")
	fr1=tk.Frame(debitwn,bg="blue")
	l_title=tk.Message(debitwn,text="Debit",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="black",justify="center",anchor="center")
	l_title.config(font=("Plagaurd","50","bold"))
	l_title.pack(side="top")
	l1=tk.Label(debitwn,relief="raised",text="Enter Amount to be debited: ")
	e1=tk.Entry(debitwn,relief="raised")
	l1.pack(side="top")
	e1.pack(side="top")
	b=tk.Button(debitwn,text="Debit",relief="raised",command=lambda:debit_write(debitwn,e1.get(),accnt,name))
	b.pack(side="top")
	debitwn.bind("<Return>",lambda x:debit_write(debitwn,e1.get(),accnt,name))




def disp_bal(accnt):
	fdet=open(accnt+".txt",'r')
	fdet.readline()
	bal=fdet.readline()
	fdet.close()
	messagebox.showinfo("Balance",bal)




def disp_tr_hist(accnt):
	disp_wn=tk.Tk()
	disp_wn.geometry("900x600")
	disp_wn.title("Transaction History")
	disp_wn.configure(bg="blue")
	fr1=tk.Frame(disp_wn,bg="white")
	l_title=tk.Message(disp_wn,text="Transaction History",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="black",justify="center",anchor="center")
	l_title.config(font=("Ar Destine","50"))
	l_title.pack(side="top")
	fr1=tk.Frame(disp_wn)
	fr1.pack(side="top")
	l1=tk.Message(disp_wn,text="Your Transaction History:",padx=100,pady=20,width=1000,bg="white",fg="black",relief="raised")
	l1.pack(side="top")
	fr2=tk.Frame(disp_wn)
	fr2.pack(side="top")
	frec=open(accnt+"-Transaction History.txt",'r')
	for line in frec:
		l=tk.Message(disp_wn,anchor="w",text=line,relief="raised",width=2000)
		l.pack(side="top")
	b=tk.Button(disp_wn,text="Quit",relief="raised",command=disp_wn.destroy)
	b.pack(side="top")
	frec.close()

def logged_in_menu(accnt,name):
	rootwn=tk.Tk()
	rootwn.geometry("1900x900")
	rootwn.title("LOGIN-"+name)
	rootwn.configure(background='blue')
	fr1=tk.Frame(rootwn)
	fr1.pack(side="top")
	bg_image = tk.PhotoImage(file ="bgimage.png")
	x = tk.Label (image = bg_image)
	x.place(y=-100)
	l_title=tk.Message(rootwn,text="ASR\n CANTEEN CARD",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="black",justify="center",anchor="center")
	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side="top")
	label=tk.Label(text="Logged in as: "+name,relief="raised",bg="black",fg="white",anchor="center",justify="center",width=20,padx=20,pady=9)
	label.pack(side="top")
	img2=tk.PhotoImage(file="credit.gif")
	myimg2=img2.subsample(2,2)
	img3=tk.PhotoImage(file="debit.png")
	myimg3=img3.subsample(2,2)
	img4=tk.PhotoImage(file="balance1.gif")
	myimg4=img4.subsample(2,2)
	img5=tk.PhotoImage(file="transaction.gif")
	myimg5=img5.subsample(2,2)
	b2=tk.Button(image=myimg2,command=lambda: Cr_Amt(accnt,name))
	b2.image=myimg2
	b3=tk.Button(image=myimg3,command=lambda: De_Amt(accnt,name))
	b3.image=myimg3
	b4=tk.Button(image=myimg4,command=lambda: disp_bal(accnt))
	b4.image=myimg4
	b5=tk.Button(image=myimg5,command=lambda: disp_tr_hist(accnt))
	b5.image=myimg5
	
	img6=tk.PhotoImage(file="logout.png")
	myimg6=img6.subsample(2,2)
	b6=tk.Button(image=myimg6,relief="raised",command=lambda: logout(rootwn))
	b6.image=myimg6

	
	b2.place(x=1100,y=200)
	b3.place(x=1100,y=300)
	b4.place(x=1100,y=400)
	b5.place(x=1100,y=500)
	b6.place(x=1100,y=600)
	rootwn.mainloop()
	
def logout(master):
	
	messagebox.showinfo("Logged Out","You Have Been Successfully Logged Out!!")
	master.destroy()
	Main_Menu()

def check_log_in(master,name,acc_num,pin):
	if(check_acc_nmb(acc_num)==0):
		master.destroy()
		Main_Menu()
		return

	if( (is_number(name))  or (is_number(pin)==0) ):
		messagebox.showinfo("Error","Invalid Credentials\nPlease try again.")
		master.destroy()
		Main_Menu()
	else:
		master.destroy()
		logged_in_menu(acc_num,name)


def log_in(master):
	master.destroy()
	loginwn=tk.Tk()
	loginwn.geometry("1600x900")
	loginwn.title("Log in")
	loginwn.configure(bg="blue")
	fr1=tk.Frame(loginwn,bg="blue")
	bg_image = tk.PhotoImage(file ="loginim.png")
	x = tk.Label (image = bg_image)
	x.place(y=-1)
	l_title=tk.Message(loginwn,text="LOGIN",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="black",justify="center",anchor="center")
	l_title.config(font=("Ar Destine","50"))
	l_title.pack(side="top")
	l1=tk.Label(loginwn,width=20,text="Enter Name:",padx=20,pady=9,relief="raised")
	l1.place(x=520,y=250)
	l1.config(font=("Ar Destine","15"))
	e1=tk.Entry(loginwn,width=20,font=("Ar Destine","25"))
	e1.place(x=780,y=250)
	l2=tk.Label(loginwn,width=20,text="Enter account number:",padx=20,pady=10,relief="raised")
	l2.place(x=520,y=300)
	l2.config(font=("Ar Destine","15"))
	e2=tk.Entry(loginwn,width=20,font=("Ar Destine","25"))
	e2.place(x=780,y=300)
	l3=tk.Label(loginwn,width=20,text="Enter your PIN:",padx=20,pady=10,relief="raised")
	l3.place(x=520,y=350)
	l3.config(font=("Ar Destine","15"))
	e3=tk.Entry(loginwn,show="*",width=20,font=("Ar Destine","25"))
	e3.place(x=780,y=350)
	b=tk.Button(loginwn,text="Submit",command=lambda: check_log_in(loginwn,e1.get().strip(),e2.get().strip(),e3.get().strip()),width=20,font=("Ar Destine","15"))
	b.place(x=720,y=450)
	b1=tk.Button(text="HOME",relief="raised",bg="black",fg="white",command=lambda: home_return(loginwn),width=20,font=("Ar Destine","15"))
	b1.place(x=720,y=525)
	loginwn.bind("<Return>",lambda x:check_log_in(loginwn,e1.get().strip(),e2.get().strip(),e3.get().strip()))
	loginwn.mainloop()

def Create():
	
	crwn=tk.Tk()
	crwn.geometry("1900x900")
	crwn.title("Create Account")
	crwn.configure(bg="blue")
	l_title=tk.Message(crwn,text="CREATE ACCOUNT",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="black",justify="center",anchor="center")
	l_title.config(font=("Ar Destine","50"))
	l_title.pack(side="top")
	l1=tk.Label(crwn,text="Enter Name:",relief="raised",width=20,padx=20,pady=9)
	l1.place(x=520,y=150)
	l1.config(font=("Ar Destine","15"))
	e1=tk.Entry(crwn,width=20,font=("Ar Destine","25"))
	e1.place(x=780,y=150)
	l2=tk.Label(crwn,text="Enter opening credit:",relief="raised",width=20,padx=20,pady=9)
	l2.place(x=520,y=200)
	l2.config(font=("Ar Destine","15"))
	e2=tk.Entry(crwn,width=20,font=("Ar Destine","25"))
	e2.place(x=780,y=200)
	l3=tk.Label(crwn,text="Enter desired PIN:",relief="raised",width=20,padx=20,pady=9)
	l3.place(x=520,y=250)
	l3.config(font=("Ar Destine","15"))
	e3=tk.Entry(crwn,show="*",width=20,font=("Ar Destine","25"))
	e3.place(x=780,y=250)
	l4=tk.Label(crwn,text="Enter Admisson num:",relief="raised",width=20,padx=20,pady=9)
	l4.place(x=520,y=300)
	l4.config(font=("Ar Destine","15"))
	e4=tk.Entry(crwn,width=20,font=("Ar Destine","25"))
	e4.place(x=780,y=300)
	l5=tk.Label(crwn,text="Enter Class And Sec:",relief="raised",width=20,padx=20,pady=9)
	l5.place(x=520,y=350)
	l5.config(font=("Ar Destine","15"))
	e5=tk.Entry(crwn,width=20,font=("Ar Destine","25"))
	e5.place(x=780,y=350)
	b=tk.Button(crwn,text="Submit",command=lambda: write(crwn,e1.get().strip(),e2.get().strip(),e3.get().strip(),e4.get().strip(),e5.get().strip()),width=20,font=("Ar Destine","15"))
	b.place(x=720,y=460)
	crwn.bind("<Return>",lambda x:write(crwn,e1.get().strip(),e2.get().strip(),e3.get().strip(),e4.get().strip(),e5.get().strip()))
	crwn.mainloop()
	return
    

def Main_Menu():
	

	rootwn=tk.Tk()
	rootwn.geometry("1900x900")
	rootwn.title("LOGIN")
	rootwn.configure(background='blue')
	fr1=tk.Frame(rootwn)
	fr1.pack(side="top")
	bg_image = tk.PhotoImage(file ="pile1.gif")
	x = tk.Label (image = bg_image)
	x.place(y=-400)
	l_title=tk.Message(text="ASR\n CANTEEN CARD ",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="black",justify="center",anchor="center")
	l_title.config(font=("Ar Destine","50"))
	l_title.pack(side="top")
	imgc1=tk.PhotoImage(file="new.gif")
	imglo=tk.PhotoImage(file="login.gif")
	imgc=imgc1.subsample(2,2)
	imglog=imglo.subsample(2,2)

	b1=tk.Button(image=imgc,command=Create)
	b1.image=imgc
	b2=tk.Button(image=imglog,command=lambda: log_in(rootwn))
	b2.image=imglog
	img6=tk.PhotoImage(file="quit.png")
	myimg6=img6.subsample(2,2)

	b6=tk.Button(image=myimg6,command=rootwn.destroy)
	b6.image=myimg6
	b1.place(x=800,y=400)
	b2.place(x=800,y=300)	
	b6.place(x=920,y=500)
	rootwn.mainloop()
Main_Menu()
