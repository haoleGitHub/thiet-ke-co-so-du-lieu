from os import curdir, terminal_size
from sqlite3.dbapi2 import enable_callback_tracebacks
from tkinter import *
from tkinter import messagebox
import sqlite3
from tkinter import ttk
from tkinter import font
from typing import Collection

win = Tk()
win.title("NHÓM 8")
win.geometry("700x500")
win.configure(background="#9999cc")
# back = PhotoImage(file='background-login.png')
# bgr = Label(win, image=back)
# bgr.place(x=0, y=0)

Label(win, text="QUẢN LÝ SINH VIÊN", font='times 40 bold').pack(ipady=20)

# cửa sổ sinh viên
def sinhVienWin():
    winSV = Tk()
    winSV.title("Sinh Viên")
    winSV.geometry("700x570")
    winSV.configure(background="#aaaaaa")

    conn = sqlite3.connect("quanlisinhvien.db")
    cur = conn.cursor()

    treeFrame = Frame(winSV)
    treeFrame.pack(pady=20)

    treeScroll = Scrollbar(treeFrame)
    treeScroll.pack(side=RIGHT, fill=Y)
    svTree = ttk.Treeview(treeFrame, yscrollcommand=treeScroll.set, height=10)
    treeScroll.config(command=svTree.yview)

    svTree['column'] = ("StudentID", "StudentName", "StudentAddress", "ClassID")

    svTree.column("#0", width=0, stretch=NO)
    svTree.column("StudentID", anchor=CENTER, width=100)
    svTree.column("StudentName", anchor=W, width=150)
    svTree.column("StudentAddress", anchor=W, width=150)
    svTree.column("ClassID", anchor=CENTER, width=100)

    svTree.heading("#0", text="", anchor=W)
    svTree.heading("StudentID", text="Mã Sinh Viên", anchor=CENTER)
    svTree.heading("StudentName", text="Họ Tên", anchor=CENTER)
    svTree.heading("StudentAddress", text="Địa Chỉ", anchor=CENTER)
    svTree.heading("ClassID", text="Lớp", anchor=CENTER)

    svTree.pack()

    cur.execute("select * from Student")
    rows = cur.fetchall()
    for i in svTree.get_children():
        svTree.delete(i)
    for row in rows:
            svTree.insert("", END, values=row)

    # reset treeview
    def resetTreeview():
        cur.execute("SELECT * FROM Student ")
        records = cur.fetchall()
        for i in svTree.get_children():
            svTree.delete(i)
        for row in records:
            svTree.insert("", END, values=row)

    # reset entry
    def resetEntry():
        maEntry.delete(0, END)
        tenEntry.delete(0, END)
        diaChiEntry.delete(0, END)
        lopCombobox2.delete(0, END)
        maEntry.focus_set()

    # xem toàn bộ danh sách sinh viên
    def showAll():
        cur.execute("select * from Student")
        rows = cur.fetchall()
        for i in svTree.get_children():
            svTree.delete(i)
        for row in rows:
            svTree.insert("", END, values=row)
        conn.commit()
        
    # lọc lớp trong combobox
    def locClass():
        cur.execute("select * from Student where ClassID = (:classid)", {
            'classid': lopCombobox.get()
        })
        if not lopCombobox.get():
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn lớp!")
        else:
            cla = cur.fetchall()
            for i in svTree.get_children():
                svTree.delete(i)
            for row in cla:
                svTree.insert("", END, values=row)
        conn.commit()

    # thêm sinh viên
    def insertSv():
        try: 
            A = maEntry.get()
            B = tenEntry.get()
            C = diaChiEntry.get()
            D = lopCombobox2.get()

            cur.execute("select ClassID from Class")
            rowss = cur.fetchall()

            if not A or not B or not C or not D:
                messagebox.showwarning("Cảnh báo", "Hãy điền đầy đủ thông tin!")
                return

            if D != rowss:
                messagebox.showerror("Lỗi", "Không tồn tại lớp này!!!")
                return
                
            else:
                cur.execute("INSERT INTO Student VALUES (:StudentID, :StudentName, :StudentAddress, :ClassID)",
                                {
                                    'StudentID': maEntry.get(),
                                    'StudentName': tenEntry.get(),
                                    'StudentAddress': diaChiEntry.get(),
                                    'ClassID': lopCombobox2.get(),
                                })
                messagebox.showinfo("Thông báo", "Đã thêm sinh viên!")

                conn.commit()

            resetTreeview()
            resetEntry()

        except sqlite3.Error as e:
            messagebox.showerror("Error", e)

    # cập nhật thông tin lại cho sinh viên
    def updateSv():
        try:
            A = maEntry.get()
            B = tenEntry.get()
            C = diaChiEntry.get()
            D = lopCombobox2.get()
            if not A or not B or not C or not D:
                messagebox.showerror('Error', 'hãy điền đầy đủ thông tin!!!')
                return
            if messagebox.askyesno('Confirm', 'Bạn có chắc là sẽ cập nhật cho sinh viên này!!!'):
                cur.execute("select StudentID from Student where StudentID = ?", (A,))
                rows = cur.fetchall()
                if not rows:
                    messagebox.showerror('Lỗi', 'Mã sinh viên không tồn tại !!!')
                    return
                else:
                    cur.execute("""UPDATE Student SET
                                    StudentName = :StdName,
                                    StudentAddress = :StdAdd,
                                    ClassID = :ClaID
                                    WHERE StudentID = :StudentID""",
                                {
                                    'StudentID': maEntry.get(),
                                    'StdName': tenEntry.get(),
                                    'StdAdd': diaChiEntry.get(),
                                    'ClaID': lopCombobox2.get(),
                                })
                conn.commit()
                messagebox.showinfo("Thông báo", "Đã cập nhật cho sinh viên!")

                resetTreeview()
                resetEntry()

        except sqlite3.Error as e:
            messagebox.showerror('Error', e)
            
    # xóa sinh viên
    def deleteSv():
        try:
            """A = maEntry.get()
            if not stdId:
                messagebox.showwarning("Lỗi", "Bạn phải chọn mã sinh viên!!!"")
                return"""
            if messagebox.askyesno("Xác nhận", "Bạn muốn xóa sinh viên này?"):
                x = svTree.selection()[0]
                svTree.delete(x)
                xoa_rac = maEntry.get()

                cur.execute("DELETE from Student WHERE StudentID= ? ", (xoa_rac,))

                conn.commit()
                #conn.close()

                maEntry.delete(0, END)
                tenEntry.delete(0, END)
                diaChiEntry.delete(0, END)
                lopCombobox2.delete(0, END)
        except sqlite3.Error as e:
            messagebox.showerror('Error', e)
        
     # Search By Name
    
    # tìm theo tên sinh viên
    def findName():
        try:
            # tìm kiếm theo tên
            lookup_record = tenEntry.get()
            lookup_record2 = maEntry.get()
            if not lookup_record:
                messagebox.showerror('Error...', 'Bạn phải nhập tên sinh viên!')
                return
            sql_search = 'SELECT * FROM Student WHERE' + ' ' + \
                'StudentName' + ' ' + 'LIKE "%' + lookup_record + '%"'
            cur.execute(sql_search)
            #cur.execute("SELECT * FROM Student WHERE StudentName = ?",('%' + lookup_record,))
            rows = cur.fetchall()
            if not rows:
                messagebox.showerror('Error', 'Tên sinh viên này không tồn tại!!!')
                return
            for i in svTree.get_children():
                svTree.delete(i)
            for row in rows:
                svTree.insert("", END, values=row)

            tenEntry.delete(0, END)

        except sqlite3.Error as e:
            messagebox.showerror('Error', e)

    # tìm theo mã sinh viên
    def findID():
        try:
            lookup_record = maEntry.get()
            if not lookup_record:
                messagebox.showerror('Error', 'Bạn phải nhập mã sinh viên!!!')
                return
            cur.execute(
                "SELECT * FROM Student WHERE StudentID = ?", (lookup_record,))
            rows = cur.fetchall()
            if not rows:
                messagebox.showerror(
                    'Error', 'Mã sinh viên này không tồn tại!!!')
                return
            for i in svTree.get_children():
                svTree.delete(i)
            for row in rows:
                svTree.insert("", END, values=row)
            maEntry.delete(0, END)
        except sqlite3.Error as e:
            messagebox.showerror('Error', e)

    # chọn sinh viên
    def chonSv(e):
        maEntry.delete(0, END)
        tenEntry.delete(0, END)
        diaChiEntry.delete(0, END)
        lopCombobox2.delete(0, END)

        selected = svTree.focus()
        values = svTree.item(selected, 'values')

        maEntry.insert(0, values[0])
        tenEntry.insert(0, values[1])
        diaChiEntry.insert(0, values[2])
        lopCombobox2.insert(0, values[3])

    svTree.bind("<ButtonRelease-1>", chonSv)

    # ô thông tin
    frame1 = LabelFrame(winSV, text="Thông tin")
    frame1.place(x=15, y=310, width=670, height=100)

    maSv = Label(frame1, text="Mã sinh viên:")
    maSv.grid(row=0, column=0, padx=10, pady=10)
    maEntry = Entry(frame1, width=15)
    maEntry.grid(row=0, column=1)

    tenSv = Label(frame1, text="Họ tên:")
    tenSv.grid(row=0, column=2, padx=10, pady=10)
    tenEntry = Entry(frame1, width=25)
    tenEntry.grid(row=0, column=3)

    diaChiSv = Label(frame1, text="Địa chỉ:")
    diaChiSv.grid(row=0, column=4, padx=10, pady=10)
    diaChiEntry = Entry(frame1, width=25)
    diaChiEntry.grid(row=0, column=5)

    """lopSv = Label(frame1, text="Lớp:")
    lopSv.grid(row=1, column=0, padx=10, pady=10)
    lopEntry = Entry(frame1, width=15)
    lopEntry.grid(row=1, column=1)"""

    Label(frame1, text="Lớp: ").grid(row=1, column=0)
    lopCombobox2 = ttk.Combobox(frame1, width=12)
    lopCombobox2.grid(row=1, column=1)
    lopList = cur.execute("select ClassID from Class")
    lopCombobox2["values"] = [r for r, in lopList]

    # nút bấm và combobox
    showAllBtn = Button(winSV, text="Xem tất cả", command=showAll, font="times 15 bold")
    showAllBtn.place(x=560, y=260)

    Label(winSV, text="Chọn lớp: ", font="times 15", bg="#aaaaaa").place(x=0, y=260)
    lopCombobox = ttk.Combobox(winSV, width=10, font="times 15")
    lopCombobox.place(x=100, y=260)
    lopList = cur.execute("select ClassID from Class")
    lopCombobox["values"] = [r for r, in lopList]

    locClassBtn = Button(winSV, text="Lọc", font="times 12 bold", width=7, command=locClass)
    locClassBtn.place(x=240, y=260)

    insertBtn = Button(winSV, text="Thêm", font="times 18 bold", width=10, command=insertSv)
    insertBtn.place(x=100, y=430)

    updateBtn = Button(winSV, text="Cập nhật", font="times 18 bold", width=10, command=updateSv)
    updateBtn.place(x=280, y=430)

    deleteBtn = Button(winSV, text="Xóa", font="times 18 bold", width=10, command=deleteSv)
    deleteBtn.place(x=460, y=430)

    findNameBtn = Button(winSV, text="Tìm theo tên", font="times 18 bold", width=10, command=findName)
    findNameBtn.place(x=370, y=500)

    findIdBtn = Button(winSV, text="Tìm theo mã", font="times 18 bold", width=10, command=findID)
    findIdBtn.place(x=190, y=500)

