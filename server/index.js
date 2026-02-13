require('dotenv').config();
const express = require('express');
const cors = require('cors');
const { GoogleGenerativeAI } = require('@google/generative-ai');

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Gemini Setup
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash" });

app.post('/analyze', async (req, res) => {
    try {
        const { myItems, theirItems } = req.body;

        if (!myItems || !theirItems) {
            return res.status(400).json({ error: 'Missing items data' });
        }

        const prompt = `
      You are an expert Adopt Me trader with a gamer persona. You are witty, slightly sarcastic, but helpful.
      Analyze the following trade:
      
      My Offer: ${JSON.stringify(myItems)}
      Their Offer: ${JSON.stringify(theirItems)}
      
      Provide a strict JSON response with the following structure:
      {
        "score": number (1-10),
        "verdict": "WIN" | "FAIR" | "LOSE" | "BIG WIN" | "BIG LOSE",
        "comment": "short witty comment about the trade",
        "tip": "short negotiation tip"
      }
      Do not include any markdown formatting or code blocks in the response, just the raw JSON.
    `;

        const result = await model.generateContent(prompt);
        const response = await result.response;
        const text = response.text();

        // Clean up potential markdown code blocks if the model adds them despite instructions
        const jsonString = text.replace(/```json\n|\n```/g, '').trim();

        const analysis = JSON.parse(jsonString);

        res.json(analysis);
    } catch (error) {
        console.error('Error analyzing trade:', error);
        res.status(500).json({ error: 'Failed to analyze trade' });
    }
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
