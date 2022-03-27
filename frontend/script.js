
async function retrieve(){
    let my_res = await fetch("http://localhost:8000/api/articles")
    return await my_res.json()
} 
// res = await res.json();
let res= await retrieve();

let btn = document.getElementById("btn_")
btn.addEventListener("click", addArtElems)
let ul = document.getElementById("news_list")

// let ids = []
// function store_or_rtn_ids(id){
//     if (id!==undefined){
//         ids.push(id);
//         return;
//     }
//     return ids
// }

function addArtElems(){
    let li = document.createElement("li");
    li.classList.add("art-row-item");

    let rdiv = document.createElement("div");
    rdiv.classList.add("row");
    li.appendChild(rdiv);
    let count=0;
    while(res.length){
        let cres = res.shift();
        if (count>=3) break;

        let ldiv = document.createElement("div");
        ldiv.classList.add("col");
        rdiv.appendChild(ldiv);
        
        let img = document.createElement("img");
        img.src = cres.images[0].image;
        ldiv.appendChild(img);

        let h2 =document.createElement("h2");
        h2.innerText= cres.title;
        ldiv.appendChild(h2);

        count++;
    }
    ul.appendChild(li);
}