# cửa sổ lớp
def lopWin():
    winLop = Tk()
    winLop.title("Lớp")
    winLop.geometry("500x650")
    winLop.configure(background="#aaaaaa")

    conn = sqlite3.connect("quanlisinhvien.db")
    cur = conn.cursor()
    cur.execute("select * from Class")
    rows = cur.fetchall()

    treeFrame = Frame(winLop)
    treeFrame.pack(pady=20)

    treeScroll = Scrollbar(treeFrame)
    treeScroll.pack(side=RIGHT, fill=Y)
    lopTree = ttk.Treeview(treeFrame, yscrollcommand=treeScroll.set, height=10)
    treeScroll.config(command=lopTree.yview)

    lopTree['column'] = ("ClassID", "ClassName", "ClassYear")

    lopTree.column("#0", width=0, stretch=NO)
    lopTree.column("ClassID", anchor=CENTER, width=100)
    lopTree.column("ClassName", anchor=W, width=150)
    lopTree.column("ClassYear", anchor=CENTER, width=150)

    lopTree.heading("#0", text="", anchor=W)
    lopTree.heading("ClassID", text="Mã lớp", anchor=CENTER)
    lopTree.heading("ClassName", text="Tên lớp", anchor=CENTER)
    lopTree.heading("ClassYear", text="Niên khóa", anchor=CENTER)

    lopTree.pack()

    for row in rows:
        lopTree.insert("", END, values=row)

    def chonLop(e):
        maEntry.delete(0, END)
        tenEntry.delete(0, END)
        nienKhoaEntry.delete(0, END)

        selected = lopTree.focus()
        values = lopTree.item(selected, 'values')

        maEntry.insert(0, values[0])
        tenEntry.insert(0, values[1])
        nienKhoaEntry.insert(0, values[2])

    lopTree.bind("<ButtonRelease-1>", chonLop)

    # xem các lớp
    def show():
        cur.execute("select * from Class")
        rows = cur.fetchall()
        for i in lopTree.get_children():
            lopTree.delete(i)
        for row in rows:
            lopTree.insert("", END, values=row)

    # thêm lớp
    def insertLop():
        try:
            A = maEntry.get()
            B = tenEntry.get()
            C = nienKhoaEntry.get()
            if not A or not B or not C:
                messagebox.showwarning("Cảnh báo", "Hãy điền đầy đủ thông tin!")
                return
            if messagebox.askyesno("Xác nhận", "Bạn muốn thêm lớp này?"):
                cur.execute("select ClassID from Class where ClassID = ?", (A,))
                rows = cur.fetchall()
                if not rows:
                    cur.execute("INSERT INTO Class VALUES (:ClassID, :ClassName, :ClassYear)",
                                    {
                                        'ClassID': maEntry.get(),
                                        'ClassName': tenEntry.get(),
                                        'ClassYear': nienKhoaEntry.get(),
                                    })
                    messagebox.showinfo("Thông báo", "Đã thêm một lớp!")

                    conn.commit()
                    show()
                else:
                    messagebox.showerror("Lỗi", "Lớp này đã tồn tai")

            maEntry.delete(0, END)
            tenEntry.delete(0, END)
            nienKhoaEntry.delete(0, END)

        except sqlite3.Error as e:
            messagebox.showerror("Error", e)

    # cập nhật cho lớp
    def updateLop():
        try:
            A = maEntry.get()
            B = tenEntry.get()
            C = nienKhoaEntry.get()
            if not A or not B or not C:
                messagebox.showerror('Error', 'Hãy điền đầy đủ thông tin!!!')
                return
            if messagebox.askyesno('Confirm', 'Bạn muốn cập nhật cho lớp này?'):
                cur.execute(
                    "select ClassID from Class where ClassId = ?", (A,))
                rows1 = cur.fetchall()
                if not rows1:
                    messagebox.showerror("Lỗi", "Không tồn tại lớp này!!!")
                else:
                    cur.execute("""UPDATE Class SET
                                        ClassName = :ClaName,
                                        ClassYear = :ClaYear
                                        WHERE ClassID = :ClaID""",
                                    {
                                        'ClaID': maEntry.get(),
                                        'ClaName': tenEntry.get(),
                                        'ClaYear': nienKhoaEntry.get(),
                                    })
                    conn.commit()
                    messagebox.showinfo("Thông báo", "Đã cập nhật cho lớp!")

                    show()

                    maEntry.delete(0, END)
                    tenEntry.delete(0, END)
                    nienKhoaEntry.delete(0, END)

        except sqlite3.Error as e:
            messagebox.showerror('Error', e)

    # tìm kiếm theo mã lớp
    def findId():
        try:
            lookup_record = lopCombobox.get()
            if not lookup_record:
                messagebox.showerror('Error', 'Hãy chọn một lớp!!!')
                return
            cur.execute(
                "SELECT * FROM Class WHERE ClassID = ?", (lookup_record,))
            rows = cur.fetchall()
            if not rows:
                messagebox.showerror('Error', 'Lớp không tồn tại!!!')
                return

            for i in lopTree.get_children():
                lopTree.delete(i)
            for row in rows:
                lopTree.insert("", END, values=row)

            lopCombobox.delete(0, END)
        except sqlite3.Error as e:
            messagebox.showerror('Error', e)

    # tìm kiếm theo tên lớp
    def findName():
        try:
            lookup_record = tenEntry.get()
            if not lookup_record:
                messagebox.showerror('Error', 'Hãy điền tên lớp vào!!!')
                return

            sql_search = 'SELECT * FROM Class WHERE' + ' ' + \
                'ClassName' + ' ' + 'LIKE "%' + lookup_record + '%"'
            cur.execute(sql_search)

            rows = cur.fetchall()
            if not rows:
                messagebox.showerror(
                    'Error', 'Tên lớp không tồn tại!!!')
                return

            for i in lopTree.get_children():
                lopTree.delete(i)
            for row in rows:
                lopTree.insert("", END, values=row) 

            tenEntry.delete(0, END)

        except sqlite3.Error as e:
            messagebox.showerror('Error', e)

    # ô thông tin
    frame1 = LabelFrame(winLop, text="Thông tin")
    frame1.place(x=15, y=280, width=470, height=100)

    maLop = Label(frame1, text="Mã lớp:")
    maLop.grid(row=0, column=0)
    maEntry = Entry(frame1, width=15)
    maEntry.grid(row=0, column=1)

    tenLop = Label(frame1, text="Tên lớp:")
    tenLop.grid(row=0, column=2, padx=10, pady=10)
    tenEntry = Entry(frame1, width=25)
    tenEntry.grid(row=0, column=3)

    nienKhoa = Label(frame1, text="Niên khóa:")
    nienKhoa.grid(row=1, column=0, padx=10, pady=10)
    nienKhoaEntry = Entry(frame1, width=15)
    nienKhoaEntry.grid(row=1, column=1)

    Label(frame1, text="Chọn lớp: ").grid(row=1,column=2)
    lopCombobox = ttk.Combobox(frame1, width=22)
    lopCombobox.grid(row=1, column=3, padx=10, pady=10)
    lopList = cur.execute("select ClassID from Class")
    lopCombobox["values"] = [r for r, in lopList]

    # nút bấm (thêm, cập nhật, xóa)
    insertBtn = Button(winLop, text="Thêm", font="times 18 bold", width=10, command=insertLop)
    insertBtn.place(x=70, y=415)

    updateBtn = Button(winLop, text="Cập nhật", font="times 18 bold", width=10, command=updateLop)
    updateBtn.place(x=280, y=415)

    findIdBtn = Button(winLop, text="Tìm theo mã", font="times 18 bold", width=10, command=findId)
    findIdBtn.place(x=70, y=497)

    findNameBtn = Button(winLop, text="Tìm theo tên", font="times 18 bold", width=10, command=findName)
    findNameBtn.place(x=280, y=497)

    showClassBtn = Button(winLop, text="Xem tất cả", font="times 18 bold", width=10, command=show)
    showClassBtn.place(x=175, y=580)

