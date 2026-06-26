document.addEventListener(
    "DOMContentLoaded",
    function()
    {


        const sliders =
            document.querySelectorAll(
                ".ingredient-slider"
            );


        const nutritionUrl =
            document
            .getElementById(
                "nutrition-url"
            )
            .dataset.url;



        function updateNutrition()
        {


            let params =
                new URLSearchParams();



            sliders.forEach(
                slider =>
                {


                    params.append(

                        "food_" +
                        slider.dataset.food,

                        slider.value

                    );



                    let amount =
                        document.getElementById(

                            "amount-" +
                            slider.dataset.food

                        );


                    if(amount)
                    {

                        amount.innerText =
                            slider.value;

                    }


                }
            );



            fetch(
                nutritionUrl +
                "?" +
                params.toString()
            )


            .then(
                response =>
                response.json()
            )


            .then(
                data =>
                {


                    Object.entries(data)
                    .forEach(
                        ([id,value]) =>
                        {


                            let nutrient =
                                document.getElementById(
                                    "nutrient-" + id
                                );



                            if(nutrient)
                            {

                                nutrient.innerText =
                                    Number(value)
                                    .toFixed(2);

                            }


                        }
                    );


                }
            );


        }



        sliders.forEach(
            slider =>
            {


                slider.addEventListener(
                    "input",
                    updateNutrition
                );


            }
        );



        updateNutrition();


    }
);