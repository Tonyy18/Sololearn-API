import sl

user = sl.Login("toni.isotalo@hotmail.com", "tonttu16")
posts = user.getPosts(order="myquestions", page=1)
print(posts)