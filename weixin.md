#github快速托管自己的博客网站

非常简单的博客，使用markdown写作，可以自定义css样式。主要思路是，将自己的md文本转化为html页面，然后维护一个主页，进行管理即可
##一.用到的python库需要自己安装：
1. 使用 [markdown2]
    源码：(https://github.com/trentm/python-markdown2);
    linux-python库安装：pip install markdown2;
    windows:git下载，运行python setup.py;
2. pygments样式库:https://github.com/richleland/pygments-css
    安装：pip install pygments,windows安装
    参考文档：http://pygments.org/docs/quickstart/
3. jinja2:github上搜索就可以获得源码，同样方法安装：pip install jinja2
   Jinja2是基于python的模板引擎，功能比较类似于于PHP的smarty，J2ee的Freemarker和velocity

##二.利用MD库将md文本进行html化
下面是将code标签获取，再利用pygments工具替换生成新的样式;
```
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
                return self._html
```
##三.获取页面信息保存到数组postlist
将遍历完的html信息（页面标题，路径，首图，摘要）放入postlist中，用于index模板：
fd.write(index_t.render(postlist=postlist))
```
def cover_all_post():
    """create posts html format and make up index.html"""
    post_basedir = join(root_dir, "post")
    postlist = []
    for (post_path, _) in all_post_file():
        p = Post(post_path)
        p.write()
        #print("页面标题，路径，首图，摘要"+p.title, p.url, p.image, p.abstract)
        postlist.append(p)
    index_t = jinja_env.get_template("index.html")
    with io.open(join(website_dir, "index.html"), "w",encoding='UTF-8') as fd:
        fd.write(index_t.render(postlist=postlist))
```

##四.index页面模板渲染列表
页面遍历postlist，并保存到js变量objectArray，用于物理分页和渲染，下面是index.html的js脚本，通过{% for post in postlist %}遍历获取信息，objectArray分页就很简单了，看一下代码，就知道了。
```
var objectArray =new Array();;
    {% for post in postlist %}
        var obejct = {
            "url":"{{ post.url }}",
            "title":"{{ post.title }}",
            "image":"{{ post.image }}",
            "abstract":"{{ post.abstract }}"
        }
        objectArray.push(obejct);
    {% endfor %}
    console.log("data："+JSON.stringify(objectArray));
```
##效果：

##五.QuickStart

1. clone 代码：git clone https://github.com/zhangzui/zhangzui.github.io.git
2. 在`post`中添加markdown文件
3. 更改`pure.py`中的`website_dir`变量为你的`github page`(需要你自己创建一个github page,然后克隆到本地,不要克隆我的)文件夹路径.
4. 运行 `python pure.py`
5. 提交github.io就可以

##六.ure.py脚本需要的更改配置
```
# 将产生的所有文件输出到page文件夹下
website_dir = "/usr/zzone/zzgit/zhangzui.github.io"
website_dir_html = "/usr/zzone/zzgit/zhangzui.github.io/html"
website_dir_css = "/usr/zzone/zzgit/zhangzui.github.io/css"
website_dir_image = "/usr/zzone/zzgit/zhangzui.github.io/images"
#jinja全局变量，博客名字
jinja_env.globals["title"] = "Myclass社区"
# 博客图标
jinja_env.globals["icon"] = "zz.jpg"
# 直接添加名字和地址
jinja_env.globals["sociallist"] = (("github", "https://github.com/zhangzui"),)
```




