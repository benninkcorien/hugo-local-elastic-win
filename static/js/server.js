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
    const wildcardQuery = query.endsWith('*') ? query.replace('*', '') : query;

    const response = await client.search({
        index: 'books',
        body: {
            query: {
                bool: {
                    should: [
                        {
                            match_phrase: {
                                content: query
                            }
                        },
                        {
                            match: {
                                content: {
                                    query: wildcardQuery,
                                    operator: "and"
                                }
                            }
                        },
                        {
                            wildcard: {
                                "content": {
                                    value: `${wildcardQuery}*`,
                                    boost: 1.0,
                                    rewrite: "constant_score"
                                }
                            }
                        }
                    ]
                }
            }
        }
    });
    res.send(response);
});


app.listen(3000, () => console.log('Server is running on port 3000'));
