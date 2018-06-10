#zhangzui.github.io,我的github博客主页

欢迎点击: <https://zhangzui.github.io>

非常简单的博客，使用markdown写作，可以自定义css样式。
更多的是一种思路,markdown 就是 html,我们只要自定义标签的样式,就可以做自己想要的东西.简单而高效.

##介绍文档

###

代码

```

```

### 怎么使用
1. clone 代码

    ```
    git clone https://github.com/zhangzui/zhangzui.github.io.git
    ```
2. 在`post`中添加markdown文件

3. 更改`pure.py`中的`website_dir`变量为你的`github page`(需要你自己创建一个github page,然后克隆到本地,不要克隆我的)文件夹路径.

4. 运行 `python pure.py`

#### 配置

```python
# 将产生的所有文件输出到page文件夹下
website_dir = "绝对路径/xxx.github.io"

jinja_env.globals["title"] = "博客名字"

# 网站头像
jinja_env.globals["icon"] = "直接输入文件名字(直接放在static/images下)"

# 直接在后面添加社交账号即可
jinja_env.globals["sociallist"] = (("github", "https://github.com/zhangzui"),)
```

#### 代码结构

```
├── README.md
├── requirements # 依赖包
├── post # 将你想要发布的文章放在这个文件夹下,文件结构直接被映射为url地址
├── pure.py # 所有的代码
├── static # 如果你想改样式,修改main.css 和 home.css
└── templates # 模板文件
```

#### 库
使用 [markdown2](https://github.com/trentm/python-markdown2) + `fenced-code-blocks` 插件
https://github.com/richleland/pygments-css

