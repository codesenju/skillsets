import { sleep } from 'k6';
import http from 'k6/http';

export const options = {
  duration: '1m',
  vus: 250,
  thresholds: {
    http_req_duration: ['p(95)<600'], // 95 percent of response times must be below 600ms
    http_req_failed: ['rate<0.01'], // http errors should be less than 1%
  },
};

export default function () {
  //const params = {
  //  timeout: '90s'
  //};
  http.get('https://uat-skillsets-api.lmasu.co.za/get_all_engineers');
  sleep(1.5);
}

// https://k6.io/blog/integrating-load-testing-with-gitlab/