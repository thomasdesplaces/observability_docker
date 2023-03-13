// init context: importing modules
import http from 'k6/http';
import { sleep, check, group } from 'k6';

// init context: define k6 options
// export const options = {
//     vus: 2,
//     duration: '10s',
// };
export const options = {
    stages: [
        { duration: '10s', target: 3}//,
        //{ duration: '20s', target: 0}
    ]
}

// init context: global variables
const url = "http://backend:5050/clients";

// init context: define custom function
function displayUrl() {
    console.log(url)
}

export default function () {
    // Display base URL
    displayUrl();

    group('Clients management', (_) => {
        // Client creation
        let newClientDetails = JSON.stringify({
            firstname: "Thomas__" + __ITER,
            lastname: "Dupont"
        })
        const newClient = http.post(url, newClientDetails);
        check(newClient, {
            'is status 201': (r) => r.status === 201,
            'is ID present': (r) => r.json().hasOwnProperty('id')
        });

        // Get clients list
        const listClients = http.get(url).json();
        check(listClients, { 'retrieved clients': (clients) => clients.length > 0});

        // Get client details
        const getClient = http.get(url+"/"+listClients[0].id);
        check (getClient, {
            'is status 200': (r) => r.status === 200
        });

        // Put client details
        let newLastname = JSON.stringify({
            lastname: "Dupond__" + __ITER
        })
        const putClient = http.get(url+"/"+listClients[0].id, newLastname);
        check (putClient, {
            'is status 200': (r) => r.status === 200
        });

        // Delete client
        const deleteClient = http.del(url+"/"+listClients[0].id);
        check (deleteClient, {
            'is status 204': (r) => r.status === 204
        });

        // Get 404 Error
        const notFound = http.get(url+"/client")
        check (notFound, {
            'is status 404': (r) => r.status === 404
        });
        sleep(1);
    })
}
