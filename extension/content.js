var searchResults
var ratingElements
var sortedItems

function collectItems () {
  // grab all search result items
  console.log('Collecting items now ')
  searchResults = document.querySelectorAll('div[data-asin]')
  console.log({ searchResults })
  sortedItems = []

  inStock = []
  ratingItems = []
  outOfOrder = []
  noSponsored = []

  for (i = 0; i < searchResults.length; i++) {
    ratingItems.push(searchResults[i])
  }

  outOfStock = []
  for (i = 0; i < searchResults.length; i++) {
    console.log('LOOP', { searchResults })
    if (searchResults[i].getElementsByClassName('sg-col-inner')[0] != null) {
      console.log('insideloop')
      var item = searchResults[i]
      console.log('RATINGGGS1', item)

      if (searchResults[i].getElementsByClassName('prod-rating')[0] != null) {
        console.log(
          'RATINGGGS2',
          searchResults[i].getElementsByClassName('prod-rating')[0].innerText
        )
        var rating =
          searchResults[i].getElementsByClassName('prod-rating')[0].innerText

        var myObject = {
          ratingKey: rating,
          itemKey: item
        }
        sortedItems.push(myObject)
      }
    }
  }

  sortedItems = sortedItems.sort(function (a, b) {
    return a.ratingKey.localeCompare(b.ratingKey)
  })
}

function highToLowRatingSort () {
  console.log('running high to low rating sort')

  // grab the footer search related elements to remove and then add later
  var relatedDiv
  var pagDiv
  var helpDiv
  var adDiv

  // get the dropdown element and store it temporarily
  var sel = document.getElementsByClassName('a-dropdown-container')[0]
  var selOptions = document.getElementById('s-result-sort-select')
  selOptions.value = 'highToLowRating'
  var prompt = document.getElementsByClassName('a-dropdown-prompt')[0]
  prompt.textContent = 'High To Low Availibitly'

  var searchElements = document.querySelectorAll('div[data-asin]')
  for (i = 0; i < searchElements.length; i++) {
    var itemResult = searchElements[i].getElementsByClassName('sg-col-inner')[0]

    var paginationFooter =
      searchElements[i].getElementsByClassName('a-pagination')[0]

    var helpFooter = searchElements[i].getElementsByClassName(
      'a-row a-spacing-base a-size-base'
    )[0]

    var adFooter = searchElements[i].getElementsByClassName(
      'amzn-safe-frame-container'
    )[0]

    var relatedBrandFooter =
      searchElements[i].getElementsByClassName('threepsl')[0]

    // remove all the items except for the header
    if (
      itemResult != null ||
      relatedBrandFooter != null ||
      helpFooter != null ||
      adFooter != null ||
      paginationFooter != null
    ) {
      searchElements[i].remove()
    }

    if (relatedBrandFooter != null) {
      relatedDiv = searchElements[i]
    }
    // if it's the pagination footer
    if (paginationFooter != null) {
      pagDiv = searchElements[i]
    }

    // if it's the helper footer
    if (helpFooter != null) {
      helpDiv = searchElements[i]
    }

    if (adFooter != null) {
      adDiv = searchElements[i]
    }
  }

  // find the div that we need to append the new items to
  var element = document.getElementsByClassName(
    's-main-slot s-result-list s-search-results sg-row'
  )

  for (i = 0; i < sortedItems.length; i++) {
    element[0].appendChild(sortedItems[i].itemKey)
  }

  // add the random footers back
  if (pagDiv != null) {
    element[0].appendChild(pagDiv)
  }
  if (relatedDiv != null) {
    element[0].appendChild(relatedDiv)
  }
  if (pagDiv != null) {
    element[0].appendChild(helpDiv)
  }
  if (pagDiv != null) {
    element[0].appendChild(adDiv)
  }
}

