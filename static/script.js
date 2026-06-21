let boardDiv=document.getElementById("board")
let scoreSpan=document.getElementById("score")

let gameOver=false
let winShown=false

function drawBoard(board){

boardDiv.innerHTML=""

for(let r=0;r<4;r++){

for(let c=0;c<4;c++){

let tile=document.createElement("div")
tile.classList.add("tile")

let value=board[r][c]

if(value!=0){

tile.innerText=value
tile.classList.add("tile-"+value)

if(value==2048 && !winShown){
document.getElementById("winBox").style.display="flex"
winShown=true
}

}

boardDiv.appendChild(tile)

}

}

}

function loadBoard(){

fetch("/board")

.then(res=>res.json())

.then(data=>{

drawBoard(data.board)

scoreSpan.innerText=data.score

})

}

document.addEventListener("keydown",function(e){

if(gameOver) return

let direction=null

if(e.key==="ArrowLeft") direction="left"
if(e.key==="ArrowRight") direction="right"
if(e.key==="ArrowUp") direction="up"
if(e.key==="ArrowDown") direction="down"

if(direction){

fetch("/move",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({direction:direction})

})

.then(res=>res.json())

.then(data=>{

drawBoard(data.board)

scoreSpan.innerText=data.score

if(data.game_over){

gameOver=true

document.getElementById("gameOverBox").style.display="flex"

document.getElementById("finalScore").innerText=data.score

}

})

}

})

document.getElementById("restartBtn").addEventListener("click",function(){

document.getElementById("gameOverBox").style.display="none"

fetch("/newgame",{method:"POST"})

.then(res=>res.json())

.then(data=>{

gameOver=false
winShown=false

drawBoard(data.board)

scoreSpan.innerText=data.score

})

})

document.getElementById("continueBtn").addEventListener("click",function(){

document.getElementById("winBox").style.display="none"

})

document.getElementById("restartWinBtn").addEventListener("click",function(){

fetch("/newgame",{method:"POST"})

.then(res=>res.json())

.then(data=>{

gameOver=false
winShown=false

drawBoard(data.board)

scoreSpan.innerText=data.score

document.getElementById("winBox").style.display="none"

})

})

document.getElementById("newGameBtn").addEventListener("click",function(){

fetch("/newgame",{method:"POST"})

.then(res=>res.json())

.then(data=>{

gameOver=false
winShown=false

drawBoard(data.board)

scoreSpan.innerText=data.score

})

})

loadBoard()