Данная игра в жанре бесконечного раннера, разработана на библиотеке PyGame. Игра доступна на любом устройстве. 

Игрок играет за машинку, которая едет по дороге, чтобы успеть добраться до пункта назначения. Игрок должен преодолевать препятствия, собирать монеты, чтобы получить наивысший результат.

Механика игры довольно проста и интуитивно понятна. Игрок может двигаться вправо или влево, прыгать. В игре есть несколько цветов автомобиля, которые могут быть использованы игроком по собственному желанию. Помимо этого, есть несколько карт, на которых можно ездить. Вместе с картами, меняется вид препятствий, монеток. Например, на стандартной карте препятствия выполнены в стиле конусов, монетки в своем естественном обличии. А на пустынной карте, конусы сменяются на кактусы, вместо монеток появляются кости с сокровищами. 

По мере вашего отдаления от старта, ваш автомобиль будет ускоряться, что усложнит игровой процесс. 

Эта игра подходит для всех возрастов, так как не имеет особо сложных механик. Наоборот, она сделана с небольшим юмором, чтобы пользователю было приятнее в нее играть. 

Разработка этой игры состояла из нескольких пунктов. В первую очередь, было необходимо сделать рабочую игру, добавить монетки, препятствие и игрока. Сама программа разделена по файлам: все активные объекты (Игрок и т.д.) были разделены и размещены в соответствующую папку в директории sprites. После, началась разработка меню игры. С помощью ООП были реализованы настройки (Где кстати и меняется скин, карта), главное меню и рекорд игрока. После нажатия на кнопку "Начать", игрок, как можно догадаться, начинает игру. В случае, если вам необходимо отойти на некоторое время, а прогресс терять нет желания - вы можете нажать на кнопку ESC, которая откроет окно с паузой. Из этого меню, вы можете вернуться в главное меню (При этом потеряв свой прогресс) или продолжить игру. Во время разработки нам пришлось решить проблему с переносом прогресса, поэтому в файле game.py вы можете видеть два класса: Game и ContGame (от Continue Game).

Сама игра запускается через main.py, при использовании функции run. Написал только перед прочтением твоего сообщения
