# Remains of a dungeon (RoD)
RoD - это компьютерная 2D игра с элементамии RPG в жанре пошаговая стратегия. Является подобием игры Shattered Pixel Dungeon

## Черепухо Семён, группа 353505

## Список функций
- Настройки
  - Меню настроек с параметрами элементов игры
- Создание и развитие персонажа
  - Возможность выбора класса персонажа на старте игры (Воин, Маг, Лучник и т. п.)
  - Отслеживание базовых параметров: уровень, здоровье, сила, ловкость и т. д.
  - Система опыта и повышение уровня с последующим распределением бонусов и разблокировкой новых умений
- Генерация подземелий
  - Генерация уровней (этажей) подземелья с различным размером
  - Размещение комнат, коридоров, дверей, лестниц и других структур случайным образом
- Враги
  - Автоматическая генерация врагов на каждом уровне
  - Реализация поведения врагов, включающего преследование игрока, атаку, отступление и бездействие
  - Определение урона, способностей и специальных эффектов для каждого типа врагов
- Инвентарь и управление предметами
  - Инвентарь, где отображаются собранные предметы
  - Возможность использовать, надевать или выбрасывать предметы
  - Система описания свойств предметов, их эффектов и ограничений (например, требуемый уровень для использования)
- Тактическая пошаговая система боев
  - Возможность перемещения персонажа и врагов по клеточному полю подземелья
  - Боевая система с расчетом удара, блоком, уклонением и нанесением урона с учетом характеристик персонажей и врагов
  - Применение предметов во время боя
- Пользовательский интерфейс
  - Отображение подземелья в виде клеточного представления
  - Информационные панели, статус-бары, окна с описанием предметов
- Звук и музыка
  - Проигрывание фоновой музыки в зависимости от ситуации в игре
  - Реализация звуковых эффектов действий: шаги, атаки, получение урона, открытие дверей и т. п.
- Система сохранения и загрузки
  - Сохранение текущего состояния игры в слоты
  - Загрузка игры из слотов с сохранением
- Смерть
   - Реализация механизма смерти без восстановления игры
   - Подсказки и подтверждения для игрока перед окончательным выходом

## Модели данных
### Классы
- **Стена** - клетка, которая ограничивает размер комнаты и не позволяет игроку/существу выйти за пределы комнаты
- **Плитка** - клетка, по которой игрок/существо может передвигаться, если она пустая, или на которой находится объект, с которым можно взаимодействовать
- **Вода** - клетка, по которой игрок/существо может передвигаться. Если на игрока/существо наложен эффект горения, при прохождении по воде эффект спадёт
- **Пропасть**
- **Сундук** - объект, размещаемый на плитке и содержащий в себе какой-либо предмет. Может быть запертым и открываться ключом или быть открытым
- **Ловушка** - объект, размещаемый на плитке и способный нанести вред игроку или врагу при прохождении по плитке с ним. Может быть видимой/невидимой, активированной/неактивированной
  - *Ловушка с шипами* - наносит мгновенный урон
  - *Ловушка с ядом* - отравляет, нанося продолжительный периодический урон
  - *Ловушка с огнём* - накладывает эффект огня, нанося продолжительный периодический урон
- **Игрок** - сущность, управляемая пользователем. Имеет различные классы: Воин, Маг, Лучник, а также индивидуальные характеристики: здоровье, интеллект, ловкость, сила, уровень, навыки
  - *Воин* - Имеет повышенную силу и быстрее увеличивает её с поднятием уровня
  - *Маг* - Имеет повышенный интеллект и быстрее увеличивает его с поднятием уровня. Единственный, кто может видеть кол-во зарядов в посохе
  - *Лучник* - Имеет повышенную ловкость и быстрее увеличивает её с поднятием уровня
- **Враг** - сущность, враждебная по отношению к игроку. Имеет различные типы, а также индивидумальные характеристики: здоровье, интеллект, ловкость, сила, уровень, навыки
  - *Рядовой* - обычный враг, атакующий игрока, имеющий средние характеристики
  - *Босс* - усиленные враг, имеющий повышенные характеристики и специфические способности. Попадается на некоторых уровнях и блокирует лестницу до его победы. Имеет иммунитет к эффектам страха и ярости
