var searchResults;
var ratingElements;
var sortedItems;

function collectItems() {
  // grab all search result items
  console.log("Collecting items now ");
  searchResults = document.querySelectorAll("div[data-asin]");
  console.log({ searchResults });
  sortedItems = [];

  inStock = [];
  ratingItems = [];
  outOfOrder = [];
  noSponsored = [];

  for (i = 0; i < searchResults.length; i++) {
    ratingItems.push(searchResults[i]);
  }

  outOfStock = [];
  for (i = 0; i < searchResults.length; i++) {
    console.log("LOOP", { searchResults });
    if (searchResults[i].getElementsByClassName("sg-col-inner")[0] != null) {
      console.log("insideloop");
      var item = searchResults[i];
      console.log("RATINGGGS1", item);

      if (searchResults[i].getElementsByClassName("prod-rating")[0] != null) {
        console.log(
          "RATINGGGS2",
          searchResults[i].getElementsByClassName("prod-rating")[0].innerText
        );
        var rating =
          searchResults[i].getElementsByClassName("prod-rating")[0].innerText;

        var myObject = {
          ratingKey: rating,
          itemKey: item
        };
        sortedItems.push(myObject);
      }
    }
  }
  sortedItems = sortedItems.sort(function (a, b) {
    return a.ratingKey.localeCompare(b.ratingKey);
  });
}

function collectItemsWalmart() {
  // grab all search result items
  console.log("Collecting items now ");
  searchResults = document.querySelectorAll(
    "div.mb0.ph1.pa0-xl.bb.b--near-white.w-25"
  );
  console.log({ searchResults });
  sortedItems = [];

  inStock = [];
  ratingItems = [];
  outOfOrder = [];
  noSponsored = [];

  for (i = 0; i < searchResults.length; i++) {
    ratingItems.push(searchResults[i]);
  }

  outOfStock = [];
  for (i = 0; i < searchResults.length; i++) {
    console.log("LOOP", { searchResults });
    if (searchResults[i].querySelector("div[data-item-id]") != null) {
      console.log("insideloop");
      var item = searchResults[i];
      console.log("RATINGGGS1", item);

      if (searchResults[i].getElementsByClassName("prod-rating")[0] != null) {
        console.log(
          "RATINGGGS2",
          searchResults[i].getElementsByClassName("prod-rating")[0].innerText
        );
        var rating =
          searchResults[i].getElementsByClassName("prod-rating")[0].innerText;

        var myObject = {
          ratingKey: rating,
          itemKey: item
        };
        sortedItems.push(myObject);
      }
    }
  }
  sortedItems = sortedItems.sort(function (a, b) {
    return a.ratingKey.localeCompare(b.ratingKey);
  });
}

function highToLowRatingSort() {
  console.log("running high to low rating sort");

  // grab the footer search related elements to remove and then add later
  var relatedDiv;
  var pagDiv;
  var helpDiv;
  var adDiv;

  // get the dropdown element and store it temporarily
  var sel = document.getElementsByClassName("a-dropdown-container")[0];
  var selOptions = document.getElementById("s-result-sort-select");
  selOptions.value = "highToLowRating";
  var prompt = document.getElementsByClassName("a-dropdown-prompt")[0];
  prompt.textContent = "High To Low Availibitly";

  var searchElements = document.querySelectorAll("div[data-asin]");
  for (i = 0; i < searchElements.length; i++) {
    var itemResult =
      searchElements[i].getElementsByClassName("sg-col-inner")[0];

    var paginationFooter =
      searchElements[i].getElementsByClassName("a-pagination")[0];

    var helpFooter = searchElements[i].getElementsByClassName(
      "a-row a-spacing-base a-size-base"
    )[0];

    var adFooter = searchElements[i].getElementsByClassName(
      "amzn-safe-frame-container"
    )[0];

    var relatedBrandFooter =
      searchElements[i].getElementsByClassName("threepsl")[0];

    // remove all the items except for the header
    if (
      itemResult != null ||
      relatedBrandFooter != null ||
      helpFooter != null ||
      adFooter != null ||
      paginationFooter != null
    ) {
      searchElements[i].remove();
    }

    if (relatedBrandFooter != null) {
      relatedDiv = searchElements[i];
    }
    // if it's the pagination footer
    if (paginationFooter != null) {
      pagDiv = searchElements[i];
    }

    // if it's the helper footer
    if (helpFooter != null) {
      helpDiv = searchElements[i];
    }

    if (adFooter != null) {
      adDiv = searchElements[i];
    }
  }

  // find the div that we need to append the new items to
  var element = document.getElementsByClassName(
    "s-main-slot s-result-list s-search-results sg-row"
  );

  for (i = 0; i < sortedItems.length; i++) {
    element[0].appendChild(sortedItems[i].itemKey);
  }

  // add the random footers back
  if (pagDiv != null) {
    element[0].appendChild(pagDiv);
  }
  if (relatedDiv != null) {
    element[0].appendChild(relatedDiv);
  }
  if (pagDiv != null) {
    element[0].appendChild(helpDiv);
  }
  if (pagDiv != null) {
    element[0].appendChild(adDiv);
  }
}

