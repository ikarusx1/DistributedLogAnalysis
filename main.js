import axios from 'axios';
const API_URL = process.env.API_URL || 'http://localhost:3000';
const fetchLogData = async () => {
  try {
    const response = await axios.get(`${API_URL}/logs`);
    return response.data;
  } catch (error) {
    console.error('Error fetching log data:', error);
    return [];
  }
};
const displayLogData = (logs) => {
  const logsContainer = document.getElementById('logs-container');
  logsContainer.innerHTML = '';
  logs.forEach(log => {
    const logElement = document.createElement('pre');
    logElement.innerText = JSON.stringify(log, null, 2);
    logsContainer.appendChild(logElement);
  });
};
fetchLogData().then(displayLogData);
document.getElementById('refresh-btn').addEventListener('click', () => {
  fetchLogData().then(displayLogData);
});
document.getElementById('filter-form').addEventListener('submit', (event) => {
  event.preventDefault();
  const level = document.getElementById('level').value;
  fetchLogData().then(logs => {
    const filteredLogs = logs.filter(log => log.level === level);
    displayLogData(filteredLogs);
  });
});