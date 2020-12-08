######## A Healthcare Domain Chatbot to simulate the predictions of a General Physician ########
######## A pragmatic Approach for Diagnosis ############

# Importing the libraries
import tkinter
from tkinter import *
from tkinter import messagebox
import os
import webbrowser

import numpy as np
import pandas as pd


class HyperlinkManager:

    def __init__(self, text):

        self.text = text

        self.text.tag_config("hyper", foreground="blue", underline=1)

        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)

        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return

# Importing the dataset
training_dataset = pd.read_csv('Training.csv')
test_dataset = pd.read_csv('Testing.csv')

# Slicing and Dicing the dataset to separate features from predictions
X = training_dataset.iloc[:, 0:132].values
Y = training_dataset.iloc[:, -1].values

# Dimensionality Reduction for removing redundancies
dimensionality_reduction = training_dataset.groupby(training_dataset['prognosis']).max()

# Encoding String values to integer constants
from sklearn.preprocessing import LabelEncoder
labelencoder = LabelEncoder()
y = labelencoder.fit_transform(Y)

# Splitting the dataset into training set and test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

# Implementing the Decision Tree Classifier
from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier()
classifier.fit(X_train, y_train)

# Saving the information of columns
cols     = training_dataset.columns
cols     = cols[:-1]


# Checking the Important features
importances = classifier.feature_importances_
indices = np.argsort(importances)[::-1]
features = cols

# Implementing the Visual Tree
from sklearn.tree import _tree

# Method to simulate the working of a Chatbot by extracting and formulating questions
def print_disease(node):
        #print(node)
        node = node[0]
        #print(len(node))
        val  = node.nonzero()
        #print(val)
        disease = labelencoder.inverse_transform(val[0])
        return disease
def recurse(node, depth):
            global val,ans
            global tree_,feature_name,symptoms_present
            indent = "  " * depth
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                yield name + " ?"
#                ans = input()
                ans = ans.lower()
                if ans == 'yes':
                    val = 1
                else:
                    val = 0
                if  val <= threshold:
                    yield from recurse(tree_.children_left[node], depth + 1)
                else:
                    symptoms_present.append(name)
                    yield from recurse(tree_.children_right[node], depth + 1)
            else:
                strData=""
                present_disease = print_disease(tree_.value[node])
#                print( "You may have " +  present_disease )
#                print()
                strData="You may have :" +  str(present_disease)

                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')

                red_cols = dimensionality_reduction.columns
                symptoms_given = red_cols[dimensionality_reduction.loc[present_disease].values[0].nonzero()]
#                print("symptoms present  " + str(list(symptoms_present)))
#                print()
                strData="symptoms present:  " + str(list(symptoms_present))
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')
#                print("symptoms given "  +  str(list(symptoms_given)) )
#                print()
                strData="symptoms given: "  +  str(list(symptoms_given))
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')
                confidence_level = (1.0*len(symptoms_present))/len(symptoms_given)
#                print("confidence level is " + str(confidence_level))
#                print()
                strData="confidence level is: " + str(confidence_level)
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')
#                print('The model suggests:')
#                print()
                strData='The model suggests:'
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')
                row = doctors[doctors['disease'] == present_disease[0]]
#                print('Consult ', str(row['name'].values))
#                print()
                strData='Consult '+ str(row['name'].values)
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')
#                print('Visit ', str(row['link'].values))
                #print(present_disease[0])
                hyperlink = HyperlinkManager(QuestionDigonosis.objRef.txtDigonosis)
                strData='Visit '+ str(row['link'].values[0])
                def click1():
                    webbrowser.open_new(str(row['link'].values[0]))
                QuestionDigonosis.objRef.txtDigonosis.insert(INSERT, strData, hyperlink.add(click1))
                #QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')
                yield strData

def tree_to_code(tree, feature_names):
        global tree_,feature_name,symptoms_present
        tree_ = tree.tree_
        #print(tree_)
        feature_name = [
            feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]
        #print("def tree({}):".format(", ".join(feature_names)))
        symptoms_present = []
#        recurse(0, 1)


def execute_bot():
#    print("Please reply with yes/Yes or no/No for the following symptoms")
    tree_to_code(classifier,cols)



# This section of code to be run after scraping the data

doc_dataset = pd.read_csv('doctors_dataset.csv', names = ['Name', 'Description'])


diseases = dimensionality_reduction.index
diseases = pd.DataFrame(diseases)

doctors = pd.DataFrame()
doctors['name'] = np.nan
doctors['link'] = np.nan
doctors['disease'] = np.nan

doctors['disease'] = diseases['prognosis']


doctors['name'] = doc_dataset['Name']
doctors['link'] = doc_dataset['Description']

record = doctors[doctors['disease'] == 'AIDS']
record['name']
record['link']




# Execute the bot and see it in Action
#execute_bot()


class QuestionDigonosis(Frame):
    objIter=None
    objRef=None
    def __init__(self,master=None):
        # master.title("Question")
        # root.iconbitmap("")
        # master.state("z")
#        master.minsize(700,350)
        QuestionDigonosis.objRef=self
        super().__init__(master=master)
        self["bg"]="light blue"
        # self.createWidget()
        self.iterObj=None

    def createWidget(self,main_frame,w,h):
        main_frame.pack(pady=int(h * .05),padx=int(w * .20))

        lbl_frame = Label(main_frame, bg='azure')
        lbl_frame.pack(fill='both', expand=True)
        lbl_header = Label(lbl_frame, bg='azure', text="Medicity ChatBot Form", width=30,
                                   font=("Times New Roman", 20, "bold"))
        lbl_header.grid(row=0, column=0, columnspan=2, pady=2)
        lbl_des = Label(lbl_frame, bg='azure', text="Here you have to provide your symptoms.",
                           font=("Times New Roman", 14, "bold"))
        lbl_des.grid(row=1, column=0, columnspan=2, pady=2)
        lbl_des2 = Label(lbl_frame, bg='azure',
                       text="Our system will suggest you  the disease and doctor also.",
                       font=("Times New Roman", 14, "bold"))
        lbl_des2.grid(row=2, column=0, columnspan=2, pady=2)
        lbl_des3 = Label(lbl_frame, bg='azure',
                         text="You can start by click on Start Button.",
                         font=("Times New Roman", 18, "bold"))
        lbl_des3.grid(row=3, column=0, columnspan=2, pady=2)
        lbl_des4 = Label(lbl_frame, bg='azure',
                         text="And provide answers on click on YES and NO button.",
                         font=("Times New Roman", 14, "bold"))
        lbl_des4.grid(row=4, column=0, columnspan=2, pady=2)


        self.lblQuestion=Label(lbl_frame,text="Question",font=("Times New Roman", 12, "bold"))
        self.lblQuestion.grid(row=5,column=0,columnspan=2,sticky="w")

        # self.varQuestion=StringVar()
        self.txtQuestion = Text(lbl_frame, width=100, height=4,font=("Times New Roman", 12, "bold"))
        self.txtQuestion.grid(row=6, column=0, rowspan=4, columnspan=2,sticky="w")

        self.lblDigonosis = Label(lbl_frame, text="Prognosis",font=("Times New Roman", 12, "bold"))
        self.lblDigonosis.grid(row=10, column=0,sticky="w",pady=2)



        self.varDiagonosis=StringVar()
        self.txtDigonosis =Text(lbl_frame, width=100,height=10,font=("Times New Roman", 12, "bold"))
        self.txtDigonosis.grid(row=11, column=0,columnspan=2,rowspan=10,pady=2,sticky="w")

        self.btnNo=Button(lbl_frame,text="No",width=16,font=("Times New Roman", 12, "bold"), command=self.btnNo_Click)
        self.btnNo.grid(row=22,column=0,sticky='w')
        self.btnYes = Button(lbl_frame, text="Yes",width=16,font=("Times New Roman", 12, "bold"), command=self.btnYes_Click)
        self.btnYes.grid(row=22, column=1,sticky="e")

        self.btnStart = Button(lbl_frame, text="Start", width=16,font=("Times New Roman", 12, "bold"), command=self.btnStart_Click)
        self.btnStart.grid(row=23, column=0, sticky="w")
        self.btnClear = Button(lbl_frame, text="Clear",width=16,font=("Times New Roman", 12, "bold"), command=self.btnClear_Click)
        self.btnClear.grid(row=23, column=1,sticky='e')

    # def createWidget(self):
    #     self.lblQuestion=Label(self,text="Question",width=12,bg="bisque")
    #     self.lblQuestion.grid(row=0,column=0,rowspan=4)
    #
    #     self.lblDigonosis = Label(self, text="Digonosis",width=12,bg="bisque")
    #     self.lblDigonosis.grid(row=4, column=0,sticky="n",pady=5)
    #
    #     # self.varQuestion=StringVar()
    #     self.txtQuestion = Text(self, width=100,height=4)
    #     self.txtQuestion.grid(row=0, column=1,rowspan=4,columnspan=20)
    #
    #     self.varDiagonosis=StringVar()
    #     self.txtDigonosis =Text(self, width=100,height=14)
    #     self.txtDigonosis.grid(row=4, column=1,columnspan=20,rowspan=20,pady=5)
    #
    #     self.btnNo=Button(self,text="No",width=12,bg="bisque", command=self.btnNo_Click)
    #     self.btnNo.grid(row=25,column=0)
    #     self.btnYes = Button(self, text="Yes",width=12,bg="bisque", command=self.btnYes_Click)
    #     self.btnYes.grid(row=25, column=1,columnspan=20,sticky="e")
    #
    #     self.btnClear = Button(self, text="Clear",width=12,bg="bisque", command=self.btnClear_Click)
    #     self.btnClear.grid(row=27, column=0)
    #     self.btnStart = Button(self, text="Start",width=12,bg="bisque", command=self.btnStart_Click)
    #     self.btnStart.grid(row=27, column=1,columnspan=20,sticky="e")
    def btnNo_Click(self):
        global val,ans
        global val,ans
        ans='no'
        str1=QuestionDigonosis.objIter.__next__()
        self.txtQuestion.delete(0.0,END)
        self.txtQuestion.insert(END,str1+"\n")

    def btnYes_Click(self):
        global val,ans
        ans='yes'
        self.txtDigonosis.delete(0.0,END)
        str1=QuestionDigonosis.objIter.__next__()

