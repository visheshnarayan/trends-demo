// FIXME : carousel stacks every time it is reloaded (clear previous information when reloading)

function update_carousel(){
    console.log("inside carousel function");

    // reverse_context["docs"] -> text data
    // will be changed to access text inside new data structure
    const texts = reverse_context['docs'];
    texts.forEach(text => {
        /**
         * initialize list first and set it equal to "first-slide" incase indexOf == 0 else create new li
         * --> this is done so the "data-active" meta-tag is assigned to the first text inserted and so the preview is not blank on load 
         * every other node created and joined the same way
         */
        var list;
        texts.indexOf(text) == 0 ? list = $("#first-slide") : list = $("<li></li>", {"class": "slide"}).appendTo("#slides");
    
        /**
         * create element nodes
         */
        const div = $("<div></div>", {"class": "content"})
        const header = $("<h3>Title</h3>")
        const p = $(`<p>${highlight(text[0], text[1])}</p>`)
        // const p = $(`<p>${text[0]}</p>`)
        highlight(text[0], text[1]);
        
        // highlight(p, texts.indexOf(text));
    
        /**
         * append all nodes
         */
        div.append(header)
        div.append(p)
        list.append(div)
        $("#slides").append(list)
    })

    /**
     * left and right buttons
     */
    const buttons = document.querySelectorAll("[data-carousel-button]")
    buttons.forEach(button => {
        button.addEventListener("click", () => {
            /**
             * go right if "next" button: go left if not
             * go into data-carousel and select data-slides
             */
            const offSet = button.dataset.carouselButton === "next" ? 1 : -1;
            const slides = button
                .closest("[data-carousel]")
                .querySelector("[data-slides]");
            const activeSlide = slides.querySelector(["[data-active]"]);

            /**
             * index of active slide + offset
             */
            let newIndex = [...slides.children].indexOf(activeSlide) + offSet;

            /**
             * if first send to last slide
             * if index greater than length (or = to) send to first slide
             */
            if (newIndex < 0) newIndex = slides.children.length - 1;
            if (newIndex >= slides.children.length) newIndex = 0;

            /**
             * create new active slide
             * delete old one
             */
            slides.children[newIndex].dataset.active = true;
            delete activeSlide.dataset.active;
        })
    });

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
                // tokens_list[locs[i]] = `<span style=\"font-weight:bold\">${tokens_list[locs[i]]}</span>`;
            } else {
                if (locs[i]!=-1) {
                    tokens_list[locs[i]] = `<span class=\"highlightRel\">${tokens_list[locs[i]]}</span>`;
                    // tokens_list[locs[i]] = `<span style=\"font-weight:bold\">${tokens_list[locs[i]]}</span>`;
                }
            }    
        }
        // console.warn(tokens_list.join(" "));
        return tokens_list.join(" ");
    }
};