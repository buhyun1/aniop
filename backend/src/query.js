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

async function getArticlesByDate(db, date) {
    try {
        const query = 'SELECT title, content FROM articles WHERE publish_date = ?';
        const [rows] = await db.query(query, [date]);
        return rows;
    } catch (err) {
        console.error('Error executing query:', err.stack);
        throw err;
    }
}

async function getArticleById(db, articleId) {
    try {
        const query = 'SELECT title, link, source FROM articles WHERE id = ?';
        const [rows] = await db.query(query, [articleId]);
        return rows[0]; // 결과가 하나의 기사 정보이므로 첫 번째 요소 반환
    } catch (err) {
        console.error('Error executing query:', err.stack);
        throw err;
    }
}

module.exports = { getArticles, getArticlesByDate, getArticleById };