#        self.txtDigonosis.insert(END,str1+"\n")

    def btnClear_Click(self):
        self.txtDigonosis.delete(0.0,END)
        self.txtQuestion.delete(0.0,END)
    def btnStart_Click(self):
        execute_bot()
        self.txtDigonosis.delete(0.0,END)
        self.txtQuestion.delete(0.0,END)
        self.txtDigonosis.insert(END,"Please Click on Yes or No for the Above symptoms in Question")
        QuestionDigonosis.objIter=recurse(0, 1)
        str1=QuestionDigonosis.objIter.__next__()
        self.txtQuestion.insert(END,str1+"\n")


class MainForm(Frame):
    main_Root = None
    def destroyPackWidget(self, parent):
        for e in parent.pack_slaves():
            e.destroy()
    def __init__(self, master=None):
        MainForm.main_Root = master
        super().__init__(master=master)
        master.geometry("300x250")
        master.title("Account Login")
        self.createWidget()
    def createWidget(self):
        self.lblMsg=Label(self, text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13))
        self.lblMsg.pack()
        self.btnLogin=Button(self, text="Login", height="2", width="30", command=self.lblLogin_Click)
        self.btnLogin.pack()
        self.btnRegister=Button(self, text="Register", height="2", width="30", command=self.btnRegister_Click)
        self.btnRegister.pack()
    def lblLogin_Click(self):
        self.destroyPackWidget(MainForm.main_Root)
        frmLogin=Login(MainForm.main_Root)
        frmLogin.pack()
    def btnRegister_Click(self):
        self.destroyPackWidget(MainForm.main_Root)
        frmSignUp = SignUp(MainForm.main_Root)
        frmSignUp.pack()
class Login(Frame):
    main_Root=None
    def destroyPackWidget(self,parent):
        for e in parent.pack_slaves():
            e.destroy()
    def __init__(self, master=None):
        Login.main_Root=master
        super().__init__(master=master)
        master.title("Login")
        master.geometry("300x250")
        self.createWidget()
    def createWidget(self):
        self.lblMsg=Label(self, text="Please enter details below to login",bg="blue")
        self.lblMsg.pack()
        self.username=Label(self, text="Username * ")
        self.username.pack()
        self.username_verify = StringVar()
        self.username_login_entry = Entry(self, textvariable=self.username_verify)
        self.username_login_entry.pack()
        self.password=Label(self, text="Password * ")
        self.password.pack()
        self.password_verify = StringVar()
        self.password_login_entry = Entry(self, textvariable=self.password_verify, show='*')
        self.password_login_entry.pack()
        self.btnLogin=Button(self, text="Login", width=10, height=1, command=self.btnLogin_Click)
        self.btnLogin.pack()
    def btnLogin_Click(self):
        username1 = self.username_login_entry.get()
        password1 = self.password_login_entry.get()
#        messagebox.showinfo("Failure", self.username1+":"+password1)
        list_of_files = os.listdir()
        if username1 in list_of_files:
            file1 = open(username1, "r")
            verify = file1.read().splitlines()
            if password1 in verify:
                messagebox.showinfo("Sucess","Login Sucessful")
                self.destroyPackWidget(Login.main_Root)
                frmQuestion = QuestionDigonosis(Login.main_Root)
                frmQuestion.pack()
            else:
                messagebox.showinfo("Failure", "Login Details are wrong try again")
        else:
            messagebox.showinfo("Failure", "User not found try from another user\n or sign up for new user")
class SignUp(Frame):
    main_Root=None
    def destroyPackWidget(self,parent):
        for e in parent.pack_slaves():
            e.destroy()
    def __init__(self, master=None):
        SignUp.main_Root=master
        master.title("Register")
        super().__init__(master=master)
        master.title("Register")
        master.geometry("300x250")
        self.createWidget()
    def createWidget(self):
        self.lblMsg=Label(self, text="Please enter details below", bg="blue")
        self.lblMsg.pack()
        self.username_lable = Label(self, text="Username * ")
        self.username_lable.pack()
        self.username = StringVar()
        self.username_entry = Entry(self, textvariable=self.username)
        self.username_entry.pack()

        self.password_lable = Label(self, text="Password * ")
        self.password_lable.pack()
        self.password = StringVar()
        self.password_entry = Entry(self, textvariable=self.password, show='*')
        self.password_entry.pack()
        self.btnRegister=Button(self, text="Register", width=10, height=1, bg="blue", command=self.register_user)
        self.btnRegister.pack()
    def register_user(self):
#        print(self.username.get())
#        print("Hello")


        file = open(self.username_entry.get(), "w")
        file.write(self.username_entry.get() + "\n")
        file.write(self.password_entry.get())
        file.close()
        self.destroyPackWidget(SignUp.main_Root)
        self.lblSucess=Label(root, text="Registration Success", fg="green", font=("calibri", 11))
        self.lblSucess.pack()
        self.btnSucess=Button(root, text="Click Here to proceed", command=self.btnSucess_Click)
        self.btnSucess.pack()
    def btnSucess_Click(self):

        self.destroyPackWidget(SignUp.main_Root)
        frmQuestion = QuestionDigonosis(SignUp.main_Root)

        frmQuestion.pack()


########### From Here is full code of Design and User Management Starts ###########
import pickle
import pymysql;
# import tkinter
import  tkinter.messagebox
import PIL
from PIL import Image,ImageTk
import os
current_master_user=None
current_user=None
def deletedatabase():
    objMaster=MasterSettings()
    if(objMaster.sql_password!=""):
        con=pymysql.connect(host=objMaster.host_name,user=objMaster.sql_user_id,password=objMaster.sql_password,port=int(objMaster.port_no))
        myCursor=con.cursor()
        strQuery="drop database if exists healthDB"
        myCursor.execute(strQuery)
        con.commit()
def deleteallSettings():
    deletedatabase()
    if os.path.exists("masters"):
        os.remove("masters")
    if os.path.exists("users"):
        os.remove("users")


class MasterSettings:
    def __init__(self):
        global current_master_user
        try:
            self.load_master_settings()
            self.is_valid = False
            current_master_user =self
            User.master_details=self
        except Exception as ex:
            self.host_name="localhost"
            self.sql_user_id="root"
            self.sql_password=""
            self.port_no="3306"
            self.is_database=False
            self.is_file=False
            self.master_id="master"
            self.master_password="password"
            self.first_name=""
            self.last_name=""
            self.email_id=""
            self.mobile_no=""
            self.con=""
            self.is_valid=False
            current_master_user = self
            User.master_details = self

    def check_database_setting(host,user,password,port):
        con=pymysql.connect(host=host,user=user,password=password,port=int(port))

    def create_database_and_table(self):
        con = pymysql.connect(host=self.host_name, user=self.sql_user_id, password=self.sql_password, port=int(self.port_no))
        myCursor = con.cursor()
        strQuery="create database if not exists healthDB"
        # con.commit()
        myCursor.execute(strQuery)
        strQuery = "use healthDB"
        myCursor.execute(strQuery)
        # con.commit()
        strQuery = "create table if not exists user (first_name varchar(50),last_name varchar(50),user_id varchar(50),password varchar(50),email_id varchar(50),mobile_no varchar(12),address varchar(500))"
        myCursor.execute(strQuery)
        con.commit()

    def login_master(self,user_id,password):
        global current_master_user
        if(self.master_id==user_id and self.master_password==password):
            self.is_valid=True
            return True
        else:
            self.is_valid = False
            return False

    def save_master_details(self):
        if self.master_id == "Write if want modification":
            self.master_id="master"
        if self.master_password == "Write if want modification":
            self.master_password = "password"
        fs=open('masters','wb')
        pickle.dump(self,fs)
    def load_master_settings(self):
        fs = open('masters', 'rb')
        masterDetails=pickle.load( fs)

        for e in masterDetails.__dict__.items():
            self.__setattr__(e[0],e[1])