- **Предмет** - объект, размещаемый на плитке, в сундуке или находящийся в инвентаре, имеющий индивидуальные свойства
  - *Броня* - Предмет, который можно экипировать на игрока. Обеспечивает защиту от входящего физического урона. Для экипировки требует определенных характеристик. При недостижении данных характеристик снижается защита и вероятность уклонения
  - *Оружие* - Предмет, который можно экипировать на игрока или использовать из инвентаря. При экипировке используется автоматически в битве. Для использования/экипировки требует определённых характеристик. При недостижении данных характеристик снижается урон и вероятность попадания
    - Меч - Оружие ближнего боя, наносящее средний физический урон, требующее средней силы
    - Тяжёлое оружие - Оружие ближнего боя, наносящее большой физический урон, требующее большой силы
    - Посох - Оружие дального боя, наносящее различный магический урон, требующее повышенного интеллекта. Имеет определённое количество зарядов, восстанавливающихся со временем
    - Лук - Оружие дального боя, наносящее физический урон, требующее повышенной ловкости
    - Метательное - Оружие дального боя, наносящее небольшой физический урон, требующее средней ловкости
  - *Зелье* - Предмет с различными свойствами, который можно метнуть или использовать. При метании на определённую клетку разбивается и накладывает ослабленный эффект в радиусе 2 клеток на всех врагов и игрока, находящихся в радиусе. При использовании накладывает эффект на игрока
    - Огня - Накладывает эффект огня
    - Яда - Накладывает эффект отравления
    - Лечения - Восстанавливает здоровье
    - Случайной телепортации - Телепортирует в случайное место на карте
    - Силы - Повышает силу
    - Ловкости - Повышает ловкость
    - Интеллекта - Повышает интеллект
    - Опыта - Повышает опыт
    - Дизориентированности - Отключает направление движения
    - Страха - Ослабляет. При использовании на врагах заставляет бежать от игрока
    - Ярости - Усиляет. При использовании на врагах заставляет нападать на игрока
  - *Свиток* - Предмет с различными свойствами, который можно применять на игрока или некоторые предметы в инвентаре
    - Усиления - увеличивает характеристики оружия/брони/аксессуара
    - Опознания - позволяет опознать зелье, свиток, оружие, броню, аксессуар
    - Ослабления - уменьшаяет характеристики оружия/брони/аксессуара
    - Проклятия - накладывает на предмет проклятие, запрещающее его снять при экипировке
    - Смерти - снимает игроку всё здоровье, оставляя лишь единицу
    - Жизни - повышает максимальный уровень здоровья
  - *Руна* - Предмет, накладывающий эффекты на оружие/броню/аксессуары. Эффекты активируются с вероятностью, зависящей от интеллекта персонажа на момент наложение и характеристик оружия
    - Огня - Накладывает на оружие эффект воспламенения
    - Яда - Накладывает на оружие эффект отравления
    - Заточки - Увеличивает наносимый физический урон
    - Удобства - Уменьшает требуемые характеристики
    - Укрепления - Увеличивает защиту
  - *Еда* - Предметы, повышающие сытость персонажа
  - *Семя* - Предмет, который можно посадить на пустую плитку. После посадки вырастает через некоторое время и накладывает эффект на игрока/врага при прохождении по нему или накладывает ослабленный эффект в радиусе 2 клеток при попадании по нему оружием дального боя
    - Огня - Накладывает эффект горения
    - Яда - Накладывает эффект отравления
    - Случайной телепортации - Телепортирует в случайное место на уровне
    - Дизориентации - Накладывает эффект дизориентации
    - Лечения - Восстанавливает здоровье
  - *Ключ* - Предмет, позволяющий открывать запертые двери или сундуки. Для каждой запертой двери/сундука есть свой индивидуальный ключ
  - *Аксессуар* - Экипируемый предмет, дающий определённые бонусы, или ослабляющий игрока
- **Лестница** - клетка, при взаимодействии с которой игрок может попасть на следующий уровень подземелья
- **Дверь** - клетка, при взаимодействии с которой игрок может проходить между комнатами и коридорами. Может быть открытой/закрытой на ключ
- **Уровень** - Таблица из клеток, которые составляют комнаты в подземелье. От номера уровня зависят находящиеся на нём враги и их характеристики, предметы и комнаты
- **Панель** - Элемент интерфейса игры, с которым пользователь может взаимодействовать
  - *Главное меню* - Содержит кнопки "Начать новую игру", "Продолжить", "Загрузить", "Настройки", "Выйти"
  - *Настройки игры* - Позволяет настраивать такие параметры, как звук, геймплей, управление
  - *Инвентарь* - Панель, доступная во время игры, позволяющая просматривать и управлять предметами, находящимися в нём
  - *Интерфейс персонажа* - Панель, находящаяся поверх отображения уровня, на которой изображены некоторые характеристики игрока, такие, как здоровье, голод, уровень, наложенные эффекты
  - *Отображение уровня* - Панель, содержащая в себе уровень и отображающая его
