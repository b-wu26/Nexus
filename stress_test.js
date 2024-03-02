import http from 'k6/http';
// import BACKEND_SERVER_DOMAIN from './settings.js';


export let options = {
    vus: 1,
    duration: '10s',
};


export default () => {
    http.get('http://127.0.0.1:5000/api/feed/3');
}
