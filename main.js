const body = document.body
link = "http://192.168.0.101"
pressedStatus = {"w": false, "s": false, "a": false, "d": false}
get_string = "/{}{}/{}{}/{}/{}"
get_comand = {"left_motor":"0",
              "right_motor":"0",
              "left_direction":"+",
              "right_direction":"+",
              "vertical_angle":"5.0",
              "horizontal_angle":"5.0"}

body.addEventListener("keydown", press_key)
body.addEventListener("keyup", release_key)
document.addEventListener("mousemove",mouse_movement)

function press_key(event) {
    pressedStatus[event.key] = true
    get_request()
}
function undone_request() {
    get_comand["left_motor"]=0
    get_comand["right_motor"]=0
    
}
function release_key(event) {
    console.log("aqui foi")
    pressedStatus[event.key] = false
    undone_request()
    get_request()
}

function do_request(){
    let new_get_string= link+"/"+get_comand["left_direction"]+get_comand["left_motor"]
    +"/"+get_comand["right_direction"]+get_comand["right_motor"]+"/"+get_comand["vertical_angle"]+"/"+get_comand["horizontal_angle"]
    if (new_get_string != get_string) {
        console.log("entrou")
        get_string = new_get_string 
        fetch(new_get_string)  
    }
}

function get_request() {
    get_args = "/"

    if (pressedStatus["w"] ==  true && pressedStatus["d"]==true){
        get_comand["left_motor"]=9
        get_comand["right_motor"]=1
        get_comand["left_direction"]="+"
        get_comand["right_direction"]="+"
    }
    else if (pressedStatus["w"] ==  true && pressedStatus["a"]==true){
        get_comand["left_motor"]=9
        get_comand["right_motor"]=9
        get_comand["left_direction"]="+"
        get_comand["right_direction"]="+"
    }
    else if (pressedStatus["s"] ==  true && pressedStatus["d"]==true){
        get_comand["left_motor"]=9
        get_comand["right_motor"]=1
        get_comand["left_direction"]="-"
        get_comand["right_direction"]="-"
        
    }
    else if (pressedStatus["s"] ==  true && pressedStatus["a"]==true){
        get_comand["left_motor"]=9
        get_comand["right_motor"]=9
        get_comand["left_direction"]="-"
        get_comand["right_direction"]="-"
    }
    else if (pressedStatus["w"] ==  true){
        get_comand["left_motor"]=9
        get_comand["right_motor"]=9
        get_comand["left_direction"]="+"
        get_comand["right_direction"]="+"
    }
    else if (pressedStatus["s"] ==  true){
        get_comand["left_motor"]=9
        get_comand["right_motor"]=9
        get_comand["left_direction"]="-"
        get_comand["right_direction"]="-"
    }
    else if (pressedStatus["a"] ==  true){
        get_comand["left_motor"]=0
        get_comand["right_motor"]=9
        get_comand["left_direction"]="+"
        get_comand["right_direction"]="+"
        
    }
    else if (pressedStatus["d"] ==  true){
        get_comand["left_motor"]=9
        get_comand["right_motor"]=0
        get_comand["left_direction"]="+"
        get_comand["right_direction"]="+"
    }
    else{

    }
    do_request()
}


let position_height = 0
let position_width = 0
function mouse_movement(event) {
    let height = window.innerHeight
    let width = window.innerWidth;
    new_position_height = (event.clientY/height)*10
    new_position_width = (event.clientX/width)*10
    if(Math.pow(new_position_height-position_height,2)>1 || Math.pow(new_position_width-position_width,2)>1){
        position_height = new_position_height
        position_width = new_position_width
        get_comand["vertical_angle"] = position_height.toFixed(1)
        get_comand["horizontal_angle"] = 10-position_width.toFixed(1)
        do_request()    
    }
    
}




let count = 0
let canva = document.getElementById("canva")
let esp_image = document.createElement("img")
esp_image.id = "esp-image"
canva.appendChild(esp_image);
const esp_cam_link = "http://192.168.0.107/cam-hi.jpg"
function updateImage()
{
    
    esp_image.src=esp_cam_link+"?random="+new Date().getTime();
    esp_image.id = "esp-img"
    
    setTimeout(updateImage, 100);
}
updateImage()
