## Описание

Нашёл свой старый проект, решил сохранить в облачном репозитории.  
Небольшая консольная игра — арена с генерируемыми мобами.  
Планирую развивать и дорабатывать в свободное время.  

#### Список команд:
| Команда     | Действие              |
| :---------- | :-------------------- |
| a / attack  | Атака                 |
| d / defense | Лечение               |
| s / stat    | Статистика            |
| saves       | Просмотр сохранений   |
| save name*  | Сохранить игру        |
| load name*  | Загрузить сохранение  |
| del name*   | Удалить сохранение    |
| new         | Начать новую игру     |
| exit / quit | Выйти из игры         |
| cheat       | Чит на характеристики |
| win         | Победа                |
| death       | Смерть                |

###### *Если параметр name не указан, ему задаётся значение fast.  

## Версии

### Версия 2.0
Создан хаб - безопасный город, при входе в которой сбрасываются все характеристики до начальных. 
В нём же начальные характеристики можно улучшить. Так же в нём можно выбрать следующую локацию.  
Улучшена система локаций. Привязка типов мобов к локациям.  
Рефакторинг, улучшение архитектуры кода.

#### Версия 1.4  
Трансформация функции main и вспомогательных функций в класс Game.  
Перенос обработку actions в класс Action в отдельный файл.  
Перенос обработки смерти персонажа/врага из main в в actions.  
Теперь проверка на смерть врага происходит сразу после действия игрока, и в случае успеха, ответного действия врага на происходит.  

#### Версия 1.3
Добавлен файл .gitignore.  
Добавлена система сохранений и загрузок через сериализацию данных об игроке и списке врагов в файлы сохранения в директории saves/.  
Если директории saves/ не существует, она создаётся автоматически.  
  
Список новых команд:
+ Сохранение: save name*  
+ Загрузка: load name*  
+ Удаление: del name*  
+ Просмотр сохранений: saves  
+ Новая игра: new  
###### *Если параметр name не указан, ему задаётся значение fast.  

#### Версия 1.2
Оптимизация и улучшение кода.  
Перенос некоторого кода в методы классов.  
Добавлены отдельные методы для восполнения здоровья.  
Изменён подсчёт критического урона, теперь он высчитыватся по формуле: обычный урон + (обычный урон * 2, но не более, чем 50% здоровья оппонента).  
Добавлен модификатор осквернённости для врагов, такие враги имеют меньше здоровья и больше силы (изменение от 0 до 50% от начальных значениий).  

#### Версия 1.1
Создан общий класс Body, родительский для Player и Enemy, данные классы вынесены в отдельный файл и импортируются в main.py  
Подсчёт кражи характеристик переписан в метод класса Player.  
Генерация мобов сделана более дружелюбной, 3 набора по 5 мобов с повышением уровня опасности.  
Небольшой ребаланс характеристик мобов.  

#### Версия 1.0
Выполнено в одном файле.  
Два класса — класс Player и класс Enemy, много одинаковых методов, которые нужно объединить в один родительский класс.  
Несколько запутанная система силы, нанесения урона и получения лечения.  
Макисмальное количество мобов за прохождение — 15.  
У игрока есть команды: a — атака, d — лечение, s — просмотр статистики.  
