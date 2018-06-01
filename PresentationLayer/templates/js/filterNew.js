        function filterByCategory()
        {
            var x = document.getElementsByClassName("itemJS");
            var i;
            for (i = 0; i < x.length; i++)
            {
                var attributesOfItems = x[i].attributes;
                var categoryOfItem = attributesOfItems[2].value;
                var inputCategory = document.getElementById("SearchForm5").value;
                if(categoryOfItem.localeCompare(inputCategory) != 0)
                {
                    x[i].hidden = true;
                }
            }
        }

        function filterByPrice()
        {
            var x = document.getElementsByClassName("itemJS");
            var i;
            for (i = 0; i < x.length; i++)
            {
                var attributesOfItems = x[i].attributes;
                var priceOfItem = parseFloat(attributesOfItems[1].value);
                var startPrice = parseFloat(document.getElementById("SearchForm6").value);
                var endPrice = parseFloat(document.getElementById("SearchForm7").value);
                if(!((startPrice <= priceOfItem) && (priceOfItem <= endPrice)))
                {
                    x[i].hidden = true;
                }
            }
        }

        function filterByItemRanking()
        {
            var x = document.getElementsByClassName("itemJS");
            var i;
            for (i = 0; i < x.length; i++)
            {
                var attributesOfItems = x[i].attributes;
                var rankingOfItem = parseFloat(attributesOfItems[3].value);
                var startRank = parseFloat(document.getElementById("SearchForm8").value);
                var endRank = parseFloat(document.getElementById("SearchForm9").value);
                if(!((startRank <= rankingOfItem) && (rankingOfItem <= endRank)))
                {
                    x[i].hidden = true;
                }
            }
        }