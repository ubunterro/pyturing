import tkinter as tk
from tkinter import messagebox
import pygubu
from main import *

qCounter = 0
alphSize = 3
guiQs = []


class QGuiStruct:
    label = tk.Label

    def __init__(self):
        self.entries: tk.Entry = []

    def gGrid(self, qCounter):

        qCounter += 1

        self.label.grid(row=qCounter)

        for i in range(0, alphSize):
            self.entries[i].grid(row=qCounter, column=i+1)


class Application:
    def __init__(self, master):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('ui.ui')

        self.mainwindow = builder.get_object('Frame_1', master)
        self.ButtonRun = builder.get_object('ButtonRun')
        self.qFrame = builder.get_object('LabelFrame_1')
        self.buttonAddQ = builder.get_object('ButtonAddQ')
        self.buttonSetAlphSize = builder.get_object('ButtonSetAlphabetSize')
        self.entryAlphSize = builder.get_object('EntryAlphSize')
        self.entryIn = builder.get_object('EntryIn')
        self.listboxOut = builder.get_object('ListboxOut')

        builder.connect_callbacks(self)

    def parseConditions(self):

        conditions = []

        def parseStr(s):
            try:
                rawStr = s.split()

                symbol = rawStr[0]
                setSymbol = rawStr[1]

                if rawStr[2] == "!":
                    goToCondition = -1
                else:
                    if int(rawStr[2]) < -1:
                        print("Состояние < -1")
                        return None
                    else:
                        goToCondition = int(rawStr[2])

                direction = 0

                if rawStr[3] in ["R", "r", "1"]:
                    direction = 1
                elif rawStr[3] in ["L", "l", "-1"]:
                    direction = -1
                elif rawStr[3] in ["!", "THIS", "0"]:
                    direction == 0
                else:
                    print("Неправильно указано направление")
                    return None

                return ConditionContainer(symbol, setSymbol, goToCondition, direction)
            except:
                messagebox.showinfo('Ошибка парсинга', s)
                return None

        #Condition(0, [ConditionContainer("b", "b", 1, RIGHT), ConditionContainer("l", "l", 0, RIGHT)], "")

        for iCond in range(0, qCounter):
            condTable = []
            for j in range(0, alphSize):
                if guiQs[iCond].entries[j].get() != "":
                    print(guiQs[iCond].entries[j].get())
                    if parseStr(guiQs[iCond].entries[j].get()) is not None:
                        condTable.append(parseStr(guiQs[iCond].entries[j].get()))
                    else:
                        return None
            conditions.append(Condition(iCond, condTable, "none"))

        return conditions

    def BtnSetAlphSize(self):
        global alphSize
        try:
            if int(self.entryAlphSize.get()) < 1 or int(self.entryAlphSize.get()) > 10:
                raise OverflowError
            alphSize = int(self.entryAlphSize.get())

            self.buttonSetAlphSize['state'] = 'disabled'
            app.ButtonRun['state'] = 'active'
            app.buttonAddQ['state'] = 'active'
        except:
            app.listboxOut.insert(tk.END, "Некорректная длина алфавита")

    def BtnRun(self):
        e = Engine()

    def BtnAddQ(self):
        global  qCounter
        tQGui = QGuiStruct()

        tQGui.label = tk.Label(self.qFrame, text="q"+str(qCounter))

        for i in range(0, alphSize):
            tQGui.entries.append(tk.Entry(self.qFrame))

        tQGui.gGrid(qCounter)
        qCounter += 1

        guiQs.append(tQGui)


class Engine:
    def __init__(self):

        m = TuringMachine()
        m.setTape(list(app.entryIn.get()))
        conditions = app.parseConditions()

        if conditions is None:
            app.listboxOut.insert(tk.END, "Парсинг не удался")
        else:
            for q in conditions:
                m.addCondition(q)

            print(m.tape)

            m.exec()

        app.entryIn.delete(0, tk.END)
        app.entryIn.insert(0, "".join(m.tape))

        log = m.getLog()

        for s in log:
            app.listboxOut.insert(tk.END, s)

        app.listboxOut.yview(tk.END)


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
