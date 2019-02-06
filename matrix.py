import numpy as np
from numpy.linalg import inv
from tinydb import TinyDB,Query

class Model:
# ***************************************************************************
    def my_input(self,str):
        self.m = int(input("Enter the number of row for " + str + ": "))
        self.n = int(input("Enter the number of columns for " + str + ": "))
        Mat1 = np.empty((self.m, self.n))
        for i in range(self.m):
            for j in range(self.n):
                temp = float(input())
                Mat1[i][j] = temp

        print(Mat1)
        return Mat1

#*****************************************************************************

    def Name(self,str):
        self.name = str
# *******************************************************************************

    def get_input(self):
        self.F = self.my_input("measurement matrix")
        self.y = self.my_input("raw data")
# *******************************************************************************
    def run_wo_weight(self):
        Ftranspose = np.transpose(self.F)
        x = np.dot(Ftranspose,self.F)
        x = inv(x)
        x = np.dot(x,Ftranspose)
        x = np.dot(x,self.y)
        self.result1 = x
        self.result2 = 0

# *******************************************************************************
    def run_with_weight(self):
        Ftranspose = np.transpose(self.F)
        x = np.dot(Ftranspose,self.w)
        x = np.dot(x,self.F)
        x = inv(x)
        x = np.dot(x,Ftranspose)
        x = np.dot(x,self.w)
        x = np.dot(x,self.y)
        self.result2 = x

# ****************************************************************************
    def save(self):
        db = TinyDB('./data/db.json')
        entry = Query()
        temp = db.search(entry.name == self.name)
        if len(temp)==0:
            db.insert({'name':self.name,'F':self.F.tolist(),'y':self.y.tolist(),'result1':self.result1.tolist(),'result2':self.result2.tolist()})
        else:
            db.update({'name':self.name,'F':self.F.tolist(),'y':self.y.tolist(),'result1':self.result1.tolist(),'result2':self.result2.tolist()},entry.name==self.name)

# ****************************************************************************
    def load(self):
        db = TinyDB('./data/db.json')
        entry = Query()
        temp = db.search(entry.name == self.name)[0]
        self.F = np.array(temp['F'])
        self.y = np.array(temp['y'])
        self.result1 = np.array(temp['result1'])
        self.result2 = np.array(temp['result2'])
        self.m = self.F.shape[0]
        self.n = self.F.shape[1]
# *********************************************************************************************************************************************
    def display(self):
        print("The values are:\nF= \n",self.F,"\ny=\n",self.y,"\nResult without weight=\n",self.result1,"\nResult with weight=\n",self.result2)
# ****************************************************************************************************************************************************
    def weight(self):
        self.w = np.eye(self.m,self.m)
        for i in range(0,self.m,1):
            self.w[i][i]=float(input("enter the weight:"))
        print(self.w)

# ******************************************************************************************************************************************************************

def display_all_values():
    print('Available Datasets:\n')
    db = TinyDB('./data/db.json')
    temp = db.all()
    for i in temp:
        print(i['name'])
    print("***************************************")

flag = int(input("Do you want to enter data or load from database:(1 for loading from database and 2 for manual entry): "))


if flag==1:
    display_all_values()
    name = str(input("Enter Filenumber"))
    my_model = Model()
    my_model.Name(name)
    my_model.load()
    my_model.run_wo_weight()
    #my_model.display()
    my_model.weight()
    my_model.run_with_weight()
    my_model.display()
    my_model.save()
else:
    name = str(input("Enter Filenumber"))
    my_model = Model()
    my_model.Name(name)
    my_model.get_input()
    my_model.run_wo_weight()
    #my_model.display()
    my_model.weight()
    my_model.run_with_weight()
    my_model.display()
    my_model.save()
