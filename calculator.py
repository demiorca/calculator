# Калькулятор, принимающий на вход строку
# Версия 1.0
# print(eval(input('Enter the expression: ')))


def make_expression():
    # Функция создания и преобразования математического выражения
    # Лишние пробелы удаляются, операнды и операторы отделяются друг друга, образуя список элементов

    input_expression = input('Enter the expression: ').split()
    input_expression = ''.join(input_expression)
    fix_input_expression = ''

    for elem in input_expression:
        if elem not in '*/+-()**':
            fix_input_expression += elem
        if elem in '*/+-()**':
            fix_input_expression = fix_input_expression + ' ' + elem + ' '

    fix_input_expression = fix_input_expression.split(' ')
    fix_input_expression = [elem for elem in fix_input_expression if elem]

    for elem in range(len(fix_input_expression)):
        if fix_input_expression[elem] == '*' and fix_input_expression[elem + 1] == '*':
            fix_input_expression[elem] = '**'
            fix_input_expression[elem + 1] = ''

    fix_input_expression = [elem for elem in fix_input_expression if elem]
    return fix_input_expression


def calculator():
    # Функция для запуска функций подсчёта, высчитывающая и возвращающая итоговый результат
    # Подсчёт идёт по приоритету: сперва скобки, затем степени, после умножение/деление, а в конце сложение/вычитание
    # Учтены возможные исключения (деление на 0, нехватка операндов/операторов, некорректное выражение)

    try:
        if len(expression) > 1:
            if '(' and ')' in expression:
                action_in_parentheses()
            if '**' in expression:
                exponentiation()
            if '*' or '/' in expression:
                multiplication_division()
            if '+' or '-' in expression:
                addition_subtraction()
            result = ''.join(expression)
            return result
        else:
            return 'Error: Enter the correct expression with all operands and operators between them'

    except ZeroDivisionError:
        return 'Error: Cannot divide by zero'
    except ValueError:
        return 'Error: Enter the correct expression with all operands and operators between them'
    except IndexError:
        return 'Error: One operand is missing in the expression'


def action_in_parentheses():
    # Функция подсчёта элементов, находящихся в скобках
    # Реализованы вложенные скобки, через цикл заполняется список, состоящий из списков индексов по приоритету подсчёта
    # Подсчёт ведётся по приоритету операторов (сперва степени, затем умножение/деление, а после сложение/вычитание)

    count_parentheses = expression.count('(') + expression.count(')')
    indexes_lp = [idx for idx, elem in enumerate(expression) if elem == '(']
    indexes_rp = [idx for idx, elem in enumerate(expression) if elem == ')']
    parentheses_indexes = []
    lp_count = len(indexes_lp)

    for _, rp_idx in zip(range(len(indexes_lp)), range(len(indexes_rp))):
        while lp_count != 0:
            for lp_idx in range(lp_count + 1)[1:]:
                rp = indexes_rp[rp_idx]
                if rp > indexes_lp[-lp_idx]:
                    lp = indexes_lp[-lp_idx]
                    parentheses_indexes.append([lp, rp])
                    del indexes_lp[-lp_idx]
                    del indexes_rp[rp_idx]
                    break
            lp_count -= 1

    while count_parentheses != 0:
        if '(' and ')' in expression:
            for parenthesis_index in parentheses_indexes:
                parentheses_count = 0
                count_parentheses_one = 2
                lp = parenthesis_index[0]
                rp = parenthesis_index[1]
                while count_parentheses_one != 0:
                    count_e_parentheses = expression[lp:rp + 1].count('**')
                    count_md_parentheses = expression[lp:rp + 1].count('*') + expression[lp:rp + 1].count('/')
                    count_as_parentheses = expression[lp:rp + 1].count('+') + expression[lp:rp + 1].count('-')

                    # Подсчёт операций возведения в степень элементов, находящихся в скобках:
                    while count_e_parentheses != 0:
                        for elem in expression[lp:rp + 1]:
                            if elem == '**':
                                expression2 = expression.copy()
                                expression2 = ['' for _ in expression2]
                                expression2[lp:rp + 1] = expression[lp:rp + 1]
                                idx = expression2.index(elem)
                                idx_start = idx - 1
                                if expression[idx] == '**':
                                    n = str(
                                        float(expression[idx - 1]) ** float(expression[idx + 1]))
                                    del expression[idx - 1:idx + 2]
                                    expression.insert(idx_start, n)
                                    rp = parenthesis_index[1] - 2
                                    parentheses_count += 2
                                    count_e_parentheses -= 1
                                    break

                    # Подсчёт операций умножения и деления элементов, находящихся в скобках:
                    while count_md_parentheses != 0:
                        for elem in expression[lp:rp + 1]:
                            if elem == '*' or elem == '/':
                                expression2 = expression.copy()
                                expression2 = ['' for _ in expression2]
                                expression2[lp:rp + 1] = expression[lp:rp + 1]
                                idx = expression2.index(elem)
                                idx_start = idx - 1
                                if expression[idx] == '*':
                                    n = str(
                                        float(expression[idx - 1]) * float(expression[idx + 1]))
                                    del expression[idx - 1:idx + 2]
                                    expression.insert(idx_start, n)
                                    rp = parenthesis_index[1] - 2
                                    parentheses_count += 2
                                    count_md_parentheses -= 1
                                    break
                                elif expression[idx] == '/':
                                    n = str(
                                        float(expression[idx - 1]) / float(expression[idx + 1]))
                                    del expression[idx - 1:idx + 2]
                                    expression.insert(idx_start, n)
                                    rp = parenthesis_index[1] - 2
                                    parentheses_count += 2
                                    count_md_parentheses -= 1
                                    break

                    # Подсчёт операций сложения и вычитания элементов, находящихся в скобках:
                    while count_as_parentheses != 0:
                        for elem in expression[lp:rp + 1]:
                            if elem == '+' or elem == '-':
                                expression2 = expression.copy()
                                expression2 = ['' for _ in expression2]
                                expression2[lp:rp + 1] = expression[lp:rp + 1]
                                idx = expression2.index(elem)
                                idx_start = idx - 1
                                if expression[idx] == '+':
                                    n = str(
                                        float(expression[idx - 1]) + float(expression[idx + 1]))
                                    del expression[idx - 1:idx + 2]
                                    expression.insert(idx_start, n)
                                    rp = parenthesis_index[1] - 2
                                    parentheses_count += 2
                                    count_as_parentheses -= 1
                                    break
                                elif expression[idx] == '-':
                                    n = str(
                                        float(expression[idx - 1]) - float(expression[idx + 1]))
                                    del expression[idx - 1:idx + 2]
                                    expression.insert(idx_start, n)
                                    rp = parenthesis_index[1] - 2
                                    parentheses_count += 2
                                    count_as_parentheses -= 1
                                    break

                    count_parentheses_one -= 2

                    if count_parentheses_one == 0:
                        del expression[lp:lp + 3:2]
                        parentheses_count += 2
                        min_parentheses = [i[0] for i in parentheses_indexes if i[0] < lp]
                        for order, parentheses in enumerate(parentheses_indexes):
                            parentheses_indexes[order] = [
                                elem - parentheses_count if elem not in min_parentheses else elem
                                for elem
                                in parentheses]

                count_parentheses -= 2