# cửa sổ môn học
def monHocWin():
    winMonHoc = Tk()
    winMonHoc.title("Môn Học")
    winMonHoc.geometry("500x620")
    winMonHoc.configure(background="#aaaaaa")

    conn = sqlite3.connect("quanlisinhvien.db")
    cur = conn.cursor()
    cur.execute("select * from Subject")
    rows = cur.fetchall()

    treeFrame = Frame(winMonHoc)
    treeFrame.pack(pady=20)

    treeScroll = Scrollbar(treeFrame)
    treeScroll.pack(side=RIGHT, fill=Y)
    monHocTree = ttk.Treeview(treeFrame, yscrollcommand=treeScroll.set, height=10)
    treeScroll.config(command=monHocTree.yview)

    monHocTree['column'] = ("SubjectID", "SubjectName", "Units")

    monHocTree.column("#0", width=0, stretch=NO)
    monHocTree.column("SubjectID", anchor=CENTER, width=100)
    monHocTree.column("SubjectName", anchor=W, width=200)
    monHocTree.column("Units", anchor=CENTER, width=100)

    monHocTree.heading("#0", text="", anchor=W)
    monHocTree.heading("SubjectID", text="Mã môn học", anchor=CENTER)
    monHocTree.heading("SubjectName", text="Tên môn học", anchor=CENTER)
    monHocTree.heading("Units", text="Số tín chỉ", anchor=CENTER)

    monHocTree.pack()

    for row in rows:
        monHocTree.insert("", END, values=row)

    def show():
        cur.execute("select * from Subject")
        rows = cur.fetchall()
        for i in monHocTree.get_children():
            monHocTree.delete(i)
        for row in rows:
            monHocTree.insert("", END, values=row)

    def chonMonHoc(e):
        maMonHocEntry.delete(0, END)
        tenMonHocEntry.delete(0, END)
        tinChiEntry.delete(0, END)

        selected = monHocTree.focus()
        values = monHocTree.item(selected, 'values')

        maMonHocEntry.insert(0, values[0])
        tenMonHocEntry.insert(0, values[1])
        tinChiEntry.insert(0, values[2])

    monHocTree.bind("<ButtonRelease-1>", chonMonHoc)

    # thêm môn học
    def insertMonHoc():
        try:
            A = maMonHocEntry.get()
            B = tenMonHocEntry.get()
            C = tinChiEntry.get()
            units = int(C)
            if not A or not B or not C:
                messagebox.showwarning(
                    "Cảnh báo", "Hãy điền đầy đủ thông tin!")
                return
            else:
                if units <= 0:
                    messagebox.showwarning("Cảnh báo", "Số tín chỉ phải lớn 0!!!")
                    return             
                else:
                    cur.execute("INSERT INTO Subject VALUES (:SubjectID, :SubjectName, :Units)",
                                {
                                    'SubjectID': maMonHocEntry.get(),
                                    'SubjectName': tenMonHocEntry.get(),
                                    'Units': tinChiEntry.get(),
                                })
                    conn.commit()
                    messagebox.showinfo("Thông báo", "Đã thêm một môn học!")

                    show()

            maMonHocEntry.delete(0, END)
            tenMonHocEntry.delete(0, END)
            tinChiEntry.delete(0, END)

        except sqlite3.Error as e:
            messagebox.showerror("Error", e)

    # cập nhật môn học
    def updateMonHoc():
        try:
            A = maMonHocEntry.get()
            B = tenMonHocEntry.get()
            C = tinChiEntry.get()
            if not A or not B or not C:
                messagebox.showerror('Error', 'Hãy điền đấy đủ thông tin!!!')
                return
            if messagebox.askyesno('Confirm', 'Bạn thực sự muốn cập nhật cho môn học này?'):
                cur.execute("select * from Subject")
                rows = cur.fetchall()
                if not rows:
                    messagebox.showerror("Lỗi", "Mã môn học không tồn tại!!!")
                    return 
                else:
                    cur.execute("""UPDATE Subject SET
                                    SubjectName = :SubName,
                                    Units = :Units
                                    WHERE SubjectID = :SubID""",
                                {
                                    'SubID': maMonHocEntry.get(),
                                    'SubName': tenMonHocEntry.get(),
                                    'Units': tinChiEntry.get(),
                                })
                    conn.commit()
                    messagebox.showinfo("Thông báo", "Đã cập nhật cho môn học!")

                show()

                maMonHocEntry.delete(0, END)
                tenMonHocEntry.delete(0, END)
                tinChiEntry.delete(0, END)

        except sqlite3.Error as e:
            messagebox.showerror('Error', e)

    # tìm kiếm theo mã môn học
    def findId():
        try:
            lookup_record = monHocCombobox.get()
            if not lookup_record:
                messagebox.showerror('Error', 'Hãy chọn một lớp!!!')
                return
            cur.execute(
                "SELECT * FROM Subject WHERE SubjectID = ?", (lookup_record,))
            rows = cur.fetchall()
            if not rows:
                messagebox.showerror('Error', 'Lớp không tồn tại!!!')
                return

            for i in monHocTree.get_children():
                monHocTree.delete(i)
            for row in rows:
                monHocTree.insert("", END, values=row)

            monHocCombobox.delete(0, END)
        except sqlite3.Error as e:
            messagebox.showerror('Error', e)

    # tìm kiếm theo tên môn học
    def findName():
        try:
            lookup_record = tenMonHocEntry.get()
            if not lookup_record:
                messagebox.showerror('Error', 'Hãy điền tên lớp vào!!!')
                return

            sql_search = 'SELECT * FROM Subject WHERE' + ' ' + \
                'SubjectName' + ' ' + 'LIKE "%' + lookup_record + '%"'
            cur.execute(sql_search)

            rows = cur.fetchall()
            if not rows:
                messagebox.showerror('Error', 'Tên lớp không tồn tại!!!')
                return

            for i in monHocTree.get_children():
                monHocTree.delete(i)
            for row in rows:
                monHocTree.insert("", END, values=row)

            tenMonHocEntry.delete(0, END)

        except sqlite3.Error as e:
            messagebox.showerror('Error', e)

    # tìm kiếm theo số tín chỉ
    def findUnit():
        try:
            lookup_record = tinChiEntry.get()
            if not lookup_record:
                messagebox.showerror('Error', 'Bạn phải nhập số tín chỉ!!!')
                return

            cur.execute(
                "SELECT * FROM Subject WHERE Units = ?", (lookup_record,))
            rows = cur.fetchall()

            if not rows:
                messagebox.showerror('Error', 'Không tồn tại số tín chỉ này!!!')
                return

            for i in monHocTree.get_children():
                monHocTree.delete(i)
            for row in rows:
                monHocTree.insert("", END, values=row)

            tinChiEntry.delete(0, END)

        except sqlite3.Error as e:
            messagebox.showerror('Error', e)

    # ô thông tin
    frame1 = LabelFrame(winMonHoc, text="Thông tin")
    frame1.place(x=15, y=280, width=470, height=100)

    Label(frame1, text="Chọn môn học: ").grid(row=1, column=2)
    monHocCombobox = ttk.Combobox(frame1, width=25)
    monHocCombobox.grid(row=1, column=3, padx=10, pady=10)
    monHocList = cur.execute("select SubjectID from Subject")
    monHocCombobox["values"] = [r for r, in monHocList]

    maMonHoc = Label(frame1, text="Mã môn học:")
    maMonHoc.grid(row=0, column=0)
    maMonHocEntry = Entry(frame1, width=15)
    maMonHocEntry.grid(row=0, column=1)

    tenMonHoc = Label(frame1, text="Tên môn học:")
    tenMonHoc.grid(row=0, column=2, padx=10, pady=10)
    tenMonHocEntry = Entry(frame1, width=28)
    tenMonHocEntry.grid(row=0, column=3)

    tinChi = Label(frame1, text="Số tín chỉ:")
    tinChi.grid(row=1, column=0, padx=10, pady=10)
    tinChiEntry = Entry(frame1, width=15)
    tinChiEntry.grid(row=1, column=1)

    # nút bấm (thêm, cập nhật, xóa)
    insertBtn = Button(winMonHoc, text="Thêm", font="times 15 bold", width=10, command=insertMonHoc)
    insertBtn.place(x=20, y=415)

    updateBtn = Button(winMonHoc, text="Cập nhật", font="times 15 bold", width=10, command=updateMonHoc)
    updateBtn.place(x=160, y=415)

    findIdBtn = Button(winMonHoc, text="Tìm theo mã", font="times 15 bold", width=10, command=findId)
    findIdBtn.place(x=20, y=490)

    findNameBtn = Button(winMonHoc, text="Tìm theo tên", font="times 15 bold", width=10, command=findName)
    findNameBtn.place(x=160, y=490)

    findUnitBtn = Button(winMonHoc, text="Tìm theo số tín chỉ", font="times 15 bold", command=findUnit)
    findUnitBtn.place(x=305, y=490)

    showAll = Button(winMonHoc, text="Xem tất cả", font="times 18 bold", bg="teal", command=show)
    showAll.place(x=350, y=415)