function highToLowRatingSortWalmart() {
  console.log("running high to low Walmart rating sort");

  var searchElements = document.querySelectorAll(
    "div.mb0.ph1.pa0-xl.bb.b--near-white.w-25"
  );
  for (i = 0; i < searchElements.length; i++) {
    searchElements[i].remove();
  }

  // find the div that we need to append the new items to
  var element = document.getElementsByClassName(
    "flex flex-wrap w-100 flex-grow-0 flex-shrink-0 ph2 pr0-xl pl4-xl mt0-xl"
  );

  for (i = 0; i < sortedItems.length; i++) {
    element[0].appendChild(sortedItems[i].itemKey);
  }
}

chrome.storage.sync.get("extensionEnabled", function (data) {
  if (data.extensionEnabled == false) {
    console.log("ext is off");
    const imagePoster = document.querySelectorAll(
      "span[data-component-type='s-product-image']"
    );
    console.log("ext is off", imagePoster);
    for (i = 0; i < imagePoster.length; i++) {
      if (imagePoster[i].getElementsByClassName("prod-rating")[0] != null) {
        imagePoster[i].getElementsByClassName("prod-rating")[0].remove();
      }
    }

    const img = document.querySelectorAll(
      "div[class='a-section a-spacing-none a-padding-none']"
    );
    console.log("ext is off2", img);
    for (i = 0; i < img.length; i++) {
      if (img[i].getElementsByClassName("prod-rating")[0] != null) {
        img[i].getElementsByClassName("prod-rating")[0].remove();
      }
    }
  }
  if (data.extensionEnabled == true && window.location.pathname == "/s") {
    chrome.storage.sync.get("primeOnlyEnabled", function (data) {
      if (
        document.querySelectorAll("[type= checkbox]")[0].checked !=
        data.primeOnlyEnabled
      ) {
        document.querySelectorAll("[type= checkbox]")[0].click();
      }
    });
    chrome.storage.sync.get("order", function (order) {
      console.log("Order ", order);
      chrome.storage.sync.get("sortOrderMap", function (sortOrderMap) {
        console.log("sortOrderMap ", sortOrderMap);
        chrome.storage.sync.get("sort", function (data) {
          console.log("sort data ", data);
          collectItems();
          if (data.sort == "lowToHighRating") {
            console.log("Sorting now", { sortedItems });
            highToLowRatingSort();
          } else if (
            document.getElementsByTagName("SELECT")[1].value !=
            sortOrderMap.sortOrderMap[data.sort]
          ) {
            document.getElementsByTagName("SELECT")[1].click();
            window.setTimeout(function () {
              document
                .getElementsByTagName("UL")
                [document.getElementsByTagName("UL").length - 1].children[
                  order.order[data.sort]
                ].children[0].click();
            }, 500);
          }
        });
      });
    });
    function getAttr(rating) {
      if (rating == "A") {
        cssText =
          "width:46px !important;clear:both !important;background-color:#73D448 !important;border:1px solid #68bf41 !important;border-radius:3px !important;height:31px !important;color:#FFFFFF !important;font-size:24px !important;font-weight:700 !important;text-align:center !important;line-height:28px !important;box-sizing:border-box !important;user-select:none !important;text-decoration:none !important;display:block !important;margin-right:8px !important;margin-top:0 !important;opacity:1 !important;";
        return cssText;
      } else if (rating == "B") {
        rcssText =
          "width:46px !important;clear:both !important;background-color:#0095EA !important;border:1px solid #0086d3 !important;border-radius:3px !important;height:31px !important;color:#FFFFFF !important;font-size:24px !important;font-weight:700 !important;text-align:center !important;line-height:28px !important;box-sizing:border-box !important;user-select:none !important;text-decoration:none !important;display:block !important;margin-right:8px !important;margin-top:0 !important;opacity:1 !important;";
        return cssText;
      } else if (rating == "C") {
        cssText =
          "width:46px !important;clear:both !important;background-color:#FFC651 !important;border:1px solid #e6b249 !important;border-radius:3px !important;height:31px !important;color:#FFFFFF !important;font-size:24px !important;font-weight:700 !important;text-align:center !important;line-height:28px !important;box-sizing:border-box !important;user-select:none !important;text-decoration:none !important;display:block !important;margin-right:8px !important;margin-top:0 !important;opacity:1 !important;";
        return cssText;
      } else if (rating == "D") {
        cssText =
          "width:46px !important;clear:both !important;background-color:#FB8746 !important;border:1px solid #e27a3f !important;border-radius:3px !important;height:31px !important;color:#FFFFFF !important;font-size:24px !important;font-weight:700 !important;text-align:center !important;line-height:28px !important;box-sizing:border-box !important;user-select:none !important;text-decoration:none !important;display:block !important;margin-right:8px !important;margin-top:0 !important;opacity:1 !important;";
        return cssText;
      } else if (rating == "E") {
        cssText =
          "width:46px !important;clear:both !important;background-color:#FFC651 !important;border:1px solid #e6b249 !important;border-radius:3px !important;height:31px !important;color:#FFFFFF !important;font-size:24px !important;font-weight:700 !important;text-align:center !important;line-height:28px !important;box-sizing:border-box !important;user-select:none !important;text-decoration:none !important;display:block !important;margin-right:8px !important;margin-top:0 !important;opacity:1 !important;";
        return cssText;
      } else {
        cssText =
          "width:46px !important;clear:both !important;background-color:#A52222 !important;border:1px solid #951f1f !important;border-radius:3px !important;height:31px !important;color:#FFFFFF !important;font-size:24px !important;font-weight:700 !important;text-align:center !important;line-height:28px !important;box-sizing:border-box !important;user-select:none !important;text-decoration:none !important;display:block !important;margin-right:8px !important;margin-top:0 !important;opacity:1 !important;";
        return cssText;
      }
    }
    chrome.storage.sync.get("ratingsEnabled", function (data) {
      if (data.ratingsEnabled == true) {
        const imagePoster = document.querySelectorAll(
          "span[data-component-type='s-product-image']"
        );
        const letters = ["A", "B", "C", "D", "E"];
        for (i = 0; i < imagePoster.length; i++) {
          if (imagePoster[i].getElementsByClassName("prod-rating")[0] == null) {
            console.log("IMAGEEEEEEE******", imagePoster);
            var rating = document.createElement("span");

            rating.className = "prod-rating";
            //rating.style.cssText =
              //"width:46px !important;clear:both !important;background-color:#FFC651 !important;border:1px solid #e6b249 !important;border-radius:3px !important;height:31px !important;color:#FFFFFF !important;font-size:24px !important;font-weight:700 !important;text-align:center !important;line-height:28px !important;box-sizing:border-box !important;user-select:none !important;text-decoration:none !important;display:block !important;margin-right:8px !important;margin-top:0 !important;opacity:1 !important;";
            const random = Math.floor(Math.random() * letters.length);
            const rat = letters[random];
            const cssT = getAttr(rat)
            rating.style.cssText = cssT
            rating.innerHTML = rat
            console.log("RATINGGG3", rating);
            imagePoster[i].prepend(rating);
            console.log("HEREEEEEE", imagePoster);
          }
        }
      }
    });

    chrome.storage.sync.get("primeOnlyEnabled", function (data) {
      if (
        document.querySelectorAll("[type= checkbox]")[0].checked !=
        data.primeOnlyEnabled
      ) {
        document.querySelectorAll("[type= checkbox]")[0].click();
      }
    });
  }
  if (
    data.extensionEnabled == true &&
    window.location.pathname.includes("/dp/")
  ) {
    chrome.storage.sync.get("ratingsEnabled", function (data) {
      console.log("RATINGSSSSS ENABLEDD DP******");
      if (data.ratingsEnabled == true) {
        console.log("URL in Fetch");
        var regex = RegExp("/([a-zA-Z0-9]{10})(?:[/?]|$)");

        m = window.location.href.match(regex);
        console.log("URL", window.location.href, regex, m.input);
        var data = new URLSearchParams();
        data.set("listing_url", m.input);

        fetch("http://127.0.0.1:4444/reviews", {
          method: "POST",
          //mode: "no-cors",

          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ url: m.input })
        }).then((response) => {
          if (response.ok) {
            response.json().then((res) => {
              console.log(res.safemart_rating);

              const imagePoster = document.querySelectorAll(
                "div[class='a-section a-spacing-none a-padding-none']"
              );
              console.log("IMAGEEEEEEE******", imagePoster);
              const letters = ["A", "B", "C", "D", "E"];
              const i = 0;
              if (
                imagePoster[i].getElementsByClassName("prod-rating")[0] == null
              ) {
                console.log("IMAGEEEEEEE******", imagePoster);
                var rating = document.createElement("span");

                rating.className = "prod-rating";
                //rating.style.cssText =
                //'-webkit-text-size-adjust: 100%; font-size: 14px; line-height: 20px; color: #0F1111; font-family: "Amazon Ember",Arial,sans-serif; direction: ltr; text-align: center; position: relative !important; display: flex !important; justify-content: center !important; height: 26px !important; width: 63px !important; top: 3px !important; background-color: rgba(255, 255, 255, 0.9) !important; border-radius: 2px !important; overflow: hidden !important; padding: 3px 6px !important; z-index: 105 !important; box-sizing: border-box !important; border: 1px solid #999CA1 !important; margin-left: 3px !important; left: 3px !important;';

                const random = Math.floor(Math.random() * letters.length);
                if (
                  res.safemart_rating.percentage <= 100 &&
                  res.safemart_rating.percentage > 80
                ) {
                  rating.style.cssText =
                    "width:46px !important;clear:both !important;background-color:#73D448 !important;border:1px solid #68bf41 !important;border-radius:3px !important;height:31px !important;color:#FFFFFF !important;font-size:24px !important;font-weight:700 !important;text-align:center !important;line-height:28px !important;box-sizing:border-box !important;user-select:none !important;text-decoration:none !important;display:block !important;margin-right:8px !important;margin-top:0 !important;opacity:1 !important;";
                  rating.innerHTML = "A";
                } else if (
                  res.safemart_rating.percentage <= 80 &&
                  res.safemart_rating.percentage > 60
                ) {
                  rating.style.cssText =
                    "width:46px !important;clear:both !important;background-color:#0095EA !important;border:1px solid #0086d3 !important;border-radius:3px !important;height:31px !important;color:#FFFFFF !important;font-size:24px !important;font-weight:700 !important;text-align:center !important;line-height:28px !important;box-sizing:border-box !important;user-select:none !important;text-decoration:none !important;display:block !important;margin-right:8px !important;margin-top:0 !important;opacity:1 !important;";
                  rating.innerHTML = "B";
                } else if (
                  res.safemart_rating.percentage <= 60 &&
                  res.safemart_rating.percentage > 40
                ) {
                  rating.style.cssText =
                    "width:46px !important;clear:both !important;background-color:#FFC651 !important;border:1px solid #e6b249 !important;border-radius:3px !important;height:31px !important;color:#FFFFFF !important;font-size:24px !important;font-weight:700 !important;text-align:center !important;line-height:28px !important;box-sizing:border-box !important;user-select:none !important;text-decoration:none !important;display:block !important;margin-right:8px !important;margin-top:0 !important;opacity:1 !important;";
                  rating.innerHTML = "C";
                } else if (
                  res.safemart_rating.percentage <= 40 &&
                  res.safemart_rating.percentage > 30
                ) {
                  rating.style.cssText =
                    "width:46px !important;clear:both !important;background-color:#FB8746 !important;border:1px solid #e27a3f !important;border-radius:3px !important;height:31px !important;color:#FFFFFF !important;font-size:24px !important;font-weight:700 !important;text-align:center !important;line-height:28px !important;box-sizing:border-box !important;user-select:none !important;text-decoration:none !important;display:block !important;margin-right:8px !important;margin-top:0 !important;opacity:1 !important;";
                  rating.innerHTML = "D";
                } else if (
                  res.safemart_rating.percentage <= 30 &&
                  res.safemart_rating.percentage > 10
                ) {
                  rating.style.cssText =
                    "width:46px !important;clear:both !important;background-color:#FFC651 !important;border:1px solid #e6b249 !important;border-radius:3px !important;height:31px !important;color:#FFFFFF !important;font-size:24px !important;font-weight:700 !important;text-align:center !important;line-height:28px !important;box-sizing:border-box !important;user-select:none !important;text-decoration:none !important;display:block !important;margin-right:8px !important;margin-top:0 !important;opacity:1 !important;";
                  rating.innerHTML = "E";
                } else {
                  rating.style.cssText =
                    "width:46px !important;clear:both !important;background-color:#A52222 !important;border:1px solid #951f1f !important;border-radius:3px !important;height:31px !important;color:#FFFFFF !important;font-size:24px !important;font-weight:700 !important;text-align:center !important;line-height:28px !important;box-sizing:border-box !important;user-select:none !important;text-decoration:none !important;display:block !important;margin-right:8px !important;margin-top:0 !important;opacity:1 !important;";
                  rating.innerHTML = "F";
                }

                console.log("PRODUCT RATING", rating);
                imagePoster[i].prepend(rating);
                var subHead = document.createElement("span");
                subHead.className = "sub-head";
                subHead.innerHTML = "Secure Marketplace Rating";

                imagePoster[i].prepend(rating);
                imagePoster[i].prepend(subHead);
                console.log("HEREEEEEE", imagePoster);
              }
            });
          }
        });
      }
    });
  }

  chrome.storage.sync.get("ratingsEnabledWalmart", function (data) {
    if (
      // data.extensionEnabled == true &&
      window.location.pathname == "/search"
    ) {
      if (data.ratingsEnabledWalmart == true) {
        const imagePoster = document.querySelectorAll(
          '[data-testid="list-view"]'
        );
        const letters = ["A", "B", "C", "D", "E"];
        for (i = 0; i < imagePoster.length; i++) {
          if (imagePoster[i].getElementsByClassName("prod-rating")[0] == null) {
            console.log("IMAGEEEEEEE******", imagePoster);
            var rating = document.createElement("span");

            rating.className = "prod-rating";
            rating.style.cssText =
              "width:46px !important;clear:both !important;background-color:#FFC651 !important;border:1px solid #e6b249 !important;border-radius:3px !important;height:31px !important;color:#FFFFFF !important;font-size:24px !important;font-weight:700 !important;text-align:center !important;line-height:28px !important;box-sizing:border-box !important;user-select:none !important;text-decoration:none !important;display:block !important;margin-right:8px !important;margin-top:0 !important;opacity:1 !important;";
            const random = Math.floor(Math.random() * letters.length);

            rating.innerHTML = letters[random];
            console.log("RATINGGG WALMARTSS", rating);
            imagePoster[i].prepend(rating);
            console.log("HEREEEEEE", imagePoster);
          }
        }
        chrome.storage.sync.get("order", function (order) {
          console.log("Order ", order);
          chrome.storage.sync.get("sortOrderMap", function (sortOrderMap) {
            console.log("sortOrderMap ", sortOrderMap);
            chrome.storage.sync.get("sort", function (data) {
              console.log("sort data ", data);
              collectItemsWalmart();
              if (data.sort == "lowToHighRating") {
                console.log("Sorting now", { sortedItems });
                highToLowRatingSortWalmart();
              } else if (
                document.getElementsByTagName("SELECT")[1].value !=
                sortOrderMap.sortOrderMap[data.sort]
              ) {
                document.getElementsByTagName("SELECT")[1].click();
                window.setTimeout(function () {
                  document
                    .getElementsByTagName("UL")
                    [document.getElementsByTagName("UL").length - 1].children[
                      order.order[data.sort]
                    ].children[0].click();
                }, 500);
              }
            });
          });
        });
      }
    }
  });

  // if (data.extensionEnabled == true) {
  //   console.log('URL')
  //   var regex = RegExp('/([a-zA-Z0-9]{10})(?:[/?]|$)')

  //   m = window.location.href.match(regex)
  //   console.log('URL', window.location.href, regex, m.input)
  //   var data = new URLSearchParams()
  //   data.set('listing_url', m.input)

  //   fetch('http://127.0.0.1:5000/scrape/1', {
  //     method: 'POST',
  //     mode: 'no-cors',

  //     headers: { 'Content-Type': 'application/json' },
  //     body: JSON.stringify({ listing_url: m.input })
  //   }).then(function (response) {
  //     // check the response object for result
  //     // const imagePoster = document.querySelectorAll(
  //     //   "div[class='a-section a-spacing-none a-padding-none']"
  //     // )[0]
  //     // console.log(imagePoster)
  //     // const letters = ["A", "B", "C", "D", "E"];
  //     // // for (i = 0; i < imagePoster.length; i++) {
  //     //   if (document.getElementsByClassName("prod-rating").length == 0) {
  //     //     console.log("IMAGEEEEEEE******", imagePoster);
  //     //     var rating = document.createElement("span");

  //     //     rating.className = "prod-rating";
  //     //     rating.style.cssText =
  //     //       '-webkit-text-size-adjust: 100%; font-size: 14px; line-height: 20px; color: #0F1111; font-family: "Amazon Ember",Arial,sans-serif; direction: ltr; text-align: center; position: relative !important; display: flex !important; justify-content: space-between !important; height: 26px !important; width: 63px !important; top: 3px !important; background-color: rgba(255, 255, 255, 0.9) !important; border-radius: 2px !important; overflow: hidden !important; padding: 3px 6px !important; z-index: 105 !important; box-sizing: border-box !important; border: 1px solid #999CA1 !important; margin-left: 3px !important; left: 3px !important;';
  //     //     //const random = Math.floor(Math.random() * letters.length);
  //     //     rating.innerHTML = response;
  //     //     console.log("RATINGGG3", rating);
  //     //     imagePoster.prepend(rating);
  //     //     console.log("HEREEEEEE", imagePoster);
  //     //   }

  //     console.log({ response })
  //   })

  //   const imagePoster = document.querySelectorAll(
  //     "div[class='a-section a-spacing-none a-padding-none']"
  //   )[0]
  //   console.log(imagePoster)
  //   const letters = ['A', 'B', 'C', 'D', 'E']
  //   // for (i = 0; i < imagePoster.length; i++) {
  //   if (document.getElementsByClassName('prod-rating').length == 0) {
  //     console.log('IMAGEEEEEEE******', imagePoster)
  //     var rating = document.createElement('span')

  //     rating.className = 'prod-rating'
  //     rating.style.cssText =
  //       '-webkit-text-size-adjust: 100%; font-size: 14px; line-height: 20px; color: #0F1111; font-family: "Amazon Ember",Arial,sans-serif; direction: ltr; text-align: center; position: relative !important; display: flex !important; justify-content: space-between !important; height: 26px !important; width: 63px !important; top: 3px !important; background-color: rgba(255, 255, 255, 0.9) !important; border-radius: 2px !important; overflow: hidden !important; padding: 3px 6px !important; z-index: 105 !important; box-sizing: border-box !important; border: 1px solid #999CA1 !important; margin-left: 3px !important; left: 3px !important;'
  //     const random = Math.floor(Math.random() * letters.length)
  //     rating.innerHTML = letters[random]
  //     console.log('RATINGGG3', rating)
  //     imagePoster.prepend(rating)
  //     console.log('HEREEEEEE', imagePoster)
  //   }
  //   //}
  // }
});
