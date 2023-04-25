/**
 * TASK: unpack new datatype 
 */
function update_carousel(){
    console.log("inside carousel function");
    console.warn(reverse_context);

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
        const p = $(`<p>${text}</p>`)
    
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
};