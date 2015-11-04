"""
Генерация комплекта для загрузки отчета на сервер
"""
import xml.etree.ElementTree as ET
import random
import string
import copy
import sys
import os

alpfabeta = 'абвгдеёжзийклмнопрстуфхцчшщэюя'
path_name = 'generated'

def str_random():
    """Генерирование строки из случаных символов"""
    return ''.join(random.SystemRandom().choice(alpfabeta.upper()) for _ in range(7))

def get_snils():
    """Генерирование СНИЛС"""

    dig = ''.join(random.SystemRandom().choice(string.digits) for _ in range(9))
    summ = sum([((i+1)*int(j)) for i, j in enumerate(dig[::-1])])
    checksum='00'
    if summ<100:
        checksum = '{:02d}'.format(summ)
    elif summ == 100 or summ == 101:
        pass
    elif summ>101:
        part = summ%101
        checksum = '00' if part == 100 or part == 101 else '{:02d}'.format(part)

    return '{}-{}-{} {}'.format(dig[0:3], dig[3:6], dig[6:9], checksum)

def main():
    tree = ET.parse(sys.argv[1])
    root = tree.getroot()
    file_name = root.find('ИмяФайла').text
    template_node = root.find('.//СВЕДЕНИЯ_О_СУММЕ_ВЫПЛАТ_И_СТРАХОВОМ_СТАЖЕ_ЗЛ')
    copy_node = copy.deepcopy(template_node)
    num_node = copy_node.find('НомерВпачке')
    snils_node = copy_node.find('СтраховойНомер')
    fio_node = copy_node.find('ФИО')
    parent = root.find('ПачкаВходящихДокументов')
    for count in range(3, int(sys.argv[2])+3):
        fio_node.find('Фамилия').text=str_random()
        fio_node.find('Имя').text=str_random()
        fio_node.find('Отчество').text=str_random()
        num_node.text = str(count)
        snils_node.text = get_snils()
        text_node = ET.tostring(copy_node, encoding='unicode')
        children = ET.XML('<root>{}</root>'.format(text_node))
        parent.extend(children)
    if not os.path.isdir(path_name):
        os.mkdir(path_name)
    else:
        pass
    tree.write(os.path.join(path_name, file_name), encoding='windows-1251')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('ERROR! XML file not generated')
        print('Usage: python create_xml.py [file] [count]')
        sys.exit(1)
    main()
    print('XML file created complete')
