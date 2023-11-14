// query.js
async function getArticles(db) {
    try {
        const [rows] = await db.query('SELECT * FROM Articles');
        return rows;
    } catch (err) {
        console.error('Error executing query: ' + err.stack);
        throw err;
    }
}

module.exports = { getArticles };

//날짜를 받으면 가져오게 하는법 
// async function getArticlesByDate(db, date) {
//     try {
//       const [rows] = await db.query('SELECT * FROM Articles WHERE date = ?', [date]);
//       return rows;
//     } catch (err) {
//       console.error('Error executing query: ' + err.stack);
//       throw err;
//     }
//   }
  
//   module.exports = { getArticles, getArticlesByDate };