chrome.storage.sync.get('extensionEnabled', function (data) {
  if (data.extensionEnabled == true && window.location.pathname == '/s') {
    chrome.storage.sync.get('primeOnlyEnabled', function (data) {
      if (
        document.querySelectorAll('[type= checkbox]')[0].checked !=
        data.primeOnlyEnabled
      ) {
        document.querySelectorAll('[type= checkbox]')[0].click()
      }
    })
    chrome.storage.sync.get('order', function (order) {
      console.log('Order ', order)
      chrome.storage.sync.get('sortOrderMap', function (sortOrderMap) {
        console.log('sortOrderMap ', sortOrderMap)
        chrome.storage.sync.get('sort', function (data) {
          console.log('sort data ', data)
          collectItems()
          if (data.sort == 'lowToHighRating') {
            console.log('Sorting now', { sortedItems })
            highToLowRatingSort()
          } else if (
            document.getElementsByTagName('SELECT')[1].value !=
            sortOrderMap.sortOrderMap[data.sort]
          ) {
            document.getElementsByTagName('SELECT')[1].click()
            window.setTimeout(function () {
              document
                .getElementsByTagName('UL')
                [document.getElementsByTagName('UL').length - 1].children[
                  order.order[data.sort]
                ].children[0].click()
            }, 500)
          }
        })
      })
    })
    chrome.storage.sync.get('ratingsEnabled', function (data) {
      if (data.ratingsEnabled == true) {
        const imagePoster = document.querySelectorAll(
          "span[data-component-type='s-product-image']"
        )
        const letters = ['A', 'B', 'C', 'D', 'E']
        for (i = 0; i < imagePoster.length; i++) {
          if (imagePoster[i].getElementsByClassName('prod-rating')[0] == null) {
            console.log('IMAGEEEEEEE******', imagePoster)
            var rating = document.createElement('span')

            rating.className = 'prod-rating'
            rating.style.cssText =
              '-webkit-text-size-adjust: 100%; font-size: 14px; line-height: 20px; color: #0F1111; font-family: "Amazon Ember",Arial,sans-serif; direction: ltr; text-align: center; position: relative !important; display: flex !important; justify-content: space-between !important; height: 26px !important; width: 63px !important; top: 3px !important; background-color: rgba(255, 255, 255, 0.9) !important; border-radius: 2px !important; overflow: hidden !important; padding: 3px 6px !important; z-index: 105 !important; box-sizing: border-box !important; border: 1px solid #999CA1 !important; margin-left: 3px !important; left: 3px !important;'
            const random = Math.floor(Math.random() * letters.length)
            rating.innerHTML = letters[random]
            console.log('RATINGGG3', rating)
            imagePoster[i].prepend(rating)
            console.log('HEREEEEEE', imagePoster)
          }
        }
      }
    })

    chrome.storage.sync.get('primeOnlyEnabled', function (data) {
      if (
        document.querySelectorAll('[type= checkbox]')[0].checked !=
        data.primeOnlyEnabled
      ) {
        document.querySelectorAll('[type= checkbox]')[0].click()
      }
    })
  }

  chrome.storage.sync.get('ratingsEnabledWalmart', function (data) {
    if (
      // data.extensionEnabled == true &&
      window.location.pathname == '/search'
    ) {
      if (data.ratingsEnabledWalmart == true) {
        const imagePoster = document.querySelectorAll(
          '[data-testid="list-view"]'
        )
        const letters = ['A', 'B', 'C', 'D', 'E']
        for (i = 0; i < imagePoster.length; i++) {
          if (imagePoster[i].getElementsByClassName('prod-rating')[0] == null) {
            console.log('IMAGEEEEEEE******', imagePoster)
            var rating = document.createElement('span')

            rating.className = 'prod-rating'
            rating.style.cssText =
              '-webkit-text-size-adjust: 100%; font-size: 14px; line-height: 20px; color: #0F1111; font-family: "Amazon Ember",Arial,sans-serif; direction: ltr; text-align: center; position: relative !important; display: flex !important; justify-content: space-between !important; height: 26px !important; width: 63px !important; top: 3px !important; background-color: rgba(255, 255, 255, 0.9) !important; border-radius: 2px !important; overflow: hidden !important; padding: 3px 6px !important; z-index: 105 !important; box-sizing: border-box !important; border: 1px solid #999CA1 !important; margin-left: 3px !important; left: 3px !important;'
            const random = Math.floor(Math.random() * letters.length)
            rating.innerHTML = letters[random]
            console.log('RATINGGG WALMARTSS', rating)
            imagePoster[i].prepend(rating)
            console.log('HEREEEEEE', imagePoster)
          }
        }
      }
    }
  })

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
})
