/*Name: Dustin Segawa*/
/*Assignment: CS336 Assignment #9*/
/*Created: 8/12/2020*/
/*Description: JavaScript Page for Registration Page*/

/*GLOBAL VARIABLES*/
const s1_elem = document.getElementsByName('session1');
const s2_elem = document.getElementsByName('session2');
const s3_elem = document.getElementsByName('session3');
const s1_feed = document.getElementById('feeds');
const s1_refl = document.getElementById('reflectors');
const s1_mat = document.getElementById('materials');
const s2_sys = document.getElementById('system');
const s2_trans = document.getElementById('transmission');
const s2_int = document.getElementById('interference');
const s3_cal = document.getElementById('calibration');
const s3_proc = document.getElementById('processing');
const s3_amp = document.getElementById('amplifiers');

var session1 = '';  /*declare variables*/
var session2 = '';
var session3 = '';
var voted = '';

/*EVENT LISTENERS*/
// document.getElementById("submit_form").addEventListener("click", beforeSubmit);
document.getElementById("confIDnum").addEventListener("blur", getCookie);
document.getElementById("reg_form").addEventListener("submit", setCookie);

/*/!*This enable/disable thing gave me a headache for 6 hours.... lol*!/
/!*Needed to remove Event Listener - can't be anonymous
* IN: event
* OUT: none
* Calls preventDefault function*!/
function preDef(event) {
    event.preventDefault();
}
/!*disables submit function on the form
* IN: none
* OUT: none
* Calls: DOM event listener function and preDef function*!/
function disableSubmit() {
    // document.getElementById("reg_form").submit(function(event){event.preventDefault();});
    document.getElementById("reg_form").addEventListener("submit", preDef);
}
/!*re/enables submit function on the form
* IN: none
* OUT: none
* Calls: DOM event listener function and preDef function*!/
function enableSubmit() {
    // document.getElementById("reg_form").unbind('submit');
    document.getElementById("reg_form").removeEventListener("submit", preDef);
}

//replaced by your recommendation
function beforeSubmit() {
    getWorkshops();
    validateWorkshops();
}*/

//replaced with your recommendation
function validateForm() {
    getWorkshops();
    return validateWorkshops();
}

/*get selected workshops from each session# into session variables
* IN: none
* OUT: none
* Calls: none*/
function getWorkshops() {
    for (let i = 0; i < s1_elem.length; i++) {  /*loop through elements*/
        if (s1_elem[i].checked) {           /*test for check*/
            session1 = s1_elem[i].value;    /*get selected value*/
            break;                          /*break loop when found*/
        }
    }
    for (let i = 0; i < s2_elem.length; i++) {
        if (s2_elem[i].checked) { session2 = s2_elem[i].value; break;}}
    for (let i = 0; i < s3_elem.length; i++) {
        if (s3_elem[i].checked) { session3 = s3_elem[i].value; break;}}
}

/*function to validate workshop selections
*   IN: none
*   OUT: none
*   Calls: getWorkshops, openErrorWindow, uncheckSession2, disableSubmit, enableSubmit*/
function validateWorkshops() {
    /*test if B in first session was selected, and anything in second session conflict*/
    if (session1 == 'reflectors' && session2 != '') {
        uncheckSession2();  /*redundant if disableSession2 runs, unchecks items in Session 2*/
        // disableSession2();   /*disables session 2*/
        openErrorWindow('http://127.0.0.1:5000/error_b');
        // disableSubmit();
        return false;
    }
    /*test if B in first session was selected, and processing in third session, causing conflict*/
    else if (session1 == 'reflectors' && session3 == 'processing') {
        openErrorWindow('http://127.0.0.1:5000/error_b3');
        // disableSubmit();
        return false;
    }
    /*test if F in second session was selected, and if processing was not taken in third session, causing conflict*/
    else if (session2 == 'interference') {
        if (session3 != 'processing') {
            // uncheckSession3();  /*unchecks session 3 selection*/
            // disableCalAmp();    /*disables calibration and amplifiers when interference selected*/
            openErrorWindow('http://127.0.0.1:5000/error_f');
            // disableSubmit();
            return false;
        }
    }
    /*test if H in third session was selected, and if interference was not taken in second session, causing conflict*/
    else if (session3 == 'processing') {
        if (session2 != 'interference') {
            // uncheckSession2();  /*unchecks session 2 selection*/
            // disableSysTrans();    /*disables system and transmission when processing selected*/
            openErrorWindow('http://127.0.0.1:5000/error_h');
            // disableSubmit();
            return false;
        }
    }
    else {
        // enableSubmit();
        return true;
    }
}

