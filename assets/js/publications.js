// Loads publication data and displays in HTML element 

function getDataSet(path) {
    return fetch(path)
            .then(r => r.text());
}


function csvStringToArray(strData) {
    const objPattern = new RegExp(("(\\,|\\r?\\n|\\r|^)(?:\"([^\"]*(?:\"\"[^\"]*)*)\"|([^\\,\\r\\n]*))"),"gi");
    let arrMatches = null, arrData = [[]];
    while (arrMatches = objPattern.exec(strData)){
        if (arrMatches[1].length && arrMatches[1] !== ",")arrData.push([]);
        arrData[arrData.length - 1].push(arrMatches[2] ? 
            arrMatches[2].replace(new RegExp( "\"\"", "g" ), "\"") :
            arrMatches[3]);
    }
    return arrData;
}


function displayDataTables(dataSet) {
    $(document).ready(function () {
        $('#example').DataTable({
            data: dataSet,
            columns: [
                { title: 'Author' },
                { title: 'Title' },
                { title: 'Date' },
                { title: 'Publication' },
                { title: 'Link',
                "render": function(data, type, row, meta){
                  if(type === 'display'){
                      data = '<a href="' + data + '">' + data + '</a>';
                  }
  
                  return data;
              }}
            ],
            order: [[2, 'desc']],
            "pageLength": 5,
            lengthMenu: [5, 10, 25, 50, 100, 200],
        });
      });
}


function displayDataSet(dataSetPath) {
    getDataSet(dataSetPath)
        .then(dataSetString => {
            // remove this line after testing
            console.log("Raw data", dataSetString);

            // handle csv or json
            var parseFunction = JSON.parse;
            if (dataSetString.includes("csv")) {
                parseFunction = csvStringToArray;
            }
            let dataSet = parseFunction(dataSetString);

            // remove this line after testing
            console.log("Parsed data", dataSet);

            displayDataTables(dataSet);
        });
}

