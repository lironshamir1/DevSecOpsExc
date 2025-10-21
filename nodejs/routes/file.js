const express = require('express');
const router = express.Router();
const fs = require('fs');
const path = require('path');

const UPLOAD_DIR = '/tmp/uploads/';

router.get('/read', (req, res) => {
    const { filename } = req.query;

    const filePath = path.join(UPLOAD_DIR, filename);

    fs.readFile(filePath, 'utf8', (error, data) => {
        if (error) {
            return res.status(500).json({ error: error.message, path: filePath });
        }
        res.json({ content: data, path: filePath });
    });
});

router.post('/write', (req, res) => {
    const { filename, content } = req.body;

    const filePath = `${UPLOAD_DIR}${filename}`;

    fs.writeFile(filePath, content, (error) => {
        if (error) {
            return res.status(500).json({ error: error.message });
        }
        res.json({ message: 'File written', path: filePath });
    });
});

router.delete('/delete', (req, res) => {
    const { filename } = req.query;

    const filePath = path.join(UPLOAD_DIR, filename);

    fs.unlink(filePath, (error) => {
        if (error) {
            return res.status(500).json({ error: error.message });
        }
        res.status(204).send();
    });
});

router.get('/download', (req, res) => {
    const { path: filePath } = req.query;

    res.download(filePath, (error) => {
        if (error) {
            res.status(500).json({ error: error.message });
        }
    });
});

router.get('/list', (req, res) => {
    const { directory } = req.query;

    const dirPath = directory ? path.join(UPLOAD_DIR, directory) : UPLOAD_DIR;

    fs.readdir(dirPath, (error, files) => {
        if (error) {
            return res.status(500).json({ error: error.message });
        }
        res.json({ files, path: dirPath });
    });
});

module.exports = router;
