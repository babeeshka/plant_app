const searchBtn = document.getElementById("search-btn");
const plantInfo = document.getElementById("plant-info");


function searchPlant() {
  var name = document.getElementById("name").value;
  fetch('/search_plant', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({name: name})
  })
  .then(response => response.json())
  .then(data => {
    var searchResults = document.getElementById("search-results");
    searchResults.style.display = "block";
    var searchResultsList = document.getElementById("search-results-list");
    searchResultsList.innerHTML = "";
    data.forEach(plant => {
      var listItem = document.createElement("li");
      listItem.className = "list-group-item";
      var link = document.createElement("a");
      link.href = "#";
      link.onclick = function() { selectPlant(plant); };
      link.innerHTML = plant.common_name + " (" + plant.scientific_name + ")";
      listItem.appendChild(link);
      searchResultsList.appendChild(listItem);
    });
  });
}

function selectPlant(plant) {
  var plantInfoBody = document.getElementById("plant-info-body");
  plantInfoBody.innerHTML = "";
  var row = document.createElement("tr");
  var commonName = document.createElement("td");
  commonName.innerHTML = plant.common_name;
  row.appendChild(commonName);
  var scientificName = document.createElement("td");
  scientificName.innerHTML = plant.scientific_name;
  row.appendChild(scientificName);
  // Add the other plant properties here...
  plantInfoBody.appendChild(row);
}


searchBtn.addEventListener("click", function() {
  // Get the user input from the search field
  const userInput = document.getElementById("plant-input").value;

  // Use the user input to search for the plant information
  const plantData = searchPlantData(userInput);

  // If the plant data is found, populate the "Plant Information" table and show it
  if (plantData) {
    populatePlantInfoTable(plantData);
    plantInfo.style.display = "block";
  } else {
    // If the plant data is not found, display an error message
    alert("Plant not found");
  }
});

function searchPlant() {
    // Get the input value
    var input = document.getElementById("name").value;

    // Make an AJAX request to the server to search for the plant
    // Replace the URL with the URL of your server endpoint
    fetch("/search_plant?name=" + input)
        .then(response => response.json())
        .then(data => {
            // Hide the search form and show the search results
            document.getElementById("search-form").style.display = "none";
            document.getElementById("search-results").style.display = "block";

            // Display the search results in a list
            var list = document.getElementById("search-results-list");
            list.innerHTML = "";
            for (var i = 0; i < data.length; i++) {
                var item = document.createElement("li");
                item.appendChild(document.createTextNode(data[i].common_name + " (" + data[i].scientific_name + ")"));
                list.appendChild(item);
            }
        })
        .catch(error => {
            console.error(error);
        });
}

function displayPlantInfo(plant) {
    const plantInfoBody = document.getElementById('plant-info-body');
    plantInfoBody.innerHTML = '';
    for (const [key, value] of Object.entries(plant)) {
        if (key !== 'id' && key !== 'image_url') {
            const row = document.createElement('tr');
            const keyCell = document.createElement('td');
            const valueCell = document.createElement('td');
            keyCell.innerHTML = key.replace('_', ' ');
            valueCell.innerHTML = value;
            row.appendChild(keyCell);
            row.appendChild(valueCell);
            plantInfoBody.appendChild(row);
        }
    }
    const plantInfo = document.getElementById('plant-info');
    plantInfo.style.display = 'block';
    const submitForm = document.getElementById('submit-form');
    submitForm.elements['id'].value = plant.id;
    submitForm.elements['plant_info[common_name]'].value = plant.common_name;
    submitForm.elements['plant_info[scientific_name]'].value = plant.scientific_name;
    plantInfo.scrollIntoView();
}

function reviewPlant() {
    const modifyButton = document.getElementById('modify-button');
    modifyButton.style.display = 'none';
    const submitButton = document.createElement('button');
    submitButton.type = 'submit';
    submitButton.classList.add('btn', 'btn-primary', 'mr-3');
    submitButton.innerHTML = 'Submit';
    submitButton.addEventListener('click', () => {
        const submitForm = document.getElementById('submit-form');
        submitForm.submit();
    });
    const cancelButton = document.createElement('button');
    cancelButton.type = 'button';
    cancelButton.classList.add('btn', 'btn-secondary');
    cancelButton.innerHTML = 'Cancel';
    cancelButton.addEventListener('click', () => {
        modifyButton.style.display = 'block';
        submitButton.remove();
        cancelButton.remove();
    });
    const submitForm = document.getElementById('submit-form');
    submitForm.appendChild(submitButton);
    submitForm.appendChild(cancelButton);
}

function populatePlantInfoTable(plantData) {
    const nameCell = document.getElementById("name-cell");
    const typeCell = document.getElementById("type-cell");
    const lightCell = document.getElementById("light-cell");
    const waterCell = document.getElementById("water-cell");
  
    nameCell.innerText = plantData.name;
    typeCell.innerText = plantData.type;
    lightCell.innerText = plantData.light;
    waterCell.innerText = plantData.water;
  }
  