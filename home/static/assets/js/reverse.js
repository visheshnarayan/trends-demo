/**
 * merge texts and buttons
 * track ID of text 
 * don't append divs
 * 
 * for click: 
 *      update id -> id+=1
 *      retrieve text -> text[id][0]
 *      swap text inside li <p> -> node.text = text[id][0]
 *      
 *  for click must exist for both buttons 
 */
function update_carousel() {
    const prevButton = $("#prevButton")[0];
    const nextButton = $("#nextButton")[0];
    const texts = reverse_context['docs'];
    var id = 0;

    // set original slide
    $("#activeText").text(highlight(texts[id][0], texts[id][1]));
    /**
     * SET INITIAL SLIDE HERE
     * set slide id to "firstSlide" or "activeSlide"
     */



    // previous button
    prevButton.addEventListener("click", () => {
        console.log("prev click");
        id == 0 ? id = texts.length-1 : id -= 1
        showSlide(id);
    });

    // next button
    nextButton.addEventListener("click", () => {
        console.log("next click");
        id == texts.length-1 ? id = 0 : id += 1
        showSlide(id);
    });

    function showSlide (id) {
        $("#activeText").text(highlight(texts[id][0], texts[id][1]));
        // var text = $("#activeText")[0];
        // text = highlight(texts[id][0], texts[id][1]);
        // console.log(text);
    }
    // // clear carousel before updating
    // clear_carousel();

    // console.log("inside carousel function");
    // console.warn(reverse_context);

    // // reverse_context["docs"] -> [text, locs]
    // const texts = reverse_context['docs'];
    // texts.forEach(text => {
    //     /**
    //      * initialize list first and set it equal to "first-slide" incase indexOf == 0 else create new li
    //      * --> this is done so the "data-active" meta-tag is assigned to the first text inserted and so the preview is not blank on load 
    //      * every other node created and joined the same way
    //      */
    //     var list;
    //     texts.indexOf(text) == 0 ? list = $("#first-slide") : list = $("<li></li>", {"class": "slide"}).appendTo("#slides");
    
    //     /**
    //      * create element nodes
    //      */
    //     const div = $("<div></div>", {"class": "content"})
    //     const header = $("<h3>Title</h3>")
    //     const p = $(`<p>${highlight(text[0], text[1])}</p>`)
    
    //     /**
    //      * append all nodes
    //      */
    //     div.append(header)
    //     div.append(p)
    //     list.append(div)
    //     $("#slides").append(list)
    // })

    /**
     * left and right buttons
     */
    // const buttons = document.querySelectorAll("[data-carousel-button]")
    // buttons.forEach(button => {
    //     button.addEventListener("click", () => {
    //         /**
    //          * go right if "next" button: go left if not
    //          * go into data-carousel and select data-slides
    //          */
    //         const offSet = button.dataset.carouselButton === "next" ? 1 : -1;
    //         const slides = button
    //             .closest("[data-carousel]")
    //             .querySelector("[data-slides]");
    //         const activeSlide = slides.querySelector(["[data-active]"]);

    //         /**
    //          * index of active slide + offset
    //          */
    //         let newIndex = [...slides.children].indexOf(activeSlide) + offSet;

    //         /**
    //          * if first send to last slide
    //          * if index greater than length (or = to) send to first slide
    //          */
    //         if (newIndex < 0) newIndex = slides.children.length - 1;
    //         if (newIndex >= slides.children.length) newIndex = 0;

    //         /**
    //          * create new active slide
    //          * delete old one
    //          */
    //         slides.children[newIndex].dataset.active = true;
    //         delete activeSlide.dataset.active;
    //     })
    // });

    /**
     * highlight: highlights given text
     * if base: highlight yellow
     * if not: highlight blue
     * @param {String} text 
     * @param {Integer[]} locs 
     */
    function highlight(text, locs) {
        var tokens_list = text.split(" ");
        for (let i = 0; i < locs.length; i++) {
            if (i==0) {
                tokens_list[locs[i]] = `<span class=\"highlightBase\">${tokens_list[locs[i]]}</span>`;
            } else {
                if (locs[i]!=-1) {
                    tokens_list[locs[i]] = `<span class=\"highlightRel\">${tokens_list[locs[i]]}</span>`;
                }
            }    
        }
        return tokens_list.join(" ");
    }

    // function clear_carousel() {
    //     const carousel = document.getElementById("#slides");
    //     // access first child
    //     if (carousel.firstChild) {
    //         console.log(carousel.firstChild);
    //     }
    //     // while (carousel.firstChild) {
    //     //     carousel.removeChild(carousel.lastChild);
    //     // }
    // }
};