from init import * 
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from ttkthemes import ThemedTk
from PIL import Image,ImageTk
import serial
import time, sys 



current_number=-1
mode=0
time_delay=1000
bits_manual_value=['0','0','0','0','0','0','0','0']

def debugstart(num_inputs,num_outputs,in_port):

    def mouse_wheel(event):

        direction = 0

        if event.num == 5 or event.delta == -120:
            direction = 1
        if event.num == 4 or event.delta == 120:
           direction = -1
        my_canvas.yview_scroll(direction, "units")


    def manualbit(bit):
        global bits_manual_value
        global current_number
        if current_number>=0:
            list_button_select[current_number].config(style='TButton')
        if(bits_manual_value[7-(bit)]=="1"):
            bits_manual_value[7-(bit)]="0"
            manual_bits_button[bit].config(style='TButton')
        elif(bits_manual_value[7-(bit)=="0"]):
            bits_manual_value[7-(bit)]="1"
            manual_bits_button[bit].config(style='inuse.TButton')
        valor=0
        for i in range(0,8):
            valor+= int(bits_manual_value[7-(i)])*(2**i)
        print(valor)
        
        current_number=valor

        process(valor)
   
        
        list_button_select[current_number].config(style='inuse.TButton')
        print(bits_manual_value)

    


    def generate_lists(inputs,outputs):
        for i in range (2**inputs):
            bin_in=str(bin(i))         
            bin_in=bin_in[2:]               
            bin_in='0'*(8-len(bin_in))+bin_in     
            for x in range(8):
                bit_in[x].append(int(bin_in[7-x]))
        for i in range(0,2**inputs):
            for x in range(0,8):
                bit_out[x].append(StringVar())
                bit_out[x][i].set("x")


    def press(entrada):
        global current_number
        list_button_select[current_number].config(style='TButton')
        current_number=entrada
        list_button_select[current_number].config(style='inuse.TButton')
        process(entrada)


    def play():
        global mode
        mode=1
        run()
    
    def run():
        global mode
        global current_number
        while True:
            if mode==0:
                return
            if current_number==(2**inputs)-1:
                return
            if current_number!=-1:
                list_button_select[current_number].config(style='TButton')
            current_number+=1
            process(current_number)
            list_button_select[current_number].config(style='inuse.TButton')
            home.update()
            global time_delay
            if mode==1:
                if time_entry.get()!="":
                    time_delay=int(time_entry.get())
                else:
                    time_delay=100 
                time.sleep(time_delay/1000)
            if list_check_var[current_number].get()==True:
                return

    def pause():
        global mode
        mode=0

    def fast():
        global mode
        mode=2
        run()

    def next():
        global current_number
        if current_number==(2**inputs)-1:
            return
        if current_number!=-1:
            list_button_select[current_number].config(style='TButton')
        current_number+=1
        process(current_number)
        list_button_select[current_number].config(style='inuse.TButton')

    def prev():
        global current_number
        if current_number<=0:
            return
        list_button_select[current_number].config(style='TButton')    
        current_number-=1
        list_button_select[current_number].config(style='inuse.TButton')
        process(current_number)


    def read(numero):
        ser.write((str(numero)+';').encode("utf-8"))
        valor=str(ord(ser.read()))


    def process(indice):
        ser.write((str(indice)+';').encode("utf-8"))
        ndecimal=ord(ser.read())

        read_out=str(bin(ndecimal))    
        read_out=read_out[2:]              
        read_out='0'*(8-len(read_out))+read_out
        print(current_number)

        input_value=str(bin(indice))
        input_value=input_value[2:]
        input_value='0'*(8-len(input_value))+input_value



        for bit in range(0,inputs):
            if(input_value[7-bit]=="1"):
                manual_bits_button[bit].config(style='inuse.TButton')
            elif (input_value[7-bit]=="0"):
                manual_bits_button[bit].config(style='TButton')
        step_row.grid(row=int(current_number))
        for x in range(8):
            bit_out[x][indice].set(read_out[7-x])
            val_manual_out[x].set(read_out[7-x])

    inputs=int(num_inputs)
    outputs=int(num_outputs)
    portset=in_port

    home=ThemedTk(background=True)
    home.config(theme=def_theme)
    home.minsize(400,400)

    #Imágenes
    im_play = PhotoImage(file=("Y:/Universidad/TFG/CodigoTFG/Python/docs/icons/play.png"))
    im_play = im_play.subsample(4)

    im_pause = PhotoImage(file=('Y:/Universidad/TFG/CodigoTFG/Python/docs/icons/pause.png'))
    im_pause=im_pause.subsample(4)

    im_stop = PhotoImage(file=(sys.path[0]+'/docs/icons/stop.png'))
    im_stop=im_stop.subsample(4)

    im_next = PhotoImage(file=(sys.path[0]+'/docs/icons/down.png'))
    im_next=im_next.subsample(4)

    im_prev = PhotoImage(file=(sys.path[0]+'/docs/icons/up.png'))
    im_prev=im_prev.subsample(4)

    im_ff = PhotoImage(file=(sys.path[0]+'/docs/icons/fast.png'))
    im_ff=im_ff.subsample(4)

    im_left= PhotoImage(file=(sys.path[0]+'/docs/icons/left.png'))
    im_left=im_left.subsample(20)

    home.iconbitmap(sys.path[0]+'/docs/icons/logo.ico')


    inuse=ttk.Style()
    inuse.theme_use(def_theme)
    inuse.configure('inuse.TButton',foreground='red')


    home.title(t_head_debug)
    home.geometry("400x400")

    #Texto in-out
    main_frame=Frame(home)
    txt_in="IN"
    txt_out="OUT"
    Label(text=txt_in).place(relx=0.27+0.0086*num_inputs,rely=0)
    Label(text=txt_out).place(relx=0.34+0.0086*num_inputs+0.0086*(num_outputs-1)*2,rely=0)


    #main_frame.pack(side=TOP,fill=BOTH,expand=1, pady=0)
    main_frame.place(x=0,y=0,relx=0,rely=0.05,relwidth=1,relheight=0.78)

    my_canvas=Canvas(main_frame,highlightthickness=0)
    my_canvas.config(bg='#d8d8d8')
    my_canvas.pack(side=TOP,fill=BOTH,expand=1)
    

    scrollbar = ttk.Scrollbar(my_canvas, orient= VERTICAL, command=my_canvas.yview)
    scrollbar.pack(side=RIGHT,fill=Y)


    my_canvas.bind("<MouseWheel>", mouse_wheel)

    my_canvas.configure(yscrollcommand=scrollbar.set)
    my_canvas.bind('<Configure>',lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    second_frame=Frame(my_canvas)

    my_canvas.create_window((60,0),window=second_frame, anchor="nw")



    step_row=Label(second_frame,image=im_left)
    step_row.grid(column=4+inputs+outputs,row=0)

    

    manual_bits_button=[]

    #Manipulación de bits
    for i in range(0,inputs):
        manual_bits_button.append(ttk.Button(home,text=str(i),command=lambda x=int(i): manualbit(x),width=4))
        manual_bits_button[i].place(relx=0.77-0.095*i,rely=0.9)
    manual_out=[]
    val_manual_out=[]
    for i in range(0,8):
        val_manual_out.append(StringVar())
        val_manual_out[i].set("x")
    for i in range(0,outputs):
        manual_out.append(ttk.Label(home,textvariable=val_manual_out[i]))
        manual_out[i].place(relx=0.79-0.095*i,rely=0.84)

    list_button_select=[]
    list_check=[]
    list_check_var=[]

    b0=[];b1=[];b2=[];b3=[];b4=[];b5=[];b6=[];b7=[]
    bit_in=[b0,b1,b2,b3,b4,b5,b6,b7]

    out0=[];out1=[];out2=[];out3=[];out4=[];out5=[];out6=[];out7=[]
    bit_out=[out0,out1,out2,out3,out4,out5,out6,out7]
    



    ser=serial.Serial(
        baudrate=115200,
        timeout=def_timeout,
        port=portset
    )
    ser.read()
    generate_lists(inputs,outputs)

    for i in range(0,2**inputs):
        list_button_select.append(ttk.Button(second_frame, text=str(i),command=lambda x=int(i): press(x),width=3))
        list_check_var.append(BooleanVar(second_frame))
        list_check.append(Checkbutton(second_frame,variable=list_check_var[i]))
        
        list_button_select[i].grid(column=0,row=i)
        list_check[i].grid(column=1,row=i)
        for x in range(0,inputs):
            dato=bit_in[inputs-x-1][i]
            Label(second_frame, text=str(dato)).grid(column=x+2,row=i)
    Label(second_frame,width=4).grid(column=3+inputs)
    for filas in range(0,2**inputs):
        for columnas in range(0,outputs):
            Label(second_frame,textvariable=bit_out[columnas][filas]).grid(column=inputs+2+1+outputs-columnas,row=filas)


    

    b_play=Button(my_canvas,image=im_play,text="play", command=play)
    b_play.place(relx=0,rely=0)

    b_pause=Button(my_canvas,text="pause",image=im_pause,command=pause)
    b_pause.place(relx=0,rely=0.16)

    b_next=Button(my_canvas,text="next",image=im_next,command=next)
    b_next.place(relx=0,rely=0.32)

    b_prev=Button(my_canvas,text="prev",image=im_prev,command=prev)
    b_prev.place(relx=0,rely=0.48)

    b_ff=Button(my_canvas,text="",image=im_ff,command=fast)
    b_ff.place(relx=0,rely=0.64)
   
    time_title=t_label_time_step[0:t_label_time_step.index(" ")]+"\n"+t_label_time_step[t_label_time_step.index(" ")+1:]
    
    
    Label(text=time_title).place(relx=0,rely=0.67)
    time_entry=Entry(my_canvas,width=8)
    time_entry.place(relx=0,rely=0.9)

    windowWidth = home.winfo_reqwidth()
    windowHeight = home.winfo_reqheight()
    positionRight = int(home.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(home.winfo_screenheight()/2 - windowHeight/2)
    home.geometry("+{}+{}".format(positionRight, positionDown))

    home.mainloop()

#debugstart(8,8,"COM7")