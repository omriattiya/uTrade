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
                var priceOfItem = attributesOfItems[1].value;
                var startPrice = document.getElementById("SearchForm6").value;
                var endPrice = document.getElementById("SearchForm7").value;
                if(!((startPrice <= priceOfItem) && (priceOfItem <= endPrice)))
                {
                    x[i].hidden = true;
                }
            }
        }