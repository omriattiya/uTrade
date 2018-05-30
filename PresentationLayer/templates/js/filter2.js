        function filterByItemRanking()
        {
            var x = document.getElementsByClassName("itemJS");
            var i;
            for (i = 0; i < x.length; i++)
            {
                var attributesOfItems = x[i].attributes;
                var rankingOfItem = attributesOfItems[3].value;
                var startRank = document.getElementById("SearchForm8").value;
                var endRank = document.getElementById("SearchForm9").value;
                if(!((startRank <= rankingOfItem) && (rankingOfItem <= endRank)))
                {
                    x[i].hidden = true;
                }
            }
        }

        function filterByShopRanking()
        {
            var x = document.getElementsByClassName("itemJS");
            var i;
            for (i = 0; i < x.length; i++)
            {
                var attributesOfItems = x[i].attributes;
                var rankingOfShop = attributesOfItems[4].value;
                var startRank = document.getElementById("SearchForm10").value;
                var endRank = document.getElementById("SearchForm11").value;
                if(!((startRank <= rankingOfShop) && (rankingOfShop <= endRank)))
                {
                    x[i].hidden = true;
                }
            }
        }