class User:
    master_details=None
    list_users=[]
    list_column_names=['First Name','Last Name','User Id','Password','Email Id','Mobile No','Address']
    def __init__(self):
        global current_user
        self.first_name = "NA"
        self.last_name = "NA"
        self.user_id="NA"
        self.password=""
        self.email_id = "NA"
        self.mobile_no = "NA"
        self.address="NA"
        self.is_updated=True
        self.is_valid=False
        if(User.master_details==None):
            User.master_details =MasterSettings()
        current_user=self
    def login_user(self,user_id,password):
        global current_user
        for u in User.list_users:
            if (u.user_id == user_id and u.password == password):
                for e in u.__dict__.items():
                    self.__setattr__(e[0], e[1])
                self.is_valid = True
                current_user = self
                return True
            else:
                self.is_valid = False
                current_user = self
                return False




    def search_user(self,userid):
        for user in User.list_users:
            if(user.user_id==userid):
                for e in user.__dict__.items():
                    self.__setattr__(e[0],e[1])
                return True
        return False

    def delete_user(self,userid):
        for user in User.list_users:
            if (user.user_id == userid):
                User.list_users.remove(user)
                if (User.master_details.is_file):
                    User.save_all_users()
                elif (User.master_details.is_database):
                    con = pymysql.connect(host=self.master_details.host_name, user=self.master_details.sql_user_id,
                                          password=self.master_details.sql_password,
                                          port=int(self.master_details.port_no))
                    myCursor = con.cursor()
                    strQuery = "use healthDb"
                    myCursor.execute(strQuery)
                    strQuery = "delete from user where user_id=%s;"
                    myCursor.execute(strQuery, (userid,))
                    con.commit()
                return True
        return False
    def modify_user(self,userid):
        for user in User.list_users:
            if (user.user_id == userid):
                for e in self.__dict__.items():
                    user.__setattr__(e[0], e[1])
                if (User.master_details.is_file):
                    User.save_all_users()
                elif (User.master_details.is_database):
                    con = pymysql.connect(host=self.master_details.host_name, user=self.master_details.sql_user_id,
                                          password=self.master_details.sql_password,
                                          port=int(self.master_details.port_no))
                    myCursor = con.cursor()
                    strQuery = "use healthDb"
                    myCursor.execute(strQuery)
                    strQuery = "update  user set first_name=%s,last_name=%s,user_id=%s,password=%s,email_id=%s,mobile_no=%s,address=%s where user_id=%s;"

                    myCursor.execute(strQuery, (user.first_name,user.last_name,user.user_id,user.password,user.email_id,user.mobile_no,user.address,userid))
                    con.commit()
                return True
        return False
    def isExistUser(self,userid):
        for user in User.list_users:
            if(user.user_id==userid):
                # for e in user.__dict__.items():
                #     self.__setattr__(e[0],e[1])
                return True
        return False
    def add_new_user(self):
        if self.isExistUser(self.user_id):
            raise Exception("User Already Exists")
        User.list_users.append(self)
        if self.master_details.is_database:
            con = pymysql.connect(host=self.master_details.host_name, user=self.master_details.sql_user_id,
                                  password=self.master_details.sql_password, port=int(self.master_details.port_no))
            myCursor = con.cursor()
            strQuery = "use healthDb"
            myCursor.execute(strQuery)
            strQuery = "insert into user values(%s,%s,%s,%s,%s,%s,%s);"

            myCursor.execute(strQuery,(self.first_name,self.last_name,self.user_id,self.password,self.email_id,self.mobile_no,self.address))
            con.commit()
        else:
            fs = open('users', 'wb')
            pickle.dump(User.list_users, fs)

    @staticmethod
    def save_all_users():
        fs = open('users', 'wb')
        pickle.dump(User.list_users, fs)
    @staticmethod
    def load_all_users():
        objMaster=MasterSettings()
        if User.master_details.is_database:
            con = pymysql.connect(host=User.master_details.host_name, user=User.master_details.sql_user_id, password=User.master_details.sql_password, port=int(User.master_details.port_no))
            myCursor=con.cursor()
            strQuery = "use healthdb"
            myCursor.execute(strQuery)
            strQuery="select * from user"
            myCursor.execute(strQuery)
            User.list_users.clear()
            for row in myCursor.fetchall():
                newuser=User()
                newuser.first_name = row[0]
                newuser.last_name = row[1]
                newuser.user_id = row[2]
                newuser.password = row[3]
                newuser.email_id = row[4]
                newuser.mobile_no = row[5]
                newuser.address = row[6]
                newuser.is_updated = False
                newuser.is_valid=False
                User.list_users.append(newuser)
        else:
            try:
                fs=open("users",'rb')
                User.list_users=pickle.load(fs)
            except Exception:
                pass

#User and Setting Validation Functions:
def showMessage_After(title,msg):
    tkinter.messagebox.showinfo(title, msg)
def showMessage(title,msg):
    global root
    root.after(1,showMessage_After,title,msg)



def is_valid_setting(showmsg="NA"):
    global root, root_label
    try:
        fs=open("masters",'rb')
        objMaster=MasterSettings()
        User.master_details=objMaster
        if(objMaster.is_database==True):
            if(objMaster.sql_password==""):
                if(showmsg=="NA"):
                    showMessage("Error","Dear User Settings are not valid please login with master user and update setting first to start.")
                # tkinter.messagebox.showerror(,,parent=root_label)
                return False
            else:
                return True

        elif(objMaster.is_file==True):
            return True
    except Exception as ex:
        if ( showmsg == "NA"):
            showMessage("Error",
                       "Dear User Settings are not valid please login with master user and update setting first to start.")
            # tkinter.messagebox.showerror("Error","Dear User Settings are not valid please login with master user and update setting first to start.",parent=root_label)
        return False

#User Management Forms
def all_users_form(main_frame,w,h):
    main_frame.pack(pady=int(h * .20),padx=int(h * .02))
    lbl_frame = tkinter.Label(main_frame, width=300, bg='azure')
    lbl_frame.pack(fill='both', expand=True)
    lbl_header = tkinter.Label(lbl_frame, bg='azure', text="All Users Details Form", width=30,
                               font=("Times New Roman", 20, "bold"))
    lbl_header.grid(row=0, column=0, columnspan=2, pady=5)
    frame_all=tkinter.Frame(lbl_frame)
    frame_all.grid(row=1, column=0, columnspan=2, pady=5)
    rowno=0
    columnno=-1
    for columnname in User.list_column_names:
        columnno+=1
        lbl_columnname = tkinter.Label(frame_all, bg='azure', text=columnname, width=15,
                                   font=("Times New Roman", 14, "bold"))
        lbl_columnname.grid(row=rowno, column=columnno, pady=2)

    for user in User.list_users:
        rowno += 1
        columnno=0
        lbl_columnname = tkinter.Label(frame_all, bg='azure', text=user.first_name, width=15,
                                       font=("Times New Roman", 14, "bold"))
        lbl_columnname.grid(row=rowno, column=columnno, pady=2)
        columnno+=1
        lbl_columnname = tkinter.Label(frame_all, bg='azure', text=user.last_name, width=15,
                                       font=("Times New Roman", 12, "bold"))
        lbl_columnname.grid(row=rowno, column=columnno, pady=2)

        columnno += 1
        lbl_columnname = tkinter.Label(frame_all, bg='azure', text=user.user_id, width=15,
                                       font=("Times New Roman", 12, "bold"))
        lbl_columnname.grid(row=rowno, column=columnno, pady=2)

        columnno += 1
        lbl_columnname = tkinter.Label(frame_all, bg='azure', text=user.password, width=15,
                                       font=("Times New Roman", 12, "bold"))
        lbl_columnname.grid(row=rowno, column=columnno, pady=2)

        columnno += 1
        lbl_columnname = tkinter.Label(frame_all, bg='azure', text=user.email_id, width=15,
                                       font=("Times New Roman", 12, "bold"))
        lbl_columnname.grid(row=rowno, column=columnno, pady=2)

        columnno += 1
        lbl_columnname = tkinter.Label(frame_all, bg='azure', text=user.mobile_no, width=15,
                                       font=("Times New Roman", 12, "bold"))
        lbl_columnname.grid(row=rowno, column=columnno, pady=2)

        columnno += 1
        lbl_columnname = tkinter.Label(frame_all, bg='azure', text=user.address, width=15,
                                       font=("Times New Roman", 12, "bold"))
        lbl_columnname.grid(row=rowno, column=columnno, pady=2)



    # btn_delete_setting = tkinter.Button(lbl_frame, bg='azure', text="Delete All Settings", width=30,
    #                                     font=("Times New Roman", 16, "bold"), command=delete_settings_click)
    # btn_delete_setting.grid(row=1, column=0, columnspan=2, pady=10)


#Setting forms functions:
def checkmaster_login():
    if (current_master_user == None):
        showMessage("Failed", "Before Master Login you cant do this ")
        return False
    elif (not current_master_user.is_valid):
        showMessage("Failed", "Before Master Login you cant do this ")
        return False
    else:
        return True
