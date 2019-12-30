import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import tkinter.ttk
import pandas as pd



rt_width=1000
rt_hgt=1000

global root
previous_count = '0'


root = tk.Tk()
root.title('卒業単位計算ツール') #タイトル
root.geometry(str(rt_width)+'x'+str(rt_hgt)) #サイズ

def syllabus_select(i):
    def x():
        global kamoku
        global unit
        global kubun
        global syubetsu
        global huriwake
        huriwake = '0'

        if(i==0):
            url = 'https://syllabus.kosen-k.go.jp/Pages/PublicSubjects?school_id=39&department_id=12&year=2019&lang=ja'
        elif(i==1):
            url = 'https://syllabus.kosen-k.go.jp/Pages/PublicSubjects?school_id=39&department_id=13&year=2019&lang=ja'
        elif(i==2):
            url = 'https://syllabus.kosen-k.go.jp/Pages/PublicSubjects?school_id=39&department_id=14&year=2019&lang=ja'
        elif(i==3):
            url = 'https://syllabus.kosen-k.go.jp/Pages/PublicSubjects?school_id=39&department_id=15&year=2019&lang=ja'
        else:
            url = 'https://syllabus.kosen-k.go.jp/Pages/PublicSubjects?school_id=39&department_id=23&year=2019&lang=ja'
        
        if(i==4):
            huriwake = '1'
        df = pd.read_html(url,header = 0)
        df = df[2].drop(df[2].index[[0,1]])
        df['授業科目']=df['授業科目'].apply(lambda x : x.split(' ')[0])
        df = df.fillna(0)
        df.to_csv("syllabus_honka_denki.csv",encoding="cp932")
        if(i==0):
            df.to_csv("syllabus_honka_kikai.csv",encoding="cp932")
        elif(i==1):
            df.to_csv("syllabus_honka_denki.csv",encoding="cp932")
        elif(i==2):
            df.to_csv("syllabus_honka_kiden.csv",encoding="cp932")
        elif(i==3):
            df.to_csv("syllabus_honka_kenkan.csv",encoding="cp932")
        else:
            df.to_csv("syllabus_senkou_denki.csv",encoding="cp932")

        df = pd.read_csv("syllabus_honka_denki.csv", encoding = "cp932")
        kamoku = df["授業科目"]
        unit = df["単位数"]
        kubun = df["科目区分"]
        syubetsu = df["単位種別"]
        makeList()
    return x



