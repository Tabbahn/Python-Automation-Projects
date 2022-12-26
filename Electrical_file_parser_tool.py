import tkinter as tk 
import pandas as pd
import matplotlib as plotly
import numpy as np
import os
import math
import xlsxwriter 

#Create GUI
class MyGUI:
    def __init__(self):
        self.root=tk.Tk()
        self.root.geometry("600x250")
        self.root.title("LF File Parser")

        self.stop_state=0

        self.label2=tk.Label(self.root,text="Enter path of folder with LF test files",font=('Arial',11))
        self.label2.pack(padx=10,pady=1)

        self.Entry1=tk.Entry(self.root, width=300, font=('Arial',11))
        self.Entry1.pack(padx=10,pady=10)


        self.label3=tk.Label(self.root,text="Enter desired path for output summary file",font=('Arial',11))
        self.label3.pack(padx=10,pady=1)

        self.Entry2=tk.Entry(self.root, width=300, font=('Arial',11))
        self.Entry2.pack(padx=10)
        
        self.status=tk.StringVar()
        self.status.set("Running...")

        self.check_state=tk.IntVar()
        self.check=tk.Checkbutton(self.root,text="Check if parsing network folder",font=('Arial',10), variable=self.check_state)
        self.check.place(x=280, y=150)
        self.Button=tk.Button(self.root, text="Run", font=('Arial',10),command=self.RunLFParser,bg='green', fg='white')
        self.Button.place(x=160, y=150)

        self.Button2=tk.Button(self.root, text="Stop", font=('Arial',10),command=self.stop_code, bg='red', fg='white')
        self.Button2.place(x=218, y=150)
        
        self.root.mainloop()

    #Define stop code function 
    def stop_code(self):
        self.stop_state=1
        self.label4=tk.Label(self.root,text="Program Stopped. "+final_count+" files processed                            " ,font=('Arial',11))
        self.label4.place(x=150, y=200)


    #Define LF File Parsing Function 
    def RunLFParser(self):
        self.stop_state=0
        E=self.Entry1.get()
        if(self.check_state.get()==0):
            slash="\ "
            E_add=E+slash[0]
        
        else:
            E=E.replace("\\","/")
            slash="/ "
            E_add=E+slash[0]

        try:        
            file_list = os.listdir(E)
        
        except Exception:
                self.label4=tk.Label(self.root,text="Error occured. Check LF folder path is correct.                 " ,fg='red',font=('Arial',11))
                self.label4.place(x=150, y=200)
        
        slash2="\ "
        E2=self.Entry2.get()
        bool=os.path.isdir(E2)
        E2=self.Entry2.get()+slash2[0]
        
        if bool==False:
            self.label4=tk.Label(self.root,text="Error occured. Check output folder path is correct.                 " ,fg='red',font=('Arial',11))
            self.label4.place(x=150, y=200)
            self.stop_code()

        output_summary=pd.DataFrame(columns=['Cont','Date and Time','PC','Username','P/F','Part Number','FR','Pk1','Pk1 M','Valley','Valley M','Pk2 ','Pk2 M'])
        #extract data from each file in folder using for loop
        counter=0;
        for file in file_list:
            filename=E_add+file
            pn_file_temp= file.split('_')
            pn_file=pn_file_temp[1]
            if(pn_file=='92401948m'):
                with open(filename,'r') as f:
                    lines = f.readlines()

                #Define values collected from waveform file
                DT=lines[0]
                cont=lines[1]
                PC=lines[2]
                user=lines[3]
                pn=lines[4]
                pre_or_post=lines[5]
                test_status1=lines[6]
                test_status= test_status1.replace(",","")
                FR=lines[7]
                Pk1=lines[8]
                Pk1_m=lines[9]
                Valley=lines[10]
                Valley_m=lines[11]
                Pk2=lines[12]
                Pk2_m=lines[13]
            
                #Append values to output dataframe ['Cont','Location','Date and Time','PC','Username','P/F','FR','Pk1','Valley','Pk2','Pk1-Pk2','Min','Max','Ratio','Pk1 Freq','Valley Freq','Pk2 Freq','Z']
                DF_line=[cont,DT,PC,user,test_status,pn, FR ,Pk1,Pk1_m,Valley,Valley_m,Pk2,Pk2_m]
                Final_line = [ele.replace("\n","") for ele in DF_line]
                output_summary.loc[len(output_summary)]=Final_line
            #Stop running 
            self.Button2=tk.Button(self.root, text="Stop", font=('Arial',10),command=self.stop_code, bg='red', fg='white')
            self.Button2.place(x=218, y=150)

            #Print out progress for every 1% files processed
            counter=counter+1

            #Progress Update
            time_left_mins=(len(file_list)-counter)/120
            if(time_left_mins>59):
                time_left=str(int(time_left_mins/60))+" hours"
            elif(time_left_mins<60):
                time_left="1 minute"
            else:
                time_left=str(int(time_left_mins))+" minutes"

            status=(str(int(counter))+" files"+" complete...this will take approximately "+time_left)
            self.label4=tk.Label(self.root,text=status,font=('Arial',11))
            self.label4.place(x=150, y=200)
            global final_count
            final_count=str(counter)
            self.root.update()
            #Exit and generate table if stop button pressed
            if (self.stop_state==1):
                break
        
        
        try:
            output_summary.to_excel(E2+"Data_summary.xlsx")
            if self.stop_state==0:
                self.label4=tk.Label(self.root,text="Complete. File summary Data_summary.xlsx generated               " ,fg='green',font=('Arial',11))
                self.label4.place(x=150, y=200)
        except Exception:
            self.label4=tk.Label(self.root,text="Error occured.Try different output folder path. Cannot output summary to folder        " ,fg='red',font=('Arial',11))
            self.label4.place(x=150, y=200)
        self.root.update()
    

MyGUI()
        

    