import os
dirpaths=[]
fileph=[]
filenms=[]
def copyingremoveInitPath(allthings):
    for file in allthings:
        print("目前的路径：",os.getcwd())
        juduipath=os.getcwd()
        newpath=os.path.join(juduipath,file)+"/"
        if os.path.isdir(newpath):
            print("这是个文件夹:",newpath)
            os.chdir(file)
            
            print("目前的路径1：",os.getcwd())
            fanhui=aquireDetails(os.getcwd())
            copyingremoveInitPath(fanhui)
        else:
            filename = os.path.splitext(file)[0];  
            filetype = os.path.splitext(file)[1]; 
            filePath=path+filename+filetype
            newname=path+filename
            print("开始复制:","copy"+" "+filename+filetype+" "+filename+".html")
            

def aquireDetails(path):
    allthings=os.listdir(path)
    return allthings

def copyFiles(allthings):
    #print("current folder:",os.getcwd())
    for file in allthings:
        Olddir = os.path.join(path, file)+"/"
        abspath=os.path.join(os.getcwd(),Olddir)
        print("current abspath:",abspath)
        if os.path.isdir(abspath):     #这个必须是绝对路径才能使用，晕！
            print("this is a folder,now,display it:",file)
            os.chdir(path+"/"+file)
           
            print("current folder,should be entired,otherwise,the operation isn't correct!",os.getcwd())
            details=aquireDetails(os.getcwd())
            #copyFiles(details)
            copyingremoveInitPath(details)
        else:
            filename = os.path.splitext(file)[0];  
            filetype = os.path.splitext(file)[1]; 
            filePath=path+filename+filetype
            newname=path+filename
            print("copying operation now")
            #os.system("copy"+" "+filename+filetype+" "+filename+".html")
            #print ("current operation folder and processing details::",os.getcwd(),"copy"+" "+filename+filetype+" "+filename+".html")


    
        
if __name__ =="__main__":
    """
   
    #print "plz ensure the input folder only containing single layer folder,no folder inside anymore"
    print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    print "<<<<<<<<<<    Rule One: plz ensure the input folder only containing>>>>>>>>>>>>>" 
    print "<<<<<<<<<<    single layer folder,no folder inside anymore        >>>>>>>>>>>>>>"
    print "<<<<<<<<<<    Rule Two: eg.input test11// or test11//dw_base      >>>>>>>>>>>>>>"
    print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    """
    
    path=input("input the path of folders::")
    
    k=aquireDetails(path)
    copyFiles(k)
    print("files in above folders copied done!!!!!!!",fileph)
