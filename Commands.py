# Создать двух пользователей (с помощью метода User.objects.create_user).

from django.contrib.auth.models import User
alex_user=User.objects.create_user(username = 'alex', email = 'alex@gmail.com', password = 'alex_password')
boris_user=User.objects.create_user(username = 'boris', email = 'boris@gmail.com', password = 'boris_password')

# Создать два объекта модели Author, связанные с пользователями.
from news.models import Author
alex = Author.objects.create(user = alex_user)
boris = Author.objects.create(user = boris_user)

# Добавить 4 категории в модель Category.
from news.models import Category
cat_sport = Category.objects.create(name = "Спорт")
cat_music = Category.objects.create(name = "Музыка")
cat_cinema = Category.objects.create(name = "Кино")
politics = Category.objects.create(name = "Политика")

text_article_sport_cinema = """статья_спорт_кино_Алекс__статья_спорт_кино_Алекс__статья_спорт_кино_Алекс_
                                   _статья_спорт_кино_Алекс__статья_спорт_кино_Алекс__"""
    
text_article_music = """статья_музыка_Борис__статья_музыка_Борис__статья_музыка_Борис_
                            _статья_музыка_Борис__статья_музыка_Борис__"""
    
text_news_politics = """новость_politics_Борис__новость_politics_Борис__новость_politics_Борис__новость_politics_Борис__
                    новость_politics_Борис__новость_politics_Борис__новость_politics_Борис__новость_politics_Борис__"""

# Добавить 2 статьи и 1 новость.
from news.models import Post
article_alex = Post.objects.create(author = alex, post_type = Post.article, title = "статья_спорт_кино_Алекс", text = text_article_sport_cinema)
article_boris = Post.objects.create(author = boris, post_type = Post.article, title = "статья_музыка_Бори", text = text_article_music)
news_boris = Post.objects.create(author = boris, post_type = Post.news, title = "новость_politics_Бори", text = text_news_politics)

# Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
from news.models import PostCategory
    PostCategory.objects.create(post = article_alex, category = cat_sport)
    PostCategory.objects.create(post = article_alex, category = cat_cinema)
    PostCategory.objects.create(post = article_boris, category = cat_music)
    PostCategory.objects.create(post = news_boris, category = cat_politics)

# Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
from news.models import Comment
    comment1 = Comment.objects.create(post = article_alex, user = boris.user, text = "коммент Бориса (первый) к статье Алекса")
    comment2 = Comment.objects.create(post = article_boris, user = alex.user, text = "коммент Алекса (второй) к статье Бориса")
    comment3 = Comment.objects.create(post = news_boris, user = boris.user, text = "коммент Бориса (третий) к новости Бориса")
    comment4 = Comment.objects.create(post = news_boris, user = alex.user, text = "коммент Алекса (четвертый) к новости Бориса")


# Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
list_for_like = [article_alex,
                    article_boris,
                    news_boris,
                    comment1,
                    comment2,
                    comment3,
                    comment4]


import random
    for i in range(100):
        random_obj = random.choice(list_for_like)
        if i % 2:
            random_obj.like()
        else:
            random_obj.dislike()
# подсчет рейтинга Алекса
rating_alex = (sum([post.rating*3 for post in Post.objects.filter(author=alex)]) 
                    + sum([comment.rating for comment in Comment.objects.filter(user=alex.user)]) 
                    + sum([comment.rating for comment in Comment.objects.filter(post__author=alex)]))
# Обновить рейтинги пользователей.
alex.update_rating(rating_alexy)

# подсчет рейтинга Бориса
rating_boris = (sum([post.rating*3 for post in Post.objects.filter(author=boris)]) 
                + sum([comment.rating for comment in Comment.objects.filter(user=boris.user)]) 
                + sum([comment.rating for comment in Comment.objects.filter(post__author=boris)]))

# Обновить рейтинги пользователей.
boris.update_rating(rating_boris)
 
# Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
best_author = Author.objects.all().order_by('-rating')[0]
print("Лучший автор")
print("username:", best_author.user.username)
print("Рейтинг:", best_author.rating)


# Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
from news.models import Post
best_article = Post.objects.filter(post_type = Post.article).order_by('-rating')[0]
print("Лучшая статья")
print("Дата:", best_article.created)
print("Автор:", best_article.author.user.username)
print("Рейтинг:", best_article.rating)
print("Заголовок:", best_article.title)
print("Превью:", best_article.preview())


# Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
from news.models import Comment
for comment in Comment.objects.filter(post = best_article):
print("Дата:", comment.created)
print("Автор:", comment.user.username)
print("Рейтинг:", comment.rating)
print("Комментарий:", comment.text)