# cửa sổ điểm
def diemWin():
    winDiem = Tk()
    winDiem.title("Điểm")
    winDiem.geometry("500x620")
    winDiem.configure(background="#aaaaaa")

    conn = sqlite3.connect("quanlisinhvien.db")
    cur = conn.cursor()
    cur.execute("select * from StudentGrades")
    rows = cur.fetchall()

    treeFrame = Frame(winDiem)
    treeFrame.pack(pady=20)

    treeScroll = Scrollbar(treeFrame)
    treeScroll.pack(side=RIGHT, fill=Y)
    diemTree = ttk.Treeview(treeFrame, yscrollcommand=treeScroll.set, height=10)
    treeScroll.config(command=diemTree.yview)

    diemTree['column'] = ("StudentID", "SubjectID", "Grades")

    diemTree.column("#0", width=0, stretch=NO)
    diemTree.column("StudentID", anchor=CENTER, width=100)
    diemTree.column("SubjectID", anchor=CENTER, width=100)
    diemTree.column("Grades", anchor=CENTER, width=100)

    diemTree.heading("#0", text="", anchor=W)
    diemTree.heading("StudentID", text="Mã sinh viên", anchor=CENTER)
    diemTree.heading("SubjectID", text="Mã môn học", anchor=CENTER)
    diemTree.heading("Grades", text="Điểm", anchor=CENTER)

    diemTree.pack()

    def locSubject():
        cur.execute("select * from StudentGrades where SubjectID = (:subjectid)", {
            'subjectid': diemCombobox.get()
        })
        cla = cur.fetchall()
        for i in diemTree.get_children():
            diemTree.delete(i)
        for row in cla:
            diemTree.insert("", END, values=row)
        conn.commit()
        diemCombobox.delete(0, END)

    Label(winDiem, text="Chọn mã môn học: ", font="times 14", bg="#aaaaaa").place(x=10, y=260)
    diemCombobox = ttk.Combobox(winDiem, width=5, font="times 15")
    diemCombobox.place(x=160, y=260)
    cur.execute("select SubjectID from Subject")
    lopList = cur.fetchall()
    diemCombobox["values"] = [r for r, in lopList]

    locSubjectBtn = Button(winDiem, text="Lọc", font="times 12 bold", command=locSubject)
    locSubjectBtn.place(x=240, y=260)

    for row in rows:
        diemTree.insert("", END, values=row)

    def show():
        cur.execute("select * from StudentGrades")
        rows = cur.fetchall()
        for i in diemTree.get_children():
            diemTree.delete(i)
        for row in rows:
            diemTree.insert("", END, values=row)

    # chọn sinh viên
    def chonSv(e):
        maSvEntry.delete(0, END)
        tenEntry.delete(0, END)
        maMHEntry.delete(0, END)
        tenMHEntry.delete(0, END)
        diemEntry.delete(0, END)

        selected = diemTree.focus()
        values = diemTree.item(selected, 'values')

        maSvEntry.insert(0, values[0])
        maMHEntry.insert(0, values[1])
        diemEntry.insert(0, values[2])

        stdId = maSvEntry.get()
        subId = maMHEntry.get()

        cur.execute("select StudentName from Student where StudentID = ?", (stdId,))
        rows4 = cur.fetchall()
        for rowstd in rows4:
            tenEntry.insert(0, rowstd[0])

        cur.execute("select SubjectName from Subject where SubjectID = ?", (subId,))
        rows5 = cur.fetchall()
        for rowsub in rows5:
            tenMHEntry.insert(0, rowsub[0])

    def resetEntry():
        maSvEntry.delete(0, END)
        tenEntry.delete(0, END)
        maMHEntry.delete(0, END)
        tenMHEntry.delete(0, END)
        diemEntry.delete(0, END)
        diemEntry.focus_set()

    diemTree.bind("<ButtonRelease-1>", chonSv)

    def insertStdGra():
        try:
            StdID = maSvEntry.get()
            SubID = maMHEntry.get()
            Grade = diemEntry.get()

            if not StdID or not SubID or not Grade:
                messagebox.showerror('Error', 'hãy điền đầy đủ thông tin!!!')
                return
            if messagebox.askyesno('Confirm', 'Bạn thực sự muôn thêm điểm?'):

                cur.execute(
                    "SELECT StudentID FROM Student WHERE StudentID = ?", (StdID,))
                rows1 = cur.fetchall()
                cur.execute(
                    "SELECT SubjectID FROM Subject WHERE SubjectID = ?", (SubID,))
                rows2 = cur.fetchall()

                if not rows2 or not rows1:
                    if not rows1:
                        messagebox.showerror(
                            'Error', 'Mã sinh viên không tồn tại!!!')
                        return
                    if not rows2:
                        messagebox.showerror(
                            'Error', 'Mã môn học không tồn tại!!!')
                        return

                sql = """INSERT INTO StudentGrades (StudentID, SubjectID, Grades)
                VALUES (?, ?, ?)"""
                val = (StdID, SubID, Grade)
                cur.execute(sql, val)
                conn.commit()
                resetEntry()
                show()
                messagebox.showinfo('message', 'Thêm thành công!!!')
                return

        except sqlite3.Error as e:
            messagebox.showerror('Error', e)

    def updateStdGra():
        try:
            StdID = maSvEntry.get()
            SubID = maMHEntry.get()
            Grade = diemEntry.get()
            if not StdID or not SubID or not Grade:
                messagebox.showerror('Error', 'Hãy điền đầy đủ thông tin!!!')
                return
            if messagebox.askyesno('Confirm', 'Bạn thực sự muốn cập nhật?'):
                cur.execute(
                    "SELECT StudentID FROM Student WHERE StudentID = ?", (StdID,))
                rows = cur.fetchall()

                cur.execute(
                    "SELECT StudentID FROM StudentGrades WHERE StudentID = ?", (StdID,))
                rows2 = cur.fetchall()

                cur.execute(
                    "SELECT SubjectID FROM Subject WHERE SubjectID = ?", (SubID,))
                rows3 = cur.fetchall()

                cur.execute(
                    "SELECT SubjectID FROM StudentGrades WHERE StudentID = ?", (StdID,))
                rows4 = cur.fetchall()

                if rows4 != rows3:
                    messagebox.showerror(
                        'Error', 'This student does not have a grade in this subject!!!')
                    return

                if not rows2:
                    messagebox.showerror(
                        'Error', 'This student has not updated grade this subject !!!')
                    return

                if not rows:
                    messagebox.showerror(
                        'Error', 'Mã sinh viên không tồn tại!!!')
                    return
                else:
                    sql = "UPDATE StudentGrades SET Grades= ? WHERE StudentId= ? and SubjectID =?"
                    val = (Grade, StdID, SubID)
                    cur.execute(sql, val)
                    conn.commit()
                    resetEntry()
                    show()
                    messagebox.showinfo('message', 'Cập nhật thành công!!!')
                    return
        except sqlite3.Error as e:
            messagebox.showerror('Error', e)

    def deleteStdGra():
        try:
            StdID1 = maSvEntry.get()
            SubID1 = maMHEntry.get()

            if not StdID1 or not SubID1:
                messagebox.showerror('Error', 'You must input Id!!!')
                return
            if messagebox.askyesno('Confirm', 'Are you sure you want to delete!!!'):
                cur.execute(
                    "SELECT StudentID FROM Student WHERE StudentID = ?", (StdID1,))
                rows1 = cur.fetchall()
                cur.execute(
                    "SELECT SubjectID FROM Subject WHERE SubjectID = ?", (SubID1,))
                rows2 = cur.fetchall()
                cur.execute(
                    "SELECT SubjectID FROM Subject WHERE SubjectID = ?", (SubID1,))
                rows3 = cur.fetchall()
                cur.execute(
                    "SELECT SubjectID FROM StudentGrades WHERE StudentID = ?", (StdID1,))
                rows4 = cur.fetchall()

                if not rows2 or not rows1:
                    if not rows1:
                        messagebox.showerror(
                            'Error', 'This StudentID does not exist!!!')
                        return
                    if not rows2:
                        messagebox.showerror(
                            'Error', 'This Subject does not exist!!!')
                        return
                if rows4 != rows3:
                    messagebox.showerror(
                        'Error', 'This student does not have a grade in this subject!!!')
                    return
                else:
                    query = "DELETE FROM StudentGrades WHERE StudentID=? and SubjectID=?"
                    val = (StdID1, SubID1)
                    cur.execute(query, val)
                    conn.commit()
                    resetEntry()
                    messagebox.showerror('message', 'Successfully Delete!!!')
                    return
        except sqlite3.Error as e:
            messagebox.showerror('Error', e)

    def findStdID():
        try:
            StdID = maSvEntry.get()
            if not StdID:
                messagebox.showerror('Error', 'Hãy nhập mã sinh viên!!!')
                return
            cur.execute(
                "SELECT * FROM StudentGrades WHERE StudentID = ?", (StdID,))
            rows = cur.fetchall()
            if not rows:
                messagebox.showerror('Error', 'Không tìm thấy sinh viên!!!')
                return
            for i in diemTree.get_children():
                diemTree.delete(i)
            for row in rows:
                diemTree.insert("", END, values=row)
            maSvEntry.delete(0, END)
        except sqlite3.Error as e:
            messagebox.showerror('Error', e)

    # ô thông tin
    frame1 = LabelFrame(winDiem, text="Thông tin")
    frame1.place(x=15, y=310, width=470, height=150)

    maSv = Label(frame1, text="Mã sinh viên:")
    maSv.grid(row=0, column=0, padx=10, pady=10)
    maSvEntry = Entry(frame1, width=10)
    maSvEntry.grid(row=0, column=1)

    tenSv = Label(frame1, text="Họ tên:")
    tenSv.grid(row=0, column=2, padx=10, pady=10)
    tenEntry = Entry(frame1, width=31)
    tenEntry.grid(row=0, column=3)

    maMHSv = Label(frame1, text="Mã môn học:")
    maMHSv.grid(row=1, column=0, padx=10, pady=10)
    maMHEntry = Entry(frame1, width=10)
    maMHEntry.grid(row=1, column=1)

    tenMonHoc = Label(frame1, text="Tên môn học:")
    tenMonHoc.grid(row=1, column=2, padx=10, pady=10)
    tenMHEntry = Entry(frame1, width=31)
    tenMHEntry.grid(row=1, column=3)

    diem = Label(frame1, text="Điểm:")
    diem.grid(row=2, column=0, padx=10, pady=10)
    diemEntry = Entry(frame1, width=10)
    diemEntry.grid(row=2, column=1)

    # nút bấm và combobox
    showAllBtn = Button(winDiem, text="Xem tất cả", command=show, font="times 15 bold")
    showAllBtn.place(x=370, y=260)

    insertBtn = Button(winDiem, text="Thêm",
                       font="times 18 bold", width=7, command=insertStdGra)
    insertBtn.place(x=40, y=480)

    updateBtn = Button(winDiem, text="Cập nhật",
                       font="times 18 bold", width=7, command=updateStdGra)
    updateBtn.place(x=200, y=480)

    deleteBtn = Button(winDiem, text="Xóa", font="times 18 bold",
                       width=7, command=deleteStdGra)
    deleteBtn.place(x=350, y=480)

    """findNameBtn = Button(winDiem, text="Tìm theo tên",
                         font="times 18 bold", width=10, command=findName)
    findNameBtn.place(x=370, y=500)"""

    findIdBtn = Button(winDiem, text="Tìm theo mã", font="times 18 bold", width=10, command=findStdID)
    findIdBtn.place(x=180, y=550)

# nút thoát
def exitWin():
    if messagebox.askyesno("Xác nhận", "Bạn thực sự muốn thoát?"):
        exit()

# 5 nút trong main forms
sinhVienBtn = Button(win, text="Sinh Viên", font="times 20 bold", width=10, background="#c6e2ff", command=sinhVienWin)
sinhVienBtn.place(x=170, y=150)

lopBtn = Button(win, text="Lớp", font="times 20 bold", width=10, background="#c6e2ff", command=lopWin)
lopBtn.place(x=370, y=150)

monHocBtn = Button(win, text="Môn học", font="times 20 bold", width=10, background="#c6e2ff", command=monHocWin)
monHocBtn.place(x=170, y=250)

diemBtn = Button(win, text="Điểm", font="times 20 bold", width=10, background="#c6e2ff", command=diemWin)
diemBtn.place(x=370, y=250)

exitBtn = Button(win, text="THOÁT", font="times 20", background="#ff9999", command=exitWin)
exitBtn.place(x=570, y=430)

win.mainloop()
