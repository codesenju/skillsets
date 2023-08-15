import { useState } from 'react';
import styles from '../styles/Home.module.css';
//const tracer = require('../../instrumentation')('example-http-client');

const EngineerManager = ({ engineers }) => {
  const [name, setName] = useState('');
  const [skills, setSkills] = useState('');
  const [updateEngineerName, setUpdateEngineerName] = useState('');
  const [editingEngineerSkills, setEditingEngineerSkills] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const addEngineer = async () => {
    if (!name || !skills) {
      setErrorMessage('Please enter a name and skills');
      return;
    }
    try {
     
        const response = await fetch('/api/engineers', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ name, skills }),

        });

      const data = await response.json();
      console.log(data);
      alert(`${JSON.stringify(data)}`);
      window.location.reload();
    } catch (error) {
      console.log(error);
    }
  };

  const deleteEngineer = async (engineerName) => {
    try {
      const response = await fetch(`/api/engineers/?engineerName=${engineerName}`, {
        method: 'DELETE',
      });
      const data = await response.json();
      console.log(data);
      window.location.reload();
    } catch (error) {
      console.log(error);
    }
  };

  const updateEngineerSkills = async () => {
    try {
      const response = await fetch(`/api/engineers/?engineerName=${updateEngineerName}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ skills: editingEngineerSkills }),
      });
      const data = await response.json();
      console.log(data);
      window.location.reload();
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div>
      <div className={styles.header}>
        <h1 className={styles.tittle}>Engineer Skillsets</h1>
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
      </div>
      <div className={styles.tableWrapper}>
        <table className={styles.table}>
          <thead>
            <tr>
              <th>Name</th>
              <th>Skills</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {engineers.map(({ name: engineerName, skills: engineerSkills }) => (
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
    </div>
  );
};

export default EngineerManager;
