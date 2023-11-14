// 메인 서버 파일 (예: index.js)
require('dotenv').config();
const { Client } = require('ssh2');
const mysql = require('mysql2/promise');
const express = require('express');
const { getArticles } = require('./query'); // query.js 모듈 가져오기
const app = express();
const sshClient = new Client();

let db;

sshClient.on('ready', () => {
  sshClient.forwardOut(
    '127.0.0.1', // 소스 주소
    12345, // 임의의 소스 포트
    process.env.RDS_HOST, // RDS 인스턴스의 내부 IP
    3306, // RDS MySQL 서버의 포트
    async (err, stream) => {
      if (err) throw err;

      // MySQL 연결 설정
      db = await mysql.createConnection({
        host: '127.0.0.1', // 로컬 호스트
        port: 3306,
        user: process.env.RDS_USER,
        password: process.env.RDS_PASSWORD,
        database: process.env.RDS_DATABASE,
        stream: stream
      });

      // 연결 성공 로그
      console.log('Connected to database'); // 데이터베이스 연결 성공 메시지
    }
  );
}).connect({
  host: process.env.SSH_HOST, // SSH 서버의 퍼블릭 IP
  port: 22,
  username: process.env.SSH_USER,
  privateKey: require('fs').readFileSync(process.env.SSH_PRIVATE_KEY_PATH)
});

// ... 나머지 Express 서버 및 라우팅 코드 ...
app.get('/articles', async (req, res) => {
  try {
    const articles = await getArticles(db);
    console.log('Fetched Articles:', articles); // 쿼리 결과 출력
    res.json(articles);
  } catch (err) {
    console.error('Error executing query: ' + err.stack); // 에러 로그
    res.status(500).send('Error fetching articles');
  }
});

/*
//POST 라우트를 설정하여 날짜에 해당하는 데이터를 검색
const { getArticlesByDate } = require('./query');

app.use(express.json()); // JSON 본문 파싱을 위한 미들웨어

app.post('/articlesByDate', async (req, res) => {
  const date = req.body.date;
  
  if (!date) {
    return res.status(400).send('No date provided');
  }

  try {
    const articles = await getArticlesByDate(db, date);
    res.json(articles);
  } catch (err) {
    console.error('Error executing query: ' + err.stack);
    res.status(500).send('Error fetching articles');
  }
});
 */

// 서버 시작
const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
