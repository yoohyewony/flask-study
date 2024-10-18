from flask import Flask, render_template, request, redirect, url_for
import os

from db import get_posts, get_post_by_id, insert_post, init_db

# Flask 인스턴스 생성하여 웹 어플리케이션 초기화
app = Flask(__name__)

# 메인 페이지 (게시글 목록)
@app.route('/')                         # 웹 애플리케이션의 URL 경로 정의. index() 함수는 루트 경로에서 실행됨.
def index():
    posts = get_posts()
    return render_template('index.html', posts=posts)   # index.html 템플릿을 렌더링. posts 데이터를 html로 전달.

# 게시글 작성 페이지
@app.route('/create', methods=['GET', 'POST'])          # GET 및 POST 요청 모두를 처리하는 경로
def create():
    # POST 요청: 사용자가 폼을 제출할 때, request.form을 통해 전송된 title과 content 값을 가져옴
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        insert_post(title, content)
        return redirect(url_for('index'))   # 데이터 저장 후 게시글 목록 페이지로 리디렉션함
    # GET 요청: 사용자가 페이지에 처음 접근할 때, 빈 폼을 보여주기 위해 create.html 템플릿을 렌더링함
    return render_template('create.html')

# 게시글 상세보기 페이지
@app.route('/post/<int:post_id>')   # 특정 게시글을 보여주는 경로. post_id는 URL에서 전달되는 변수로, 해당 게시글의 고유 ID
def post(post_id):
    post = get_post_by_id(post_id)
    return render_template('post.html', post=post)      # post.html 템플릿을 렌더링하며, 선택된 게시글의 데이터를 넘김

#@app.route('/post/<int:post_id>')   # 특정 게시글을 보여주는 경로. post_id는 URL에서 전달되는 변수로, 해당 게시글의 고유 ID

if __name__ == '__main__':
    # init_db()               # db 초기화
    # app.run(debug=True)     # FLASK 개발 서버 실행.
    # if not os.path.exists('/mnt/data'):
    #     os.makedirs('/mnt/data')
    init_db()
    app.run(debug=True, host='0.0.0.0')
