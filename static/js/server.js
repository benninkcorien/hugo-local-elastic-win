const express = require('express');
const { Client } = require('@elastic/elasticsearch');
const cors = require('cors');

const app = express();

const client = new Client({
    node: 'http://localhost:9200',
    auth: {
        username: 'elastic',
        password: 'ripx=UG=JxKPHnCzAlGA'  // Replace with your actual password
    }
});

app.use(express.json());

app.use(cors({
    origin: '*'
}));

app.get('/search', async (req, res) => {
    const query = req.query.q;
    const response = await client.search({
        index: 'books',
        body: {
            query: {
                multi_match: {
                    query,
                    fields: ["title", "content"]
                }
            }
        }
    });
    res.send(response); 
});

app.listen(3000, () => console.log('Server is running on port 3000'));
