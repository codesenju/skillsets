import { useState, useEffect } from 'react';
import EngineerManager from '../components/EngineerManager';
import styles from '../styles/Home.module.css';

const Home = () => {
  const [engineers, setEngineers] = useState([]);
  useEffect(() => {
    const fetchEngineers = async () => {
      try {
        const response = await fetch('api/engineers');
        const data = await response.json();

        console.log(`data: ${data.data}`)
        setEngineers(data.data || [
          {
            "name": "John Doe",
            "skills": ["JavaScript", "React", "Node.js"]
          },
          {
            "name": "Jane Smith",
            "skills": ["Python", "Django", "PostgreSQL"]
          },
          {
            "name": "Bob Johnson",
            "skills": ["Java", "Spring", "MySQL"]
          }
        ]);
        
        console.log(`Response: ${response.data}`)
      } catch (error) {
        console.log(error);
      }
    };
    fetchEngineers();
  }, []);
  

  return (
    
    <div className={styles.container}>
      <EngineerManager engineers={engineers} />
    </div>
  );
};

export default Home;


