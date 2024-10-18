from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

# Flask 인스턴스 생성하여 웹 어플리케이션 초기화
app = Flask(__name__)

# 데이터베이스 파일 경로 설정
DATABASE = '/mnt/data/board.db'

# 데이터베이스 초기화 함수
def init_db():
    # board.db라는 SQLite 데이터베이스 파일을 연결. 파일 없을 시 새로 생성.
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    # posts라는 테이블 생성. 3개의 열 (id, title, content)
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()   # db 변경사항 저장
    conn.close()    # db 연결 종료

# 메인 페이지 (게시글 목록)
@app.route('/')                         # 웹 애플리케이션의 URL 경로 정의. index() 함수는 루트 경로에서 실행됨.
def index():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM posts')    # 게시글 데이터를 db에서 모두 가져옴 (select all from posts)
    posts = c.fetchall()                # 모든 결과를 가져와 posts 리스트에 저장
    conn.close()
    return render_template('index.html', posts=posts)   # index.html 템플릿을 렌더링. posts 데이터를 html로 전달.

# 게시글 작성 페이지
@app.route('/create', methods=['GET', 'POST'])          # GET 및 POST 요청 모두를 처리하는 경로
def create():
    # POST 요청: 사용자가 폼을 제출할 때, request.form을 통해 전송된 title과 content 값을 가져옴
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))     # 데이터베이스에 INSERT INTO 쿼리를 실행하여 새 게시글 작성
        conn.commit()
        conn.close()

        return redirect(url_for('index'))   # 데이터 저장 후 게시글 목록 페이지로 리디렉션함

    # GET 요청: 사용자가 페이지에 처음 접근할 때, 빈 폼을 보여주기 위해 create.html 템플릿을 렌더링함
    return render_template('create.html')

# 게시글 상세보기 페이지
@app.route('/post/<int:post_id>')   # 특정 게시글을 보여주는 경로. post_id는 URL에서 전달되는 변수로, 해당 게시글의 고유 ID
def post(post_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM posts WHERE id = ?', (post_id,))   # 주어진 post_id와 일치하는 게시글을 db에서 가져옴
    post = c.fetchone()     # 쿼리 결과에서 한 개의 행만 가져옴. post에는 ID, title, content가 포함됨
    conn.close()
    return render_template('post.html', post=post)      # post.html 템플릿을 렌더링하며, 선택된 게시글의 데이터를 넘김

#@app.route('/post/<int:post_id>')   # 특정 게시글을 보여주는 경로. post_id는 URL에서 전달되는 변수로, 해당 게시글의 고유 ID

if __name__ == '__main__':
    # init_db()               # db 초기화
    # app.run(debug=True)     # FLASK 개발 서버 실행.
    if not os.path.exists('/mnt/data'):
        os.makedirs('/mnt/data')
    init_db()
    app.run(debug=True, host='0.0.0.0')
