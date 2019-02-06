from numpy import*
from numpy.linalg import inv
from tinydb import TinyDB,Query

class calculation():

    def __init__(self):
        self.n=int(input("enter the number of buses:"))
#####################################################################################################
    def my_input(self,str):                         #only for bus power and angle delta
        print("enter the "+str+":")
        Mat1 = empty((self.n-1, 1))
        for i in range(self.n-1):
            temp = float(input())
            Mat1[i][0] = temp
        #print(Mat1)
        return Mat1

###########################################################################################
    def admit(self):                                    #only for admittance matrix
        #self.n=int(input("enter the number of bus:"))           #to input non diagonal admittance value of transmission line
        self.mat1=empty((self.n,self.n))
        self.mat2=empty((self.n,self.n))
        self.mat3=empty((self.n-1,self.n-1))
        for i in range(self.n):
            for j in range(i+1,self.n,1):
                print("enter the y",i,j)
                self.mat1[i][j]=self.mat1[j][i]=float(input())
        #print(self.mat1)
#****************************************************************************************
        for i in range(self.n):                             # to creat admittance matrix where diagonan element=sum of tr lin connected
            for j in range(self.n):
                if(i==j):
                    for k in range(self.n):
                        self.mat2[i][j]+=self.mat1[i][k]
                else:
                    self.mat2[i][j]=-self.mat1[i][j]
        #print(self.mat2)
#*******************************************************************************************
        for i in range(1,self.n):                       #to reduce the admittance matrix by 1 in both column and row
            for j in range(1,self.n):
                self.mat3[i-1][j-1]=self.mat2[i][j]
        #print(self.mat3)
        return (self.mat3)

#################################################################################################
    def power(self):                                   #only for power of transmission lines
                                                       #this function has n*n pow transmission line matrix and n*1 pow trans line matrix
                                                        #it only returns n*1 trans_line matrix
        self.pow1 = empty((self.n, self.n))                          #creating power transmission line for input
        #print(self.pow1)
        # self.pow22 = empty((self.n, self.n))
        # print(self.pow22)
        for i in range(self.n):
            for j in range(self.n):
                print("enter the power of p", i, j, "transmission line:")
                self.pow1[i][j] = float(input())
        #print(self.pow1)
#**************************************************************************************
        self.pow22 = empty((self.n, self.n))                        #creating empty matrix for transmission line calculation
        self.pow2 = empty((self.n, 1))
        self.pow22_1=empty((self.n,self.n-1))
        # print(self.pow22)
        #print("outside the function:\n",self.pow22)
        for i in range(self.n):
            for j in range(self.n):
                self.pow22[i][j]=0
                self.pow2[i][0] = 0
        for i in range(self.n):
            for j in range(self.n-1):
                self.pow22_1[i][j]=0
        #print(self.pow22)
#*********************************************************************************************
        k=0                                                           #creating the relation between anglr and power trans matrix
        for i in range(self.n):
            for j in range(self.n):
                if self.pow1[i][j]==0:
                    continue
                else:
                    #print(self.pow22)
                    self.pow2[k][0]=self.pow1[i][j]
                    self.pow22[k][i]=self.mat1[i][j]
                    self.pow22[k][j]=-self.mat1[i][j]
                    k=k+1
                    #print(k)
 #************************************************************************************************
        for i in range(self.n):                         #reducing the first column
            k=0
            for j in range(self.n):
                if j==0:
                    continue
                else:
                    self.pow22_1[i][k]=self.pow22[i][j]
                    k=k+1

        #print(self.pow22_1)
        #print(self.pow2)
        return (self.pow2)

##############################################################################################
    def creat(self):                                       #calling power of bus,reactance of each buses,power of transmission line,angle
       self. pow_bus = self.my_input("power of buses")
       self.react = self.admit()
       self.pow_tr =self.power()
       self. ang = self.my_input("voltage angle(delta)")
 ##############################################################################################
    def outputs(self):                                  #display the outputs of following
        print("power of each buses:\n",self.pow_bus)
        print("reactance of transmission line:\n",self.react)
        print("power of each transmission line",self.pow_tr)
        print("voltage angle(delta)",self.ang)
##############################################################################################
    def con_cat(self,mm,nn):                            #concatenate two array along row wise
        con=vstack((mm,nn))
        #print(con)
        return con
#######################################################################################
    def delta_cal(self,mat,pow):                        #calculation to find delta
        #delta=empty((self.n-1,1))
        Ftranspose = transpose(mat)
        mat = dot(Ftranspose, mat)
        mat=inv(mat)
        mat= dot(mat, Ftranspose)
        #x = np.dot(x, self.y)
        delta=dot(mat,pow)
        return delta
###########################################################################################3
    def sub_cases(self):                                    #carry out all possible cases
        print("only using Pij:\n")
        #delta=empty((self.n-1,1))
        #print(self.pow22_1)
        delta=self. delta_cal(self.pow22_1,self.pow_tr)
        print(delta)
#***************************************************************************
        print("only using Pi:\n")
        delta=self.delta_cal(self.react,self.pow_bus)
        print(delta)
#*******************************************************************************
        print("using both Pij and delta")
        self.d1=eye(self.n-1,self.n-1)
        self.s1=self.con_cat(self.pow22_1,self.d1)
        self.s2=self.con_cat(self.pow_tr,self.ang)
        delta=self.delta_cal(self.s1,self.s2)
        print(delta)
#**********************************************************************
        print("using Pij,Pi,delta")
        self.s3=self.con_cat(self.s1,self.react)
        self.s4=self.con_cat(self.s2,self.pow_bus)
        delta=self.delta_cal(self.s3,self.s4)
        print(delta)

#########################################################################################3
    def case(self):                                     #start
        #print("introducing error in Pij")
        self.creat()
        self.sub_cases()



c1=calculation()
#c1.creat()
c1.case()
#c1.outputs()




