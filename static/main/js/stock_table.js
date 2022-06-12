const stockSearch = document.querySelector('#stock-button')
let stockSymbol
stockSearch.addEventListener('click', function () {
    console.log("Clicked")
    stockSymbol = document.querySelector('#stock-symbol').value
    fetchData(stockSymbol)
})


function fetchData(symbol) {

    //fetch('https://data.sec.gov/submissions/CIK##########.json')
    console.log("yes ", symbol)
}

fetch('https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json', {
    method: 'GET',
    headers: {
        //'Access-Control-Allow-Origin': 'https://www.sec.gov',
        //'Vary': 'Origin',
        //'Access-Control-Allow-Credentials': 'true',
        'User-Agent': "My Company bab385@gmail.com",
        'Accept-Encoding': "gzip, deflate",
        'Host': "www.sec.gov",
    },
}).then(response => {
    if (!response.ok) {
        throw response;
    }
    //console.log(response)
    return response.json()
}).then(data => {
    console.log(data)
    // for (i = 0; i < data.length; i++) {
    //     console.log(data[i])
    // }
})

const tableBody = document.querySelector("#stock-table-body")
const newvar = "hello"
tableBody.innerHTML += `<tr>
                            <td>${newvar}</td>
                            <td></td>
                        </tr>`
console.log(tableBody)