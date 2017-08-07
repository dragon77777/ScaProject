#coding:utf-8
#from flask import *   #引入第flask模板的内置工具，快捷用法，*表示引入全部内置方法
import traceback
from flask import Flask,render_template,request,redirect,url_for,jsonify ,abort#引入具体的需要用到的内置的工具
app = Flask(__name__,static_url_path='/static')



from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/sca_database?charset=utf8'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    #每个属性定义一个字段
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True)
    password = db.Column(db.String(64))

    def __repr__(self):
        return '<User %r>' % self.username
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]
@app.route('/todo/api/v1.0/tasks', methods=['GET'])#获取任务列表
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])#获取指定任务
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


@app.route("/index")#主页
def index():
    return render_template('index.html',id=tasks[0]['id'])

@app.route("/",methods=['POST','GET'])#登陆页面
def login():
    try:
        error = None
        if request.method == 'POST':
            username_post=request.form['username']
            password_post=request.form['password']
            username_filter=User.query.filter_by(username=username_post).first()
            if username_filter!=None:
                if username_filter.password==password_post:
                    return render_template('index.html')
                else:
                    error='please check your password !'
                    return render_template('login.html',error=error)
            else:
                error = 'please check your account !'
                return render_template('login.html', error=error)
        return render_template('login.html',error=error)
    except Exception,e:
        s = traceback.format_exc()
        print s
        print e

@app.route("/adduser",methods=['POST','GET'])#添加用户页面
def adduser():
    try:
        error = None
        if request.method == 'POST':
            username_post = request.form['username']
            password_post = request.form['password']
            if username_post!='' and password_post!='':
                user=User(username=username_post,password=password_post)
                db.session.add(user)
                db.session.commit()
            else:
                return render_template('adduser.html',error=error)
        return render_template('adduser.html',error=error)
    except Exception,e:
        s=traceback.format_exc()
        print s
        print e

@app.route("/chart")#表单页面
def chart():
    return render_template('chart.html')


@app.route("/file")#文件页面
def file():
    return render_template('ui-elements.html')

@app.route("/tools")#工具页面
def tools():
    return render_template('tab-panel.html')

@app.route("/control")#处理页面
def control():
    return render_template('table.html')

@app.route("/asymmetric")#非对称密码算法分析
def asymmetric():
    return render_template('form.html')

@app.route("/symmetric")#对称密码算法分析
def symmetric():
    return render_template('form.html')


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8888,
        debug=True)