def create_setting(main_frame,w,h):
    global current_master_user
    if(checkmaster_login()):
        def file_handling_form(frame):
            def apply_file_settings():
                objMaster=MasterSettings()
                objMaster.is_database=False
                objMaster.is_file = True
                objMaster.is_database = False
                objMaster.first_name = var_first_name.get()
                objMaster.last_name = var_last_name.get()
                objMaster.email_id = var_email_id.get()
                objMaster.mobile_no = var_mobile_no.get()

                objMaster.master_id = var_master_id.get()
                objMaster.master_password = var_master_password.get()
                objMaster.save_master_details()
                showMessage("Sucess","You are sucessfully opted for File Handling Settings")
                destroy_global_frame()
            for e in frame.grid_slaves():
                e.destroy()

            rowno = 0
            lbl_first_name = tkinter.Label(frame, bg='azure', anchor='e', text="First Name:", width=20,
                                           font=("Times New Roman", 16, "bold"))
            lbl_first_name.grid(row=rowno, column=0, sticky='e', pady=6)
            var_first_name = tkinter.StringVar()
            entry_first_name = tkinter.Entry(frame, textvariable=var_first_name, width=20,
                                             font=("Times New Roman", 16, "bold"))
            entry_first_name.grid(row=rowno, column=1, sticky='w', pady=6)

            rowno += 1
            lbl_last_name = tkinter.Label(frame, bg='azure', anchor='e', text="Last Name:", width=20,
                                          font=("Times New Roman", 16, "bold"))
            lbl_last_name.grid(row=rowno, column=0, sticky='e', pady=6)
            var_last_name = tkinter.StringVar()
            entry_last_name = tkinter.Entry(frame, textvariable=var_last_name, width=20,
                                            font=("Times New Roman", 16, "bold"))
            entry_last_name.grid(row=rowno, column=1, sticky='w', pady=6)

            rowno += 1
            lbl_master_id = tkinter.Label(frame, bg='azure', anchor='e', text="Master Id:", width=20,
                                          font=("Times New Roman", 16, "bold"))
            lbl_master_id.grid(row=rowno, column=0, sticky='e', pady=6)
            var_master_id = tkinter.StringVar()
            entry_master_id = tkinter.Entry(frame, textvariable=var_master_id, width=30,
                                            font=("Times New Roman", 16, "bold"))
            entry_master_id.grid(row=rowno, column=1, sticky='w', pady=6)
            var_master_id.set("Write if want modification")
            rowno += 1
            lbl_master_password = tkinter.Label(frame, bg='azure', text="Master Password:", anchor='e', width=20,
                                                font=("Times New Roman", 16, "bold"))
            lbl_master_password.grid(row=rowno, column=0, sticky='e', pady=6)
            var_master_password = tkinter.StringVar()
            entry_master_password = tkinter.Entry(frame, show='*', textvariable=var_master_password, width=30,
                                                  font=("Times New Roman", 16, "bold"))
            entry_master_password.grid(row=rowno, column=1, sticky='w', pady=6)
            var_master_password.set("Write if want modification")
            rowno += 1
            lbl_email_id = tkinter.Label(frame, bg='azure', anchor='e', text="Email ID:", width=20,
                                         font=("Times New Roman", 16, "bold"))
            lbl_email_id.grid(row=rowno, column=0, sticky='e', pady=6)
            var_email_id = tkinter.StringVar()
            entry_email_id = tkinter.Entry(frame, textvariable=var_email_id, width=20,
                                           font=("Times New Roman", 16, "bold"))
            entry_email_id.grid(row=rowno, column=1, sticky='w', pady=6)

            rowno += 1
            lbl_mobile_no = tkinter.Label(frame, bg='azure', anchor='e', text="Mobile No:", width=20,
                                          font=("Times New Roman", 16, "bold"))
            lbl_mobile_no.grid(row=rowno, column=0, sticky='e', pady=6)
            var_mobile_no = tkinter.StringVar()
            entry_mobile_no = tkinter.Entry(frame, textvariable=var_mobile_no, width=20,
                                            font=("Times New Roman", 16, "bold"))
            entry_mobile_no.grid(row=rowno, column=1, sticky='w', pady=6)

            rowno+=1

            btn_file = tkinter.Button(frame, bg='azure', text="Apply File Settings", width=25,
                                       font=("Times New Roman", 16, "bold"),command=apply_file_settings)
            btn_file.grid(row=rowno, column=0, columnspan=2,pady=10)
        def database_form(frame):

            for e in frame.grid_slaves():
                e.destroy()
            def applydatabase_setting():
                try:
                    host=var_host_name.get()
                    user=var_user.get()
                    pasword=var_password.get()
                    port=var_port_no.get()
                    MasterSettings.check_database_setting(host,user,pasword,port)
                    objMaster=MasterSettings()
                    objMaster.sql_password=pasword
                    objMaster.sql_user_id=user
                    objMaster.host_name=host
                    objMaster.port_no=port
                    objMaster.is_database=True
                    objMaster.is_file=False
                    objMaster.first_name=var_first_name.get()
                    objMaster.last_name = var_last_name.get()
                    objMaster.email_id = var_email_id.get()
                    objMaster.mobile_no = var_mobile_no.get()
                    objMaster.master_id=var_master_id.get()
                    objMaster.master_password=var_master_password.get()
                    objMaster.save_master_details()
                    objMaster.create_database_and_table()
                    showMessage("Sucess", "Database Connectivity parameters are correct and it saved successfully")
                    destroy_global_frame()
                except Exception as ex:
                    showMessage("Error",str(ex))


            rowno=0
            lbl_host_name = tkinter.Label(frame, bg='azure', anchor='e', text="Host Name:", width=20,
                                          font=("Times New Roman", 16, "bold"))
            lbl_host_name.grid(row=rowno, column=0, sticky='e', pady=6)
            var_host_name = tkinter.StringVar()
            entry_host_name = tkinter.Entry(frame, textvariable=var_host_name, width=20,
                                            font=("Times New Roman", 16, "bold"))
            entry_host_name.grid(row=rowno, column=1, sticky='w', pady=6)
            var_host_name.set('localhost')

            rowno += 1
            lbl_user = tkinter.Label(frame, bg='azure', anchor='e', text="Database User:", width=20,
                                        font=("Times New Roman", 16, "bold"))
            lbl_user.grid(row=rowno, column=0, sticky='e', pady=6)
            var_user = tkinter.StringVar()
            entry_user = tkinter.Entry(frame, textvariable=var_user, width=20,
                                          font=("Times New Roman", 16, "bold"))
            entry_user.grid(row=rowno, column=1, sticky='w', pady=6)
            var_user.set('root')

            rowno += 1
            lbl_password = tkinter.Label(frame, bg='azure', text="Database Password:", anchor='e', width=20,
                                         font=("Times New Roman", 16, "bold"))
            lbl_password.grid(row=rowno, column=0, sticky='e', pady=6)
            var_password = tkinter.StringVar()
            entry_password = tkinter.Entry(frame, show='*', textvariable=var_password, width=20,
                                           font=("Times New Roman", 16, "bold"))
            entry_password.grid(row=rowno, column=1, sticky='w', pady=6)
            rowno += 1
            lbl_port_no = tkinter.Label(frame, bg='azure', anchor='e', text="Port No:", width=20,
                                         font=("Times New Roman", 16, "bold"))
            lbl_port_no.grid(row=rowno, column=0, sticky='e', pady=6)
            var_port_no = tkinter.StringVar()
            entry_port_no = tkinter.Entry(frame, textvariable=var_port_no, width=20,
                                           font=("Times New Roman", 16, "bold"))
            entry_port_no.grid(row=rowno, column=1, sticky='w', pady=6)
            var_port_no.set("3306")

            rowno += 1
            lbl_first_name = tkinter.Label(frame, bg='azure', anchor='e', text="First Name:", width=20,
                                        font=("Times New Roman", 16, "bold"))
            lbl_first_name.grid(row=rowno, column=0, sticky='e', pady=6)
            var_first_name = tkinter.StringVar()
            entry_first_name = tkinter.Entry(frame, textvariable=var_first_name, width=20,
                                          font=("Times New Roman", 16, "bold"))
            entry_first_name.grid(row=rowno, column=1, sticky='w', pady=6)

            rowno += 1
            lbl_last_name = tkinter.Label(frame, bg='azure', anchor='e', text="Last Name:", width=20,
                                           font=("Times New Roman", 16, "bold"))
            lbl_last_name.grid(row=rowno, column=0, sticky='e', pady=6)
            var_last_name = tkinter.StringVar()
            entry_last_name = tkinter.Entry(frame, textvariable=var_last_name, width=20,
                                             font=("Times New Roman", 16, "bold"))
            entry_last_name.grid(row=rowno, column=1, sticky='w', pady=6)

            rowno += 1
            lbl_master_id = tkinter.Label(frame, bg='azure', anchor='e', text="Master Id:", width=20,
                                          font=("Times New Roman", 16, "bold"))
            lbl_master_id.grid(row=rowno, column=0, sticky='e', pady=6)
            var_master_id = tkinter.StringVar()
            entry_master_id = tkinter.Entry(frame, textvariable=var_master_id, width=30,
                                            font=("Times New Roman", 16, "bold"))
            entry_master_id.grid(row=rowno, column=1, sticky='w', pady=6)
            var_master_id.set("Write if want modification")
            rowno += 1
            lbl_master_password = tkinter.Label(frame, bg='azure', text="Master Password:", anchor='e', width=20,
                                         font=("Times New Roman", 16, "bold"))
            lbl_master_password.grid(row=rowno, column=0, sticky='e', pady=6)
            var_master_password = tkinter.StringVar()
            entry_master_password = tkinter.Entry(frame, show='*', textvariable=var_master_password, width=30,
                                           font=("Times New Roman", 16, "bold"))
            entry_master_password.grid(row=rowno, column=1, sticky='w', pady=6)
            var_master_password.set("Write if want modification")
            rowno += 1
            lbl_email_id = tkinter.Label(frame, bg='azure', anchor='e', text="Email ID:", width=20,
                                          font=("Times New Roman", 16, "bold"))
            lbl_email_id.grid(row=rowno, column=0, sticky='e', pady=6)
            var_email_id = tkinter.StringVar()
            entry_email_id = tkinter.Entry(frame, textvariable=var_email_id, width=20,
                                            font=("Times New Roman", 16, "bold"))
            entry_email_id.grid(row=rowno, column=1, sticky='w', pady=6)

            rowno += 1
            lbl_mobile_no = tkinter.Label(frame, bg='azure', anchor='e', text="MObile No:", width=20,
                                         font=("Times New Roman", 16, "bold"))
            lbl_mobile_no.grid(row=rowno, column=0, sticky='e', pady=6)
            var_mobile_no = tkinter.StringVar()
            entry_mobile_no = tkinter.Entry(frame, textvariable=var_mobile_no, width=20,
                                           font=("Times New Roman", 16, "bold"))
            entry_mobile_no.grid(row=rowno, column=1, sticky='w', pady=6)

            rowno += 1

            btn_database = tkinter.Button(frame, bg='azure', text="Check and Update Database Setting", width=30,
                                       font=("Times New Roman", 16, "bold"),command=applydatabase_setting)
            rowno += 1
            btn_database.grid(row=rowno, column=0, columnspan=2, pady=10)

        def rbt_setting_click():
                if(var_setting.get()==1):
                    # frame_database_file = tkinter.Frame(lbl_frame)
                    # frame_database_file.grid(row=2, column=0, columnspan=2)
                    file_handling_form(frame_file)
                else:
                    # frame_database_file = tkinter.Frame(lbl_frame)
                    # frame_database_file.grid(row=2, column=0, columnspan=2)
                    database_form(frame_file)
        main_frame.pack(pady=int(h * .05))
        lbl_frame = tkinter.Label(main_frame, width=300, bg='azure')
        lbl_frame.pack(fill='both', expand=True)
        lbl_header = tkinter.Label(lbl_frame, bg='azure', text="Manage Setting Form", width=30,
                                   font=("Times New Roman", 26, "bold"))
        lbl_header.grid(row=0, column=0, columnspan=2, pady=10)
        rowno=0
        rowno += 1
        lbl_select_setting = tkinter.Label(lbl_frame, bg='azure', anchor='e', text="Select Setting Option:", width=20,
                                       font=("Times New Roman", 16, "bold"))
        lbl_select_setting.grid(row=rowno, column=0, sticky='e', pady=10)


        frame_setting=tkinter.Frame(lbl_frame)
        frame_setting.grid(row=rowno,column=1)
        var_setting=tkinter.IntVar()
        rbt_file_handling=tkinter.Radiobutton(frame_setting,text='User File Handling',variable=var_setting,value=1,command=rbt_setting_click)
        rbt_file_handling.grid(row=0,column=0)
        rbt_database = tkinter.Radiobutton(frame_setting,text='User Database', variable=var_setting, value=0,command=rbt_setting_click)
        rbt_database.grid(row=0, column=1)
        var_setting.set(1)
        rowno += 1
        frame_file=tkinter.Frame(lbl_frame)
        frame_file.grid(row=rowno,column=0,columnspan=2)
        file_handling_form(frame_file)
