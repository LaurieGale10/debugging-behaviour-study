
title = 'debugging-prelim-study-exercises';

exerciseNumber = 0;
exerciseDescriptions = [
  `Alex has measured out the dimensions of a cuboid to use for a science experiment. Alex has made a program to calcuate the volume of the cuboid and print it to the screen. However, the program contains some errors.<br><br>The height and depth of the cuboid are 25cm and its width is 50cm. The volume of a cuboid is calculated using the equation below: <br><br>Volume = height x width x depth<br><br>This program contains 2 errors - have a go at fixing them all.`,
  `This program inputs the user's first name, surname, and the year they were born. It then prints a sentence to the screen with their full name and how old they will be at the end of the year.<br><br>If a user's first name is Jo, their last name is Bloggs, and they were born in 2008, the program should print: "Your name is Jo Bloggs and at the end of this year you will be 15".<br><br>This program has 3 errors - have a go at fixing them all.`,
  `This program checks if someone should apply to be a computing teacher using the steps below: <ul><li>Input the user's age.</li><li>Input the user's response to the question "Do you have a passion for teaching computing? Enter 'yes' or 'no': "</li><li>If the user is <strong>21 or over</strong> and does have a passion for teaching computing, the check should be a success. Otherwise, the check should be unsuccessful.</li><li>Print the result of the check.</li></ul>This program has 4 errors - have a go at fixing them all.`,
  `This program should display the first 12 multiples of the number 6 using a while loop, from 1x6 up to 12x6. Fix the errors to make sure it prints them properly.<br><br>This program has 4 errors - have a go at fixing them all.`,
  `This program simulates a game of rock, paper, scissors between two players. This is done using the following steps:<ul><li>Randomly generate a choice for each player using the random.choice() function, which selects a random item from a given list.</li><li>Work out which player won the game or if it was a draw.</li><li>Print the winner to the screen. If the match is a draw, then "The winner is Neither" should be printed.</li></ul>This program has 4 errors - have a go at fixing them all.`
];
exercisePrograms = [
    `height = depth\nwidth = 50\ndepth = 25\nvolume = height * width * depth\nprint("The volume is,volume)`,
    `input("What year were you born in? ") = year_born\n  age = 2023-int(year_born)\n\nfirst_name = input("What is your first name? ")\nlast_name = input("What is your last name? ")\nprint("Your name is",first_name,last_name,"and at the end of this year you will be age")`,
    `print("This program will check if you should apply to be a computing teacher")\nage = int(input("What is your age? "))\ncomputing_degree = input("Do you have a passion for teaching computing? Enter 'yes' or 'no': ")\n\nif age > 21 or computing_degree = "yes":\n  allowed_to_apply = "Successful"\nelse:\n  allowed_to_apply = "Unsuccessful"\n  print("Result of check:",allowed_to_apply)`,
    `count="1"\nprint("The first 12 multiples of the number 6 are:")\nwhile count<12:\n  times_table = 6 * count\n  count=count+1\nprint(times_Table)`,
    `import random\nplayer_1 = random.choice(["Rock","Paper","Scissors"])\nprint("Player 1 has chosen "+player_1)\nplayer_2 = random.choice(["Rock","Paper","Scissors"])\nprint("Player 2 has chosen "+player_2)\n\nif player_1 == player_2:\n  winner = "Neither"\nelif player_1 == "Rock" and player_2 == "Scissors":\n  winner = "Player 1"\nelif player_1 =="Paper" or player_2 == "Rock":\n  winner = "Player 1"\nelif player_1 == "Scissors" or player_2 == "Paper":\n  winner = "Player 1"\nelif:\n  winner = "Player 2"\n  print("The winner is "+winner)`
];

document.getElementById("exerciseNumber").textContent = exerciseNumber+1;
document.getElementById("exerciseDescription").innerHTML = exerciseDescriptions[exerciseNumber];

var participantId;

/**
 * Adjusts the UI based on whether the student has completed all of the exercises or not.
 * In the study, if a student had completed all the debugging exercises, they were unable to retry any of the exercises.
 */
window.onload = function onLoad() {
    if (localStorage.getItem('participantId') != null) {
        participantId = localStorage.getItem('participantId');
        if (JSON.parse(localStorage.getItem('isComplete')) === true) {
            displayComplete();
        }
    }
    else {
        //Generates uuid for participant, used in both the logs and the questionnaire
        participantId = crypto.randomUUID();
        localStorage.setItem('participantId',participantId);
    }
}

window.addEventListener('beforeunload', (event) => {
    event.returnValue = `Are you sure you want to leave or refresh this page? All of your experiment data will be lost.`;
});

/**
 * In the original study, this function writes the program log data to a database, but this functionality is omitted from this open-source version of the code.
 * Instead, view the console to see the data that would've been written to the logs database.
 * @param {*} data JSON object containing log data, as well as timestamp and other data
 */
