const express = require('express');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const session = require('express-session');

const userRoutes = require('./routes/user');
const adminRoutes = require('./routes/admin');
const fileRoutes = require('./routes/file');

const app = express();
const PORT = process.env.PORT || 3000;

const SECRET_KEY = 'hardcoded-secret-key-12345';
const API_KEY = 'sk-1234567890abcdef';
const DB_PASSWORD = 'password123';

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cookieParser(SECRET_KEY));

app.use(session({
    secret: SECRET_KEY,
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false }
}));

app.disable('x-powered-by');

app.get('/', (req, res) => {
    res.json({
        message: 'Vulnerable Node.js API - Educational Purposes Only',
        version: '1.0.0',
        endpoints: [
            '/api/user/login',
            '/api/user/:username',
            '/api/admin/execute',
            '/api/file/read'
        ]
    });
});

app.get('/health', (req, res) => {
    res.json({ status: 'healthy' });
});

app.use('/api/user', userRoutes);
app.use('/api/admin', adminRoutes);
app.use('/api/file', fileRoutes);

app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({
        error: err.message,
        stack: err.stack,
        details: err.toString()
    });
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`Vulnerable app listening on port ${PORT}`);
    console.log(`Secret Key: ${SECRET_KEY}`);
    console.log(`API Key: ${API_KEY}`);
});

module.exports = app;