def delete_setting(main_frame,w,h):
    global current_master_user
    if (checkmaster_login()):
        def delete_settings_click():
            res = tkinter.messagebox.askyesno("DELETE", "Do you want to delete all settings.Note that after this you lost your all setting and user related data that will not recovered")
            if res:
                deleteallSettings()
                showMessage("Sucess", "All settings are deleted sucessfully")
            destroy_global_frame()

        main_frame.pack(pady=int(h * .20))
        lbl_frame = tkinter.Label(main_frame, width=300, bg='azure')
        lbl_frame.pack(fill='both', expand=True)
        lbl_header = tkinter.Label(lbl_frame, bg='azure', text="Delete Setting Form", width=30,
                                   font=("Times New Roman", 26, "bold"))
        lbl_header.grid(row=0, column=0, columnspan=2, pady=10)
        btn_delete_setting = tkinter.Button(lbl_frame, bg='azure', text="Delete All Settings", width=30,
                                  font=("Times New Roman", 16, "bold"), command=delete_settings_click)
        btn_delete_setting.grid(row=1, column=0, columnspan=2, pady=10)


#Others Forms function
def login_master_user(frame,w,h):
    def master_login():
        global current_master_user,current_user
        objMaster=MasterSettings();
        if(objMaster.login_master(var_user_id.get(),var_password.get())):
            current_user=None
            showMessage("Sucess","Login Success Now you can perform all activity. Start now according to Menu.")
            destroy_global_frame()
        else:
            showMessage("Failed", "User Id or Password Incorrect")
    frame.pack(pady=int(h*.20))
    lbl_frame = tkinter.Label(frame,width=300,bg='azure')
    lbl_frame.pack(fill='both', expand=True)
    lbl_header=tkinter.Label(lbl_frame,bg='azure',text="Master Login Form",width=30,font=("Times New Roman", 26, "bold"))
    lbl_header.grid(row=0,column=0,columnspan=2,pady=10)
    lbl_user_id = tkinter.Label(lbl_frame, bg='azure',anchor='e', text="Master User ID", width=20, font=("Times New Roman", 16, "bold"))
    lbl_user_id.grid(row=1, column=0,sticky ='e',pady=10)
    var_user_id=tkinter.StringVar()
    entry_user_id = tkinter.Entry(lbl_frame, textvariable=var_user_id, width=20, font=("Times New Roman", 16, "bold"))
    entry_user_id.grid(row=1, column=1,sticky ='w',pady=10)
    lbl_password = tkinter.Label(lbl_frame, bg='azure', anchor='e', text="Password:", width=20,
                                font=("Times New Roman", 16, "bold"))
    lbl_password.grid(row=2, column=0, sticky='e', pady=10)
    var_password = tkinter.StringVar()
    entry_password = tkinter.Entry(lbl_frame,show='*', textvariable=var_password, width=20,
                                  font=("Times New Roman", 16, "bold"))
    entry_password.grid(row=2, column=1, sticky='w', pady=10)
    btn_login = tkinter.Button(lbl_frame, bg='azure',  text="Login", width=20,
                                 font=("Times New Roman", 16, "bold"),command=master_login)
    btn_login.grid(row=3, column=0,columnspan=2,  pady=10)
def login_user(frame,w,h):
    # Checking for Settings
    if not is_valid_setting():
        return
    def user_login():
        global current_master_user,current_user
        objUser=User()
        if(objUser.login_user(var_user_id.get(),var_password.get())):
            current_master_user=None
            showMessage("Sucess","Login Sucess Now you can perform all activity that is valid for you. Please user Chatbot for your medical suggessions")
            destroy_global_frame()
        else:
            showMessage("Failed", "User Id or Password Incorrect")
    frame.pack(pady=int(h*.20))
    lbl_frame = tkinter.Label(frame,width=300,bg='azure')
    lbl_frame.pack(fill='both', expand=True)
    lbl_header=tkinter.Label(lbl_frame,bg='azure',text="Login Form",width=30,font=("Times New Roman", 26, "bold"))
    lbl_header.grid(row=0,column=0,columnspan=2,pady=10)
    lbl_user_id = tkinter.Label(lbl_frame, bg='azure',anchor='e', text="User ID", width=20, font=("Times New Roman", 16, "bold"))
    lbl_user_id.grid(row=1, column=0,sticky ='e',pady=10)
    var_user_id=tkinter.StringVar()
    entry_user_id = tkinter.Entry(lbl_frame, textvariable=var_user_id, width=20, font=("Times New Roman", 16, "bold"))
    entry_user_id.grid(row=1, column=1,sticky ='w',pady=10)
    lbl_password = tkinter.Label(lbl_frame, bg='azure', anchor='e', text="Password:", width=20,
                                font=("Times New Roman", 16, "bold"))
    lbl_password.grid(row=2, column=0, sticky='e', pady=10)
    var_password = tkinter.StringVar()
    entry_password = tkinter.Entry(lbl_frame,show='*', textvariable=var_password, width=20,
                                  font=("Times New Roman", 16, "bold"))
    entry_password.grid(row=2, column=1, sticky='w', pady=10)
    btn_login = tkinter.Button(lbl_frame, bg='azure',  text="Login", width=20,
                                 font=("Times New Roman", 16, "bold"),command=user_login)
    btn_login.grid(row=3, column=0,columnspan=2,  pady=10)
