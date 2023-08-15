import { useState, useEffect } from 'react';
import EngineerManager from '../components/EngineerManager';
import styles from '../styles/Home.module.css';
import axios from 'axios';
// const tracer = require('../../instrumentation')('example-http-client');

const Home = () => {
  const [engineers, setEngineers] = useState([]);
  useEffect(() => {
    const fetchEngineers = async () => {
      // console.log(`NEXT_PUBLIC_API_ENDPOINT: ${process.env.NEXT_PUBLIC_API_ENDPOINT}`)
      try {
        const r = await axios.get('api/engineers');
        const engineers = Object.entries(r.data).map(([name, skills]) => ({ name, skills }));
        console.log(engineers)
        setEngineers(engineers);
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