/*function to open error window in the center of the screen
*   IN: input parameter is URL link to open
*   OUT: none
*   Calls: none*/
function openErrorWindow(url_link) {
    const err_win_w = 500;                              /*window width and height*/
    const err_win_h = 400;
    const center_w = screen.width / 2;                  /*center of screen width and height*/
    const center_h = screen.height / 2;
    const center_win_w = center_w - (err_win_w / 2);    /*calculate center of the screen offset by window size*/
    const center_win_h = center_h - (err_win_h / 2);

    let params =
        'width =' +err_win_w+
        ',height =' +err_win_h+
        ',left =' +center_win_w+
        ',top =' +center_win_h+
        'menubar = no, toolbar = no, location = no, status = no, resizable = no, scrollbars = no';

    window.open(url_link, 'errMsg', params);
}

/*Uncheck session options, these need to be expanded for disable/enable button function logic to work correctly
* IN: none
* OUT: none
* Calls: none*/
function uncheckSession2() {
    s2_sys.checked = false;
    s2_trans.checked = false;
    s2_int.checked = false;
    session2 = '';
}

/*// disabled interactive check/uncheck buttons
// function uncheckSession3() {
//     s3_cal.checked = false;
//     s3_proc.checked = false;
//     s3_amp.checked = false;
//     session3 = '';
// }

// /!*Enable or disable radio buttons for workshop sessions*!/
// function disableSession2() {
//     uncheckSession2();  /!*uncheck items before disabling*!/
//     s2_sys.disabled = true;
//     s2_trans.disabled = true;
//     s2_int.disabled = true;
//     disableWkspH();     /!*disables workshop H, unable to take linked workshop*!/
// }
// function disableSysTrans() {
//     uncheckSession2();  /!*uncheck items before disabling*!/
//     s2_sys.disabled = true;
//     s2_trans.disabled = true;
// }
// function enableSession2() {
//     getWorkshops();
//     if (session1 != 'reflectors' && session3 !='processing') {
//         s2_sys.disabled = false;
//         s2_trans.disabled = false;
//         s2_int.disabled = false;
//         enableSession3();  /!*reenables workshop H if session 2 is open*!/
//     }
// }
// function disableWkspH() {
//     uncheckSession3();  /!*uncheck items before disabling*!/
//     s3_proc.disabled = true;
// }
// function disableCalAmp() {
//     uncheckSession3();  /!*uncheck items before disabling*!/
//     s3_cal.disabled = true;
//     s3_amp.disabled = true;
// }
// function enableSession3() {
//     s3_cal.disabled = false;
//     s3_proc.disabled = false;
//     s3_amp.disabled = false;
// }*/

