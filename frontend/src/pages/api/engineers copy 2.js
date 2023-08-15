import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_ENDPOINT,
});

export default async function handler(req, res) {
  console.log(`NEXT_PUBLIC_API_ENDPOINT: ${process.env.NEXT_PUBLIC_API_ENDPOINT}`)
  if (req.method === 'GET') {
    try {
      const response = await api.get('/get_all_engineers');
      res.status(200).json(response.data);
    } catch (error) {
      console.error(error);
      res.status(500).json({ message: 'Internal server error' });
    }
  } else if (req.method === 'POST') {
    const { name, skills } = req.body;
    try {
      const response = await api.post('/add_engineer', { name, skills });
      res.status(200).json(response.data);
    } catch (error) {
      console.error(error);
      res.status(500).json({ message: 'Internal server error' });
    }
  } else if (req.method === 'DELETE') {
    const { engineerName } = req.query;
    try {
      const response = await api.delete(`/delete_engineer/${engineerName}`);
      res.status(200).json(response.data);
    } catch (error) {
      console.error(error);
      res.status(500).json({ message: 'Internal server error' });
    }
  } else if (req.method === 'PUT') {
    const { engineerName } = req.query;
    const { skills } = req.body;

    try {
      const response = await api.put(`/update_engineer_skillset/${engineerName}`, { skills });
      res.status(200).json(response.data);
    } catch (error) {
      console.error(error);
      res.status(500).json({ message: 'Internal server error' });
    }
  } else {
    res.status(404).json({ message: 'Not found' });
  }
}
