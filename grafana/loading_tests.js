// init context: importing modules
import http from 'k6/http';
import { sleep, check, group } from 'k6';

export const options = {
    tags: {
        testid: "grafana-front"
    },
    stages: [
        {
            //duration: '30s', target: 10
            duration: '5m', target: 10
        }
    ]
}

// init context: global variables
const url = "http://grafanaha-395633272.eu-west-3.elb.amazonaws.com/";

// init context: define custom function
function displayUrl() {
    console.log(url)
}

export default function () {
    // Display base URL
    displayUrl();

    group('Grafana loading test', (_) => {
        // Get welcome page
        const welcomePage = http.get(url);
        check(welcomePage, { 
            'is status 200': (r) => r.status === 200
        });
    })
}
