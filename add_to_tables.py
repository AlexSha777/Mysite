# -*- coding: utf8 -*-

import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mytestsite.settings")
django.setup()


from money_move.models import Income, Spendings, MoneySource, SpendingKind, Cash, CashKind
from datetime import date
from django.utils import timezone, dateformat


#def add_info_in_models(model, add_tuple):
'''
    add_tuple = [
    [first_column, second_column, .. , ],
    [first_column, second_column, .. , ],
    [..],
    [..], 

    ]
'''
def unique_checking(element_to_check, Model_to_check):
    
    # element_to_check = Model_to_check(column_name= 'new_element_name')

    all_elements = Model_to_check.objects.all()
    element = element_to_check
    for i in all_elements:    
        i = str.strip(str(i))
        print(i)

        if str.lower(str.strip(i)) == str.lower(str.strip(str(element))):
            print('Already is in tuple')
            return False

        else:
            print('Checked uniqu')

    return True



def add_many_items(string, model_to_add):

    
    #  string =  'Item1, Item2, Item2.1 Item2.2, ...'

    dict_to_add = {}
    
    string_split = string.split(',')

    string_split_strip = []
    for i in string_split:
        string_split_strip.append(str.strip(i))

    #print(string_split_strip)
    #print()

    iterator = 0
    string_split_strip_normaliz = []
    for i in string_split_strip:
        if i.find(' ')!= -1:
            iterator_inner = 0
            inner_list = []
            i = i.split(' ')
            for k in i:
                if k.istitle():
                    inner_list.append(k)
                    iterator_inner = iterator_inner + 1
                else:
                    inner_list[iterator_inner-1] = str(inner_list[iterator_inner-1]) + ' ' + k 
                
            string_split_strip_normaliz.append(inner_list)
            iterator = iterator + 1
        
        else:
            string_split_strip_normaliz.append([i])
            iterator = iterator + 1
    
    print(string_split_strip_normaliz)

    
    

    field_names = []
    field_names = get_field_names(model_to_add)

    
    iterator_1 = 0

    for i in string_split_strip_normaliz:
        
        if len(i) ==1:
            
            b = model_to_add(first_level_kind = str(i[0]))
            print(b)
            b.save()
            iterator_1 = iterator_1 + 1

        elif len(i) == 2:
                        
            x = model_to_add(first_level_kind = str(i[0]), second_level_kind = str(i[1]))
            print(x)
            x.save()
            iterator_1 = iterator_1 + 1


string = 'Автомобиль, Автомобиль Бензин, Автомобиль Мойка, Автомобиль Ремонт, Автомобиль Запчасти, Автомобиль Страховка, Автомобиль Стоянка, Автомобиль Техосмотр, Автомобиль Налоги, Автомобиль Штрафы, Автомобиль Парковка, Бизнес, Бизнес Налоги, Бизнес Зарплата, Бизнес Реклама, Бизнес Офис и канцелярия, Бизнес Услуги, Благотворительность, Благотворительность Помощь, Благотворительность Подарки, Бытовая техника, Бытовая техника Компьютер, Бытовая техника Расходные материалы, Дети, Дети Одежда, Дети Питание, Дети Игрушки, Дети Книги, Дети Няня, Дети Мебель, Дети Услуги, Дети Развлечения, Домашние животные Питание, Домашние животные Товары для животных, Домашние животные Услуги ветеринара, Здоровье и красота Косметика, Здоровье и красота Парфюмерия, Здоровье и красота Салоны красоты, Здоровье и красота Спорт, Здоровье и красота Лекарства, Здоровье и красота Услуги, Ипотека, Ипотека Выплата по ипотеке, Ипотека Досрочное гашение долга, Ипотека Покрытие процентов Долги, Кредиты, Кредиты Выплата по кредиту, Кредиты Досрочное гашение долга, Кредиты Покрытие процентов, Квартира и связь, Квартира и связь Электричество, Квартира и связь Вода, Квартира и связь Тепло, Квартира и связь Газ, Квартира и связь Радио, Квартира и связь Телефон, Квартира и связь Интернет, Квартира и связь Аренда, Квартира и связь Вывоз мусора, Квартира и связь Кабельное телевидение, Квартира и связь Телевидение, Квартира и связь Охрана, Квартира и связь Консьерж, Квартира и связь Интернет, Квартира и связь Интернет и телевидение, Налоги, Страхование, Образование, Образование Учебники, Образование Канцтовары, Образование Плата за обучение, Образование Репетитор, Одежда и аксессуары, Одежда и аксессуары Одежда, Одежда и аксессуары Обувь, Одежда и аксессуары Аксессуары, Одежда и аксессуары Украшения, Одежда и аксессуары Химчистка, Одежда и аксессуары Ателье, Одежда и аксессуары Ремонт обуви, Отдых и развлечение, Отдых и развлечение Игры, Отдых и развлечение Фильмы, Отдых и развлечение Книги, Отдых и развлечение Диски, Отдых и развлечение Журналы, Отдых и развлечение Кафе и рестораны, Отдых и развлечение Кино, Отдых и развлечение Фото, Отдых и развлечение Театр, Отдых и развлечение Выставки, Отдых и развлечение Боулинг, Питание, Питание Основные продукты, Питание Деликатесы, Питание Алкоголь, Питание Еда на работе, Питание Фрукты и овощи, Питание Мясные продукты, Питание Прочее, Разное, Ремонт, Товары для дома, Товары для дома Белье, Товары для дома Мелкая техника, Товары для дома Инструменты, Товары для дома Посуда, Товары для дома Кухонная утварь, Товары для дома Товары для ванной, Товары для дома Предметы интерьера, Транспорт, Транспорт Автобус, Транспорт Проездные, Транспорт Авиа, Транспорт Метро, Транспорт Такси, Транспорт Электричка, Хобби'

def get_field_names(model):

    field_names = []
    for f in model._meta.get_fields():
        field_names.append(f.name)
        
    
    field_names_normal = []

    iterator = 0
    for i in field_names:
        if i == 'id':
            field_names_normal = field_names[iterator+1:]  
            break
        iterator = iterator + 1

    
    return field_names_normal

   

if __name__ == '__main__':
    
    
    #b = MoneySource(first_level_source= 'Дивиденды')
    #b.save()

    
    #print(all_entries)
    #print(SpendingKind)

    # передача названия именованной переменной как переменную!!!! print(Income.objects.all().filter(**{a:1}))
    # запрос списка значений поля таблицы print(Income.objects.all().values_list('id', flat=True))
   
    
    spendingkind_objects = SpendingKind.objects.all()
    
    for p in spendingkind_objects:
        print(p.id)

    print(spendingkind_objects)
   