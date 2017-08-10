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


@app.route("/file")#工程管理页面
def file():
    return render_template('fileManage.html')


@app.route("/parameter")#rsa参数管理页面
def parameter():
    return render_template('rsa-parameter.html')

@app.route("/open-file")#打开文件页面
def open_file():
    return render_template('open-file.html')


@app.route("/tools")#数据采集页面
def tools():
    return render_template('data-acquisition.html')

@app.route("/low-pass-filter")#曲线处理页面/低通滤波
def low_pass_filter():
    return render_template('low-pass-filter.html')

@app.route("/move")#曲线处理页面/滑动平均滤波
def move():
    return render_template('moving-average-filter.html')

@app.route("/alignment")#曲线处理页面/静态对齐
def alignment():
    return render_template('static-alignment.html')

@app.route("/rsa-analysis")#RSA算法分析
def rsa_analysis():
    return render_template('rsa-analysis.html')

@app.route("/des-cpa-analysis")#des-cpa密码算法分析
def des_cpa_analysis():
    return render_template('des-cpa-analysis.html')

@app.route("/aes-cpa-analysis")#aes-cpa密码算法分析
def aes_cpa_analysis():
    return render_template('aes-cpa-analysis.html')

@app.route("/sm4-cpa-analysis")#sm4-cpa密码算法分析
def sm4_cpa_analysis():
    return render_template('sm4-cpa-analysis.html')

@app.route("/more")#更多内容页面
def more():
    return render_template('more.html')



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8888,
        debug=True)