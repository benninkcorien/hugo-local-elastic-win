const express = require('express');
const { Client } = require('@elastic/elasticsearch');
const cors = require('cors');  // Import the cors package

const app = express();

const client = new Client({
    node: 'http://localhost:9200',
    auth: {
        username: 'elastic',
        password: 'ripx=UG=JxKPHnCzAlGA'  // Replace with your actual password
    }
});

// Enable CORS for all origins
app.use(cors({
    origin: '*'
}));

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

        // Debugging: Log the full response object
        console.log("Elasticsearch full response:", body);

        // Ensure that hits property exists and is an array
        const hits = body && body.hits && body.hits.hits ? body.hits.hits : [];
        res.json(hits);
    } catch (error) {
        console.error("Error during search:", error);
        res.status(500).json({
            error: error.message,
            details: error.meta,
            stack: error.stack // Include the stack trace for more details
        });
    }
});

app.listen(3000, () => console.log('Server is running on port 3000'));
