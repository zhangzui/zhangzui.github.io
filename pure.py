#!/usr/bin/env python
#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
import re
import shutil
import io
from os.path import join, dirname, basename as filename, splitext
from urllib import pathname2url
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

import markdown2
from jinja2 import PackageLoader, Environment


class Post(object):
    def __init__(self, from_file):
        if not os.path.isfile(from_file): raise RuntimeError("not a file")
        self.fromfile = from_file
        post_dir = join(root_dir, "post")
        self.destfile = join(dirname(self.fromfile.replace(post_dir, website_dir)),
                             splitext(filename(self.fromfile))[0] + ".html")
        self.url = pathname2url(self.destfile.split(website_dir)[1])
        self._html = None
        self._title = None
        self._image = None
        self._abstract = None
        self.lexer = get_lexer_by_name("java", stripall=True)
        self.formatter = HtmlFormatter()

    @property
    def html(self):
        if not self._html:
            with io.open(self.fromfile,'r',encoding='UTF-8') as f:
                self._html = markdown2.markdown(f.read(),extras=['fenced-code-blocks', 'footnotes'])
                codearray = re.findall("<code>(.*?)</code>", self.html,re.S)
                for zzvar in codearray:
                    newcode = highlight(zzvar, self.lexer, self.formatter)
                    #print ("zzzzzzzzzzzzz:"+newcode)
                    self._html = self._html.replace("<pre><code>"+zzvar+"</code></pre>",newcode);

                c = re.compile("<p>(\\n)+</p>")
                self._html = re.sub(c, '</br>', self._html)
                #print("self._html:"+self._html)
        return self._html

    @property
    def abstract(self):
        if not self._abstract:
             abstract = re.findall("<p>(.*?)</p>", self.html,re.S)
             self._abstract = abstract[0] if abstract else filename(self.destfile).rsplit(".")[0]
             print("self._abstract:"+self._abstract)
        return self._abstract

    @property
    def title(self):
        if not self._title:
            title = re.findall("<h1>(.*?)</h1>", self.html)
            self._title = title[0] if title else filename(self.destfile).rsplit(".")[0]
            print("self._title:"+self._title)
        return self._title

    @property
    def image(self):
        if not self._image:
            self._image = self.url.rsplit(".")[0]
            print("self._image:"+self._image)
        return self._image

    def write(self):
        if not os.path.exists(dirname(self.destfile)):
            os.makedirs(dirname(self.destfile))
        with io.open(self.destfile, "w", encoding="utf-8") as fd:
            html = jinja_env.get_template("post.html").render(title=self.title, content=self.html)
            # print(html)
            fd.write(html)

def all_post_file():
    post_basedir = join(root_dir, "post")
    postlist = []
    for root, dirs, files in os.walk(post_basedir):
        for f_name in files:
            #设置忽略格式
            if f_name.startswith(".") or f_name.endswith(("pdf",)): continue
            post_path = join(root, f_name)
            c_time = os.stat(post_path).st_ctime
            postlist.append((post_path, c_time))
    return sorted(postlist, key=lambda x:x[1], reverse=True)

def cover_all_post():
    """create posts html format and make up index.html"""
    post_basedir = join(root_dir, "post")
    postlist = []
    for (post_path, _) in all_post_file():
        p = Post(post_path)
        p.write()
        print("--------"+p.title, p.url, p.image, p.abstract)
        postlist.append(p)
    index_t = jinja_env.get_template("index.html")
    with io.open(join(website_dir, "index.html"), "w",encoding='UTF-8') as fd:
        fd.write(index_t.render(postlist=postlist))


def copy_all_static():
    """拷贝 static/* 到 设置的website文件夹下"""
    base_websit = join(root_dir, "static")

    for root, dirs, files in os.walk(base_websit):
        relative_path = root.split(base_websit)[1].strip("/")
        for filename in files:
            if not os.path.exists(join(website_dir_css , relative_path)):
                os.makedirs(join(website_dir_css , relative_path))
            shutil.copy(join(root, filename),
                        join(website_dir_css , relative_path, filename))


def push_to_github():
    os.system("""cd %s && git add * && git commit -m "update" && git push origin master""" % website_dir)


def develop():
    """部署到github"""
    copy_all_static()
    cover_all_post()
    #push_to_github()


root_dir = dirname(__file__)
jinja_env = Environment(loader=PackageLoader(__name__))

# 文件输出地址,确定已经git init,可以直接git push origin master
#website_dir = "D:\\User\\zhangzuigit\\zhangzui.github.io"
#website_dir_html = "D:\\User\\zhangzuigit\\zhangzui.github.io\\html"
#website_dir_css = "D:\\User\\zhangzuigit\\zhangzui.github.io\\css"

website_dir = "/usr/zzone/zzgit/zhangzui.github.io"
website_dir_html = "/usr/zzone/zzgit/zhangzui.github.io/html"
website_dir_css = "/usr/zzone/zzgit/zhangzui.github.io/css"

# 博客名字
jinja_env.globals["title"] = "Myclass社区"

# 博客图标
jinja_env.globals["icon"] = "zz.jpg"

# 直接添加名字和地址
jinja_env.globals["sociallist"] = (("github", "https://github.com/zhangzui"),)
if __name__ == "__main__":
    develop()
