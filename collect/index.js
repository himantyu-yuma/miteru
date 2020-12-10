const express = require('express');
const fs = require('fs');
const bp = require('body-parser');

const app = express();

// リクエストボディをjsonに変換する
app.use(bp.urlencoded({ extended: true }));
app.use(bp.json());
app.listen(3000)

app.post('/api', (req, res, next) => {
    console.log(req.body);
    // cors対策
    res.set({ 'Access-Control-Allow-Origin': '*' });
    res.send('OK')
    // 書き込み
    // ファイル名
    const now = new Date();
    const fileName = now.toISOString().replace(/:/g, '-').replace(/.[0-9]{3}Z/, '');
    fs.writeFile(`log/${fileName}.json`, req.body.data, (err, data) => {
        if (err) console.log(err);
        else console.log('write end');
    });
    return;
});

