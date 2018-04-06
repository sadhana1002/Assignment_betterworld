/* data route */
    var url = "/gender_growth_over_years";
    femaleBorrowers = []
    year = []
    maleBorrowers = []
    
    var countryList = []  
    var sectorNames = [];  
    var femaleCount = []; 
    var maleCount = []     
    
    var sectoreResponseData
    var borrowerResponseData

    function getCountryData(chosenCountry) {

        var country_yearwise_list = borrowerResponseData[chosenCountry]
        femaleBorrowers = []
        year = []
        maleBorrowers = []
        for (var i = 0 ; i < country_yearwise_list.length ; i++){
            
                countryData = country_yearwise_list[i]                    
                femaleBorrowers.push(countryData.FEMALE)
                maleBorrowers.push(countryData.MALE)
                year.push(countryData.YEAR)                    
        }     
    }    

    function setBubblePlot(chosenCountry) {
        getCountryData(chosenCountry);        

        var trace1 = {
            x:year ,
            y: femaleBorrowers,
            mode: 'lines+markers',
            name: "Female Borrower Growth Over Years",
            marker: {
                size: 12,
                opacity: 0.5
            },
            line: {
                color: "Green"
            }
        };

        var trace2 = {
            x: year,
            y: maleBorrowers,
            mode: 'lines+markers',
            name: "Male Borrower Growth Over Years",
            marker: {
                size: 12,
                opacity: 0.5
            },
            line: {
                color: "Red"
            }
        };

    

        var data = [trace1, trace2];

        var layout = {
            title: "Borrower Gender Growth Over Years",
            xaxis: {
                type: "date"
            },
            yaxis: {
                autorange: true,
                type: "linear"
            }
        };

        Plotly.newPlot("plot", data, layout);
    }


    Plotly.d3.json(url, function(error, response) {

            console.log(response);
            borrowerResponseData = response    
            
            for (countryName in response){       

                var each = response[countryName]         
                countryList.push(countryName)
            }
            
            assignOptions(countryList, countrySelector);
            setBubblePlot('Afghanistan');
    });

    // // Default Country Data      
    

    // // // /* data route */

    function getSectorCountryData(chosenCountry) {

        var country_yearwise_list = sectoreResponseData[chosenCountry]
        sectorNames = [];  
        femaleCount = []; 
        maleCount = []       
        
        for (var i = 0 ; i < country_yearwise_list.length ; i++){
            
                countryData = country_yearwise_list[i]
                // console.log(countryData)                    
                femaleCount.push(countryData.Female)
                maleCount.push(countryData.Male)
                sectorNames.push(countryData.Sector)                    
        }     
    } 

    function setBarPlot(chosenCountry) {
        getSectorCountryData(chosenCountry);        

        var trace1 = {
            x: sectorNames,
            y: femaleCount,
            type: 'bar',
            name: "Female Count By Sector",
            
        };

        var trace2 = {
            x: sectorNames,
            y: maleCount,
            type: 'bar',
            name: "Male Count By Sector",
        };


        var data = [trace1, trace2];

        var layout = {
            title: "Sector Popularity by Gender",
            barmode: 'group'
        };

        Plotly.newPlot("sectorplot", data, layout);
    }
    var url2 = "/genderwise_popular_sector";

    Plotly.d3.json(url2, function(error, response) {

        sectoreResponseData = response
        // for (countryName in response){
        //     var each = response[countryName]         
        //     countryList.push(countryName)
        // } 
        
        // // Default Country Data      
        setBarPlot('Afghanistan');  
    });

    var innerContainer = document.querySelector('[data-num="0"'),
        plotEl = innerContainer.querySelector('#plot', '#sectorplot'),
        countrySelector = innerContainer.querySelector('.countrydata');

    function assignOptions(textArray, selector) {
        for (var i = 0; i < textArray.length;  i++) {
            var currentOption = document.createElement('option');
            currentOption.text = textArray[i];
            selector.appendChild(currentOption);
        }
    }    

    function updateCountry(){
        setBubblePlot(countrySelector.value);
        setBarPlot(countrySelector.value);
    }

    countrySelector.addEventListener('change', updateCountry, false);

    
