const dotenv = require('dotenv').config({ path: __dirname + '/.env' });
const mysql = require('mysql2/promise');
const express = require('express');
const { getArticles, getArticlesByDate, getArticlesByIds } = require('./query'); // query.js 모듈 가져오기
const cors = require('cors');
const app = express();
const path = require('path');
const axios = require('axios')
let db;
app.use(cors()); // 모든 출처 허용

async function initializeDatabase() {
  try {
    db = await mysql.createConnection({
      host: process.env.MYSQL_HOST,
      port: process.env.MYSQL_PORT,
      user: process.env.MYSQL_USER,
      password: process.env.MYSQL_PASSWORD,
      database: process.env.MYSQL_DATABASE
    });

    console.log('Connected to the database');

    const port = process.env.PORT || 3000;
    app.listen(port, () => {
      console.log(`Server running on port ${port}`);
    });

  } catch (error) {
    console.error('Database connection error:', error);
  }
}

app.use(express.json());

// app.use(express.static('dist'));

app.get('/api/articles', async (req, res) => {
  try {
    console.log('Handling /api/articles request'); // 새로운 로그 메시지 추가
    const articles = await getArticles(db);
    console.log('Fetched articles:', articles); // 새로운 로그 메시지 추가
    res.json(articles);
  } catch (err) {
    console.error('Error fetching articles:', err.stack);
    res.status(500).send('Internal Server Error');
  }
});

app.post('/api/articles/by-ids', async (req, res) => {
  try {
    const { articleId } = req.body;
    if (articleId !== undefined) {
      const article = await getArticlesByIds(db, articleId);
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

const data = {
  news: [
    // 여기에 뉴스 기사 제목과 관련 데이터를 포함
  ]
};
app.post('/api/articles/by-date', async (req, res) => {
  const { startdate, enddate } = req.body;
  try {
    const articles = await getArticlesByDate(db, startdate, enddate);
    
    // Combine articles and word cloud image URL in the response
    const response = await axios.post('http://wordcloud-service:5000/generate-wordcloud', articles);
    
    const combinedResponse = {
        articles: articles,
        wordCloudImageUrl: response[0]
    };
    res.json(combinedResponse);
  } catch (error) {
    console.error("An error occurred while fetching articles:", error);
    res.status(500).json({ error: "Failed to fetch articles" });
  }
});
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

initializeDatabase();