import { useState } from 'react';
import axios from 'axios';
import styles from '../styles/Home.module.css';
import { basePath } from '../../next.config';

const api = axios.create({
  baseURL : process.env.NEXT_PUBLIC_API_ENDPOINT,
})

const EngineerManager = ({ engineers }) => {
  const [name, setName] = useState('');
  const [skills, setSkills] = useState('');
  const [updateEngineerName, setUpdateEngineerName] = useState('');
  const [editingEngineerSkills, setEditingEngineerSkills] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const API_URL = process.env.NEXT_PUBLIC_API_ENDPOINT;

  console.log(`API_URL: ${API_URL}`);


  //const API_URL = "https://uat-skillsets.lmasu.co.za";
  const addEngineer = async () => {
    if (!name || !skills) {
      setErrorMessage('Please enter a name and skills');
      return;
    }
    try {
      const response = await api.post(`/add_engineer`, { name, skills });
      console.log(response.data);
      //setErrorMessage(`${JSON.stringify(response.data)}`);
      alert(`${JSON.stringify(response.data)}`);
      window.location.reload();
    } catch (error) {
      console.log(error);
    }
  };

  const deleteEngineer = async (engineerName) => {
    const response = await api.delete(`/delete_engineer/${engineerName}`);
    console.log(response.data);
    window.location.reload();
  };

  const updateEngineerSkills = async () => {
    const response = await api.put(`/update_engineer_skillset/${updateEngineerName}`, { skills: editingEngineerSkills });
    console.log(response.data);
    window.location.reload();
  };
  return (
    <div>
      <h1>Engineer Skillsets</h1>
      <div className={styles.inputContainer}>
        <input
          type="text"
          placeholder="Engineer name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          type="text"
          placeholder="Skills (comma separated)"
          value={skills}
          onChange={(e) => setSkills(e.target.value)}
        />
        <button
          className={styles.addButton}
          onClick={addEngineer}
          disabled={!name || !skills}
        >
          Add Engineer
        </button>
        {errorMessage && (
          <p className={styles.errorMessage}>{errorMessage}</p>
        )}
      </div>
      <table className={styles.table}>
        <thead>
          <tr>
            <th>Name</th>
            <th>Skills</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {engineers.map(
            ({ name: engineerName, skills: engineerSkills }) => (
              <tr key={engineerName}>
                <td>{engineerName}</td>
                <td>
                  {updateEngineerName === engineerName ? (
                    <input
                      type="text"
                      placeholder="Skills (comma separated)"
                      value={editingEngineerSkills}
                      onChange={(e) => setEditingEngineerSkills(e.target.value)}
                      className={styles.wideInput}
                    />
                  ) : (
                    engineerSkills
                  )}
                </td>
                <td>
                  {updateEngineerName === engineerName ? (
                    <>
                      <button
                        className={styles.updateButton}
                        onClick={updateEngineerSkills}
                      >
                        Save
                      </button>
                      <button
                        className={styles.cancelButton}
                        onClick={() => setUpdateEngineerName(null)}
                      >
                        Cancel
                      </button>
                    </>
                  ) : (
                    <>
                      <button
                        className={styles.editButton}
                        onClick={() => {
                          setUpdateEngineerName(engineerName);
                          setEditingEngineerSkills(engineerSkills);
                        }}
                      >
                        Edit
                      </button>
                      <button
                        className={styles.deleteButton}
                        onClick={() => deleteEngineer(engineerName)}
                      >
                        Delete
                      </button>
                    </>
                  )}
                </td>
              </tr>
            ))}
        </tbody>
      </table>
    </div>
  )
};

export default EngineerManager;

export async function getServerSideProps() {
  const response = await api.get("/get_all_engineers");
  console.log(response.data);
  const engineers = Object.entries(response.data).map(([name, skills]) => ({ name, skills }));
  return { props: { engineers } };
}
