# Тестовое задание компании «Webtronics»

1. [Инструкции по использованию API](#title1)
2. [Инструкции по установке и запуску приложения.](#title2)


## <a id='title1'>Инструкция по использованию API</a>

Пройдя по ссылке:
```
http://localhost:8000/docs#/
```
вы попадете на страницу с документацией к проекту. 
На этой странице содержится информация:
* о эндпоинтах и типах запросов к ним
* о параметрах запросов, их типах и ограничениях
* о результатах запросов в случае успешного выполнения или ошибок

Далее я подробно описываю работу каждого эндпоинта:

#### POST /users/registration/
С помощью данного эндпоинта осуществляется регистрация пользователя. В теле запроса передаются следующие параметры в виде JSON:
* username — имя пользователя (должен быть не короче 5 символов и содержать буквы, цифры и знаки !@#$%^&*-_)
* password — пароль (должен быть не короче 4 символов и содержать буквы, цифры и знак _)

В случае передачи неверных значений будут выводиться соответсвующие сообщения об ошибках.

В случае успешного выполнения запроса в базе данных создастся новый пользователь. А результатом запроса будет JSON который содержит всю информацию о новом пользователе.

#### POST /users/token/
С помощью данного эндпоинта осуществляется получение токена для зарешестрированного пользователя.
В теле запроса передаются следующие параметры в виде JSON:
* username — имя пользователя
* password — пароль

В случае передачи неверных значений будут выводиться соответсвующие сообщения об ошибках.

Результатом запроса будет JSON который содержит Bearer—токен для авторизации пользователя в **последующих эндпоинтах**.

#### GET /users/me/
С помощью данного эндпоинта осуществляется просмотр данных о пользователе, чей токен был передан в headers при отправке запроса.

В случае успешного выполнения запроса, его результатом будет JSON который содержит всю актуальную информацию о текущем пользователе. 

#### GET /posts/
С помощью данного эндпоинта осуществляется вывод всех постов. В качестве параметра запроса передаются `limit` (по-умолчанию равен 15) и `offset` (по-умолчанию равен 0). С помощью этих параметров осуществляется перемещение по списку постов.

В случае успешного выполения запроса будет выведен список словарей, в которых содержится вся информация о постах, их авторах, количестве лайков и дизлайков. Если постов в базе данных нет, то вернется пустой список.

#### POST /posts/
С помощью данного эндпоинта осуществляется добавление поста в базу данных. В теле запроса передается следующий параметр в JSON:

Данные о курсе:
* text — текст поста

В случае передачи неверных значений будут выводиться соответсвующие сообщения об ошибках.

В случае успешного выполнения запроса в базе данных создастся новый пост. А результатом запроса будет JSON с информацией о новом посте.

#### PUT /posts/{post_id}/
С помощью данного эндпоинта осуществляется редактирование текста поста. В качестве параметра запроса передается `post_id`, который соответсвует ID записи поста в базе данных. Если запись с таким ID в базе данных не найдена, то будет выведено сообщение об ошибке.  

В теле запроса передается следующий параметр в виде JSON:
* text  — новый текст для поста

В случае передачи неверных значений будут выводиться соответсвующие сообщения об ошибках.

В случае успешного выполнения запроса, его результатом будет JSON который содержит всю актуальную информацию изменного поста.

#### DELETE /posts/{post_id}/
С помощью данного эндпоинта осуществляется удаление поста. В качестве параметра запроса передается `post_id`, который соответсвует ID записи поста в базе данных. Если запись с таким ID в базе данных не найдена, то будет выведено сообщение об ошибке.

В случае успешного выполения запроса вернется ответ без тела.

#### POST /posts/{post_id}/like/
С помощью данного эндпоинта осуществляется добавление лайка к выбранному посту. В качестве параметра запроса передается `post_id`, который соответсвует ID записи поста в базе данных. Если запись с таким ID в базе данных не найдена, то будет выведено сообщение об ошибке.

Ограничения:
— пользователь не может ставить лайк на пост, который он создал
— пользователь не может ставить лайк на пост, если он уже стоит

Если у выбранного поста данный пользователь поставил дизлайк, то при выполнении запроса на данный эндпоит, дизлайк будет удален и добавлен лайк.

В случае успешного выполения запроса вернется ответ без тела.

#### POST /posts/{post_id}/dislike/
С помощью данного эндпоинта осуществляется добавление дизлайка к выбранному посту. В качестве параметра запроса передается `post_id`, который соответсвует ID записи поста в базе данных. Если запись с таким ID в базе данных не найдена, то будет выведено сообщение об ошибке.

Ограничения:
— пользователь не может ставить дизлайк на пост, который он создал
— пользователь не может ставить дизлайк на пост, если он уже стоит

Если у выбранного поста данный пользователь поставил лайк, то при выполнении запроса на данный эндпоит, лайк будет удален и добавлен дизлайк.

В случае успешного выполения запроса вернется ответ без тела.

## <a id='title3'>Инструкция установке и запуску приложения</a>

1. [Установить Docker](https://www.docker.com)
2. [Установить Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
3. Клонировать проект в локальную директорию:
```
https://github.com/mym1chelle/webtronics.git
```
4. Переименовать файл [.env.example](./.env.example) в `.env`
5. В директории клонированного проекта запусть сбор образов и запуск контейнеров Docker:

```
docker compose up --build
```