def all_users_search_delete_modify(frame,w,h):
    # Checking for Settings
    if not is_valid_setting():
        return

    def search_user():
        u=User()
        user_id= var_user_id.get()
        b=u.search_user(user_id)
        if(b):
            var_first_name.set(u.first_name)
            var_last_name.set(u.last_name)
            var_address.set(u.address)
            var_password.set(u.password)
            var_email_id.set(u.email_id)
            var_mobile_no.set(u.mobile_no)
            showMessage("Success","User Found Sucessfully")

        else:
            showMessage("Failed","User Id Not found")
    def delete_user():
        u = User()
        user_id = var_user_id.get()
        b = u.delete_user(user_id)
        if (b):
            showMessage("Success", "User Deleted Sucessfully")

        else:
            showMessage("Failed", "User Id Not found")
    def modify_user():
        user=User()
        user.mobile_no = var_mobile_no.get()
        user.email_id = var_email_id.get()
        user.first_name = var_first_name.get()
        user.password = var_password.get()
        user.user_id = var_user_id.get()
        user.last_name = var_last_name.get()
        user.address = var_address.get()
        user_id = var_user_id.get()
        b = user.modify_user(user_id)
        if (b):
            showMessage("Success", "User Modified Sucessfully")

        else:
            showMessage("Failed", "User Id Not found")
    def add_new_user():
        try:
            user=User()
            user.mobile_no=var_mobile_no.get()
            user.email_id=var_email_id.get()
            user.first_name=var_first_name.get()
            user.password=var_password.get()
            user.user_id=var_user_id.get()
            user.last_name=var_last_name.get()
            user.address=var_address.get()
            user.add_new_user()
            showMessage("Success", "User Added Sucessfully")
            # destroy_global_frame()
        except Exception as ex:
            showMessage("Error",str(ex))

    frame.pack(pady=int(h*.05))
    lbl_frame = tkinter.Label(frame,width=300,bg='azure')
    lbl_frame.pack(fill='both', expand=True)
    lbl_header=tkinter.Label(lbl_frame,bg='azure',text="User Management Form",width=30,font=("Times New Roman", 20, "bold"))
    lbl_header.grid(row=0,column=0,columnspan=4,pady=3)
    rowno = 1
    lbl_user_id = tkinter.Label(lbl_frame, bg='azure', anchor='e', text="User ID", width=20,
                                font=("Times New Roman", 14, "bold"))
    lbl_user_id.grid(row=rowno, column=0, columnspan=2, sticky='e', pady=3)
    var_user_id = tkinter.StringVar()
    entry_user_id = tkinter.Entry(lbl_frame, textvariable=var_user_id, width=20, font=("Times New Roman", 14, "bold"))
    entry_user_id.grid(row=rowno, column=2, columnspan=2, sticky='w', pady=3)
    rowno += 1
    lbl_first_name = tkinter.Label(lbl_frame, bg='azure', anchor='e', text="First Name:", width=20,
                                font=("Times New Roman", 16, "bold"))
    lbl_first_name.grid(row=rowno, column=0, columnspan=2, sticky='e', pady=3)
    var_first_name = tkinter.StringVar()
    entry_first_name = tkinter.Entry(lbl_frame, textvariable=var_first_name, width=20,font=("Times New Roman", 14, "bold"))
    entry_first_name.grid(row=rowno, column=2,columnspan=2, sticky='w', pady=3)

    rowno+=1
    lbl_last_name = tkinter.Label(lbl_frame, bg='azure', anchor='e', text="Last Name:", width=20,
                                   font=("Times New Roman", 14, "bold"))
    lbl_last_name.grid(row=rowno, column=0,columnspan=2, sticky='e', pady=3)
    var_last_name = tkinter.StringVar()
    entry_last_name = tkinter.Entry(lbl_frame, textvariable=var_last_name, width=20, font=("Times New Roman", 14, "bold"))
    entry_last_name.grid(row=rowno, column=2,columnspan=2, sticky='w', pady=3)


    rowno += 1
    lbl_password = tkinter.Label(lbl_frame, bg='azure',text="Password:", anchor='e', width=20,font=("Times New Roman", 14, "bold"))
    lbl_password.grid(row=rowno, column=0,columnspan=2, sticky='e', pady=6)
    var_password = tkinter.StringVar()
    entry_password = tkinter.Entry(lbl_frame,show='*', textvariable=var_password, width=20,font=("Times New Roman", 14, "bold"))
    entry_password.grid(row=rowno, column=2, columnspan=2,sticky='w', pady=6)
    rowno += 1
    lbl_confirm_password = tkinter.Label(lbl_frame, bg='azure',text="Confirm Password:" ,anchor='e', width=20,font=("Times New Roman", 14, "bold"))
    lbl_confirm_password.grid(row=rowno, column=0,columnspan=2, sticky='e', pady=6)
    var_confirm_password = tkinter.StringVar()
    entry_confirm_password = tkinter.Entry(lbl_frame, show='*', textvariable=var_confirm_password, width=20,font=("Times New Roman", 14, "bold"))
    entry_confirm_password.grid(row=rowno, column=2,columnspan=2, sticky='w', pady=6)

    rowno += 1
    lbl_email_id = tkinter.Label(lbl_frame, bg='azure', anchor='e', text="Email ID:", width=20,
                                font=("Times New Roman", 14, "bold"))
    lbl_email_id.grid(row=rowno, column=0,columnspan=2, sticky='e', pady=6)
    var_email_id = tkinter.StringVar()
    entry_email_id = tkinter.Entry(lbl_frame, textvariable=var_email_id, width=20, font=("Times New Roman", 14, "bold"))
    entry_email_id.grid(row=rowno, column=2,columnspan=2, sticky='w', pady=6)

    rowno += 1
    lbl_mobile_no = tkinter.Label(lbl_frame, bg='azure', anchor='e', text="Mobile No:", width=20,
                                font=("Times New Roman", 14, "bold"))
    lbl_mobile_no.grid(row=rowno, column=0,columnspan=2, sticky='e', pady=3)
    var_mobile_no = tkinter.StringVar()
    entry_mobile_no = tkinter.Entry(lbl_frame, textvariable=var_mobile_no, width=20, font=("Times New Roman", 14, "bold"))
    entry_mobile_no.grid(row=rowno, column=2, columnspan=2,sticky='w', pady=3)
    rowno += 1
    lbl_address = tkinter.Label(lbl_frame, bg='azure', anchor='e', text="Address:", width=20,
                                  font=("Times New Roman", 14, "bold"))
    lbl_address.grid(row=rowno, column=0, columnspan=2, sticky='e', pady=3)
    var_address = tkinter.StringVar()
    entry_address = tkinter.Entry(lbl_frame, textvariable=var_address, width=20,
                                    font=("Times New Roman", 14, "bold"))
    entry_address.grid(row=rowno, column=2, columnspan=2, sticky='w', pady=3)

    rowno += 1
    btn_add_new_user = tkinter.Button(lbl_frame, bg='azure',  text="Add User", width=10,
                                 font=("Times New Roman", 14, "bold"),command=add_new_user)

    btn_add_new_user.grid(row=rowno, column=0,  pady=3)
    btn_search_user = tkinter.Button(lbl_frame, bg='azure', text="Search User", width=11,
                                      font=("Times New Roman", 14, "bold"), command=search_user)

    btn_search_user.grid(row=rowno, column=1, pady=3)

    btn_delete_user = tkinter.Button(lbl_frame, bg='azure', text="Delete User", width=11,
                                     font=("Times New Roman", 14, "bold"), command=delete_user)

    btn_delete_user.grid(row=rowno, column=2, pady=3)

    btn_modify_user = tkinter.Button(lbl_frame, bg='azure', text="Modify User", width=11,
                                     font=("Times New Roman", 14, "bold"), command=modify_user)

    btn_modify_user.grid(row=rowno, column=3, pady=3)
    rowno += 1
    lbl_msg = tkinter.Label(lbl_frame, bg='azure', text="Search Delete and Modify are works for user id only:", width=80,
                                  font=("Times New Roman", 14, "bold"))
    lbl_msg.grid(row=rowno, column=0, columnspan=4, pady=3)