#表を作成
def makeList():
    global kamoku
    global unit
    global kubun
    global syubetsu
    num_list = len(kamoku) #リストの数
    frame0 = tk.Frame(root ,bg='white',width = '1000', height = '600')#背景を白に
    frame0.grid(row=0,column=0)
    frame1 = tk.Frame(root ,width = '500', height = '600')#背景を白に
    frame1.grid(row=0,column=1)

    #Canvas widgetを生成
    canvas = tk.Canvas(frame0,width=500,height=600,bg='white') #背景を白に
    canvas.grid(row=1,column=0,columnspan=5)     #7行x5列分

    #スクロールバー
    vbar=tk.ttk.Scrollbar(frame0,orient=tkinter.VERTICAL) #縦方向
    vbar.grid(row=1,rowspan=7,column=5,sticky='ns')        

    #スクロールバーの制御をCanvasに通知する処理
    vbar.config(command=canvas.yview)

    #Canvasの可動域をスクロールバーに通知する処理
    canvas.config(yscrollcommand=vbar.set)

    #スクロール可動域＜＝これがないと、どこまでもスクロールされてしまう。
    #sc_hgt=int(len(kamoku)*30)
    canvas.config(scrollregion=(0,0,500,len(kamoku)*26))

    #Frameを作成
    frame = tk.LabelFrame(canvas, text = "シラバス", bg='white',width = '500', height = '600') #背景を白に

    #frameをcanvasに配置
    canvas.create_window((0,0),window=frame,anchor=tk.NW,width=canvas.cget('width'))   #anchor&lt;=NWで左上に寄せる

    #各ラベルの幅(文字がある場合は文字ユニットとなる)
    c0_width=5  #チェックボックス
    c1_width=30 #科目名
    c2_width=5  #単位数
    c3_width=10 #科目区分
    c4_width=10 #単位種別

    #header row=1に設定する文字列 余白は0に
    e0=tk.Label(frame,width=c0_width,text='select',background='white')
    e0.grid(row=1,column=0,padx=0,pady=0,ipadx=0,ipady=0) #0列目

    e1=tk.Label(frame,width=c1_width,text='授業科目',background='white',anchor='w')
    e1.grid(row=1,column=1,padx=0,pady=0,ipadx=0,ipady=0) #1列目

    e2=tk.Label(frame,width=c2_width,text='単位数',background='white',anchor='w')
    e2.grid(row=1,column=2,padx=0,pady=0,ipadx=0,ipady=0) #2列目

    e3=tk.Label(frame,width=c3_width,text='科目区分',background='white',anchor='w')
    e3.grid(row=1,column=3,padx=0,pady=0,ipadx=0,ipady=0) #3列目 

    e4=tk.Label(frame,width=c4_width,text='単位種別',background='white',anchor='w')
    e4.grid(row=1,column=4,padx=0,pady=0,ipadx=0,ipady=0) #3列目

    btn = tk.Button(frame1,text = "計算",command = hantei)
    btn.grid(row = 0, column = 0, padx=0,pady=0,ipadx=0,ipady=0)

    irow = 2
    irow0=2
    erow=num_list+irow0

    global list_chk	
    list_chk = []
 
    while irow < erow:
        #色の設定
        if irow%2==0:
            color='#cdfff7'  #薄い青
        else:
            color='white'
        i = irow - irow0

        #チェックボックスの設置
        bln=tk.BooleanVar()		
        bln.set(False) 	
        c = tk.Checkbutton(frame,variable = bln,width=c0_width,text='',background='white')
    
        list_chk.append(bln) #チェックボックスの初期値
        #print(list_chk[i].get())

        c.grid(row=irow,column=0,padx=0,pady=0,ipadx=0,ipady=0)  #0列目
        #科目名
        a1=kamoku[i]
        b1=tk.Label(frame,width=c1_width,text=a1,background=color,anchor='w')
        b1.grid(row=irow,column=1,padx=0,pady=0,ipadx=0,ipady=0) #1列目
        #単位数
        a2=unit[i]
        b2=tk.Label(frame,width=c2_width,text=a2,background=color,anchor='w')
        b2.grid(row=irow,column=2,padx=0,pady=0,ipadx=0,ipady=0) #2列目
        #科目区分   
        a3=kubun[i]
        b3=tk.Label(frame,width=c3_width,text=a3,background=color,anchor='w')
        b3.grid(row=irow,column=3,padx=0,pady=0,ipadx=0,ipady=0) #3列目
        #単位種別      
        a4=syubetsu[i]
        b4=tk.Label(frame,width=c4_width,text=a4,background=color,anchor='w')
        b4.grid(row=irow,column=4,padx=0,pady=0,ipadx=0,ipady=0) #3列目
    
        irow=irow+1

    #リストの下に設置するチェックボックスとボタン
    if(previous_count == '0'):
        allSelectButton = tk.Button(root,text='全て選択',command=allSelect_click)
        allSelectButton.grid(row=erow,column=0)  #1列目
        allClearButton = tk.Button(root, text='選択解除',command=allClear_click)
        allClearButton.grid(row=erow, column=1)   #1列目
        previousButton = tk.Button(root,text='学科選択に戻る',command=previous)
        previousButton.grid(row=erow, column=2)   #2列目

