const mysql = require('mysql');
const fs = require('fs');

const setting = JSON.parse(fs.readFileSync('./appsetting.json', { encoding: 'utf8' }));

const conn = mysql.createConnection({
    host: setting.host,
    user: setting.user,
    password: setting.password,
    port: setting.port,
});
conn.connect(err => {
    if(err)
    {
        console.log(`Connect Fails: ${err}`);
        return;
    }
    else console.log('Connect successfully.');
});

conn.query('use stocks;');

conn.query("show tables;", (err, rows) => {
    if(err) console.log(`query error: ${err}`);
    else console.log(rows);
})

conn.end();