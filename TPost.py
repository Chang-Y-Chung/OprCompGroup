#!/usr/bin/env python

import re
import time


class Post:
    def __init__(self, id=0, dt='', sub='', tags=[]):
        self.id, self.dt, self.sub, self.tags = id, dt, sub, tags
    def __repr__(self):
        args = (self.id, self.dt, self.sub, self.tags)
        return 'Post(id=%r, dt=%r, sub=%r, tags=%r)' % args

class Tag:
    def __init__(self, key='', ids=[]):
        self.key, self.ids = key, ids
    def __repr__(self):
        args = (self.key, self.ids)
        return 'Tag(key=%r, ids=%r)' % args


class Posts(dict):
    def __init__(self, *args, **kws):
        super(Posts, self).__init__(*args, **kws)
        self._compile_pattern()
        if 'raw' in kws:
            self._parse(kws['raw'])
            del self['raw']

    # private
    def _compile_pattern(self):
        a = r'.*?'                 # non-greedy any
        id = r'>>> Item #(\d+)'    # item id
        dt = r'\((.*?)\)'          # datetime literal within parens
        sub = r'\-\ (.*?)\s*?'     # subject string starts with a dash
        tags = r'<tag>(.*?)</tag>' # tags
        self._pattern = re.compile(id + a + dt + a + sub + tags, re.DOTALL)

    def _norm_nl(self, lines):
        return '\n'.join(lines.split('\n'))

    def _norm_dt(self, dt):
        infmt = '%d %b %Y %H:%M'
        outfmt = '%Y-%m-%d %H:%M:%S' # iso8601
        return time.strftime(outfmt, time.strptime(dt, infmt))

    def _norm_sentence(self, sentence):
        return ' '.join(sentence.split())

    def _norm_tags(self, tags):
        return map(lambda x: x.strip().upper(), tags.split(','))

    def _parse(self, fn):
        with open(fn, 'r') as f:
            txt = self._norm_nl(f.read())
        for id, dt, sub, tags in re.findall(self._pattern, txt):
            post = Post(int(id),
                        self._norm_dt(dt),
                        self._norm_sentence(sub),
                        self._norm_tags(tags))
            self[post.id] = post

class Tags(dict):
    def __init__(self, *args, **kws):
        super(Tags, self).__init__(*args, **kws)
        if 'posts' in kws:
            self._populate(kws['posts'])
            del self['posts']

    # private
    def _new_or_update(self, tag, id):
        if self.get(tag, None):
            self[tag].append(id)
        else:
            self[tag] = [id]

    def _populate(self, posts):
        for id, post in posts.items():
            for t in post.tags:
                self._new_or_update(t, id)


if __name__ == '__main__':

    post = Post(9, '2014-04-16 17:42;00', 'test', ['service', 'archive'])
    print post

    tag = Tag('service', [0, 1, 9])
    print tag

    P = Posts(raw="apr16.txt")
    print P

    T = Tags(posts=P)
    for t in sorted(T):
        posts = [P[id] for id in T[t]]
        print
        print t, '({0})'.format(len(posts))
        for post in posts:
            sub = post.sub[:30] + '...'
            id = '#{0}'.format(post.id)
            md = '{0}/{1}'.format(post.dt[5:7], post.dt[8:10])
            print " " * 4, sub, '({0}, {1})'.format(id, md)


