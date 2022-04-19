const searchField = document.querySelector('#searchField');
const tableOutput = document.querySelector('.table-output');
const appTable = document.querySelector('.app-table')
const paginationContainer = document.querySelector('.pagination-container')
const tBody = document.querySelector('.table-body')
const noResult = document.querySelector('.no-result')






tableOutput.style.display = "none";
searchField.addEventListener("keyup", (e) => {

    // We use javascript here because we need to search stuff 
    const searchValue = e.target.value;

    if (searchValue.trim().length > 0) {
        paginationContainer.style.display = 'none';

        tBody.innerHTML = "";
        fetch("search-income", { //search-expenses is the url we have assigned and from where it fetches is api
            
            body: JSON.stringify({ searchText: searchValue }),
            method: "POST",
            
        })

            .then((res) => res.json())
            .then((data) => {
                console.log("data", data);

                tableOutput.style.display = 'block';
                appTable.style.display = 'none';


                if (data.length === 0) {

                    noResult.style.display = 'block';
                    tableOutput.style.display = 'none';



                    




                }


                

                

                else {
                    noResult.style.display = 'none';

                    data.forEach((item) => {


                        tBody.innerHTML += `

                        
                        <tr>
                        <td>${item.amount} </td>
                        <td>${item.source} </td>
                        <td>${item.description} </td>
                        <td>${item.date} </td>

                        </tr>    
                        `;

                    });
                }







            });







    }

    else {
        appTable.style.display = 'block';
        paginationContainer.style.display = 'block';
        tableOutput.style.display = 'none';
        noResult.style.display = 'none';








    }



});