function postData(data) {
    data['participantId'] = participantId;
    data['exerciseNumber'] = exerciseNumber+1;
    console.log(data) //Note that the "snapshots" JSON array represents the logs collected for each run.

    if (exerciseNumber == 4) {
        complete();
    }
    else {
        nextExercise();
    }
}

/**
 * Function that sends the program log data to the db and updates display for next programming exercise
 */
function nextExercise() {
    exerciseNumber++;
    setupFrame(exerciseNumber);
    document.getElementById("exerciseNumber").textContent = exerciseNumber+1;
    document.getElementById("exerciseDescription").innerHTML = exerciseDescriptions[exerciseNumber];
    if (exerciseNumber == 4) {
        document.getElementById("nextExercise").style = "display: none";
        document.getElementById("finish").style.display = "block";
    }
}

/**
 * Displays the appropriate UI elements for when a student has completed all of the programming exercises.
 */
function displayComplete() {
    document.getElementById("exercisesDiv").style = "display: none";
    document.getElementById("programmingExercisesTitle").style = "display: none";
    document.getElementById("completedDiv").style.display = "block";
    document.getElementById("completedExercisesTitle").style.display = "block";
}

/**
 * Function that runs when user has attempted all programming exercises and presses "Complete".
 * Calls the displayComplete() function and sets a value in local storage to indicate a student has completed all the debugging exercises and cannot attempt them anymore.
 */
function complete() { 
    displayComplete();
    localStorage.setItem('isComplete', true);
}

/**
 * Function implemented for the purpose of open sourcing, so that viewers of the exercises are not restricted to seeing the debugging exercises just once.
 */
function retryExercises() {
    localStorage.setItem('isComplete', false);
    exerciseNumber = 0;
    //Adjust UI
    document.getElementById("exercisesDiv").style = "display: block";
    document.getElementById("programmingExercisesTitle").style = "display: block";
    document.getElementById("completedDiv").style.display = "none";
    document.getElementById("completedExercisesTitle").style.display = "none";

    //Display exercise 1 info
    setupFrame(exerciseNumber);
    document.getElementById("exerciseNumber").textContent = exerciseNumber+1;
    document.getElementById("exerciseDescription").innerHTML = exerciseDescriptions[exerciseNumber];
}

function makeid(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

// Iframe message passing code for Ada code editor ============================================================
const CODE_EDITOR_BASE_URL = "https://code-editor.ada-cs.org/";
const iFrame = document.getElementById("code-editor");
const iFrameContainer = document.getElementById("ide");
let targetDomainSource;
let targetDomainOrigin;
let uid = makeid(10);
iFrame.src = CODE_EDITOR_BASE_URL + "/#" + uid;

function sendMessage(obj) {
    obj.uid = uid;
    if (iFrame instanceof HTMLElement) {
        iFrame.contentWindow?.postMessage(obj, iFrame.src);
    } else if (undefined !== targetDomainSource && undefined !== targetDomainOrigin) {
        targetDomainSource.postMessage(obj, targetDomainOrigin);
    } else {
        // This should only happen if undefined foreignDomain and no message is received yet
        console.log("If foreignDomain is undefined, useIFrameMessages can only reply to messages (i.e. can send only after the first message has been received)");
    }
}

function handleReceive(e) {
    if (e.origin === window.origin) return;

    // Make sure that the data is what we expect, and that it has a correct uid
    if (!(typeof e.data === 'object' && e.data !== null && !Array.isArray(e.data) && e.data.hasOwnProperty('uid')
        && e.data.uid === uid)) {
        return;
    }

    if (e.data.hasOwnProperty('type')) {
        if (!targetDomainSource) {
            targetDomainSource = e.source;
            targetDomainOrigin = e.origin;
        } 
        if (replyCallback && e.source) {
            console.log("Calling reply callback")
            const r = replyCallback(e.data);
            if (r && typeof r === "object") {
                //e.source.postMessage(r);
            }
        }
    }
}
window.addEventListener("message", handleReceive);
// ========================================================================================

/**
 * The function that handles any data returned from the code editor.
 * If you return an object, it will be sent to the editor. Return undefined/null/void to not send a reply.
 * @param {*} data Any logs stored tracked by the code editor at the time of the function being called.
 */
function replyCallback(data) {
    console.log("replyCallback() being called")
    switch (data.type) {
        case "resize":
            if (typeof data.height === "number") {
                // TODO this should actually set the height of the div to data.height
                iFrameContainer.setAttribute("style", `height: ${data.height}px`);
            }
            break;
        case "logs":
            postData(data);
            break;
    }
}

/**
 * Function that initialises the code editor with come code, as defined in the "exercisePrograms" list
 */
function setupFrame() {
    sendMessage({
        type: "initialise",
        code:  `# Question ${exerciseNumber + 1}\n`+exercisePrograms[exerciseNumber],
        language: "python",
        logChanges: true
    });
}

/**
 * Function that asks the code editor for logs.
 * It is then up to `replyCallback(data) to change to the next exercise if the logs are received.
 */
function requestLogsAndPostData() {
    sendMessage({
        type: "logs",
        timestamp: Date.now()
    });
}