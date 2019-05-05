# константы
LEFT = -1
RIGHT = 1

THIS = 0
HALT = -1


class Dbg:
    @staticmethod
    def dprint(str):
        print(str) #might be redeloaded

    @staticmethod
    def fatalError(str):
        print("!!! " + str)  # надо сделать красивое окошечко с варнингом


class TuringMachine:
    conditionsList = [] # список всех состояний (q) Машины
    tape = []  # лента
    tapePtr = 0  # текущая позиция головки
    condition = 0  # текущее состояние
    isRunning = True

    def setTape(self, tape):
        TuringMachine.tape = tape

    def addCondition(self, condition):
        TuringMachine.conditionsList.append(condition)

    @staticmethod
    def printTape():
        out = ""
        for s in TuringMachine.tape:
            out += s
        print(out + "\n")

    def exec(self):
        print("Входные данные:")
        TuringMachine.printTape()

        while TuringMachine.isRunning:
            symbolExists = False #флаг, который поднимается, если обработчик для символа был найден.
            # Если нет - выкидываем исключение, т.к. неверно задано условие

            # Сравниваем поочередно символы в состоянии с символом в текущей ячейке
            for conditionContainer in TuringMachine.conditionsList[TuringMachine.condition].conditionsTable:
                if conditionContainer.symbol == TuringMachine.tape[TuringMachine.tapePtr]:
                    symbolExists = True
                    #print("simvol sovpal")
                    # Нашли. Заменяем символ на указанную подстановку
                    TuringMachine.tape[TuringMachine.tapePtr] = conditionContainer.setSymbol

                    if conditionContainer.goToCondition == HALT:
                        Dbg.dprint("Встречена конечная команда. Остановка машины.")
                        TuringMachine.isRunning = False
                        break

                    # Меняем положение головки на +1 (вправо) или на -1 (влево)
                    TuringMachine.tapePtr += conditionContainer.direction
                    Dbg.dprint("Позиция головки: " + str(TuringMachine.tapePtr) + " текущий символ: " + conditionContainer.symbol)

                    if conditionContainer.goToCondition != THIS:
                        if conditionContainer.goToCondition < len(TuringMachine.conditionsList) or conditionContainer.goToCondition < 0:
                            # Если всё необходимо сменить состояние, и указанное - валидно, то переходим на указанное
                            TuringMachine.condition = conditionContainer.goToCondition
                        else:
                            Dbg.fatalError("Несуществующее состояние, всё плохо")
                            TuringMachine.isRunning = False
                    Dbg.dprint("Текущее состояние = q" + str(TuringMachine.condition)+ "\n")

            if not symbolExists:  # если флаг не поднял ни один из символов
                Dbg.fatalError("Найден символ, для которого нет обработчика")
                TuringMachine.isRunning = False


        TuringMachine.isRunning = False

        print("Выходные данные:")
        TuringMachine.printTape()


class Condition:
    def __init__(self, number, conditionsTable, disclaimer):

        self.conditionsTable = conditionsTable
        self.number = number
        self.disclaimer = disclaimer


# ячейка таблицы
class ConditionContainer:
    def __init__(self, symbol, setSymbol, goToCondition, direction):
        """

        :param symbol: для какого символа обработчик
        :param goToCondition : на какое состояние перейдём
        :param direction: LEFT, RIGHT, HALT (остановка)
        :param setSymbol: на какой символ заменим. Если не на какой - просто написать тот же что и есть

        """
        self.setSymbol = setSymbol
        self.direction = direction
        self.goToCondition = goToCondition
        self.symbol = symbol


def __main__():
    m = TuringMachine()

    '''
    m.setTape(["l", "b", "b", "b", "b", "l"])

    #symbol, setSymbol, goToCondition, direction
    m.addCondition(Condition(0, [ConditionContainer("b", "b", 1, RIGHT), ConditionContainer("l", "l", 0, RIGHT) ], "prev is L"))
    m.addCondition(Condition(1, [ConditionContainer("b", "b", 1, RIGHT), ConditionContainer("l", "a", 2, LEFT)], "prev is b"))
    m.addCondition(Condition(2, [ConditionContainer("b", "b", 2, LEFT), ConditionContainer("l", "a", HALT, HALT)], "goto begining"))
    '''

    m.setTape(["0", "1", "1", "0", "1", "L"])

    m.addCondition(Condition(0, [ConditionContainer("0", "0", 0, RIGHT), ConditionContainer("1", "1", 0, RIGHT), ConditionContainer("L", "L", 1, LEFT)], "ищем конец числа"))
    m.addCondition(Condition(1, [ConditionContainer("0", "1", HALT, HALT), ConditionContainer("1", "0", 1, LEFT), ConditionContainer("L", "1", HALT, HALT)], "увеличиваем на 1"))

    m.exec()


if __name__ == "__main__":
    __main__()

