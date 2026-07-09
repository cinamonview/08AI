// ======================================
// 요소 가져오기
// ======================================

const brand = document.getElementById("brand");
const model = document.getElementById("model");




// ======================================
// 표시 변환 함수
// ======================================


function transmissionName(code){

    const map = {

        "A":"Automatic",
        "M":"Manual",
        "CVT":"CVT",
        "Dual Clutch":"Dual Clutch"

    };


    return map[code] || code;

}




function wheelName(code){

    const map = {

        "FWD":"Front Wheel Drive",
        "RWD":"Rear Wheel Drive",
        "AWD":"All Wheel Drive",
        "4WD":"Four Wheel Drive"

    };


    return map[code] || code;

}




function engineName(value){

    if(!value){

        return "";

    }


    const cc = Number(value);


    return (

        cc / 1000

    ).toFixed(1)

    +

    " L ("

    +

    cc

    +

    " cc)";

}





// ======================================
// 메인 페이지
// 브랜드 선택
// ======================================


if(brand){


brand.addEventListener(
"change",
()=>{


    model.innerHTML =
    '<option value="">Select Model</option>';



    clearVehicleInfo();



    if(brand.value===""){

        return;

    }




    fetch(
        "/models/"
        +
        encodeURIComponent(
            brand.value
        )
    )


    .then(
        res=>res.json()
    )


    .then(
        models=>{


            models.forEach(
                car=>{


                    const option =
                    document.createElement(
                        "option"
                    );


                    option.value = car;

                    option.textContent = car;


                    model.appendChild(
                        option
                    );


                }
            );


        }
    );


});


}







// ======================================
// 모델 선택
// ======================================


if(model){


model.addEventListener(
"change",
()=>{


clearVehicleInfo();



if(model.value===""){

    return;

}




fetch(

"/vehicle/"

+

encodeURIComponent(
brand.value
)

+

"/"

+

encodeURIComponent(
model.value
)

)



.then(
res=>res.json()
)



.then(
info=>{


console.log(
"VEHICLE INFO",
info
);



const fuel =
document.getElementById(
"fuel"
);


const transmission =
document.getElementById(
"transmission"
);



const engine =
document.getElementById(
"engine"
);



const wheel =
document.getElementById(
"wheel"
);




if(fuel)
fuel.value =
info.fuel_type ?? "";



if(transmission)
transmission.value =
transmissionName(
info.transmission
);



if(engine)
engine.value =
engineName(
info.engine_displacement
);



if(wheel)
wheel.value =
wheelName(
info.wheel_system
);



}


);



});



}









// ======================================
// Predict
// ======================================


const predictForm =
document.getElementById(
"predictForm"
);



if(predictForm){



predictForm.addEventListener(
"submit",
event=>{


event.preventDefault();



const sendData = {


make_name:
brand.value,


model_name:
model.value,


year:
document.getElementById(
"year"
).value,


mileage:
document.getElementById(
"mileage"
).value,


has_accidents:
document.getElementById(
"accident"
).value==="True",


frame_damaged:
document.getElementById(
"frame"
).value==="True"


};





fetch(

"/predict",

{

method:"POST",

headers:{

"Content-Type":
"application/json"

},

body:
JSON.stringify(
sendData
)

}

)



.then(
res=>res.json()
)



.then(
result=>{


console.log(
"PREDICT RESULT",
result
);



const shapData =
encodeURIComponent(

JSON.stringify(
result.shap ?? []
)

);





window.location.href =

"/result?"

+

"price="
+
result.price

+

"&brand="
+
result.brand

+

"&model="
+
result.model

+

"&year="
+
result.year

+

"&mileage="
+
result.mileage

+

"&fuel="
+
result.fuel

+

"&transmission="
+
result.transmission

+

"&engine="
+
result.engine

+

"&wheel="
+
result.wheel

+

"&shap="
+
shapData;

+

"&confidence="
+
result.confidence;


}

);



}

);


}









// ======================================
// RESULT PAGE SHAP
// ======================================


document.addEventListener(
"DOMContentLoaded",
()=>{


const shapArea =
document.getElementById(
"shapArea"
);



if(!shapArea){

    return;

}




const params =
new URLSearchParams(
window.location.search
);



const shap =
JSON.parse(

params.get("shap")
||
"[]"

);



console.log(
"SHAP DATA",
shap
);



shap.forEach(
item=>{


const div =
document.createElement(
"div"
);



const impact =
Number(
item.impact
);



const direction =

impact >=0

?

"📈 가격 상승 요인"

:

"📉 가격 하락 요인";





div.className =
"alert alert-info";



div.innerHTML =


`

<h5>

${item.feature}

</h5>


<p>

${direction}

</p>


<strong>

영향도 :
$${Math.abs(
impact
).toLocaleString()}

</strong>


`;



shapArea.appendChild(
div
);



}



);



}

);










// ======================================
// 차량정보 초기화
// ======================================


function clearVehicleInfo(){


[
"fuel",
"transmission",
"engine",
"body",
"wheel"

].forEach(

id=>{


const element =
document.getElementById(
id
);



if(element){

element.value="";

}


}

);


}