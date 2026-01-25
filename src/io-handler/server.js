const express = require('express');
const axios = require('axios');

const app = express();
const port = 3000;

app.get('/acft-data', async (req, res) => {
  try {
    const response = await axios.get('https://24data.ptfs.app/acft-data');
    const data = response.data;

    //  For demonstration purposes, just send the whole response.
    //  In a real application, you'd likely process the data and send
    //  only the specific fields you need.
    res.json(data);

  } catch (error) {
    console.error('Error fetching data:', error);
    res.status(500).json({ error: 'Failed to fetch aircraft data' });
  }
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});
// End of file: server.js