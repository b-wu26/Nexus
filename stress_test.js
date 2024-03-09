import http from 'k6/http';


export let options = {
    vus: 100,
    duration: '10s',
};


export default () => {
    http.get('http://127.0.0.1:5000/api/feed/3');
    http.get('http://127.0.0.1:5000/api/enrolled_courses/3');
}
