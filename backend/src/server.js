const dotenv = require('dotenv').config({ path: __dirname + '/.env' });
const mysql = require('mysql2/promise');
const express = require('express');
const { getArticles, getArticlesByDate, getArticleById } = require('./query'); // query.js 모듈 가져오기
const app = express();
const path = require('path');

let db;

// MySQL 연결 설정 (퍼블릭 MySQL 호스트 및 포트를 사용)
async function initializeDatabase() {
  try {
    db = await mysql.createConnection({
      host: process.env.MYSQL_HOST, // MySQL 호스트 주소 (퍼블릭)
      port: process.env.MYSQL_PORT, // MySQL 포트
      user: process.env.MYSQL_USER, // MySQL 사용자 이름
      password: process.env.MYSQL_PASSWORD, // MySQL 비밀번호
      database: process.env.MYSQL_DATABASE // MySQL 데이터베이스 이름
    });

    // 데이터베이스 연결이 성공적으로 설정됨
    console.log('Connected to the database');

    // 서버 시작
    const port = process.env.PORT || 3000;
    app.listen(port, () => {
      console.log(`Server running on port ${port}`);
    });
    
  } catch (error) {
    console.error('Database connection error:', error);
  }
}
app.use(express.json())

// 기사 ID로 기사 정보 조회
app.post('/api/articles/by-id', async (req, res) => {
    try {
        const { articleId } = req.body; // 요청 바디에서 articleId를 구조분해할 때 기본값을 설정합니다.
        if (articleId !== undefined) {
            // articleId가 정의되어 있는 경우에만 실행
            const article = await getArticleById(db, articleId);
            if (article) {
                res.json(article);
            } else {
                res.status(404).send('Article not found');
            }
        } else {
            res.status(400).send('articleId is missing in the request body');
        }
    } catch (err) {
        console.error('Error fetching article by ID:', err.stack);
        res.status(500).send('Internal Server Error');
    }
});
// API 라우트 예시
app.use('/api', (req, res) => {
  res.json({ message: '이것은 API 응답입니다.' });
});

// Vue.js 빌드 파일을 정적 파일로 제공
// Dockerfile에서 복사된 위치를 기반으로 경로 설정
app.use(express.static('dist'));

// API 경로를 제외한 모든 경로에 대해 index.html 제공
app.get('*', (req, res) => {
  console.log(`GET request received: ${req.path}`);
  if (!req.path.startsWith('/api')) {    
    const absolutePath = path.resolve(__dirname, '..', 'dist', 'index.html');
    console.log(`Serving index.html from: ${absolutePath}`);
    res.sendFile(absolutePath);
  } else {
    res.status(404).send('API not found');
    console.log(`404 - API not found for path: ${req.path}`);
  }
});

// 모든 기사 조회
app.get('/api/articles', async (req, res) => {
    try {
        const articles = await getArticles(db);
        res.json(articles);
    } catch (err) {
        console.error('Error fetching articles:', err.stack);
        res.status(500).send('Internal Server Error');
    }
});

// 특정 날짜의 기사 조회
app.post('/api/articles/by-date', async (req, res) => {
    const { date } = req.body;
    try {
        const articles = await getArticlesByDate(db, date);
        res.json(articles);
    } catch (err) {
        console.error('Error fetching articles by date:', err.stack);
        res.status(500).send('Internal Server Error');
    }
});



// MySQL 연결 설정 및 서버 시작
initializeDatabase();
