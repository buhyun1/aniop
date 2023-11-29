// query.js
const mysql = require('mysql2/promise');

async function getArticles(db) {
    try {
        const [rows] = await db.query('SELECT * FROM Articles');
        return rows;
    } catch (err) {
        console.error('Error executing query:', err.stack);
        throw err;
    }
}

async function getArticlesByDate(db, startDate, endDate) {
    try {
        const query = 'SELECT Title, Body, PublishedDate, ArticleID, CategoryID FROM Articles WHERE PublishedDate BETWEEN ? AND ?';
        const [rows] = await db.query(query, [startDate, endDate]);
        return rows;
    } catch (err) {
        console.error('Error executing query:', err.stack);
        throw err;
    }
}

async function getArticlesByIds(db, articleIds) {
    try {
<<<<<<< HEAD
        const query = 'SELECT Title, ArticleLink, Body, Source, PublishedDate FROM Articles WHERE ArticleID IN (?)'; 
        const [rows] = await db.query(query, [articleIds]);
=======
        const query = 'SELECT ArticleID, Title, ArticleLink, Body, Source, PublishedDate, CategoryID FROM Articles WHERE ArticleID IN (?)'; 
        const [rows] = await db.query(query, [articleId]);
>>>>>>> b069dac2b8b51c1380dc378a2061c5858b828736
        return rows; // 여러 기사 정보가 포함된 배열 반환
    } catch (err) {
        console.error('Error executing query:', err.stack);
        throw err;
    }
}


module.exports = { getArticles, getArticlesByDate, getArticlesByIds };