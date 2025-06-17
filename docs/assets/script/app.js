const h1 = document.querySelector('header h1');
const searchForm = document.getElementById('search');
const defaultView = document.getElementById('default');
const searchResults = document.getElementById('search-results');
const showDetails = document.getElementById('show-details');
const spoiler = document.getElementById('spoiler');
const backToSearch = document.getElementById('back-to-search');
const noImage = 'https://static.tvmaze.com/images/no-img/no-img-portrait-text.png';
const views = [
    defaultView,
    searchResults,
    showDetails
];

function hideViews() {
    views.forEach(view => view.classList.add('hidden'));
    spoiler.open = false;
};

function clickHandler(id) {
    let data;
    fetch(`https://api.tvmaze.com/shows/${id}?embed=episodes`).then(function(response) {
        if (response.status == 200) return response.json();
    }).then(function(data) {
        populateDetails(data);
    }).catch(function(err) {
        console.log('Fetch Error: ', err)
    });
};

function populateSelect(seasons) {
    let selectHTML = '';
    for (let season in seasons) {
        if (season == '1') {
            selectHTML += `<option selected="selected" value="${season}">Season ${season}</option>`;
        } else {
            selectHTML += `<option value="${season}">Season ${season}</option>`;
        }
    }
    return selectHTML;
}

function populateTable(episodes) {
    tableHTML = '';
    for (let episode of episodes) {
        tableHTML += `<tr>
        <td>${episode.season.toString().length < 2 ?
            '0' + episode.season : episode.season
        }x${episode.number.toString().length < 2 ?
            '0' + episode.number : episode.number
        }</td>
        <td>${episode.name}</td>
        <td>${episode.airdate}</td>
        </tr>`
    }
    return tableHTML;
}

function populateDetails(show) {
    hideViews();

    const showDetails = {
        container: document.getElementById('show-details'),
        title: document.getElementById('show-title'),
        id: document.getElementById('show-id'),
        status: document.getElementById('show-status'),
        img: document.getElementById('show-img'),
        seasonSelect: document.getElementById('season-select'),
        episodesTable: document.getElementById('episodes'),
        episodes: {}
    };

    if (show._embedded.episodes.length) {
        show._embedded.episodes.forEach(function(episode) {
            if (!(`${episode.season}` in showDetails.episodes)) {
                showDetails.episodes[`${episode.season}`] = [];
            }
            showDetails.episodes[`${episode.season}`].push(episode);
        });
    }
    
    showDetails.title.innerText = show.name;
    showDetails.id.innerText = show.id;
    showDetails.status.innerText = show.status;
    showDetails.img.src = show.image ? show.image.medium : noImage;

    if (show._embedded.episodes.length) {
        const season1 = Object.keys(showDetails.episodes)[0];
        showDetails.episodesTable.innerHTML = `${
            populateTable(showDetails.episodes[season1])
        }`;
        
        showDetails.seasonSelect.innerHTML = `${
            populateSelect(showDetails.episodes)
        }`;
        showDetails.seasonSelect.addEventListener('change', evt => {
            showDetails.episodesTable.innerHTML = `${populateTable(
                showDetails.episodes[showDetails.seasonSelect.value]
            )}`
        });
    } else {
        showDetails.seasonSelect.innerHTML = '';
        showDetails.episodesTable.innerHTML = '';
    }
    showDetails.container.classList.remove('hidden');
};

function populateResults(query, results) {
    hideViews();
    searchForm.query.value = '';
    const searchResults = document.getElementById('search-results');
    
    searchResults.innerHTML = `<div id="search-summary">Search Results for "${query}"</div>`;
    results.forEach(result => {
        const resultDiv = document.createElement('div');
        const resultImage = result.show.image ? result.show.image.medium : noImage;
        resultDiv.classList.add('search-result');
        resultDiv.innerHTML = `<div>
        <p>
            <span onClick="clickHandler(${result.show.id})"><b>${result.show.name}</b><br></span>
            ID: ${result.show.id}<br>
            Status: ${result.show.status}<br>
        </p>
        </div>
        <img src="${resultImage}" alt="" onClick="clickHandler(${result.show.id})">
        `;
        searchResults.appendChild(resultDiv);
    });

    searchResults.classList.remove('hidden');
};

searchForm.addEventListener('submit', evt => {
    evt.preventDefault();

    const query = searchForm.query.value;

    if (query.length) {
        let data;
        fetch(`https://api.tvmaze.com/search/shows?q=${query}`).then(function(response) {
            if (response.status == 200) return response.json();
            throw Error('Something Went Wrong!')
        }).then(function(data) {
            populateResults(query, data);
        }).catch(function(err) {
            console.log('Fetch Error: ', err)
        });
    }
});

h1.addEventListener('click', evt => {
    hideViews();
    defaultView.classList.remove('hidden');
});

backToSearch.addEventListener('click', evt => {
    hideViews();
    searchResults.classList.remove('hidden');
});