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
  try {
    const logsContainer = document.getElementById('logs-container');
    if (!logsContainer) {
      throw new Error('Logs container not found');
    }
    logsContainer.innerHTML = '';
    logs.forEach(log => {
      const logElement = document.createElement('pre');
      logElement.innerText = JSON.stringify(log, null, 2);
      logsContainer.appendChild(logElement);
    });
  } catch (error) {
    console.error('Error displaying log data:', error);
  }
};

const handleRefresh = () => {
  fetchLogData().then(displayLogData).catch((error) => {
    console.error('Error refreshing log data:', error);
  });
};

const handleFilterSubmit = (event) => {
  event.preventDefault();
  try {
    const level = document.getElementById('level').value;
    if (!level) {
      throw new Error('Log level value is missing');
    }
    fetchLogData().then(logs => {
      const filteredLogs = logs.filter(log => log.level === level);
      displayLogData(filteredLogs);
    }).catch((error) => {
      console.error('Error applying filter on log data:', error);
    });
  } catch (error) {
    console.error('Error with the filter form submission:', error);
  }
};

const refreshBtn = document.getElementById('refresh-btn');
if (refreshBtn) {
  refreshBtn.addEventListener('click', handleRefresh);
} else {
  console.error('Refresh button not found');
}

const filterForm = document.getElementById('filter-form');
if (filterForm) {
  filterForm.addEventListener('submit', handleFilterSubmit);
} else {
  console.error('Filter form not found');
}