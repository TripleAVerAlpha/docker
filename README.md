# Запуск скриптов Python в Docker
## Dockerfile
Запуск python в контейнере бывает полезно, когда мы хотим обучить несколько моделей параллельно, когда хотим ограничить наш скрипт или сделать его быстро перемещаемым и масштабируемым.
Здесь обернем проект My Project написанный на python в Docker контейнер с выводом логов на локальную машину (вместо логов может быть файлы БД, обученная модель или другие файлы которые вы хотите достать из контейнера). 
Начнем с создания [Dockerfile](Dockerfile) ([Описание всех команд поддерживаемых Dockerfile](https://docs.docker.com/engine/reference/builder/)):
```
FROM python:3.10
```
Сначала создаем минимально требуемую оболочку. Так как мы будем запускать python то выберем оболочку под него, но есть и другие узко специализированные оболочки (Например: Posgree), но если вы хотите развернуть, что-то более масштабное, то в качестве оболочки можно поднять и Linux.

```
ADD ./my_project/ /my_project/
```
Далее скопируем наш проект внутрь контейнера.

```
RUN pip install --upgrade pip
RUN pip3 install -r my_project/setting/requirements.txt
```

Поднимем нужное окружение с установкой библиотек

```
CMD ["python", "my_project/src/start.py"] 
```

И скажем Docker'у как запускать проект.

## 'Строим' и 'Бежим'
Теперь надо создать образ этого контейнера.

```bash
docker build --pull --rm -f "Dockerfile" -t my-project "."
```
И можно запускать 

```bash
docker run --rm -d my-project:latest
``` 

При запуске видим, что локально ни чего не изменилось, а значит, все, что сделал контейнер умерло вместе с ним.
Вмонтируем папку с локальными логами в контейнер, чтобы достать их из контенера.

```bash
-v ~/my_project/log:/my_project/log
```

А так же зададим имя, чтобы не потерять запущенный контейнер и не запустить его дважды:

```bash
--name my_script
```

Получили строку запуска:

``` bash
docker run --rm -d -v ~/my_project/log:/my_project/log --name my_script my-project:latest
```

## Сахарок
Добавим полученные комманды в виде alias'ов для быстрого доступа([add_command](add_command)):
```bash
source ./add_command
```

```bash
# Сбор образа(запускаем после изменений в коде или Dockerfile)
build
# Старт контейнера
start
```