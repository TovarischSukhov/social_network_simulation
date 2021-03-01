# social_network_simulation

Код для симуляции модели взаимодействия работников с работодателями, при условии, что работники могут обмениваться информацией.

## Описание модели
### Допущения модели:
- Все работники обладают одинаковым опытом и скиллами
- Все работодатели обладают знанием об объективной стоимости работника
- Работодатели хотят купить как можно дешевле работника
- Работник сам предлагает уровень зп
- Решения где-с кем работать принимаются на каждом шаге заново
- Инфляции нет
- Количество работодателей и и работников не изменяется
- Все работодатели одинаковые
- Все контракты заключаются на 1 период, то есть в начале “торгов” все оказываются свободными от обязательств (кажется где-то была такая модель  рынка)
- На каждой итерации не работник не учитывает свой предыдущий уровень заработной платы, только считает новый 

### Участники:
- компания
- работник 1 типа (нормальная самооценка) (beta)
- работник второго типа (заниженная самооценка) (1-beta)
### Сеть:
- у каждого работника случайное количество  знакомых (из нормального распределения, с мат ожиданием [2, 10])
- все знакомства равноценные
- сеть статична, то есть во время эволюции новых связей не появляется
- каждый работник принадлежит к одному из типов и типы не меняются
- каждый работник знает про себя сколько он сейчас получает
- при инициализации каждому человку генерится по фисированному количеству знакомств, независимо. Поэтому получатся, что у человека КАК МИНИМУМ константа знакомых, но может быть больше
- изначально у всех равные з
- ответы на этапе рекогносцировки недетерминированы, то есть в разные итерации по одной и той же связи может как прийти ответ, так и нет
### “Торги”:
Каждый раунд состоит из 3х шагов: рекогносцировка, предложение, решение.  (need link) (что-то похожее было в микроэкономике в торгах за зп)
#### Рекогносцировка:
Каждый участник задает вопрос об уровне дохода всем (или случайному числу\проценту) своим знакомым в сети и с вероятностью alpha получает ответ. Если в предыдущей итерации человек не работал - ответа не дает.
Далее по формуле самооценки-самопредставления рассчитывает желаемый уровень зп. ( средняя зарплата знакомых * самооценку)

#### Предложение:
каждой фирме надо нанять N сотрудников (три случая, сумма всех N больше, меньше или равно числу работников в сети)
Фирма случайным образом делает по (2-3-4) предложения о работе на каждую вакансию. Работники отвечают ожидаемой зп.

#### Решение:
Компании делают оффер самому дешевому работнику на вакансию
работник получает оффер, если офферов несколько - выбирает случайно.
На этом модель останавливается, собирает статистику и переходит к новой итерации



## Структкра кода:
- запуск main
- компания
  - действи
  - полезность
- участник
  - действи
  - полезность
- мир
  - инициализация
  - шаги 
  - вывод стейта и статистики
  