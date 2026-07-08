const brand = document.getElementById("brand");
const model = document.getElementById("model");

// 브랜드 선택
brand.addEventListener("change", () => {

    fetch("/models/" + brand.value)
        .then(response => response.json())
        .then(models => {

            model.innerHTML = "";

            models.forEach(car => {

                let option = document.createElement("option");

                option.value = car;
                option.textContent = car;

                model.appendChild(option);

            });

        });

});

// 모델 선택
model.addEventListener("change", () => {

    fetch("/vehicle/" + brand.value + "/" + model.value)
        .then(response => response.json())
        .then(info => {

            document.getElementById("fuel_type").value = info.fuel_type || "";
            document.getElementById("transmission").value = info.transmission || "";
            document.getElementById("body_type").value = info.body_type || "";
            document.getElementById("engine_displacement").value = info.engine_displacement || "";
            document.getElementById("engine_cylinders").value = info.engine_cylinders || "";
            document.getElementById("engine_type").value = info.engine_type || "";
            document.getElementById("wheel_system").value = info.wheel_system || "";

        });

});