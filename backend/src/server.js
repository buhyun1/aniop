require('dotenv').config();

const { Client } = require('ssh2');
const mysql = require('mysql2');

const sshClient = new Client();

sshClient.on('ready', () => {
  sshClient.forwardOut(
    '127.0.0.1', // 소스 주소
    22, // 임의의 소스 포트
    process.env.RDS_HOST, // RDS 인스턴스의 내부 IP
    3306, // RDS MySQL 서버의 포트
    (err, stream) => {
      if (err) throw err;

      // MySQL 연결 설정
      const db = mysql.createConnection({
        host: '127.0.0.1', // 로컬 호스트
        port: 3306,
        user: process.env.RDS_USER,
        password: process.env.RDS_PASSWORD,
        database: process.env.RDS_DATABASE,
        stream: stream
      });

      // MySQL에 연결
      db.connect(err => {
        if (err) {
          console.error('Database connection failed: ' + err.stack);
          return;
        }
        console.log('Connected to database');

        // articles 테이블에서 데이터를 가져오는 SQL 쿼리 실행
        db.query('SELECT * FROM Articles', (err, results) => {
          if (err) {
            console.error('Error executing query: ' + err.stack);
            return;
          }

          // 결과 출력
          console.log('Fetched ' + results.length + ' rows');
          results.forEach(row => {
            console.log(row); // 각 행의 데이터 출력
          });

          // 연결 종료
          db.end(err => {
            if (err) {
              console.error('Error closing connection: ' + err.stack);
              return;
            }
            console.log('Connection closed');
          });
        });
      });
    }
  );
}).connect({
  host: process.env.SSH_HOST, // SSH 서버의 퍼블릭 IP
  port: 22,
  username: process.env.SSH_USER,
  privateKey: require('fs').readFileSync(process.env.SSH_PRIVATE_KEY_PATH)
});
