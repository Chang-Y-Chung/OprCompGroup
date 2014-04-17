import TPost

P = TPost.Posts(raw="apr16.raw")
T = TPost.Tags(posts=P)

for t in sorted(T):
    posts = [P[id] for id in T[t]]
    print
    print t, '({0})'.format(len(posts))
    for post in posts:
        sub = post.sub[:30] + '...'
        id = '#{0}'.format(post.id)
        md = '{0}/{1}'.format(post.dt[5:7], post.dt[8:10])
        print " " * 4, sub, '({0}, {1})'.format(id, md)