def hantei():
    if(huriwake=='1'):
        req_unit = ['16', '46', '62']
    else:
        req_unit = ['75', '82', '167']
    kamoku_syubetsu = ['一般', '専門', '合計']
    ippan = 0
    senmon = 0

    for i in range(len(kamoku)):
        if(list_chk[i].get()==True and kubun[i]!= "専門"):
            ippan = ippan + unit[i]
        if(list_chk[i].get()==True and kubun[i]== "専門"):
            senmon = senmon + unit[i]
    
    grad_hantei = [0,0,0]
    if(ippan >= int(req_unit[0])):
        grad_hantei[0] = '単位は足りています'
    else:
        grad_hantei[0] = '卒業できません'
    if(senmon >= int(req_unit[1])):
        grad_hantei[1] = '単位は足りています'
    else:
        grad_hantei[1] = '卒業できません'
    if(senmon + ippan >= int(req_unit[2])):
        grad_hantei[2] = '単位は足りています'
    else:
        grad_hantei[2] = '卒業できません'

    frame2 = tk.LabelFrame(root, text = "判定結果" ,width = '500', height = '600')#背景を白に
    frame2.grid(row=0,column=2)

    c1_width=10  #科目区分
    c2_width=10  #取得単位数
    c3_width=10 #必要単位数
    c4_width=15 #判定

    #header row=1に設定する文字列 余白は0に
    e1=tk.Label(frame2,width=c1_width,text='科目区分',background='white',anchor='w')
    e1.grid(row=1,column=1,padx=0,pady=0,ipadx=0,ipady=0) #1列目

    e2=tk.Label(frame2,width=c2_width,text='取得単位数',background='white',anchor='w')
    e2.grid(row=1,column=2,padx=0,pady=0,ipadx=0,ipady=0) #2列目

    e3=tk.Label(frame2,width=c3_width,text='必要単位数',background='white',anchor='w')
    e3.grid(row=1,column=3,padx=0,pady=0,ipadx=0,ipady=0) #3列目 

    e4=tk.Label(frame2,width=c4_width,text='判定',background='white',anchor='w')
    e4.grid(row=1,column=4,padx=0,pady=0,ipadx=0,ipady=0) #3列目

    
    irow = 2
    irow0=2
    erow=5

    while irow < erow:
        #色の設定
        if irow%2==0:
            color='#cdfff7'  #薄い青
        else:
            color='white'
        i = irow - irow0
        #科目区分
        a1=kamoku_syubetsu[i]
        b1=tk.Label(frame2,width=c1_width,text=a1,background=color,anchor='w')
        b1.grid(row=irow,column=1,padx=0,pady=0,ipadx=0,ipady=0) #1列目
        #取得単位数
        if(i==0):
            a2 = ippan
        elif(i==1):
            a2 = senmon
        else:
            a2 = ippan + senmon
        
        b2=tk.Label(frame2,width=c2_width,text=a2,background=color,anchor='w')
        b2.grid(row=irow,column=2,padx=0,pady=0,ipadx=0,ipady=0) #2列目
        #必要単位数
        a3=req_unit[i]
        b3=tk.Label(frame2,width=c3_width,text=a3,background=color,anchor='w')
        b3.grid(row=irow,column=3,padx=0,pady=0,ipadx=0,ipady=0) #3列目
        #判定     
        a4 = grad_hantei[i]
        b4=tk.Label(frame2,width=c4_width,text=a4,background=color,anchor='w')
        b4.grid(row=irow,column=4,padx=0,pady=0,ipadx=0,ipady=0) #3列目
    
        irow=irow+1


#全て選択をクリック
def allSelect_click():
	for i in range(len(list_chk)):
		list_chk[i].set(True)
 
#選択解除をクリック
def allClear_click():
	for i in range(len(list_chk)):
		list_chk[i].set(False)

def previous():
    global previous_count
    previous_count = '1'
    main()

#main	
def main():	
    
    
    select = ['機械工学科', '電気情報工学科', '機械電子工学科', '建設環境工学科', '創造工学専攻 電気情報工学コース']
    for  i in range(len(select)):
        btn = tk.Button(root, text = select[i] ,relief = "groove",command = syllabus_select(i))
        btn.place(x=10, y=10+i*30)
    
    #ウィンドウを動かす
    root.mainloop()

if __name__ == '__main__':
	main()