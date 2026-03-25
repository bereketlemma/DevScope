import axios from 'axios';

const client = axios.create({
  baseURL: 'https://devscope-api-965448962417.us-central1.run.app/api/v1',
  timeout: 15_000,
  headers: { 'Content-Type': 'application/json' },
});

client.interceptors.response.use(
  (res) => res,
  (err) => {
    console.error('[API Error]', err.response?.data || err.message);
    return Promise.reject(err);
  }
);

export default client;