/*COOKIES*/
function setCookie(){
    let defaultID = 123456;
    if (document.getElementById('confIDnum').value === '') {        /*test if ID is blank*/
        document.getElementById('confIDnum').value = defaultID;     /*give default value*/
    }
    let cookieName = document.getElementById('confIDnum').value;    /*get key from conference ID*/
    let cookieArr = [];
    cookieArr[0] = 'title:' + document.getElementById('titleList').value;
    cookieArr[1] = 'firstname:' + document.getElementById('fname').value;
    cookieArr[2] = 'lastname:' + document.getElementById('lname').value;
    cookieArr[3] = 'street1:' + document.getElementById('street1').value;
    cookieArr[4] = 'street2:' + document.getElementById('street2').value;
    cookieArr[5] = 'city:' + document.getElementById('city').value;
    cookieArr[6] = 'state:' + document.getElementById('stateList').value;
    cookieArr[7] = 'zip:' + document.getElementById('zip').value;
    cookieArr[8] = 'telephone:' + document.getElementById('telephone').value;
    cookieArr[9] = 'email:' + document.getElementById('email').value;
    cookieArr[10] = 'co_name:' + document.getElementById('company_name').value;
    cookieArr[11] = 'co_web:' + document.getElementById('company_web').value;
    cookieArr[12] = 'co_pos:' + document.getElementById('company_pos').value;
    cookieArr[13] = 'session1:' + session1;
    cookieArr[14] = 'session2:' + session2;
    cookieArr[15] = 'session3:' + session3;

                        /*key = cookie values; path*/
    document.cookie = cookieName + '=' + cookieArr + ';path=/;';
}

function getCookie(){
    let cookieName = document.getElementById("confIDnum").value;
    let cookies_raw = document.cookie;                  /*loads all cookies into a lump*/
    let cookie_list = cookies_raw.split(';');   /*splits individual cookies*/

    if (cookie_list != '') {                    /*test if there were no cookies found at all*/
        let name_list = [];                     /*initialize local array variables*/
        let content_list = [];
        let content = [];
        let cookie_data = [];

        /*loop through all cookies found in lump*/
        let i = 0;
        for (i in cookie_list) {
            name_list[i] = cookie_list[i].split('=')[0].trim(); /*pulls keys/names into an array, trims whitespace*/
            content_list[i] = cookie_list[i].split('=')[1];     /*pulls content into an array*/
            if (name_list[i] === cookieName) {                          /*test if key matches current user*/
                alert('Welcome back, your Conference ID Number is: ' + cookieName);
                content = content_list[i].split(',');                   /*pulls fields out of a content node*/

                /*loops through all content found in node*/
                let j = 0;
                for (j in content) {
                    // cookie_data[j] = content[j].split(':');      /*numbered array better?*/

                    /*this puts data into a field name array, I like this better for legibility*/
                    if (content[j].split(':')[2] === undefined) {       /*test for undefined field 3*/
                        cookie_data[content[j].split(':')[0]] = content[j].split(':')[1];
                    } else {                                                    /*rebuild web address*/
                        cookie_data[content[j].split(':')[0]] = content[j].split(':')[1] + ':' + content[j].split(':')[2];
                    }
                }
                console.log(cookie_data);
                propReg(cookie_data);
            }
        }
    }
}

function propReg(cookie_data) {
    /*propagate fields*/
    document.getElementById('titleList').value = cookie_data['title'];
    document.getElementById('fname').value = cookie_data['firstname'];
    document.getElementById('lname').value = cookie_data['lastname'];
    document.getElementById('street1').value = cookie_data['street1'];
    document.getElementById('street2').value = cookie_data['street2'];
    document.getElementById('city').value = cookie_data['city'];
    document.getElementById('stateList').value = cookie_data['state'];
    document.getElementById('zip').value = cookie_data['zip'];
    document.getElementById('telephone').value = cookie_data['telephone'];
    document.getElementById('email').value = cookie_data['email'];
    document.getElementById('company_name').value = cookie_data['co_name'];
    document.getElementById('company_web').value = cookie_data['co_web'];
    document.getElementById('company_pos').value = cookie_data['co_pos'];

    /*propagate workshops*/
    for (let i = 0; i < s1_elem.length; i++) {      /*loop through elements*/
        if (cookie_data['session1'] === s1_elem[i].value) {     /*test for match from cookie*/
            s1_elem[i].checked = true;              /*test for check*/
            break;                                  /*break loop when found*/
        }
    }
    for (let i = 0; i < s2_elem.length; i++) {
        if (cookie_data['session2'] === s2_elem[i].value) {s2_elem[i].checked = true; break;}}
    for (let i = 0; i < s3_elem.length; i++) {
        if (cookie_data['session3'] === s3_elem[i].value) {s3_elem[i].checked = true; break;}}
}
