const express = require('express');
const router = express.Router();
const { exec } = require('child_process');
const yaml = require('js-yaml');
const xml2js = require('xml2js');

const ADMIN_PASSWORD = 'admin123';
const API_SECRET = 'secret-api-key-xyz';

router.post('/execute', (req, res) => {
    const { command } = req.body;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            return res.status(500).json({
                error: error.message,
                command: command
            });
        }
        res.json({ output: stdout, error: stderr });
    });
});

router.post('/ping', (req, res) => {
    const { host } = req.body;

    exec(`ping -c 4 ${host}`, (error, stdout, stderr) => {
        if (error) {
            return res.status(500).json({ error: error.message });
        }
        res.json({ output: stdout });
    });
});

router.post('/yaml', (req, res) => {
    const { data } = req.body;

    try {
        const parsed = yaml.load(data);
        res.json({ parsed });
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

router.post('/xml', (req, res) => {
    const { data } = req.body;

    const parser = new xml2js.Parser({
        explicitArray: false
    });

    parser.parseString(data, (error, result) => {
        if (error) {
            return res.status(400).json({ error: error.message });
        }
        res.json({ result });
    });
});

router.get('/config', (req, res) => {
    res.json({
        adminPassword: ADMIN_PASSWORD,
        apiSecret: API_SECRET,
        dbConnection: 'mysql://root:password123@localhost/vulnerable_db',
        awsAccessKey: 'AKIAIOSFODNN7EXAMPLE',
        awsSecretKey: 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
    });
});

router.post('/eval', (req, res) => {
    const { code } = req.body;

    try {
        const result = eval(code);
        res.json({ result });
    } catch (error) {
        res.status(500).json({
            error: error.message,
            stack: error.stack
        });
    }
});

module.exports = router;