def new_user(frame,w,h):
    # Checking for Settings
    if not is_valid_setting():
        return
    def add_new_user():
        try:
            user=User()
            user.mobile_no=var_mobile_no.get()
            user.email_id=var_email_id.get()
            user.first_name=var_first_name.get()
            user.password=var_password.get()
            user.user_id=var_user_id.get()
            user.last_name=var_last_name.get()
            user.address="NA"
            user.add_new_user()
            showMessage("Success", "User Added Sucessfully.Now you can user our Chatbot automation for your halth issues")
            destroy_global_frame()
        except Exception as ex:
            showMessage("Error",str(ex))

    frame.pack(pady=int(h*.05))
    lbl_frame = tkinter.Label(frame,width=300,bg='azure')
    lbl_frame.pack(fill='both', expand=True)
    lbl_header=tkinter.Label(lbl_frame,bg='azure',text="Register Form",width=30,font=("Times New Roman", 26, "bold"))
    lbl_header.grid(row=0,column=0,columnspan=2,pady=6)
    rowno = 1
    lbl_first_name = tkinter.Label(lbl_frame, bg='azure', anchor='e', text="First Name:", width=20,
                                font=("Times New Roman", 16, "bold"))
    lbl_first_name.grid(row=rowno, column=0, sticky='e', pady=6)
    var_first_name = tkinter.StringVar()
    entry_first_name = tkinter.Entry(lbl_frame, textvariable=var_first_name, width=20,font=("Times New Roman", 16, "bold"))
    entry_first_name.grid(row=rowno, column=1, sticky='w', pady=6)

    rowno+=1
    lbl_last_name = tkinter.Label(lbl_frame, bg='azure', anchor='e', text="Last Name:", width=20,
                                   font=("Times New Roman", 16, "bold"))
    lbl_last_name.grid(row=rowno, column=0, sticky='e', pady=6)
    var_last_name = tkinter.StringVar()
    entry_last_name = tkinter.Entry(lbl_frame, textvariable=var_last_name, width=20, font=("Times New Roman", 16, "bold"))
    entry_last_name.grid(row=rowno, column=1, sticky='w', pady=6)

    rowno+=1
    lbl_user_id = tkinter.Label(lbl_frame, bg='azure',anchor='e', text="User ID", width=20, font=("Times New Roman", 16, "bold"))
    lbl_user_id.grid(row=rowno, column=0,sticky ='e',pady=6)
    var_user_id=tkinter.StringVar()
    entry_user_id = tkinter.Entry(lbl_frame, textvariable=var_user_id, width=20, font=("Times New Roman", 16, "bold"))
    entry_user_id.grid(row=rowno, column=1,sticky ='w',pady=6)

    rowno += 1
    lbl_password = tkinter.Label(lbl_frame, bg='azure',text="Password:", anchor='e', width=20,font=("Times New Roman", 16, "bold"))
    lbl_password.grid(row=rowno, column=0, sticky='e', pady=6)
    var_password = tkinter.StringVar()
    entry_password = tkinter.Entry(lbl_frame,show='*', textvariable=var_password, width=20,font=("Times New Roman", 16, "bold"))
    entry_password.grid(row=rowno, column=1, sticky='w', pady=6)
    rowno += 1
    lbl_confirm_password = tkinter.Label(lbl_frame, bg='azure',text="Confirm Password:" ,anchor='e', width=20,font=("Times New Roman", 16, "bold"))
    lbl_confirm_password.grid(row=rowno, column=0, sticky='e', pady=6)
    var_confirm_password = tkinter.StringVar()
    entry_confirm_password = tkinter.Entry(lbl_frame, show='*', textvariable=var_confirm_password, width=20,font=("Times New Roman", 16, "bold"))
    entry_confirm_password.grid(row=rowno, column=1, sticky='w', pady=6)

    rowno += 1
    lbl_email_id = tkinter.Label(lbl_frame, bg='azure', anchor='e', text="Email ID:", width=20,
                                font=("Times New Roman", 16, "bold"))
    lbl_email_id.grid(row=rowno, column=0, sticky='e', pady=6)
    var_email_id = tkinter.StringVar()
    entry_email_id = tkinter.Entry(lbl_frame, textvariable=var_email_id, width=20, font=("Times New Roman", 16, "bold"))
    entry_email_id.grid(row=rowno, column=1, sticky='w', pady=6)

    rowno += 1
    lbl_mobile_no = tkinter.Label(lbl_frame, bg='azure', anchor='e', text="Mobile No:", width=20,
                                font=("Times New Roman", 16, "bold"))
    lbl_mobile_no.grid(row=rowno, column=0, sticky='e', pady=6)
    var_mobile_no = tkinter.StringVar()
    entry_mobile_no = tkinter.Entry(lbl_frame, textvariable=var_mobile_no, width=20, font=("Times New Roman", 16, "bold"))
    entry_mobile_no.grid(row=rowno, column=1, sticky='w', pady=6)
    rowno += 1
    btn_add_new_user = tkinter.Button(lbl_frame, bg='azure',  text="Add New User", width=20,
                                 font=("Times New Roman", 16, "bold"),command=add_new_user)

    btn_add_new_user.grid(row=rowno, column=0,columnspan=2,  pady=6)
