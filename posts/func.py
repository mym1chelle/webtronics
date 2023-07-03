def annotate(query):
    for post, likes, dislikes in query:
        post.likes = likes
        post.dislikes = dislikes
        yield post
