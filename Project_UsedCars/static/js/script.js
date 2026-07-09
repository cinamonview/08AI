// ======================================
// AutoPrice AI v2.0
// Frontend Script
// ======================================



const brand = document.getElementById("brand");

const model = document.getElementById("model");





// ======================================
// BRAND CHANGE
// ======================================


brand.addEventListener(
    "change",
    function(){


        model.innerHTML = 
            '<option value="">Select Model</option>';



        clearVehicleInfo();



        if(
            brand.value === ""
        ){

            return;

        }



        fetch(
            "/models/" 
            + encodeURIComponent(
                brand.value
            )
        )

        .then(
            response => response.json()
        )

        .then(
            models => {


                models.forEach(
                    car => {


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


    }
);









// ======================================
// MODEL CHANGE
// ======================================


model.addEventListener(
    "change",
    function(){


        clearVehicleInfo();



        if(
            model.value === ""
        ){

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
            response => response.json()
        )


        .then(
            info => {


                console.log(info);



                document
                .getElementById(
                    "fuel"
                )
                .value =
                    info.fuel_type ?? "";



                document
                .getElementById(
                    "transmission"
                )
                .value =
                    transmissionName(
                        info.transmission
                    );



                document
                .getElementById(
                    "engine"
                )
                .value =
                    engineName(
                        info.engine_displacement
                    );



                document
                .getElementById(
                    "body"
                )
                .value =
                    info.body_type ?? "";



                document
                .getElementById(
                    "wheel"
                )
                .value =
                    wheelName(
                        info.wheel_system
                    );


            }
        );



    }
);









// ======================================
// DISPLAY FORMAT
// ======================================


function transmissionName(code){


    const map = {


        "A":
            "Automatic",


        "M":
            "Manual",


        "CVT":
            "CVT"


    };


    return map[code] || code;


}







function wheelName(code){


    const map = {


        "FWD":
            "Front Wheel Drive",


        "RWD":
            "Rear Wheel Drive",


        "AWD":
            "All Wheel Drive",


        "4WD":
            "Four Wheel Drive"


    };


    return map[code] || code;


}








function engineName(value){


    if(
        !value
    ){

        return "";

    }



    return (

        Number(value)
        /
        1000

    ).toFixed(1)
    +
    " L";


}









// ======================================
// CLEAR VEHICLE INFO
// ======================================


function clearVehicleInfo(){


    document.getElementById(
        "fuel"
    ).value = "";



    document.getElementById(
        "transmission"
    ).value = "";



    document.getElementById(
        "engine"
    ).value = "";



    document.getElementById(
        "body"
    ).value = "";



    document.getElementById(
        "wheel"
    ).value = "";


}









// ======================================
// PREDICT
// ======================================


const predictForm =
    document.getElementById(
        "predictForm"
    );





predictForm.addEventListener(

    "submit",

    function(e){


        e.preventDefault();





        const inputData = {


            make_name:

                brand.value,



            model_name:

                model.value,



            year:

                document
                .getElementById(
                    "year"
                )
                .value,



            mileage:

                document
                .getElementById(
                    "mileage"
                )
                .value,



            has_accidents:

                document
                .getElementById(
                    "accident"
                )
                .value === "True",



            frame_damaged:

                document
                .getElementById(
                    "frame"
                )
                .value === "True"


        };





        console.log(
            inputData
        );







        fetch(

            "/predict",

            {


                method:
                    "POST",



                headers:
                {

                    "Content-Type":
                        "application/json"

                },


                body:

                    JSON.stringify(
                        inputData
                    )


            }

        )



        .then(

            response =>
                response.json()

        )



        .then(

            result => {


                console.log(
                    result
                );



                if(
                    result.error
                ){

                    alert(
                        result.error
                    );

                    return;

                }






                location.href =

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

                    "&confidence="
                    +
                    result.confidence


                    +

                    "&shap="
                    +
                    encodeURIComponent(
                        JSON.stringify(
                            result.shap
                        )
                    );


            }

        );


    }

);