import  QuestionDiagonosisTkinter
def applyMenu(root):
    def showall():
        if (checkmaster_login()):
            global root_label
            destroy_global_frame()
            frm_top = tkinter.Frame(root_label)
            frm_top.pack(fill="x")
            applyWelcomeMessage(frm_top)
            frm_screen = tkinter.Frame(root_label)
            all_users_form(frm_screen, root.winfo_screenwidth(), root.winfo_screenheight())


    def newuser():
        global root_label
        destroy_global_frame()
        frm_top = tkinter.Frame(root_label)
        frm_top.pack(fill="x")
        applyWelcomeMessage(frm_top)
        frm_screen = tkinter.Frame(root_label)
        new_user(frm_screen, root.winfo_screenwidth(), root.winfo_screenheight())

    def deleteuser():
        if (checkmaster_login()):
            global root_label
            destroy_global_frame()
            frm_top = tkinter.Frame(root_label)
            frm_top.pack(fill="x")
            applyWelcomeMessage(frm_top)
            frm_screen = tkinter.Frame(root_label)
            all_users_search_delete_modify(frm_screen, root.winfo_screenwidth(), root.winfo_screenheight())
    def modifyeuser():
        if (checkmaster_login()):
            global root_label
            destroy_global_frame()
            frm_top = tkinter.Frame(root_label)
            frm_top.pack(fill="x")
            applyWelcomeMessage(frm_top)
            frm_screen = tkinter.Frame(root_label)
            all_users_search_delete_modify(frm_screen, root.winfo_screenwidth(), root.winfo_screenheight())

    def searchuser():
        if (checkmaster_login()):
            global root_label
            destroy_global_frame()
            frm_top = tkinter.Frame(root_label)
            frm_top.pack(fill="x")
            applyWelcomeMessage(frm_top)
            frm_screen = tkinter.Frame(root_label)
            all_users_search_delete_modify(frm_screen, root.winfo_screenwidth(), root.winfo_screenheight())

    def login():
        global root_label
        destroy_global_frame()
        frm_top=tkinter.Frame(root_label)
        frm_top.pack(fill="x")
        applyWelcomeMessage(frm_top)
        frm_screen=tkinter.Frame(root_label)
        login_user(frm_screen, root.winfo_screenwidth(), root.winfo_screenheight())

    def changepassword():
        pass
    def adminlogin():
        global root_label
        destroy_global_frame()
        frm_top = tkinter.Frame(root_label)
        frm_top.pack(fill="x")
        applyWelcomeMessage(frm_top)
        frm_screen = tkinter.Frame(root_label)
        login_master_user(frm_screen, root.winfo_screenwidth(), root.winfo_screenheight())
        # //frm_screen.update_idletasks()
        # root.update()
    def adminchangepassword():
        pass
    def addsetting():
        global root_label
        destroy_global_frame()
        frm_top = tkinter.Frame(root_label)
        frm_top.pack(fill="x")
        applyWelcomeMessage(frm_top)
        frm_screen = tkinter.Frame(root_label)
        create_setting(frm_screen, root.winfo_screenwidth(), root.winfo_screenheight())

    def deletesetting():
        global root_label
        destroy_global_frame()
        frm_top = tkinter.Frame(root_label)
        frm_top.pack(fill="x")
        applyWelcomeMessage(frm_top)
        frm_screen = tkinter.Frame(root_label)
        delete_setting(frm_screen, root.winfo_screenwidth(), root.winfo_screenheight())
    def callChatBot():
        global root_label
        destroy_global_frame()
        frm_top = tkinter.Frame(root_label)
        frm_top.pack(fill="x")
        applyWelcomeMessage(frm_top)
        frm_screen = tkinter.Frame(root_label)
        frm_screen.pack(fill="both", expand=True)
        frmChatBot = QuestionDiagonosisTkinter.QuestionDigonosis(frm_screen)
        frmChatBot.createWidget(frm_screen, root.winfo_screenwidth(), root.winfo_screenheight())

    def chatbot():
        if (current_master_user == None):
            if  current_user==None:
                showMessage("Failed", "Before  Login you cant Access this ")
                return
            elif current_user.is_valid:
                callChatBot()
            else:
                showMessage("Failed", "Before  Login you cant Access this ")
        elif current_user!=None:
            if current_user.is_valid:
                callChatBot()
            else:
                showMessage("Failed", "Before  Login you cant Access this ")
        elif current_master_user.is_valid:
            callChatBot()
        else:
            showMessage("Failed", "Before  Login you cant Access this ")



    def wiki():
        global root_label
        destroy_global_frame()
        frm_top = tkinter.Frame(root_label)
        frm_top.pack(fill="x")
        applyWelcomeMessage(frm_top)
        frm_screen = tkinter.Frame(root_label)
        h=root.winfo_screenheight()
        w=root.winfo_screenwidth()
        frm_screen.pack(pady=int(h * .20))
        lbl_frame = tkinter.Label(frm_screen, width=300, bg='azure')
        lbl_frame.pack(fill='both', expand=True)
        lbl_header = tkinter.Label(lbl_frame, bg='azure', text="Health Wikipedia", width=30,
                                   font=("Times New Roman", 26, "bold"))
        lbl_header.grid(row=0, column=0, columnspan=2, pady=10)
        label_image=tkinter.Label(lbl_frame)

        load_img = Image.open("img/wiki.jpg")
        img_photo = ImageTk.PhotoImage(load_img)
        label_image.image = img_photo
        label_image["image"] = img_photo
        label_image.grid(row=1, column=0, columnspan=2, pady=50,padx=50)

    def covid():
        global root_label
        destroy_global_frame()
        frm_top = tkinter.Frame(root_label)
        frm_top.pack(fill="x")
        applyWelcomeMessage(frm_top)
        frm_screen = tkinter.Frame(root_label)
        h = root.winfo_screenheight()
        w = root.winfo_screenwidth()
        frm_screen.pack(pady=int(h * .20))
        lbl_frame = tkinter.Label(frm_screen, width=300, bg='azure')
        lbl_frame.pack(fill='both', expand=True)
        lbl_header = tkinter.Label(lbl_frame, bg='azure', text="Covid Update Form", width=30,
                                   font=("Times New Roman", 26, "bold"))
        lbl_header.grid(row=0, column=0, columnspan=2, pady=10)
        label_image = tkinter.Label(lbl_frame)

        load_img = Image.open("img/covid-19.jpg")
        img_photo = ImageTk.PhotoImage(load_img)
        label_image.image = img_photo
        label_image["image"] = img_photo
        label_image.grid(row=1, column=0, columnspan=2, pady=50, padx=50)

    def medicoz():
        global root_label
        destroy_global_frame()
        frm_top = tkinter.Frame(root_label)
        frm_top.pack(fill="x")
        applyWelcomeMessage(frm_top)
        frm_screen = tkinter.Frame(root_label)
        h = root.winfo_screenheight()
        w = root.winfo_screenwidth()
        frm_screen.pack(pady=int(h * .20))
        lbl_frame = tkinter.Label(frm_screen, width=300, bg='azure')
        lbl_frame.pack(fill='both', expand=True)
        lbl_header = tkinter.Label(lbl_frame, bg='azure', text="Medicoz", width=30,
                                   font=("Times New Roman", 26, "bold"))
        lbl_header.grid(row=0, column=0, columnspan=2, pady=10)
        label_image = tkinter.Label(lbl_frame)

        load_img = Image.open("img/medicoz.jpg")
        img_photo = ImageTk.PhotoImage(load_img)
        label_image.image = img_photo
        label_image["image"] = img_photo
        label_image.grid(row=1, column=0, columnspan=2, pady=50, padx=50)

    # def aboutus():
    #     global root_label
    #     destroy_global_frame()
    #     frm_top = tkinter.Frame(root_label)
    #     frm_top.pack(fill="x")
    #     applyWelcomeMessage(frm_top)
    #     frm_screen = tkinter.Frame(root_label)
    #     h = root.winfo_screenheight()
    #     w = root.winfo_screenwidth()
    #     frm_screen.pack(pady=int(h * .20))
    #     lbl_frame = tkinter.Label(frm_screen, width=300, bg='azure')
    #     lbl_frame.pack(fill='both', expand=True)
    #     lbl_header = tkinter.Label(lbl_frame, bg='azure', text="About Us Form", width=30,
    #                                font=("Times New Roman", 26, "bold"))
    #     lbl_header.grid(row=0, column=0, columnspan=2, pady=10)
    #     label_image = tkinter.Label(lbl_frame)
    #
    #     load_img = Image.open("img/aboutus.jpg")
    #     img_photo = ImageTk.PhotoImage(load_img)
    #     label_image.image = img_photo
    #     label_image["image"] = img_photo
    #     label_image.grid(row=1, column=0, columnspan=2, pady=50, padx=50)

    def DietPlanSystem():
        global root_label
        destroy_global_frame()
        frm_top = tkinter.Frame(root_label)
        frm_top.pack(fill="x")
        applyWelcomeMessage(frm_top)
        frm_screen = tkinter.Frame(root_label)
        h = root.winfo_screenheight()
        w = root.winfo_screenwidth()
        frm_screen.pack(pady=int(h * .20))
        lbl_frame = tkinter.Label(frm_screen, width=300, bg='azure')
        lbl_frame.pack(fill='both', expand=True)
        lbl_header = tkinter.Label(lbl_frame, bg='azure', text="Diet Plan", width=30,
                                   font=("Times New Roman", 26, "bold"))
        lbl_header.grid(row=0, column=0, columnspan=2, pady=10)
        label_image = tkinter.Label(lbl_frame)

        load_img = Image.open("img/diet.jpg")
        img_photo = ImageTk.PhotoImage(load_img)
        label_image.image = img_photo
        label_image["image"] = img_photo
        label_image.grid(row=1, column=0, columnspan=2, pady=50, padx=50)

    menu_main=tkinter.Menu(root)
    submenu_user=tkinter.Menu(root)
    submenu_user.add_command(label="New User",command=newuser)
    submenu_user.add_command(label="Login", command=login)
    submenu_user.add_command(label="Change Password", command=changepassword)
    menu_main.add_cascade(label="User",menu=submenu_user)
    submenu_admin=tkinter.Menu(root)
    submenu_config=tkinter.Menu(root)
    submenu_admin.add_command(label="Master Login", command=adminlogin)
    submenu_admin.add_command(label="Change Password", command=adminchangepassword)
    submenu_config.add_command(label="Add Setting",command=addsetting)
    submenu_config.add_command(label="Delete Setting", command=deletesetting)
    submenu_admin.add_cascade(label="Configuration",menu=submenu_config)
    submenu_admin.add_command(label="Show All Users",command=showall)
    submenu_admin.add_command(label="Search User", command=searchuser)
    submenu_admin.add_command(label="Add User", command=newuser)
    submenu_admin.add_command(label="Delete User", command=deleteuser)
    submenu_admin.add_command(label="Modify User", command=modifyeuser)

    menu_main.add_cascade(label="Admin",menu=submenu_admin)
    menu_main.add_command(label="ChatBot",command=chatbot)
    menu_main.add_command(label="Health wiki", command=wiki)
    menu_main.add_command(label="Covid-19", command=covid)
    menu_main.add_command(label="Medicoz", command=medicoz)
    # menu_main.add_command(label="About Us", command=aboutus)
    menu_main.add_command(label="Diet Plan System", command=DietPlanSystem)
    root.config(menu=menu_main)
# global lbl_welcome
def applyWelcomeMessage(top_frame):
    # global root_label
    lbl_welcome=tkinter.Label(top_frame,bg="white",fg='blue',font=("Times New Roman", 26, "bold"), text="Welcome to HealthCare Bot")
    lbl_welcome.pack(fill="both",expand=True)
    # top_frame.pack(fill='x',expand=True)
def destroy_global_frame():
    global root_label
    for e in root_label.pack_slaves():
        e.destroy()

def main():
    #Initialization and size of root
    root.minsize(root.winfo_screenwidth(),root.winfo_screenheight())
    #Title of root
    root.title("Medicity Chatbot ")
    #Icon of root
    load_img_icon = Image.open("img/homeicon.png")
    img_photo_icon = ImageTk.PhotoImage(load_img_icon)
    root.image = img_photo_icon
    root.iconphoto(True,img_photo_icon)
    #Background Image on root Using Label
    global root_label
    root_label=tkinter.Label(root,bg="white")
    load_img=Image.open("img/home.jpeg")
    img_photo=ImageTk.PhotoImage(load_img)
    load_img.image=img_photo
    root_label["image"]=img_photo
    root_label.pack(fill='both',expand=True)
    #Menu on root
    applyMenu(root)
    #Top Frame for Welcome Message
    global top_frame

    top_frame=tkinter.Frame(root_label)
    # root_label.l = top_frame
    top_frame.pack(fill='x')
    applyWelcomeMessage(top_frame)
    # Checking for Settings

    is_valid_setting()
    User.load_all_users()
        #Frame Display start from here
    # global frame_global
    # frame_global=tkinter.Frame(root_label)
    # frame_global.pack(pady=100)
    # login_user(frame_global,root.winfo_screenwidth(),root.winfo_screenheight())
    # destroy_global_frame()
    #main loop to show Tkinter window

    root.mainloop()


########### Here is full code of Design and User Management Ends ###########

########### From Execution is Starts ###########
global root_label
# global top_frame
# global frame_global
root=tkinter.Tk()
main()
########### Here Execution is Ends ###########