def exponentiation():
    # Функция подсчёта операций возведения в степень элементов вне скобок

    count_e = expression.count('**')

    while count_e != 0:
        for elem in expression:
            if elem == '**':
                idx = expression.index(elem)
                idx_start = idx - 1
                if expression[idx] == '**':
                    n = str(float(expression[idx - 1]) ** float(expression[idx + 1]))
                    del expression[idx - 1:idx + 2]
                    expression.insert(idx_start, n)
                    count_e -= 1


def multiplication_division():
    # Функция подсчёта операций умножения и деления элементов вне скобок

    count_md = expression.count('*') + expression.count('/')

    while count_md != 0:
        for elem in expression:
            if elem == '*' or elem == '/':
                idx = expression.index(elem)
                idx_start = idx - 1
                if expression[idx] == '*':
                    n = str(float(expression[idx - 1]) * float(expression[idx + 1]))
                    del expression[idx - 1:idx + 2]
                    expression.insert(idx_start, n)
                    count_md -= 1
                    break
                elif expression[idx] == '/':
                    n = str(float(expression[idx - 1]) / float(expression[idx + 1]))
                    del expression[idx - 1:idx + 2]
                    expression.insert(idx_start, n)
                    count_md -= 1
                    break


def addition_subtraction():
    # Функция подсчёта операций сложения и вычитания элементов вне скобок

    while len(expression) > 1:
        for elem in expression:
            if elem == '+' or elem == '-':
                idx = expression.index(elem)
                idx_start = idx - 1
                if expression[idx] == '+':
                    n = str(float(expression[idx - 1]) + float(expression[idx + 1]))
                    del expression[idx - 1:idx + 2]
                    expression.insert(idx_start, n)
                    break
                elif expression[idx] == '-':
                    n = str(float(expression[idx - 1]) - float(expression[idx + 1]))
                    del expression[idx - 1:idx + 2]
                    expression.insert(idx_start, n)
                    break


# Создаём математическое выражение и выводим результат на экран:
expression = make_expression()
print(calculator())
another_example = input('Once again? Write 1 (or "Yes") or 2 (or "No"): ').lower()

# Зацикливание программы для повторных подсчётов:
while True:
    if another_example == '1' or another_example == 'yes':
        expression = make_expression()
        print(calculator())
        another_example = input('Once again? Write 1 (or "Yes") or 2 (or "No"): ').lower()
    elif another_example == '2' or another_example == 'no':
        break
    else:
        another_example = input('You have entered something wrong. Write 1 (or "Yes") or 2 (or "No"): ').lower()
