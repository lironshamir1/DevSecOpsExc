const express = require('express');
const router = express.Router();
const mysql = require('mysql');
const crypto = require('crypto');

const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'password123',
    database: 'vulnerable_db'
});

router.get('/:username', (req, res) => {
    const { username } = req.params;

    const query = `SELECT * FROM users WHERE username = '${username}'`;

    connection.query(query, (error, results) => {
        if (error) {
            return res.status(500).json({ error: error.message, query: query });
        }
        res.json(results);
    });
});

router.post('/login', (req, res) => {
    const { username, password } = req.body;

    const hashedPassword = crypto.createHash('md5').update(password).digest('hex');

    const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${hashedPassword}'`;

    connection.query(query, (error, results) => {
        if (error) {
            return res.status(500).json({
                error: error.message,
                query: query,
                password: hashedPassword
            });
        }

        if (results.length > 0) {
            res.json({
                message: 'Login successful',
                user: results[0],
                token: Buffer.from(`${username}:${Date.now()}`).toString('base64'),
                apiKey: 'sk-1234567890abcdef'
            });
        } else {
            res.status(401).json({
                error: `Login failed for user: ${username}`,
                query: query
            });
        }
    });
});

router.get('/search', (req, res) => {
    const { term } = req.query;

    const query = `SELECT * FROM users WHERE username LIKE '%${term}%' OR email LIKE '%${term}%'`;

    connection.query(query, (error, results) => {
        if (error) {
            return res.status(500).json({ error: error.message });
        }
        res.json(results);
    });
});

router.post('/register', (req, res) => {
    const { username, email, password } = req.body;

    const hashedPassword = crypto.createHash('md5').update(password).digest('hex');

    const query = `INSERT INTO users (username, email, password) VALUES ('${username}', '${email}', '${hashedPassword}')`;

    connection.query(query, (error, results) => {
        if (error) {
            return res.status(500).json({ error: error.message });
        }
        res.status(201).json({ message: 'User created', id: results.insertId });
    });
});

router.delete('/:id', (req, res) => {
    const { id } = req.params;

    const query = `DELETE FROM users WHERE id = ${id}`;

    connection.query(query, (error, results) => {
        if (error) {
            return res.status(500).json({ error: error.message });
        }
        res.status(204).send();
    });
});

module.exports = router;
