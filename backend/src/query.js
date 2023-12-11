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
        const query = 'SELECT Title, Body, PublishedDate, ArticleID, CategoryID, DailyRelatedArticleCount FROM Articles WHERE PublishedDate BETWEEN ? AND ?';
        const [rows] = await db.query(query, [startDate, endDate]);
        return rows;
    } catch (err) {
        console.error('Error executing query:', err.stack);
        throw err;
    }
}

async function getArticlesByIds(db, articleId) {
    try {
        const query = 'SELECT ArticleID, Title, ArticleLink, Body, Source, PublishedDate, CategoryID, DailyRelatedArticleCount FROM Articles WHERE ArticleID IN (?)'; 
        const [rows] = await db.query(query, [articleId]);
        return rows; // 여러 기사 정보가 포함된 배열 반환
    } catch (err) {
        console.error('Error executing query:', err.stack);
        throw err;
    }
}


module.exports = { getArticles, getArticlesByDate, getArticlesByIds };