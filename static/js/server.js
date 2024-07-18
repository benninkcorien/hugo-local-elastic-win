const express = require('express');
const { Client } = require('@elastic/elasticsearch');
const app = express();
 
const client = new Client({
    node: 'http://localhost:9200',
    auth: {
        username: 'elastic',
        password: 'ripx=UG=JxKPHnCzAlGA'  // Replace with your actual password
    }
});

app.use(express.json());

app.get('/search', async (req, res) => {
    const query = req.query.q;
    try {
        const { body } = await client.search({
            index: 'books',
            body: {
                query: {
                    match: {
                        content: query
                    }
                }
            }
        });
        res.json(body.hits.hits);
    } catch (error) {
        console.error(error);
        res.status(500).send('Error occurred while searching.');
    }
});

app.listen(3000, () => console.log('Server is running on port 3000'));
