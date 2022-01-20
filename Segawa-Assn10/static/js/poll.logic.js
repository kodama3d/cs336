/*Name: Dustin Segawa*/
/*Assignment: CS336 Assignment #9*/
/*Created: 8/12/2020*/
/*Description: JavaScript Page for Poll Page*/

/*GLOBAL VARIABLES*/
const poll_elem = document.getElementsByName('award_poll');
let vote;              /*current user's vote*/
let voteArr = [];
var ctx = document.getElementById('myChart');
var chartData = new Array();
var myChart = new Chart(ctx, {                                  /*chart.js plugin*/
    type: 'bar',
    data: {
        labels: ['Antenna #1', 'Antenna #2', 'Antenna #3'],
        datasets: [{
            label: '# of Votes',
            data: chartData,
            backgroundColor: [
                'rgba(255, 0, 0, .5)',
                'rgba(0, 0, 255, .5)',
                'rgba(0, 255, 0, .5)'
            ],
            borderColor: [
                'rgba(255, 0, 0, 1)',
                'rgba(0, 0, 255, 1)',
                'rgba(0, 255, 0, 1)'
            ],
            borderWidth: 3
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});

/*EVENT LISTENER*/
document.getElementById("poll_form").addEventListener("submit", submitVote);

/*runs when page is finished loading*/
window.onload = function () {                       /*runs function once page loads*/
    voteArr = getVotes('votes');              /*call function to pull local storage into vote array*/
    setVotes(voteArr[0], voteArr[1], voteArr[2]);   /*update page to show current vote*/
    updateChart();                                  /*updates chart on page*/
}

/*gets current vote count out of local storage, if not found, sets votes to 0
* IN: key for local storage
* OUT: voting array
* Calls: none*/
function getVotes(name) {
    let localVote = localStorage.getItem(name);         /*get local storage*/

    if (localVote !== null) {                           /*test for missing local storage file*/
        let votesSplit = [];
        votesSplit = localVote.split(',');      /*split vote pairs*/
        let i = 0;                                      /*loops through vote pairs*/
        for (i in votesSplit) {
            voteArr[i] = Number(votesSplit[i]);         /*convert string into number*/
        }
    }
    else voteArr = [0, 0, 0];       /*set to 0 if no local storage file found*/
    console.log(voteArr);
    return voteArr;
}

/*updates displayed vote count on the page
* IN: voting array
* OUT: none
* Calls: none*/
function setVotes(vote1, vote2, vote3) {
    document.getElementById("vote1").innerHTML = vote1;
    document.getElementById("vote2").innerHTML = vote2;
    document.getElementById("vote3").innerHTML = vote3;
}

/*Runs on vote submission, getting polling results, updating votes, and saving in local storage
* IN: none
* OUT: none
* Calls: getPoll, updateVotes, setVotes, storeVotes*/
function submitVote() {
    let voteNum = getPoll();    /*function to get selected vote from poll page*/
    updateVotes(voteNum);       /*increment vote count array*/
    setVotes();                 /*update the vote count on the page*/
    updateChart();              /*updates chart on the page*/
    storeVotes();               /*save the votes into local storage*/
    alert("Thank you for voting for: " + vote);
}

/*Get selected item from poll page
* IN: none
* OUT: selected poll item number
* Calls: none*/
function getPoll() {
    for (let j = 0; j < poll_elem.length; j++) {    /*loop through elements*/
        if (poll_elem[j].checked) {                 /*test for check*/
            vote = poll_elem[j].value;              /*get selected value*/
            return j;
            // break;                               /*break loop when found*/
        }
    }
}

/*stores vote count array into local storage
* IN: none
* OUT: none
* Calls: none*/
function storeVotes() {
    localStorage.setItem('votes', voteArr);
}

/*increments vote count array based on selected item
* IN: selected poll number
* OUT: none
* Calls: none*/
function updateVotes(voteNum) {
    voteArr[voteNum]++;
}

/*Updates chart, plugin requires array to be in a specific format
* IN: none
* OUT: none
* Calls: none*/
function updateChart() {
    chartData.push(voteArr[0]);     /*pushes into next node*/
    chartData.push(voteArr[1]);
    chartData.push(voteArr[2]);
    myChart.update();               /*manually updates chart after push*/
    console.log(chartData);
}