import json

replicas = {
"start":
"""
Добавляйте отметки о выпитом напитке,
просто набирая его название
и количество выпитого в миллилитрах в окне чата.
Если не укажете названия посчитаю как воду.
Установить норму воды на день можно командой:
/norm {количество в миллилитрах}
""",
"norm": "Новая дневная норма воды установлена",
"wrong_norm": "Укажите целое количство миллилитров",
"today": "Сегодня выпито: "
}

with open("replicas.json", "w") as w_file:
    json.dump(replicas, w_file)
 
# States
