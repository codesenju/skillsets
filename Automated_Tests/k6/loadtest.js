// Creator: k6 Browser Recorder 0.6.2

import { sleep, group } from 'k6'
import http from 'k6/http'

export const options = {
  duration: '1m',
  vus: 250,
  thresholds: {
    http_req_duration: ['p(95)<600'], // 95 percent of response times must be below 600ms
    http_req_failed: ['rate<0.01'], // http errors should be less than 1%
  },
};

export default function main() {
  let response

  group('page_1 - https://uat-skillsets-ui.lmasu.co.za/', function () {
    response = http.get('https://uat-skillsets-ui.lmasu.co.za/', {
      headers: {
        'upgrade-insecure-requests': '1',
        'user-agent':
          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
      },
    })

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/css/287a67d354840dfc.css',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/css/a1dab137a0571bdd.css',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/chunks/webpack-8fa1640cc84ba8fe.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/chunks/framework-2c79e2a64abdb08b.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/chunks/main-4df221df76d0b5c0.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/chunks/pages/_app-7172e87d084d5d88.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/chunks/154-deb465655e695968.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/chunks/pages/index-08dcade2b75708d9.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/JZql7vvy5nq_gp2vF1alT/_buildManifest.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/JZql7vvy5nq_gp2vF1alT/_ssgManifest.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get('https://uat-skillsets-ui.lmasu.co.za/api/engineers', {
      headers: {
        accept: 'application/json, text/plain, */*',
        referer: 'https://uat-skillsets-ui.lmasu.co.za/',
        'user-agent':
          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
      },
    })

    response = http.get('https://uat-skillsets-ui.lmasu.co.za/favicon.ico', {
      headers: {
        referer: 'https://uat-skillsets-ui.lmasu.co.za/',
        'user-agent':
          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
      },
    })

    response = http.post(
      'https://uat-skillsets-ui.lmasu.co.za/api/engineers',
      '{"name":"k6","skills":"load testing"}',
      {
        headers: {
          'content-type': 'application/json',
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get('https://uat-skillsets-ui.lmasu.co.za/', {
      headers: {
        referer: 'https://uat-skillsets-ui.lmasu.co.za/',
        'upgrade-insecure-requests': '1',
        'user-agent':
          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
      },
    })

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/css/287a67d354840dfc.css',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/css/a1dab137a0571bdd.css',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/chunks/webpack-8fa1640cc84ba8fe.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/chunks/framework-2c79e2a64abdb08b.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/chunks/main-4df221df76d0b5c0.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/chunks/pages/_app-7172e87d084d5d88.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/chunks/154-deb465655e695968.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/chunks/pages/index-08dcade2b75708d9.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/JZql7vvy5nq_gp2vF1alT/_buildManifest.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/JZql7vvy5nq_gp2vF1alT/_ssgManifest.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get('https://uat-skillsets-ui.lmasu.co.za/api/engineers', {
      headers: {
        accept: 'application/json, text/plain, */*',
        referer: 'https://uat-skillsets-ui.lmasu.co.za/',
        'user-agent':
          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
      },
    })

    response = http.get('https://uat-skillsets-ui.lmasu.co.za/favicon.ico', {
      headers: {
        referer: 'https://uat-skillsets-ui.lmasu.co.za/',
        'user-agent':
          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
      },
    })

    response = http.put(
      'https://uat-skillsets-ui.lmasu.co.za/api/engineers/?engineerName=k6',
      '{"skills":"load testing, X-Ray, CloudWatch, Adot Addon"}',
      {
        headers: {
          'content-type': 'application/json',
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get('https://uat-skillsets-ui.lmasu.co.za/', {
      headers: {
        referer: 'https://uat-skillsets-ui.lmasu.co.za/',
        'upgrade-insecure-requests': '1',
        'user-agent':
          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
      },
    })

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/css/287a67d354840dfc.css',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/css/a1dab137a0571bdd.css',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/chunks/webpack-8fa1640cc84ba8fe.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/chunks/framework-2c79e2a64abdb08b.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/chunks/main-4df221df76d0b5c0.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/chunks/pages/_app-7172e87d084d5d88.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/chunks/154-deb465655e695968.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/chunks/pages/index-08dcade2b75708d9.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/JZql7vvy5nq_gp2vF1alT/_buildManifest.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/JZql7vvy5nq_gp2vF1alT/_ssgManifest.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get('https://uat-skillsets-ui.lmasu.co.za/api/engineers', {
      headers: {
        accept: 'application/json, text/plain, */*',
        referer: 'https://uat-skillsets-ui.lmasu.co.za/',
        'user-agent':
          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
      },
    })

    response = http.get('https://uat-skillsets-ui.lmasu.co.za/favicon.ico', {
      headers: {
        referer: 'https://uat-skillsets-ui.lmasu.co.za/',
        'user-agent':
          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
      },
    })

    response = http.del(
      'https://uat-skillsets-ui.lmasu.co.za/api/engineers/?engineerName=k6',
      null,
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get('https://uat-skillsets-ui.lmasu.co.za/', {
      headers: {
        referer: 'https://uat-skillsets-ui.lmasu.co.za/',
        'upgrade-insecure-requests': '1',
        'user-agent':
          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
      },
    })

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/css/287a67d354840dfc.css',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/css/a1dab137a0571bdd.css',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/chunks/webpack-8fa1640cc84ba8fe.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/chunks/framework-2c79e2a64abdb08b.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/chunks/main-4df221df76d0b5c0.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/chunks/pages/_app-7172e87d084d5d88.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/chunks/154-deb465655e695968.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/chunks/pages/index-08dcade2b75708d9.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/JZql7vvy5nq_gp2vF1alT/_buildManifest.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get(
      'https://uat-skillsets-ui.lmasu.co.za/_next/static/JZql7vvy5nq_gp2vF1alT/_ssgManifest.js',
      {
        headers: {
          referer: 'https://uat-skillsets-ui.lmasu.co.za/',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"macOS"',
        },
      }
    )

    response = http.get('https://uat-skillsets-ui.lmasu.co.za/api/engineers', {
      headers: {
        accept: 'application/json, text/plain, */*',
        referer: 'https://uat-skillsets-ui.lmasu.co.za/',
        'user-agent':
          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
      },
    })

    response = http.get('https://uat-skillsets-ui.lmasu.co.za/favicon.ico', {
      headers: {
        referer: 'https://uat-skillsets-ui.lmasu.co.za/',
        'user-agent':
          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
      },
    })
  })

  // Automatically added sleep
  sleep(1)
}
